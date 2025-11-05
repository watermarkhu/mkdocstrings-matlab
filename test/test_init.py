"""Tests for the `__init__` module."""

from __future__ import annotations

import logging


def test_return_type_warning_filter() -> None:
    """Test that the ReturnTypeWarningFilter correctly filters warnings."""
    from mkdocstrings_handlers.matlab import ReturnTypeWarningFilter

    filter_instance = ReturnTypeWarningFilter()

    # Create a mock log record with the warning message
    record_with_warning = logging.LogRecord(
        name="test",
        level=logging.WARNING,
        pathname="test.py",
        lineno=1,
        msg="No type or annotation for returned value",
        args=(),
        exc_info=None,
    )

    # Create a mock log record without the warning message
    record_without_warning = logging.LogRecord(
        name="test",
        level=logging.WARNING,
        pathname="test.py",
        lineno=1,
        msg="Some other warning",
        args=(),
        exc_info=None,
    )

    # The filter should block the return type warning
    assert filter_instance.filter(record_with_warning) is False

    # The filter should allow other warnings
    assert filter_instance.filter(record_without_warning) is True


def test_return_type_warning_filter_no_msg() -> None:
    """Test that the filter handles records without msg attribute."""
    from mkdocstrings_handlers.matlab import ReturnTypeWarningFilter

    filter_instance = ReturnTypeWarningFilter()

    # Create a mock log record without msg attribute
    record = logging.LogRecord(
        name="test",
        level=logging.WARNING,
        pathname="test.py",
        lineno=1,
        msg="",
        args=(),
        exc_info=None,
    )
    delattr(record, "msg")

    # The filter should not crash and should return True
    assert filter_instance.filter(record) is True


def test_docstring_section_extensions() -> None:
    """Test that custom MATLAB docstring sections are registered."""
    from griffe._internal.docstrings import google, numpy
    from griffe._internal.enumerations import DocstringSectionKind

    # Check that MATLAB-specific sections are registered in Google parser
    assert google._section_kind.get("arguments") == DocstringSectionKind.parameters
    assert google._section_kind.get("input arguments") == DocstringSectionKind.parameters
    assert google._section_kind.get("outputs") == DocstringSectionKind.returns
    assert google._section_kind.get("output arguments") == DocstringSectionKind.returns
    assert google._section_kind.get("name value arguments") == DocstringSectionKind.other_parameters
    assert google._section_kind.get("name-value arguments") == DocstringSectionKind.other_parameters
    assert google._section_kind.get("name value pairs") == DocstringSectionKind.other_parameters
    assert google._section_kind.get("name-value pairs") == DocstringSectionKind.other_parameters
    assert google._section_kind.get("properties") == DocstringSectionKind.attributes
    assert google._section_kind.get("namespaces") == DocstringSectionKind.modules
    assert google._section_kind.get("packages") == DocstringSectionKind.modules

    # Check that MATLAB-specific sections are registered in NumPy parser
    assert numpy._section_kind.get("arguments") == DocstringSectionKind.parameters
    assert numpy._section_kind.get("input arguments") == DocstringSectionKind.parameters
    assert numpy._section_kind.get("outputs") == DocstringSectionKind.returns
    assert numpy._section_kind.get("output arguments") == DocstringSectionKind.returns
    assert numpy._section_kind.get("name value arguments") == DocstringSectionKind.other_parameters
    assert numpy._section_kind.get("properties") == DocstringSectionKind.attributes
    assert numpy._section_kind.get("namespaces") == DocstringSectionKind.modules
