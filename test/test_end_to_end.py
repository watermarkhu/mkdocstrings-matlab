"""End-to-end tests for every combination of MATLAB options."""

from __future__ import annotations

import json
import re
from typing import TYPE_CHECKING, Any

import bs4
import pytest
from inline_snapshot import outsource

from test import snapshots

if TYPE_CHECKING:
    from mkdocstrings_handlers.matlab import MatlabHandler


def _normalize_html(html: str) -> str:
    soup = bs4.BeautifulSoup(html, features="html.parser")
    html = soup.prettify()
    html = re.sub(r"\b(0x)[a-f0-9]+\b", r"\1...", html)
    html = re.sub(r"^(Build Date UTC ?:).+", r"\1...", html, flags=re.MULTILINE)
    html = re.sub(r"\b[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\b", r"...", html)
    html = re.sub(r'(?<=id="cell-id=)\w+(?=")', r"...", html)
    return html


def _render(handler: MatlabHandler, identifier: str, final_options: dict[str, Any]) -> str:
    final_options.pop("handler", None)
    final_options.pop("session_handler", None)
    handler_options = final_options.copy()

    # Some default options to make snapshots easier to review.
    handler_options.setdefault("heading_level", 1)
    handler_options.setdefault("show_root_heading", True)
    handler_options.setdefault("show_source", False)

    options = handler.get_options(handler_options)
    data = handler.collect(identifier, options)

    html = handler.render(data, options)

    if stash := handler.env.filters["stash_crossref"].stash:
        for key, value in stash.items():
            html = re.sub(rf"\b{key}\b", value, html)
        stash.clear()

    return _normalize_html(html)


def _render_options(options: dict[str, Any]) -> str:
    return f"<!--\n{json.dumps(options, indent=2, sort_keys=True)}\n-->\n\n"


@pytest.mark.parametrize("show_signature_annotations", [True, False])
@pytest.mark.parametrize("signature_crossrefs", [True, False])
@pytest.mark.parametrize("separate_signature", [True, False])
def test_end_to_end_for_signatures(
    session_handler: MatlabHandler,
    show_signature_annotations: bool,
    signature_crossrefs: bool,
    separate_signature: bool,
) -> None:
    """Test rendering of MATLAB signatures with different options.

    Parameters:
        session_handler: MATLAB handler (fixture).
        show_signature_annotations: Whether to show type annotations.
        signature_crossrefs: Whether to enable cross-references.
        separate_signature: Whether to separate signature from heading.
    """
    final_options = {
        "show_signature_annotations": show_signature_annotations,
        "signature_crossrefs": signature_crossrefs,
        "separate_signature": separate_signature,
    }
    html = _render_options(final_options) + _render(
        session_handler, "module_arguments", final_options
    )
    snapshot_key = tuple(sorted(final_options.items()))
    assert outsource(html, suffix=".html") == snapshots.signatures[snapshot_key]


@pytest.mark.parametrize("inherited_members", [(), ("method1",), True, False])
@pytest.mark.parametrize("members", [(), ("module_function",), True, False, None])
@pytest.mark.parametrize(
    "filters", [(), ("!module_function",), ("module_function",), "public", None]
)
def test_end_to_end_for_members(
    session_handler: MatlabHandler,
    inherited_members: list[str] | bool | None,
    members: list[str] | bool | None,
    filters: list[str] | None,
) -> None:
    """Test rendering of MATLAB members with different options.

    Parameters:
        session_handler: MATLAB handler (fixture).
        inherited_members: Inherited members configuration.
        members: Members configuration.
        filters: Filters configuration.
    """
    final_options = {
        "inherited_members": inherited_members,
        "members": members,
        "filters": filters,
    }
    html = _render_options(final_options) + _render(
        session_handler,
        "subClass",
        final_options,  # Test folder identifier
    )

    snapshot_key = tuple(sorted(final_options.items()))
    assert outsource(html, suffix=".html") == snapshots.members[snapshot_key]


@pytest.mark.parametrize("separate_signature", [True, False])
@pytest.mark.parametrize("heading", ["", "Some heading"])
def test_end_to_end_for_headings(
    session_handler: MatlabHandler,
    separate_signature: bool,
    heading: str,
) -> None:
    """Test rendering of MATLAB headings with different options.

    Parameters:
        session_handler: MATLAB handler (fixture).
        separate_signature: Whether to separate signature from heading.
        heading: Custom heading text.
    """
    final_options = {
        "separate_signature": separate_signature,
        "heading": heading,
        "show_if_no_docstring": True,
        "members": False,
    }
    html = _render_options(final_options) + _render(
        session_handler, "module_function", final_options
    )
    snapshot_key = tuple(sorted(final_options.items()))
    assert outsource(html, suffix=".html") == snapshots.headings[snapshot_key]


@pytest.mark.parametrize("show_subnamespaces", [True, False])
def test_end_to_end_for_namespaces(
    session_handler: MatlabHandler,
    show_subnamespaces: bool,
) -> None:
    """Test rendering of MATLAB namespaces.

    Parameters:
        session_handler: MATLAB handler (fixture).
        show_subnamespaces: Whether to show sub-namespaces.
    """
    final_options = {
        "show_subnamespaces": show_subnamespaces,
    }
    html = _render_options(final_options) + _render(
        session_handler, "+moduleNamespace", final_options
    )
    snapshot_key = tuple(sorted(final_options.items()))
    assert outsource(html, suffix=".html") == snapshots.namespaces[snapshot_key]
