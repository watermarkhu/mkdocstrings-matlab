"""Tests for the `rendering` module."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

import pytest
from maxx.exceptions import CyclicAliasError as MaxxCyclicAliasError

from mkdocstrings_handlers.matlab import rendering


@dataclass
class _FakeMatlabObject:
    name: str
    inherited: bool = False
    parent: None = None
    is_alias: bool = False
    is_private: bool = False
    is_hidden: bool = False
    is_folder: bool = False
    has_docstring: bool = True
    path: str = ""

    def __post_init__(self):
        """Default `path` to `name`."""
        if not self.path:
            self.path = self.name


@dataclass
class _FakeContainer:
    """Minimal stand-in for a maxx container/alias with controllable `members`."""

    name: str
    has_docstring: bool = False
    is_alias: bool = False
    target_obj: Any = None
    children: list[Any] = field(default_factory=list)
    raises: Exception | None = None

    @property
    def target(self) -> Any:
        """Return the aliased object, or raise the configured error."""
        if self.raises is not None:
            raise self.raises
        return self.target_obj

    @property
    def members(self) -> dict[str, Any]:
        """Wrap each child in a new alias on every access, like `maxx.objects.Alias.members`."""
        return {
            child.name: _FakeContainer(child.name, is_alias=True, target_obj=child)
            for child in self.children
        }


def test_has_docstrings_terminates_on_alias_cycle() -> None:
    """Repeated alias wrappers around the same target must not recurse forever."""
    parent = _FakeContainer("parent")
    parent.children.append(parent)

    assert rendering._has_docstrings(parent) is False  # ty: ignore[invalid-argument-type]


def test_has_docstrings_finds_documented_descendant_through_aliases() -> None:
    """A documented descendant is found even when every level is reached via a fresh alias."""
    leaf = _FakeContainer("leaf", has_docstring=True)
    mid = _FakeContainer("mid", children=[leaf])
    root = _FakeContainer("root", children=[mid])

    assert rendering._has_docstrings(root) is True  # ty: ignore[invalid-argument-type]


def test_has_docstrings_treats_maxx_cyclic_alias_error_as_undocumented() -> None:
    """A maxx `CyclicAliasError` while resolving an alias must read as "no docstring"."""
    broken = _FakeContainer("broken", is_alias=True, raises=MaxxCyclicAliasError(["a", "b", "a"]))
    root = _FakeContainer("root", children=[])
    root.children.append(broken)

    assert rendering._has_docstrings(broken) is False  # ty: ignore[invalid-argument-type]
    assert rendering._has_docstrings(root) is False  # ty: ignore[invalid-argument-type]


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

    filtered = rendering.do_filter_objects(objects, **filter_params)  # ty: ignore[invalid-assignment]
    filtered_names = {obj.name for obj in filtered}
    assert set(filtered_names) == set(expected_names)


def test_filter_objects_keeps_folders_without_docstring() -> None:
    """Folders without their own docstring must survive the `show_if_no_docstring` filter.

    Folders are structural containers: dropping an undocumented folder would also hide its
    children, which is unrelated to the `show_if_no_docstring` setting. Only `show_subfolders`
    (applied in the template) should decide whether a folder's contents are shown.
    """
    objects = {
        "undocumented_function": _FakeMatlabObject("undocumented_function", has_docstring=False),
        "undocumented_folder": _FakeMatlabObject(
            "undocumented_folder", has_docstring=False, is_folder=True
        ),
    }

    filtered_names = {
        obj.name
        for obj in rendering.do_filter_objects(objects, keep_no_docstrings=False)  # ty: ignore[invalid-assignment]
    }

    assert filtered_names == {"undocumented_folder"}


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
    ordered = rendering.do_order_members(members, order, members_list)  # ty: ignore[invalid-assignment]
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
