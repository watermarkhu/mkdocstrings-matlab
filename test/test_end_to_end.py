"""End-to-end tests for every combination of MATLAB options."""

from __future__ import annotations

import json
import re
from typing import TYPE_CHECKING, Any

import bs4
import pytest
from inline_snapshot import outsource, register_format_alias

from test import snapshots

# Can be declared in conftest.py
register_format_alias(".html", ".txt")


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


def _render_options(options: dict[str, Any]) -> str:
    return f"<!--\n{json.dumps(options, indent=2, sort_keys=True)}\n-->\n\n"


def _render(handler: "MatlabHandler", identifier: str, final_options: dict[str, Any]) -> str:
    final_options.pop("handler", None)
    final_options.pop("session_handler", None)
    handler_options = final_options.copy()

    # Some default options to make snapshots easier to review.
    handler_options.setdefault("heading_level", 1)
    handler_options.setdefault("show_root_heading", True)
    handler_options.setdefault("show_source", False)

    options = handler.get_options(handler_options)
    data = handler.collect(identifier, options)

    if data.docstring:
        if "parsed" in data.docstring.__dict__:
            del data.docstring.__dict__["parsed"]

    html = handler.render(data, options)

    if stash := handler.env.filters["stash_crossref"].stash:
        for key, value in stash.items():
            html = re.sub(rf"\b{key}\b", value, html)
        stash.clear()

    return _render_options(final_options) + _normalize_html(html)


@pytest.mark.parametrize("show_signature", [True, False])
@pytest.mark.parametrize("identifer", ["module_function", "moduleClass", "classFolder"])
def test_end_to_end_signature_show(
    session_handler: "MatlabHandler",
    show_signature: bool,
    identifer: str,
) -> None:
    final_options = {
        "show_signature": show_signature,
        "identifier": identifer,
    }
    html = _render(session_handler, identifer, final_options)
    snapshot_key = tuple(sorted(final_options.items()))
    assert outsource(html, suffix=".html") == snapshots.signature_show[snapshot_key]


@pytest.mark.parametrize("show_bases", [True, False])
def test_end_to_end_inheritance(
    session_handler: "MatlabHandler",
    show_bases: bool,
) -> None:
    final_options = {
        "show_bases": show_bases,
    }
    html = _render(session_handler, "subClass", final_options)
    snapshot_key = tuple(sorted(final_options.items()))
    assert outsource(html, suffix=".html") == snapshots.inheritance[snapshot_key]


@pytest.mark.parametrize("heading_level", [1, 2])
@pytest.mark.parametrize("argument_headings", [True, False])
def test_end_to_end_headings(
    session_handler: "MatlabHandler",
    heading_level: int,
    argument_headings: bool,
) -> None:
    final_options = {"heading_level": heading_level, "argument_headings": argument_headings}
    html = _render(session_handler, "module_function", final_options)
    snapshot_key = tuple(sorted(final_options.items()))
    assert outsource(html, suffix=".html") == snapshots.headings[snapshot_key]


@pytest.mark.parametrize("show_root_heading", [True, False])
@pytest.mark.parametrize("show_root_full_path", [True, False])
@pytest.mark.parametrize("show_root_members_full_path", [True, False])
def test_end_to_end_headings_root(
    session_handler: "MatlabHandler",
    show_root_heading: bool,
    show_root_full_path: bool,
    show_root_members_full_path: bool,
) -> None:
    final_options = {
        "show_root_heading": show_root_heading,
        "show_root_full_path": show_root_full_path,
        "show_root_members_full_path": show_root_members_full_path,
    }
    html = _render(session_handler, "module_arguments", final_options)
    snapshot_key = tuple(sorted(final_options.items()))
    assert outsource(html, suffix=".html") == snapshots.headings_root[snapshot_key]


@pytest.mark.parametrize("show_object_full_path", [True, False])
@pytest.mark.parametrize("show_category_heading", [True, False])
@pytest.mark.parametrize("show_symbol_type_heading", [True, False])
def test_end_to_end_headings_namespace(
    session_handler: "MatlabHandler",
    show_object_full_path: bool,
    show_category_heading: bool,
    show_symbol_type_heading: bool,
) -> None:
    final_options = {
        "show_object_full_path": show_object_full_path,
        "show_category_heading": show_category_heading,
        "show_symbol_type_heading": show_symbol_type_heading,
    }
    html = _render(session_handler, "+moduleNamespace", final_options)
    snapshot_key = tuple(sorted(final_options.items()))
    assert outsource(html, suffix=".html") == snapshots.headings_namespace[snapshot_key]


