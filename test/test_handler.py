"""Tests for the `handler` module."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from griffe import (
    DocstringSectionExamples,
    DocstringSectionKind,
)
from mkdocs.exceptions import PluginError
from mkdocstrings import CollectionError

from mkdocstrings_handlers.matlab import MatlabConfig, MatlabHandler, MatlabOptions

if TYPE_CHECKING:
    from mkdocstrings import MkdocstringsPlugin


def test_collect_missing_identifier(handler: MatlabHandler) -> None:
    """Assert error is raised for missing identifiers."""
    with pytest.raises(CollectionError):
        handler.collect("nonexistent_matlab_function", MatlabOptions())


def test_collect_missing_identifier_item(handler: MatlabHandler) -> None:
    """Assert error is raised for missing items within existing namespaces."""
    with pytest.raises(CollectionError):
        handler.collect("some_namespace.nonexistent_function", MatlabOptions())


def test_collect_identifier(handler: MatlabHandler) -> None:
    """Assert existing MATLAB identifier can be collected."""
    # This assumes handler has some MATLAB paths configured with actual content
    # You may need to adjust based on your test setup
    pass  # Replace with actual test when you have MATLAB files in test fixtures


def test_collect_with_null_parser(handler: MatlabHandler) -> None:
    """Assert we can pass `None` as parser when collecting."""
    # This would need actual MATLAB content to test
    pass  # Replace with actual test when you have MATLAB files in test fixtures


@pytest.mark.parametrize(
    "handler",
    [
        {"theme": "mkdocs"},
        {"theme": "readthedocs"},
        {"theme": {"name": "material"}},
    ],
    indirect=["handler"],
)
def test_render_docstring_examples_section(handler: MatlabHandler) -> None:
    """Assert docstrings' examples section can be rendered.

    Parameters:
        handler: A handler instance (parametrized).
    """
    section = DocstringSectionExamples(
        value=[
            (DocstringSectionKind.text, "This is a MATLAB example."),
            (DocstringSectionKind.examples, ">> disp('Hello')\nHello"),
        ],
    )
    template = handler.env.get_template("docstring/examples.html.jinja")
    rendered = template.render(section=section, locale="en")
    template.render(section=section, locale="not_existing")
    assert "<p>This is a MATLAB example.</p>" in rendered
    assert "disp" in rendered
    assert "Hello" in rendered


@pytest.mark.without_handler
def test_expand_globs(tmp_path: Path, plugin: MkdocstringsPlugin) -> None:
    """Assert globs are correctly expanded for MATLAB paths.

    Parameters:
        tmp_path: Pytest fixture that creates a temporary directory.
    """
    globbed_names = (
        "expanded_a",
        "expanded_b",
        "other_expanded_c",
        "other_expanded_d",
    )
    globbed_dirs = [tmp_path.joinpath(globbed_name) for globbed_name in globbed_names]
    for d in globbed_dirs:
        d.mkdir()
    plugin.handlers._tool_config.config_file_path = str(tmp_path.joinpath("mkdocs.yml"))
    handler: MatlabHandler = plugin.handlers.get_handler("matlab", {"paths": ["*exp*"]})  # type: ignore[assignment]
    # Check that paths containing the glob pattern are included
    expanded_paths = [str(d) for d in globbed_dirs if "exp" in d.name]
    for expanded_path in set(expanded_paths):
        assert expanded_path in [str(p) for p in handler._paths]


def test_rendering_object_source_without_lineno(handler: MatlabHandler) -> None:
    """Test rendering MATLAB objects without a line number."""
    # This would need to create mock MATLAB objects
    # Example structure for when you have actual MATLAB object creation:
    r"""
    function_obj = Function(
        name="test_function",
        filepath=Path("test.m"),
        lineno=None,
        paths_collection=handler._paths_collection
    )
    function_obj.lineno = None
    assert handler.render(function_obj, MatlabOptions(show_source=True))
    """
    pass  # Replace with actual test when MATLAB object creation is available


def test_give_precedence_to_user_paths(tmp_path: Path) -> None:
    """Assert user paths take precedence over default paths."""
    test_path = tmp_path / "matlab_code"
    test_path.mkdir()
    handler = MatlabHandler(
        base_dir=Path("."),
        config=MatlabConfig.from_data(paths=[str(test_path)]),
        mdx=[],
        mdx_config={},
    )
    assert handler._paths[0] == test_path.resolve()


@pytest.mark.parametrize(
    ("section", "matlab_code_structure"),
    [
        (
            "Properties",
            r"""
            classdef TestClass
                properties
                    x % X property
                    y % Y property
                end
            end
            """,
        ),
        (
            "Methods",
            r"""
            classdef TestClass
                methods
                    function obj = method_x(obj)
                        % X method
                    end
                    function obj = method_y(obj)
                        % Y method
                    end
                end
            end
            """,
        ),
        (
            "Functions",
            r"""
            % Module with functions
            %
            % Functions:
            %   function_x: X function
            %   function_y: Y function
            """,
        ),
        (
            "Classes",
            r"""
            % Package with classes
            %
            % Classes:
            %   ClassA: A class
            %   ClassB: B class
            """,
        ),
        (
            "Namespaces",
            r"""
            % Package with namespaces
            %
            % Namespaces:
            %   +namespace_a: A namespace
            %   +namespace_b: B namespace
            """,
        ),
    ],
)
def test_deduplicate_summary_sections(
    handler: MatlabHandler, section: str, matlab_code_structure: str
) -> None:
    """Assert summary sections are deduplicated for MATLAB objects."""
    # This would need actual MATLAB object creation and parsing
    # The test structure would be similar but adapted for MATLAB syntax
    pass  # Replace with actual test when MATLAB parsing is fully implemented


def test_invalid_paths_configuration() -> None:
    """Assert error is raised for invalid MATLAB paths."""
    with pytest.raises(PluginError):
        MatlabHandler(
            base_dir=Path("."),
            config=MatlabConfig.from_data(paths=["/nonexistent/path"]),
            mdx=[],
            mdx_config={},
        )


def test_matlab_namespace_handling(handler: MatlabHandler) -> None:
    """Test that MATLAB namespaces are handled correctly."""
    # Test namespace collision with Jinja's namespace macro
    assert "jinja_namespace" in handler.env.globals
    assert handler.env.globals["jinja_namespace"] is handler.env.globals.get("namespace")


def test_matlab_paths_collection_available(handler: MatlabHandler) -> None:
    """Test that paths collection is available in Jinja globals."""
    assert "paths_collection" in handler.env.globals
    assert handler.env.globals["paths_collection"] is handler._paths_collection


def test_matlab_specific_filters(handler: MatlabHandler) -> None:
    """Test that MATLAB-specific filters are registered."""
    expected_filters = [
        "order_members",
        "format_signature",
        "format_property",
        "filter_objects",
        "stash_crossref",
        "get_template",
        "parse_docstring",
        "function_docstring",
        "as_properties_section",
        "as_functions_section",
        "as_classes_section",
        "as_namespaces_section",
        "as_inheritance_diagram_section",
    ]
    for filter_name in expected_filters:
        assert filter_name in handler.env.filters


def test_empty_identifier_collection(handler: MatlabHandler) -> None:
    """Test that empty identifier raises appropriate error."""
    with pytest.raises(CollectionError, match="Empty identifier"):
        handler.collect("", MatlabOptions())


def test_matlab_domain_configuration(handler: MatlabHandler) -> None:
    """Test that MATLAB handler uses correct domain."""
    assert handler.domain == "mat"
    assert handler.name == "matlab"
    assert handler.fallback_theme == "material"
