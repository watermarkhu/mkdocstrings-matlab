"""Configuration for the pytest test suite."""

from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING

import pytest

from test import helpers

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path

    from markdown.core import Markdown
    from mkdocs.config.defaults import MkDocsConfig
    from mkdocstrings import MkdocstringsPlugin

    from mkdocstrings_handlers.matlab import MatlabHandler


# --------------------------------------------
# Function-scoped fixtures.
# --------------------------------------------
@pytest.fixture
def mkdocs_conf(request: pytest.FixtureRequest, tmp_path: Path) -> Iterator[MkDocsConfig]:
    """Yield a MkDocs configuration object.

    Parameters:
        request: Pytest fixture.
        tmp_path: Pytest fixture.

    Yields:
        MkDocs config.
    """
    with helpers.mkdocs_conf(request, tmp_path) as mkdocs_conf:
        yield mkdocs_conf


@pytest.fixture
def plugin(mkdocs_conf: MkDocsConfig) -> MkdocstringsPlugin:
    """Return a plugin instance.

    Parameters:
        mkdocs_conf: Pytest fixture (see conftest.py).

    Returns:
        mkdocstrings plugin instance.
    """
    return helpers.plugin(mkdocs_conf)


@pytest.fixture
def ext_markdown(mkdocs_conf: MkDocsConfig) -> Markdown:
    """Return a Markdown instance with MkdocstringsExtension.

    Parameters:
        mkdocs_conf: Pytest fixture (see conftest.py).

    Returns:
        A Markdown instance.
    """
    return helpers.ext_markdown(mkdocs_conf)


@pytest.fixture
def handler(plugin: MkdocstringsPlugin, ext_markdown: Markdown) -> Iterator[MatlabHandler]:
    """Return a handler instance.

    Parameters:
        plugin: Pytest fixture (see conftest.py).

    Returns:
        A handler instance.
    """
    handler = helpers.handler(plugin, ext_markdown)
    yield handler
    assert len(handler.env.filters["stash_crossref"].stash) == 0


# --------------------------------------------
# Session-scoped fixtures.
# --------------------------------------------
@pytest.fixture(scope="session")
def session_mkdocs_conf(
    request: pytest.FixtureRequest,
    tmp_path_factory: pytest.TempPathFactory,
) -> Iterator[MkDocsConfig]:
    """Yield a MkDocs configuration object.

    Parameters:
        request: Pytest fixture.
        tmp_path: Pytest fixture.

    Yields:
        MkDocs config.
    """
    with helpers.mkdocs_conf(request, tmp_path_factory.mktemp("project")) as mkdocs_conf:
        yield mkdocs_conf


@pytest.fixture(scope="session")
def session_plugin(session_mkdocs_conf: MkDocsConfig) -> MkdocstringsPlugin:
    """Return a plugin instance.

    Parameters:
        mkdocs_conf: Pytest fixture (see conftest.py).

    Returns:
        mkdocstrings plugin instance.
    """
    return helpers.plugin(session_mkdocs_conf)


@pytest.fixture(scope="session")
def session_ext_markdown(session_mkdocs_conf: MkDocsConfig) -> Markdown:
    """Return a Markdown instance with MkdocstringsExtension.

    Parameters:
        mkdocs_conf: Pytest fixture (see conftest.py).

    Returns:
        A Markdown instance.
    """
    return helpers.ext_markdown(session_mkdocs_conf)


@pytest.fixture(scope="session")
def session_handler(
    session_plugin: MkdocstringsPlugin, session_ext_markdown: Markdown
) -> Iterator[MatlabHandler]:
    """Return a handler instance.

    Parameters:
        plugin: Pytest fixture (see conftest.py).

    Returns:
        A handler instance.
    """
    handler = helpers.handler(session_plugin, session_ext_markdown)
    yield handler
    assert len(handler.env.filters["stash_crossref"].stash) == 0


@pytest.fixture(autouse=True)
def disable_cached_property(monkeypatch):
    def identity(x):
        return x

    monkeypatch.setattr("functools.cached_property", identity)
