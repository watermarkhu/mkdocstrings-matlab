"""Tests for MATLAB live script documentation support."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from mkdocstrings import CollectionError

from mkdocstrings_handlers.matlab import MatlabConfig, MatlabHandler
from mkdocstrings_handlers.matlab.rendering import do_strip_livescript_comments

if TYPE_CHECKING:
    pass


# ---------------------------------------------------------------------------
# Tests for do_strip_livescript_comments
# ---------------------------------------------------------------------------


def test_strip_livescript_comments_empty() -> None:
    """Assert empty string is returned unchanged."""
    assert do_strip_livescript_comments("") == ""


def test_strip_livescript_comments_plain_text() -> None:
    """Assert lines without % prefix are returned unchanged (binary .mlx text)."""
    content = "This is plain text.\nWith multiple lines."
    assert do_strip_livescript_comments(content) == content


def test_strip_livescript_comments_percent_lines() -> None:
    """Assert % prefix is stripped from comment lines."""
    content = "% First line\n% Second line"
    result = do_strip_livescript_comments(content)
    assert result == "First line\nSecond line"


def test_strip_livescript_comments_percent_space_lines() -> None:
    """Assert '% ' prefix (with space) is stripped from comment lines."""
    content = "% First line\n% Second line\n%No space after percent"
    result = do_strip_livescript_comments(content)
    assert result == "First line\nSecond line\nNo space after percent"


def test_strip_livescript_comments_mixed() -> None:
    """Assert mixed comment and code lines are handled correctly."""
    content = "% This is a comment\nx = 1;\n% Another comment"
    result = do_strip_livescript_comments(content)
    assert result == "This is a comment\nx = 1;\nAnother comment"


# ---------------------------------------------------------------------------
# Tests for live script collection via path-based identifiers
# ---------------------------------------------------------------------------


def test_collect_livescript_plaintext() -> None:
    """Assert a R2025a plain-text live script .m file can be collected by path."""
    repo_root = Path(__file__).parent.parent

    handler = MatlabHandler(
        base_dir=repo_root,
        config=MatlabConfig.from_data(paths=["."]),
        theme="material",
        custom_templates=None,
        mdx=[],
        mdx_config={},
    )

    model = handler.collect("test/fixture/my_livescript.m", handler.get_options({}))
    assert model is not None
    assert model.name == "my_livescript"
    assert hasattr(model, "sections")
    assert len(model.sections) > 0


def test_collect_livescript_sections() -> None:
    """Assert collected live script has correctly classified sections."""
    repo_root = Path(__file__).parent.parent

    handler = MatlabHandler(
        base_dir=repo_root,
        config=MatlabConfig.from_data(paths=["."]),
        theme="material",
        custom_templates=None,
        mdx=[],
        mdx_config={},
    )

    model = handler.collect("test/fixture/my_livescript.m", handler.get_options({}))
    assert model is not None

    # Check that sections have the expected kinds
    section_kinds = {s.kind for s in model.sections}
    assert "text" in section_kinds
    assert "code" in section_kinds


def test_collect_livescript_not_found(tmp_path: Path) -> None:
    """Assert CollectionError is raised for a non-existent live script path."""
    handler = MatlabHandler(
        base_dir=tmp_path,
        config=MatlabConfig.from_data(paths=["."]),
        theme="material",
        custom_templates=None,
        mdx=[],
        mdx_config={},
    )

    with pytest.raises(CollectionError, match="is not a valid path"):
        handler.collect("nonexistent/livescript.mlx", handler.get_options({}))


def test_collect_livescript_mlx(tmp_path: Path) -> None:
    """Assert a plain-text .mlx live script can be collected by path."""
    from maxx.livescript import LiveScriptParser

    # Create a minimal plain-text .mlx file (not binary ZIP) for testing
    mlx_file = tmp_path / "demo.mlx"
    mlx_file.write_text("%% Demo\n% A simple live script.\nx = 42;\n")

    handler = MatlabHandler(
        base_dir=tmp_path,
        config=MatlabConfig.from_data(paths=["."]),
        theme="material",
        custom_templates=None,
        mdx=[],
        mdx_config={},
    )

    model = handler.collect("demo.mlx", handler.get_options({}))
    assert model is not None
    assert model.name == "demo"
    assert hasattr(model, "sections")


def test_collect_livescript_invalid_mlx(tmp_path: Path) -> None:
    """Assert CollectionError with message is raised for an invalid binary .mlx file."""
    # Write a file that claims to be a binary ZIP .mlx but is not valid
    mlx_file = tmp_path / "bad.mlx"
    mlx_file.write_bytes(b"PK\x03\x04invalid content")

    handler = MatlabHandler(
        base_dir=tmp_path,
        config=MatlabConfig.from_data(paths=["."]),
        theme="material",
        custom_templates=None,
        mdx=[],
        mdx_config={},
    )

    with pytest.raises(CollectionError, match="bad.mlx"):
        handler.collect("bad.mlx", handler.get_options({}))


# ---------------------------------------------------------------------------
# Tests for parse_live_scripts config option
# ---------------------------------------------------------------------------


def test_parse_live_scripts_config_default() -> None:
    """Assert parse_live_scripts defaults to False."""
    config = MatlabConfig.from_data()
    assert config.parse_live_scripts is False


def test_parse_live_scripts_config_enabled() -> None:
    """Assert parse_live_scripts can be set to True."""
    config = MatlabConfig.from_data(parse_live_scripts=True)
    assert config.parse_live_scripts is True


def test_handler_parse_live_scripts_passed_to_collection(tmp_path: Path) -> None:
    """Assert parse_live_scripts is passed to the PathsCollection."""
    handler = MatlabHandler(
        base_dir=tmp_path,
        config=MatlabConfig.from_data(parse_live_scripts=True),
        theme="material",
        custom_templates=None,
        mdx=[],
        mdx_config={},
    )
    assert handler._paths_collection._parse_live_scripts is True


# ---------------------------------------------------------------------------
# Tests for live script template rendering
# ---------------------------------------------------------------------------


def test_live_script_template_exists(handler: MatlabHandler) -> None:
    """Assert the live_script template exists in the Jinja environment."""
    templates = handler.env.list_templates()
    assert "live_script.html.jinja" in templates


def test_strip_livescript_comments_filter_registered(handler: MatlabHandler) -> None:
    """Assert the strip_livescript_comments filter is registered."""
    assert "strip_livescript_comments" in handler.env.filters


def test_render_livescript(handler: MatlabHandler) -> None:
    """Assert a live script can be rendered to HTML."""
    from maxx.objects import LiveScript, LiveScriptSection

    live_script = LiveScript(
        "demo",
        sections=[
            LiveScriptSection("text", "% A simple demo."),
            LiveScriptSection("code", "x = 42;"),
        ],
    )

    options = handler.get_options({})
    html = handler.render(live_script, options)
    assert html is not None
    assert len(html) > 0
    # The HTML should contain the code (rendered with syntax highlighting)
    assert "42" in html
    # The text section (after stripping %) should be rendered
    assert "A simple demo" in html