@pytest.mark.parametrize("show_root_toc_entry", [True, False])
@pytest.mark.parametrize("show_symbol_type_toc", [True, False])
def test_end_to_end_toc(
    session_handler: "MatlabHandler", show_root_toc_entry: bool, show_symbol_type_toc: bool
) -> None:
    final_options = {
        "show_root_toc_entry": show_root_toc_entry,
        "show_symbol_type_toc": show_symbol_type_toc,
    }
    html = _render(session_handler, "fixture/", final_options)
    snapshot_key = tuple(sorted(final_options.items()))
    assert outsource(html, suffix=".html") == snapshots.toc[snapshot_key]


@pytest.mark.parametrize("members_order", ["alphabetical", "source"])
@pytest.mark.parametrize("members", [("method1",), True, False])
@pytest.mark.parametrize("filters", [("!method1",), ("method*",), False])
def test_end_to_end_for_members(
    session_handler: "MatlabHandler",
    members_order: str,
    members: list[str] | bool | None,
    filters: list[str] | None,
) -> None:
    final_options = {
        "members_order": members_order,
        "members": members,
        "filters": filters,
    }
    html = _render(
        session_handler,
        "moduleClass",
        final_options,  # Test folder identifier
    )

    snapshot_key = tuple(sorted(final_options.items()))
    assert outsource(html, suffix=".html") == snapshots.members[snapshot_key]


@pytest.mark.parametrize("show_subnamespaces", [True, False])
@pytest.mark.parametrize("hidden_members", [True, False])
@pytest.mark.parametrize("group_by_category", [True, False])
def test_end_to_end_members_namespace(
    session_handler: "MatlabHandler",
    show_subnamespaces: bool,
    hidden_members: bool,
    group_by_category: bool,
) -> None:
    final_options = {
        "show_subnamespaces": show_subnamespaces,
        "hidden_members": hidden_members,
        "group_by_category": group_by_category,
    }
    html = _render(session_handler, "+moduleNamespace", final_options)
    snapshot_key = tuple(sorted(final_options.items()))
    assert outsource(html, suffix=".html") == snapshots.members_namespace[snapshot_key]


@pytest.mark.parametrize(
    "summary",
    [
        True,
        False,
        {"properties": True, "functions": True, "classes": True, "namespaces": True},
        {"properties": True, "functions": False, "classes": True, "namespaces": False},
        {"properties": False, "functions": True, "classes": False, "namespaces": True},
    ],
)
def test_end_to_end_members_summary(
    session_handler: "MatlabHandler",
    summary: bool | dict[str, bool],
) -> None:
    final_options = {
        "summary": summary,
    }
    html = _render(session_handler, "+moduleNamespace", final_options)

    snapshot_key = summary if isinstance(summary, bool) else tuple(sorted(summary.items()))
    assert outsource(html, suffix=".html") == snapshots.members_summary[snapshot_key]


@pytest.mark.parametrize("hidden_members", [True, False])
@pytest.mark.parametrize("private_members", [True, False])
@pytest.mark.parametrize("show_attributes", [True, False])
@pytest.mark.parametrize("inherited_members", [True, False])
def test_end_to_end_members_class(
    session_handler: "MatlabHandler",
    hidden_members: bool,
    private_members: bool,
    show_attributes: bool,
    inherited_members: bool,
) -> None:
    final_options = {
        "hidden_members": hidden_members,
        "private_members": private_members,
        "show_attributes": show_attributes,
        "inherited_members": inherited_members,
    }
    html = _render(session_handler, "subClass", final_options)
    snapshot_key = tuple(sorted(final_options.items()))
    assert outsource(html, suffix=".html") == snapshots.members_class[snapshot_key]


@pytest.mark.parametrize("parse_arguments", [True, False])
@pytest.mark.parametrize("show_docstring_examples", [True, False])
@pytest.mark.parametrize("docstring_section_style", ["table", "list", "spacy"])
def test_end_to_end_docstring_arguments(
    session_handler: "MatlabHandler",
    parse_arguments: bool,
    show_docstring_examples: bool,
    docstring_section_style: str,
) -> None:
    final_options = {
        "parse_arguments": parse_arguments,
        "show_docstring_examples": show_docstring_examples,
        "docstring_section_style": docstring_section_style,
    }
    html = _render(session_handler, "module_arguments", final_options)
    snapshot_key = tuple(sorted(final_options.items()))
    assert outsource(html, suffix=".html") == snapshots.docstring_arguments[snapshot_key]


