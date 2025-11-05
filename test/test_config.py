"""Tests for the `config` module."""

from __future__ import annotations

from mkdocstrings_handlers.matlab.config import (
    AutoStyleOptions,
    GoogleStyleOptions,
    MatlabConfig,
    MatlabInputOptions,
    MatlabOptions,
    NumpyStyleOptions,
    PerStyleOptions,
    SphinxStyleOptions,
    SummaryOption,
)


def test_google_style_options_defaults() -> None:
    """Test GoogleStyleOptions with default values."""
    options = GoogleStyleOptions()
    assert options.ignore_init_summary is False
    assert options.returns_multiple_items is True
    assert options.returns_named_value is True
    assert options.returns_type_in_property_summary is False
    assert options.receives_multiple_items is True
    assert options.receives_named_value is True
    assert options.trim_doctest_flags is True
    assert options.warn_unknown_params is True


def test_numpy_style_options_defaults() -> None:
    """Test NumpyStyleOptions with default values."""
    options = NumpyStyleOptions()
    assert options.ignore_init_summary is False
    assert options.trim_doctest_flags is True
    assert options.warn_unknown_params is True


def test_sphinx_style_options() -> None:
    """Test SphinxStyleOptions creation."""
    options = SphinxStyleOptions()
    assert options is not None


def test_per_style_options_from_data() -> None:
    """Test PerStyleOptions.from_data with nested options."""
    data = {
        "google": {"ignore_init_summary": True},
        "numpy": {"trim_doctest_flags": False},
        "sphinx": {},
    }
    options = PerStyleOptions.from_data(**data)
    assert isinstance(options.google, GoogleStyleOptions)
    assert options.google.ignore_init_summary is True
    assert isinstance(options.numpy, NumpyStyleOptions)
    assert options.numpy.trim_doctest_flags is False
    assert isinstance(options.sphinx, SphinxStyleOptions)


def test_auto_style_options_from_data() -> None:
    """Test AutoStyleOptions.from_data with per_style_options."""
    data = {
        "method": "max_sections",
        "default": "google",
        "per_style_options": {
            "google": {"ignore_init_summary": True},
        },
    }
    options = AutoStyleOptions.from_data(**data)
    assert options.method == "max_sections"
    assert options.default == "google"
    assert isinstance(options.per_style_options, PerStyleOptions)
    assert options.per_style_options.google.ignore_init_summary is True


def test_summary_option_defaults() -> None:
    """Test SummaryOption with default values."""
    option = SummaryOption()
    assert option.properties is False
    assert option.functions is False
    assert option.classes is False
    assert option.namespaces is False


def test_matlab_input_options_coerce_docstring_options() -> None:
    """Test MatlabInputOptions.coerce with different docstring styles."""
    # Test Google style
    data = {"docstring_style": "google", "docstring_options": {"ignore_init_summary": True}}
    coerced = MatlabInputOptions.coerce(**data)
    assert isinstance(coerced["docstring_options"], GoogleStyleOptions)
    assert coerced["docstring_options"].ignore_init_summary is True

    # Test NumPy style
    data = {"docstring_style": "numpy", "docstring_options": {"trim_doctest_flags": False}}
    coerced = MatlabInputOptions.coerce(**data)
    assert isinstance(coerced["docstring_options"], NumpyStyleOptions)
    assert coerced["docstring_options"].trim_doctest_flags is False

    # Test Sphinx style
    data = {"docstring_style": "sphinx", "docstring_options": {}}
    coerced = MatlabInputOptions.coerce(**data)
    assert isinstance(coerced["docstring_options"], SphinxStyleOptions)

    # Test Auto style
    data = {"docstring_style": "auto", "docstring_options": {"method": "max_sections"}}
    coerced = MatlabInputOptions.coerce(**data)
    assert isinstance(coerced["docstring_options"], AutoStyleOptions)
    assert coerced["docstring_options"].method == "max_sections"


