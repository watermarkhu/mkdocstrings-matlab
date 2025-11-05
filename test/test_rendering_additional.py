"""Additional tests for the rendering module to improve coverage."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
from unittest.mock import MagicMock

from griffe import Docstring

from mkdocstrings_handlers.matlab import rendering

if TYPE_CHECKING:
    pass


@dataclass
class _FakeProperty:
    """Fake property for testing."""

    name: str
    type: str | None = None
    default: str | None = None
    docstring: Docstring | None = None
    is_private: bool = False


@dataclass
class _FakeFunction:
    """Fake function for testing."""

    name: str
    docstring: Docstring | None = None
    parent: _FakeClass | None = None
    is_private: bool = False


@dataclass
class _FakeClass:
    """Fake class for testing."""

    name: str
    docstring: Docstring | None = None
    is_private: bool = False
    is_class: bool = True


@dataclass
class _FakeNamespace:
    """Fake namespace for testing."""

    name: str
    docstring: Docstring | None = None
    is_internal: bool = False


def test_sort_key_alphabetical() -> None:
    """Test alphabetical sorting key function."""

    @dataclass
    class Item:
        name: str | None

    item1 = Item(name="zebra")
    item2 = Item(name="apple")
    item3 = Item(name=None)

    assert rendering._sort_key_alphabetical(item1) == "zebra"
    assert rendering._sort_key_alphabetical(item2) == "apple"
    # Items without name should go to end
    import sys

    assert rendering._sort_key_alphabetical(item3) == chr(sys.maxunicode)


def test_sort_key_source() -> None:
    """Test source order sorting key function."""

    @dataclass
    class Item:
        lineno: int | None

    item1 = Item(lineno=10)
    item2 = Item(lineno=5)
    item3 = Item(lineno=None)

    assert rendering._sort_key_source(item1) == 10
    assert rendering._sort_key_source(item2) == 5
    # Items without lineno should go to end
    assert rendering._sort_key_source(item3) == float("inf")


def test_order_members_with_manual_list() -> None:
    """Test ordering members with a manual list."""

    @dataclass
    class Member:
        name: str
        lineno: int = 0

    members = [
        Member(name="third", lineno=3),
        Member(name="first", lineno=1),
        Member(name="second", lineno=2),
    ]

    # Manual ordering
    result = rendering.do_order_members(members, "alphabetical", ["second", "third", "first"])
    assert [m.name for m in result] == ["second", "third", "first"]

    # When name is not in list, it should be excluded
    result = rendering.do_order_members(members, "alphabetical", ["second"])
    assert [m.name for m in result] == ["second"]


def test_order_members_with_list_order() -> None:
    """Test ordering members with a list of order methods."""

    @dataclass
    class Member:
        name: str
        lineno: int = 0

    members = [Member(name="b", lineno=2), Member(name="a", lineno=1)]

    # List of order methods - should use first valid one
    result = rendering.do_order_members(members, ["alphabetical", "source"], None)
    assert [m.name for m in result] == ["a", "b"]

    # Source order
    result = rendering.do_order_members(members, ["source"], None)
    assert [m.lineno for m in result] == [1, 2]


def test_keep_object() -> None:
    """Test _keep_object filtering function."""
    import re

    # Test with include filter only
    filters = [(re.compile(r"^test_"), False)]
    assert rendering._keep_object("test_function", filters) is True
    assert rendering._keep_object("other_function", filters) is False

    # Test with exclude filter only
    filters = [(re.compile(r"^_"), True)]
    assert rendering._keep_object("_private", filters) is False
    assert rendering._keep_object("public", filters) is True

    # Test with mixed filters (include and exclude)
    # When we have both include and exclude, no match means keep
    filters = [(re.compile(r"^test_"), False), (re.compile(r"_helper$"), True)]
    assert rendering._keep_object("test_something", filters) is True
    assert rendering._keep_object("test_helper", filters) is False
    # With mixed rules, "other" doesn't match any rule, so it's kept
    assert rendering._keep_object("other", filters) is True


def test_parents() -> None:
    """Test _parents function."""

    @dataclass
    class Obj:
        path: str
        parent: Obj | None = None

    # Create a hierarchy
    root = Obj(path="root", parent=None)
    middle = Obj(path="root.middle", parent=root)
    leaf = Obj(path="root.middle.leaf", parent=middle)

    parents = rendering._parents(leaf)  # type: ignore[arg-type]
    assert "root.middle" in parents
    assert "root" in parents


def test_do_parse_docstring() -> None:
    """Test do_parse_docstring function."""
    # Test with None docstring
    result = rendering.do_parse_docstring(None, "google", None)
    assert result == []

    # Test with actual docstring would require creating proper Docstring objects
    # For now, we verify the function exists and handles None


def test_do_as_properties_section() -> None:
    """Test conversion of properties to docstring section."""
    # Create mock context
    context = MagicMock()
    context.parent = {"config": MagicMock(show_signature_types=True)}

    # Create fake properties
    prop1 = _FakeProperty(name="prop1", type="double", default="0")
    prop1_docstring = Docstring("Property 1 description", lineno=1, endlineno=1)
    prop1.docstring = prop1_docstring

    prop2 = _FakeProperty(name="_private_prop", is_private=True)

    properties = [prop1, prop2]

    # Test with check_public=True (should exclude private)
    section = rendering.do_as_properties_section(context, properties, check_public=True)
    assert len(section.value) == 1
    assert section.value[0].name == "prop1"

    # Test with check_public=False (should include all)
    section = rendering.do_as_properties_section(context, properties, check_public=False)
    assert len(section.value) == 2


def test_do_as_functions_section() -> None:
    """Test conversion of functions to docstring section."""
    context = MagicMock()
    context.parent = {"config": MagicMock(merge_constructor_into_class=False)}

    # Create fake functions
    func1 = _FakeFunction(name="method1")
    func1_docstring = Docstring("Method 1 description", lineno=1, endlineno=1)
    func1.docstring = func1_docstring

    func2 = _FakeFunction(name="_private_method", is_private=True)

    functions = [func1, func2]

    # Test with check_public=True
    section = rendering.do_as_functions_section(context, functions, check_public=True)
    assert len(section.value) == 1
    assert section.value[0].name == "method1"

    # Test with check_public=False
    section = rendering.do_as_functions_section(context, functions, check_public=False)
    assert len(section.value) == 2


def test_do_as_functions_section_with_constructor() -> None:
    """Test that constructors are filtered when merge_constructor_into_class is True."""
    context = MagicMock()
    context.parent = {"config": MagicMock(merge_constructor_into_class=True)}

    # Create a class and its constructor
    parent_class = _FakeClass(name="MyClass")
    constructor = _FakeFunction(name="MyClass", parent=parent_class)
    constructor_docstring = Docstring("Constructor", lineno=1, endlineno=1)
    constructor.docstring = constructor_docstring

    regular_method = _FakeFunction(name="method1", parent=parent_class)
    method_docstring = Docstring("Regular method", lineno=1, endlineno=1)
    regular_method.docstring = method_docstring

    functions = [constructor, regular_method]

    section = rendering.do_as_functions_section(context, functions, check_public=True)
    # Constructor should be excluded when merge_constructor_into_class is True
    assert len(section.value) == 1
    assert section.value[0].name == "method1"


def test_do_as_classes_section() -> None:
    """Test conversion of classes to docstring section."""
    context = MagicMock()

    # Create fake classes
    cls1 = _FakeClass(name="Class1")
    cls1_docstring = Docstring("Class 1 description", lineno=1, endlineno=1)
    cls1.docstring = cls1_docstring

    cls2 = _FakeClass(name="_PrivateClass", is_private=True)

    classes = [cls1, cls2]

    # Test with check_public=True
    section = rendering.do_as_classes_section(context, classes, check_public=True)
    assert len(section.value) == 1
    assert section.value[0].name == "Class1"

    # Test with check_public=False
    section = rendering.do_as_classes_section(context, classes, check_public=False)
    assert len(section.value) == 2


def test_do_as_namespaces_section() -> None:
    """Test conversion of namespaces to docstring section."""
    context = MagicMock()

    # Create fake namespaces
    ns1 = _FakeNamespace(name="namespace1")
    ns1_docstring = Docstring("Namespace 1 description", lineno=1, endlineno=1)
    ns1.docstring = ns1_docstring

    ns2 = _FakeNamespace(name="internal_namespace", is_internal=True)

    namespaces = [ns1, ns2]

    # Test with check_public=True
    section = rendering.do_as_namespaces_section(context, namespaces, check_public=True)
    assert len(section.value) == 1
    assert section.value[0].name == "namespace1"

    # Test with check_public=False
    section = rendering.do_as_namespaces_section(context, namespaces, check_public=False)
    assert len(section.value) == 2


def test_do_as_inheritance_diagram_section_no_bases() -> None:
    """Test inheritance diagram with no base classes."""

    @dataclass
    class SimpleClass:
        name: str
        bases: list = None

        def __post_init__(self):
            if self.bases is None:
                self.bases = []

    cls = SimpleClass(name="MyClass")
    result = rendering.do_as_inheritance_diagram_section(cls)  # type: ignore[arg-type]
    assert result is None


def test_do_as_inheritance_diagram_section_no_bases_attribute() -> None:
    """Test inheritance diagram with object that has no bases attribute."""

    @dataclass
    class SimpleClass:
        name: str

    cls = SimpleClass(name="MyClass")
    result = rendering.do_as_inheritance_diagram_section(cls)  # type: ignore[arg-type]
    assert result is None


def test_do_get_template() -> None:
    """Test template name generation."""
    # Test with string input
    result = rendering.do_get_template("class")  # type: ignore[arg-type]
    assert result == "class.html.jinja"

    result = rendering.do_get_template("function")  # type: ignore[arg-type]
    assert result == "function.html.jinja"


def test_autorefs_hook_expand_identifier() -> None:
    """Test AutorefsHook expand_identifier method."""

    @dataclass
    class Obj:
        kind: MagicMock
        path: str
        docstring: MagicMock | None = None
        filepath: str = "test.m"
        parent: None = None

    obj = Obj(kind=MagicMock(value="function"), path="test.function")
    hook = rendering.AutorefsHook(obj, {})  # type: ignore[arg-type]

    # expand_identifier should return the identifier unchanged
    assert hook.expand_identifier("some.identifier") == "some.identifier"


def test_autorefs_hook_get_context() -> None:
    """Test AutorefsHook get_context method."""

    @dataclass
    class Obj:
        kind: MagicMock
        path: str
        docstring: MagicMock | None = None
        filepath: str = "test.m"
        parent: None = None

    obj = Obj(kind=MagicMock(value="function"), path="test.function", filepath="test.m")
    obj.docstring = MagicMock()
    obj.docstring.parent.filepath = "test.m"
    obj.docstring.lineno = 10

    hook = rendering.AutorefsHook(obj, {})  # type: ignore[arg-type]
    context = hook.get_context()

    assert context.domain == "mat"
    assert context.role == "func"
    assert context.origin == "test.function"
    assert context.filepath == "test.m"
    assert context.lineno == 10


def test_autorefs_hook_get_context_method() -> None:
    """Test AutorefsHook context for class methods."""

    @dataclass
    class Parent:
        is_class: bool = True

    @dataclass
    class Obj:
        kind: MagicMock
        path: str
        parent: Parent
        docstring: MagicMock | None = None
        filepath: str = "test.m"

    parent = Parent()
    obj = Obj(kind=MagicMock(value="function"), path="test.Class.method", parent=parent)
    obj.docstring = MagicMock()
    obj.docstring.parent.filepath = "test.m"
    obj.docstring.lineno = 20

    hook = rendering.AutorefsHook(obj, {})  # type: ignore[arg-type]
    context = hook.get_context()

    assert context.role == "meth"  # Should be method, not func


def test_autorefs_hook_get_context_no_docstring() -> None:
    """Test AutorefsHook context when object has no docstring."""

    @dataclass
    class Obj:
        kind: MagicMock
        path: str
        docstring: None = None
        filepath: str = "test.m"
        parent: None = None

    obj = Obj(kind=MagicMock(value="class"), path="test.MyClass")
    hook = rendering.AutorefsHook(obj, {})  # type: ignore[arg-type]
    context = hook.get_context()

    assert context.domain == "mat"
    assert context.role == "class"
    assert context.filepath == "test.m"
    assert context.lineno == 0  # Should default to 0


def test_stash_crossref_unique_keys() -> None:
    """Test that stash_crossref generates unique keys."""
    stash = rendering.do_stash_crossref

    # Clear any existing stash
    stash.stash.clear()

    # Generate multiple keys
    key1 = stash("ref1", length=10)
    key2 = stash("ref2", length=10)
    key3 = stash("ref3", length=10)

    # All keys should be unique
    assert key1 != key2
    assert key2 != key3
    assert key1 != key3

    # All should be in stash
    assert key1 in stash.stash
    assert key2 in stash.stash
    assert key3 in stash.stash

    # Clean up
    stash.stash.clear()