@pytest.mark.parametrize("docstring_style", ["google", "numpy", "sphinx", None])
def test_end_to_end_docstring_style(
    session_handler: "MatlabHandler",
    docstring_style: str | None,
) -> None:
    final_options = {
        "docstring_style": docstring_style,
    }
    html = _render(session_handler, "forced_docstring", final_options)
    snapshot_key = tuple(sorted(final_options.items()))
    assert outsource(html, suffix=".html") == snapshots.docstring_style[snapshot_key]


@pytest.mark.parametrize("show_if_no_docstring", [True, False])
def test_end_to_end_no_docstring(
    session_handler: "MatlabHandler",
    show_if_no_docstring: bool,
) -> None:
    final_options = {
        "show_if_no_docstring": show_if_no_docstring,
    }
    html = _render(session_handler, "+moduleNamespace.internal", final_options)
    snapshot_key = tuple(sorted(final_options.items()))
    assert outsource(html, suffix=".html") == snapshots.no_docstring[snapshot_key]


@pytest.mark.parametrize("show_docstring_properties", [True, False])
@pytest.mark.parametrize("show_docstring_description", [True, False])
@pytest.mark.parametrize("merge_constructor_into_class", [True, False])
def test_end_to_end_docstring_class(
    session_handler: "MatlabHandler",
    show_docstring_properties: bool,
    show_docstring_description: bool,
    merge_constructor_into_class: bool,
) -> None:
    final_options = {
        "show_docstring_properties": show_docstring_properties,
        "show_docstring_description": show_docstring_description,
        "merge_constructor_into_class": merge_constructor_into_class,
    }
    html = _render(session_handler, "subClass", final_options)
    snapshot_key = tuple(sorted(final_options.items()))
    assert outsource(html, suffix=".html") == snapshots.docstring_class[snapshot_key]


@pytest.mark.parametrize("show_docstring_functions", [True, False])
@pytest.mark.parametrize("show_docstring_classes", [True, False])
@pytest.mark.parametrize("show_docstring_namespaces", [True, False])
def test_end_to_end_docstring_namespace(
    session_handler: "MatlabHandler",
    show_docstring_functions: bool,
    show_docstring_classes: bool,
    show_docstring_namespaces: bool,
) -> None:
    final_options = {
        "show_docstring_functions": show_docstring_functions,
        "show_docstring_classes": show_docstring_classes,
        "show_docstring_namespaces": show_docstring_namespaces,
    }
    html = _render(session_handler, "+moduleNamespace", final_options)
    snapshot_key = tuple(sorted(final_options.items()))
    assert outsource(html, suffix=".html") == snapshots.docstring_namespace[snapshot_key]


@pytest.mark.parametrize("show_docstring_input_arguments", [True, False])
@pytest.mark.parametrize("show_docstring_name_value_arguments", [True, False])
@pytest.mark.parametrize("show_docstring_output_arguments", [True, False])
def test_end_to_end_docstring_function(
    session_handler: "MatlabHandler",
    show_docstring_input_arguments: bool,
    show_docstring_name_value_arguments: bool,
    show_docstring_output_arguments: bool,
) -> None:
    final_options = {
        "show_docstring_input_arguments": show_docstring_input_arguments,
        "show_docstring_name_value_arguments": show_docstring_name_value_arguments,
        "show_docstring_output_arguments": show_docstring_output_arguments,
    }
    html = _render(session_handler, "module_arguments", final_options)
    snapshot_key = tuple(sorted(final_options.items()))
    assert outsource(html, suffix=".html") == snapshots.docstring_function[snapshot_key]


@pytest.mark.parametrize("show_signature_annotations", [True, False])
@pytest.mark.parametrize("signature_crossrefs", [True, False])
@pytest.mark.parametrize("separate_signature", [True, False])
def test_end_to_end_for_signatures(
    session_handler: "MatlabHandler",
    show_signature_annotations: bool,
    signature_crossrefs: bool,
    separate_signature: bool,
) -> None:
    final_options = {
        "show_signature_annotations": show_signature_annotations,
        "signature_crossrefs": signature_crossrefs,
        "separate_signature": separate_signature,
    }
    html = _render(session_handler, "module_arguments", final_options)
    snapshot_key = tuple(sorted(final_options.items()))
    assert outsource(html, suffix=".html") == snapshots.signatures[snapshot_key]