def test_matlab_input_options_coerce_summary() -> None:
    """Test MatlabInputOptions.coerce with summary options."""
    # Test summary as True
    data = {"summary": True}
    coerced = MatlabInputOptions.coerce(**data)
    assert isinstance(coerced["summary"], SummaryOption)
    assert coerced["summary"].properties is True
    assert coerced["summary"].functions is True
    assert coerced["summary"].classes is True
    assert coerced["summary"].namespaces is True

    # Test summary as False
    data = {"summary": False}
    coerced = MatlabInputOptions.coerce(**data)
    assert isinstance(coerced["summary"], SummaryOption)
    assert coerced["summary"].properties is False
    assert coerced["summary"].functions is False
    assert coerced["summary"].classes is False
    assert coerced["summary"].namespaces is False

    # Test summary as dict
    data = {
        "summary": {"properties": True, "functions": False, "classes": True, "namespaces": False}
    }
    coerced = MatlabInputOptions.coerce(**data)
    assert isinstance(coerced["summary"], SummaryOption)
    assert coerced["summary"].properties is True
    assert coerced["summary"].functions is False
    assert coerced["summary"].classes is True
    assert coerced["summary"].namespaces is False


def test_matlab_options_coerce_filters() -> None:
    """Test MatlabOptions.coerce with filter patterns."""
    import re

    # Test with regular filters
    data = {"filters": ["!^_", "test*"]}
    coerced = MatlabOptions.coerce(**data)
    assert len(coerced["filters"]) == 2
    assert isinstance(coerced["filters"][0][0], re.Pattern)
    assert coerced["filters"][0][1] is True  # Exclude pattern
    assert isinstance(coerced["filters"][1][0], re.Pattern)
    assert coerced["filters"][1][1] is False  # Include pattern

    # Test with None filters
    data = {"filters": None}
    coerced = MatlabOptions.coerce(**data)
    assert coerced["filters"] == []

    # Test with empty filters
    data = {"filters": []}
    coerced = MatlabOptions.coerce(**data)
    assert coerced["filters"] == []


def test_matlab_input_options_extract_extra() -> None:
    """Test MatlabInputOptions._extract_extra method."""
    data = {
        "heading_level": 2,
        "show_source": True,
        "custom_option": "value",
        "another_custom": 123,
    }
    extra, remaining = MatlabInputOptions._extract_extra(data)
    assert "custom_option" in extra
    assert "another_custom" in extra
    assert "heading_level" in remaining
    assert "show_source" in remaining


def test_matlab_config_from_data() -> None:
    """Test MatlabConfig.from_data creation."""
    data = {
        "paths": ["src", "lib"],
        "paths_recursive": True,
        "options": {"heading_level": 3},
        "locale": "en",
    }
    config = MatlabConfig.from_data(**data)
    assert config.paths == ["src", "lib"]
    assert config.paths_recursive is True
    assert config.locale == "en"


def test_matlab_input_options_defaults() -> None:
    """Test MatlabInputOptions with all default values."""
    options = MatlabInputOptions()
    assert options.docstring_section_style == "table"
    assert options.docstring_style == "auto"
    assert options.parse_arguments is True
    assert options.group_by_category is True
    assert options.heading == ""
    assert options.heading_level == 2
    assert options.hidden_members is False
    assert options.private_members is False
    assert options.inherited_members is False
    assert options.line_length == 60
    assert options.members is None
    assert options.members_order == "alphabetical"
    assert options.merge_constructor_into_class is False
    assert options.argument_headings is False
    assert options.separate_signature is False
    assert options.show_bases is True
    assert options.show_category_heading is False
    assert options.show_docstring_classes is True
    assert options.show_docstring_description is True
    assert options.show_docstring_examples is True
    assert options.show_docstring_functions is True
    assert options.show_docstring_namespaces is True
    assert options.show_docstring_properties is True
    assert options.show_docstring_input_arguments is True
    assert options.show_docstring_name_value_arguments is True
    assert options.show_docstring_output_arguments is True
    assert options.show_if_no_docstring is False
    assert options.show_inheritance_diagram is False
    assert options.show_attributes is True
    assert options.show_object_full_path is False
    assert options.show_root_full_path is True
    assert options.show_root_heading is False
    assert options.show_root_members_full_path is False
    assert options.show_root_toc_entry is True
    assert options.show_signature_types is False
    assert options.show_signature is True
    assert options.show_source is True
    assert options.show_subnamespaces is False
    assert options.show_symbol_type_heading is False
    assert options.show_symbol_type_toc is False
    assert options.signature_crossrefs is False
    assert options.toc_label == ""
    assert isinstance(options.summary, SummaryOption)
    assert isinstance(options.extra, dict)


def test_matlab_options_from_data() -> None:
    """Test MatlabOptions.from_data with filter coercion."""
    data = {
        "filters": ["!^_private", "public*"],
        "summary": True,
    }
    options = MatlabOptions.from_data(**data)
    assert len(options.filters) == 2
    assert isinstance(options.summary, SummaryOption)
    assert options.summary.properties is True
