"""Tests for the `rendering` module."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

import pytest

from mkdocstrings_handlers.matlab import rendering


@dataclass
class _FakeMatlabObject:
    name: str
    inherited: bool = False
    parent: None = None
    is_alias: bool = False
    is_private: bool = False
    is_hidden: bool = False
    path: str = ""

    def __post_init__(self):
        if not self.path:
            self.path = self.name


@pytest.mark.parametrize(
    ("names", "filter_params", "expected_names"),
    [
        # Test name filtering with regex
        (
            ["funcA", "funcB", "funcC", "methodD"],
            {"filters": [(re.compile("^func[^B]"), True)]},
            {"funcB", "methodD"},
        ),
        # Test explicit members list
        (
            ["funcA", "funcB", "funcC", "methodD"],
            {"members_list": ["funcA", "funcB"]},
            {"funcA", "funcB"},
        ),
        # Test private member filtering
        (["publicFunc", "_privateFunc"], {"private_members": False}, {"publicFunc"}),
        # Test hidden member filtering
        (["normalFunc", "__hiddenFunc"], {"hidden_members": False}, {"normalFunc"}),
    ],
)
def test_filter_objects(
    names: list[str], filter_params: dict[str, Any], expected_names: set[str]
) -> None:
    """Assert the MATLAB objects filter works correctly.

    Parameters:
        names: Names of the MATLAB objects.
        filter_params: Parameters passed to the filter function.
        expected_names: Names expected to be kept.
    """
    objects = {}
    for name in names:
        obj = _FakeMatlabObject(name)
        # Set private/hidden status based on naming convention
        if name.startswith("_") and not name.startswith("__"):
            obj.is_private = True
        elif name.startswith("__"):
            obj.is_hidden = True
        objects[name] = obj

    filtered = rendering.do_filter_objects(objects, **filter_params)  # type: ignore[arg-type]
    filtered_names = {obj.name for obj in filtered}
    assert set(filtered_names) == set(expected_names)


@pytest.mark.parametrize(
    ("members", "inherited_members", "expected_names"),
    [
        (True, True, {"baseMethod", "mainMethod"}),
        (True, False, {"mainMethod"}),
        (True, ["baseMethod"], {"baseMethod", "mainMethod"}),
        (True, [], {"mainMethod"}),
        (False, True, {"baseMethod"}),
        (False, False, set()),
        (False, ["baseMethod"], {"baseMethod"}),
        (False, [], set()),
        ([], True, {"baseMethod"}),
        ([], False, set()),
        ([], ["baseMethod"], {"baseMethod"}),
        ([], [], set()),
        (None, True, {"baseMethod", "mainMethod"}),
        (None, False, {"mainMethod"}),
        (None, ["baseMethod"], {"baseMethod", "mainMethod"}),
        (None, [], {"mainMethod"}),
        (["baseMethod"], True, {"baseMethod"}),
        (["baseMethod"], False, set()),
        (["baseMethod"], ["baseMethod"], {"baseMethod"}),
        (["baseMethod"], [], set()),
        (["mainMethod"], True, {"mainMethod"}),
        (["mainMethod"], False, {"mainMethod"}),
        (["mainMethod"], ["baseMethod"], {"baseMethod", "mainMethod"}),
        (["mainMethod"], [], {"mainMethod"}),
    ],
)
def test_filter_inherited_members(
    members: bool | list[str] | None,
    inherited_members: bool | list[str],
    expected_names: set[str],
) -> None:
    """Test inherited members filtering for MATLAB classes.

    Parameters:
        members: Members option (parametrized).
        inherited_members: Inherited members option (parametrized).
        expected_names: The expected result as a set of member names.
    """
    # Create mock MATLAB objects representing inheritance
    objects = {
        "baseMethod": _FakeMatlabObject("baseMethod", inherited=True),
        "mainMethod": _FakeMatlabObject("mainMethod", inherited=False),
    }

    filtered = rendering.do_filter_objects(
        objects, members_list=members, inherited_members=inherited_members
    )
    names = {obj.name for obj in filtered}
    assert names == expected_names


@pytest.mark.parametrize(
    ("order", "members_list", "expected_names"),
    [
        ("alphabetical", None, ["funcA", "funcB", "funcC"]),
        ("source", None, ["funcC", "funcB", "funcA"]),
        ("alphabetical", ["funcC", "funcB"], ["funcC", "funcB"]),
        ("source", ["funcA", "funcC"], ["funcA", "funcC"]),
        ("alphabetical", [], ["funcA", "funcB", "funcC"]),
        ("source", [], ["funcC", "funcB", "funcA"]),
        ("alphabetical", True, ["funcA", "funcB", "funcC"]),
        ("source", False, ["funcC", "funcB", "funcA"]),
    ],
)
def test_ordering_members(
    order: rendering.Order, members_list: list[str] | None | bool, expected_names: list[str]
) -> None:
    """Assert MATLAB objects are correctly ordered.

    Parameters:
        order: The order to use (alphabetical or source).
        members_list: The user specified members list.
        expected_names: The expected ordered list of object names.
    """

    class MatlabObj:
        def __init__(self, name: str, lineno: int | None = None) -> None:
            self.name = name
            self.lineno = lineno

    members = [MatlabObj("funcA", 10), MatlabObj("funcB", 9), MatlabObj("funcC", 8)]
    ordered = rendering.do_order_members(members, order, members_list)  # type: ignore[arg-type]
    assert [obj.name for obj in ordered] == expected_names


def test_stash_crossref_filter() -> None:
    """Test that cross-reference stashing works correctly."""
    stash_filter = rendering.do_stash_crossref

    # Test stashing a cross-reference
    crossref = "SomeClass.method"
    key = stash_filter(crossref, length=10)

    assert isinstance(key, str)
    assert len(key) == 10
    assert key in stash_filter.stash
    assert stash_filter.stash[key] == crossref
    stash_filter.stash.clear()  # Clear stash after test


def test_format_property() -> None:
    """Test MATLAB property formatting."""
    # This would need actual Property objects for full testing
    # Basic test to ensure the function exists and can be called
    assert hasattr(rendering, "do_format_property")


def test_as_properties_section() -> None:
    """Test conversion of MATLAB properties to docstring section."""
    # This would need actual Property objects for full testing
    assert hasattr(rendering, "do_as_properties_section")


def test_as_functions_section() -> None:
    """Test conversion of MATLAB functions to docstring section."""
    # This would need actual Function objects for full testing
    assert hasattr(rendering, "do_as_functions_section")


def test_as_classes_section() -> None:
    """Test conversion of MATLAB classes to docstring section."""
    # This would need actual Class objects for full testing
    assert hasattr(rendering, "do_as_classes_section")


def test_as_namespaces_section() -> None:
    """Test conversion of MATLAB namespaces to docstring section."""
    # This would need actual Namespace objects for full testing
    assert hasattr(rendering, "do_as_namespaces_section")


def test_function_docstring_processing() -> None:
    """Test MATLAB function docstring processing."""
    # This would need actual Function objects with arguments/returns for full testing
    assert hasattr(rendering, "do_function_docstring")


def test_inheritance_diagram_section() -> None:
    """Test inheritance diagram generation for MATLAB classes."""
    # This would need actual Class objects with inheritance for full testing
    assert hasattr(rendering, "do_as_inheritance_diagram_section")


def test_autorefs_hook() -> None:
    """Test AutorefsHook for MATLAB objects."""
    # This would need actual MATLAB objects for full testing
    assert hasattr(rendering, "AutorefsHook")

    # Test basic hook creation
    from mkdocstrings_handlers.matlab.rendering import AutorefsHook

    assert AutorefsHook is not None
