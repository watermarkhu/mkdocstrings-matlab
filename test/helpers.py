"""Configuration for the pytest test suite."""

from __future__ import annotations

from collections import ChainMap
from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING, Any

from markdown.core import Markdown
from mkdocs.config.defaults import MkDocsConfig

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path

    import pytest
    from mkdocstrings import MkdocstringsPlugin

    from mkdocstrings_handlers.matlab import MatlabHandler


@contextmanager
def mkdocs_conf(request: pytest.FixtureRequest, tmp_path: Path) -> Iterator[MkDocsConfig]:
    """Yield a MkDocs configuration object.

    Parameters:
        request: Pytest request fixture.
        tmp_path: Temporary path.

    Yields:
        MkDocs config.
    """
    while hasattr(request, "_parent_request") and hasattr(
        request._parent_request, "_parent_request"
    ):
        request = request._parent_request

    mkdocstring_config = {"default_handler": "matlab"}
    marker = request.node.get_closest_marker("without_handler")
    if marker is None:
        mkdocstring_config["handlers"] = {"matlab": {"paths": ["fixture"]}}

    conf = MkDocsConfig()
    conf_dict = {
        "site_name": "foo",
        "site_url": "https://example.org/",
        "site_dir": str(tmp_path),
        "plugins": [{"mkdocstrings": mkdocstring_config}],
        **getattr(request, "param", {}),
    }
    # Re-create it manually as a workaround for https://github.com/mkdocs/mkdocs/issues/2289
    mdx_configs: dict[str, Any] = dict(ChainMap(*conf_dict.get("markdown_extensions", [])))

    conf.load_dict(conf_dict)
    conf.config_file_path = str((Path(__file__).parent / "mkdocs.yml").resolve())
    assert conf.validate() == ([], [])

    conf["mdx_configs"] = mdx_configs
    conf["markdown_extensions"].insert(0, "toc")  # Guaranteed to be added by MkDocs.

    conf = conf["plugins"]["mkdocstrings"].on_config(conf)
    conf = conf["plugins"]["autorefs"].on_config(conf)
    yield conf
    conf["plugins"]["mkdocstrings"].on_post_build(conf)


def plugin(mkdocs_conf: MkDocsConfig) -> MkdocstringsPlugin:
    """Return a plugin instance.

    Parameters:
        mkdocs_conf: MkDocs configuration.

    Returns:
        mkdocstrings plugin instance.
    """
    return mkdocs_conf["plugins"]["mkdocstrings"]


def ext_markdown(mkdocs_conf: MkDocsConfig) -> Markdown:
    """Return a Markdown instance with MkdocstringsExtension.

    Parameters:
        mkdocs_conf: MkDocs configuration.

    Returns:
        A Markdown instance.
    """
    return Markdown(
        extensions=mkdocs_conf["markdown_extensions"], extension_configs=mkdocs_conf["mdx_configs"]
    )


def handler(plugin: MkdocstringsPlugin, ext_markdown: Markdown) -> MatlabHandler:
    """Return a handler instance.

    Parameters:
        plugin: Plugin instance.

    Returns:
        A handler instance.
    """
    handler = plugin.handlers.get_handler("matlab")
    handler._update_env(ext_markdown)
    return handler
