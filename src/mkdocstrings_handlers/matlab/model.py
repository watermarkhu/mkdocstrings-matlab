"""The documentation model: `malt_index` objects dressed for the templates.

`malt_index` returns plain facts read from the source (strings, spans, members). The
templates and the rendering helpers expect objects that behave like Griffe's: a parsed
`Docstring` attached to the object, aliases for inherited members, a `canonical_path`, and
expressions that can be walked token by token. This module wraps the index objects in
classes with those attributes. Nothing here reads files or parses MATLAB.
"""

from __future__ import annotations

import json
import re
from collections.abc import Iterator
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

import malt_index
from griffe import Docstring

if TYPE_CHECKING:
    from malt_index import PathsCollection as IndexPaths

__all__ = [
    "Alias",
    "Argument",
    "ArgumentKind",
    "Arguments",
    "Class",
    "CyclicAliasError",
    "Expr",
    "Folder",
    "Function",
    "Kind",
    "Namespace",
    "Object",
    "PathsCollection",
    "Property",
    "Script",
    "wrap",
]

CyclicAliasError = malt_index.CyclicAliasError
FilePathError = malt_index.FilePathError
ParserConfig = malt_index.ParserConfig


class Kind(str, Enum):
    """The kinds of documented objects (the values the templates are named after)."""

    FOLDER = "folder"
    NAMESPACE = "namespace"
    CLASS = "class"
    FUNCTION = "function"
    SCRIPT = "script"
    LIVE_SCRIPT = "live_script"
    PROPERTY = "property"


class ArgumentKind(str, Enum):
    """The kinds of function arguments."""

    positional_only = "positional-only"
    optional = "optional"
    keyword_only = "keyword-only"
    varargin = "varargin"


MATHWORKS_DOC_URL = "https://www.mathworks.com/help/matlab"


@lru_cache(maxsize=1)
def _builtins() -> dict[str, str]:
    """The documentation page (relative to the MATLAB help) of each builtin name."""
    path = Path(__file__).parent / "matlab_builtins.json"
    return json.loads(path.read_text(encoding="utf-8", errors="replace"))


_TOKEN = re.compile(r"[A-Za-z_][A-Za-z0-9_]*|\s+|.", re.DOTALL)


class Expr:
    """A type, default, validator or base expression.

    `str(expr)` is the source text. Iterating gives the tokens, so a template can link
    each name separately. `doc` is the documentation URL of the first builtin in it.
    """

    def __init__(self, text: str) -> None:
        self.text = text

    def __iter__(self) -> Iterator[str]:
        yield from _TOKEN.findall(self.text)

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return f"Expr({self.text!r})"

    def __eq__(self, other: object) -> bool:
        return self.text == str(other) if isinstance(other, (Expr, str)) else NotImplemented

    def __hash__(self) -> int:
        return hash(self.text)

    @property
    def doc(self) -> str:
        """The documentation URL of the first builtin name in the expression, or ``""``."""
        builtins = _builtins()
        for token in self:
            if token in builtins:
                return f"{MATHWORKS_DOC_URL}/{builtins[token]}"
        return ""


def _expr(value: Any) -> Expr | None:
    if value is None or value == "":
        return None
    return Expr(str(value))


def _docstring(raw: Any, parent: Any) -> Docstring | None:
    value = getattr(raw, "docstring", None)
    if value is None:
        return None
    return Docstring(
        value,
        lineno=getattr(raw, "docstring_lineno", None),
        endlineno=getattr(raw, "docstring_endlineno", None),
        parent=parent,
    )


class PathsCollection:
    """The MATLAB search path, with the lookups the handler and the templates use."""

    def __init__(
        self,
        paths: list[Path] | list[str],
        *,
        recursive: bool = False,
        working_directory: str | Path | None = None,
        parser_config: Any = None,
    ) -> None:
        self._index: IndexPaths = malt_index.PathsCollection(
            [str(p) for p in paths],
            recursive=recursive,
            working_directory=str(working_directory) if working_directory else None,
            parser_config=parser_config,
        )
        self.lines_collection = self._index.lines_collection
        self._wrapped: dict[int, Object] = {}

    @property
    def members(self) -> dict[str, Object]:
        """The top-level names on the path."""
        return {name: wrap(raw, self) for name, raw in self._index.members.items()}

    def get_member(self, identifier: str) -> Object | None:
        """The object with this dotted name, or `None`."""
        raw = self._index.get(identifier)
        return None if raw is None else wrap(raw, self)

    def get_folder(self, path: str | Path) -> Object | None:
        """The folder on the path with this path (relative paths are to the working directory)."""
        try:
            raw = self._index[str(path)]
        except KeyError:
            return None
        return wrap(raw, self)

    def __contains__(self, identifier: object) -> bool:
        return isinstance(identifier, str) and self._index.get(identifier) is not None

    def __getitem__(self, identifier: str) -> Object:
        member = self.get_member(identifier)
        if member is None:
            raise KeyError(identifier)
        return member


class Argument:
    """An input argument, or a returned value."""

    def __init__(self, raw: Any, parent: Object) -> None:
        self._raw = raw
        self.parent = parent
        self.name: str = raw.name
        self.kind = ArgumentKind(raw.kind) if getattr(raw, "kind", None) else None
        self.type = _expr(raw.type)
        self.dimensions = list(raw.dimensions) if raw.dimensions else None
        self.validators = _expr(raw.validators)
        self.default = _expr(raw.default)
        self.docstring = _docstring(raw, self)

    @property
    def required(self) -> bool:
        """Whether the argument is a positional input with no default."""
        return bool(self._raw.required)

    @property
    def has_docstring(self) -> bool:
        """Whether the argument has a docstring (empty or not)."""
        return bool(self.docstring)

    def __repr__(self) -> str:
        return f"Argument({self.name!r}, {self.kind!r})"


class Arguments:
    """An ordered collection of arguments, addressable by name or position."""

    def __init__(self, *arguments: Argument) -> None:
        self._arguments = list(arguments)

    def __getitem__(self, key: int | str) -> Argument:
        if isinstance(key, str):
            for argument in self._arguments:
                if argument.name == key:
                    return argument
            raise KeyError(key)
        return self._arguments[key]

    def __iter__(self) -> Iterator[Argument]:
        return iter(self._arguments)

    def __len__(self) -> int:
        return len(self._arguments)

    def __contains__(self, name: object) -> bool:
        return any(argument.name == name for argument in self._arguments)

    def __repr__(self) -> str:
        return f"Arguments({self._arguments!r})"


class _MembersByKind:
    """The member views of an object or an alias, by kind."""

    @property
    def all_members(self) -> dict[str, Any]:
        raise NotImplementedError

    def _of_kind(self, kind: Kind) -> dict[str, Any]:
        return {name: m for name, m in self.all_members.items() if m.kind is kind}

    @property
    def folders(self) -> dict[str, Any]:
        return self._of_kind(Kind.FOLDER)

    @property
    def namespaces(self) -> dict[str, Any]:
        return self._of_kind(Kind.NAMESPACE)

    @property
    def scripts(self) -> dict[str, Any]:
        return self._of_kind(Kind.SCRIPT)

    @property
    def classes(self) -> dict[str, Any]:
        return self._of_kind(Kind.CLASS)

    @property
    def functions(self) -> dict[str, Any]:
        return self._of_kind(Kind.FUNCTION)

    @property
    def properties(self) -> dict[str, Any]:
        return self._of_kind(Kind.PROPERTY)

    @property
    def enumerations(self) -> dict[str, Any]:
        return {}


class Object(_MembersByKind):
    """A documented object: a folder, namespace, class, function, script or property."""

    is_collection = False
    inherited = False

    def __init__(
        self, raw: Any, paths_collection: PathsCollection, *, parent: Object | None = None
    ) -> None:
        self._raw = raw
        self._paths_collection = paths_collection
        self._parent = parent
        self.docstring: Docstring | None = _docstring(raw, self)
        self.extra: dict[str, dict[str, Any]] = {}

    # identity ---------------------------------------------------------------

    @property
    def name(self) -> str:
        return self._raw.name

    @property
    def path(self) -> str:
        return self.canonical_path

    @property
    def canonical_path(self) -> str:
        # Inside a folder the index prefixes the folder (`/fixture/classFolder`); the
        # documented name is the dotted name alone.
        return self._raw.path.rsplit("/", 1)[-1]

    @property
    def kind(self) -> Kind:
        raw = self._raw.kind
        # Enumeration members are rendered as properties.
        return Kind.PROPERTY if raw == "enumeration" else Kind(raw)

    @property
    def lineno(self) -> int | None:
        return self._raw.lineno

    @property
    def endlineno(self) -> int | None:
        return self._raw.endlineno

    @property
    def filepath(self) -> Path:
        return Path(self._raw.filepath)

    @property
    def relative_filepath(self) -> Path:
        try:
            return self.filepath.relative_to(Path.cwd())
        except ValueError:
            return self.filepath

    @property
    def relative_package_filepath(self) -> Path:
        return self.relative_filepath

    @property
    def lines(self) -> list[str]:
        return list(self._raw.lines)

    @property
    def source(self) -> str:
        return self._raw.source

    @property
    def paths_collection(self) -> PathsCollection:
        return self._paths_collection

    @property
    def lines_collection(self) -> Any:
        return self._paths_collection.lines_collection

    # state ------------------------------------------------------------------

    @property
    def is_alias(self) -> bool:
        return False

    @property
    def parent(self) -> Object | None:
        if self._parent is not None:
            return self._parent
        raw_parent = self._raw.parent
        return None if raw_parent is None else wrap(raw_parent, self._paths_collection)

    @property
    def attributes(self) -> set[str]:
        return set(self._raw.attributes)

    @property
    def is_internal(self) -> bool:
        """Whether the file is in a `+internal` package."""
        return "+internal" in self.filepath.parts

    @property
    def is_private(self) -> bool:
        """Whether the file is in a `private` folder, or the access is not public."""
        return "private" in self.filepath.parts or bool(self._raw.is_private)

    @property
    def is_hidden(self) -> bool:
        """Whether the object is internal or declared `Hidden`."""
        return self.is_internal or bool(self._raw.is_hidden)

    @property
    def has_docstring(self) -> bool:
        return bool(self.docstring)

    def has_attributes(self, *attributes: str) -> bool:
        own = self.attributes
        return all(attribute in own for attribute in attributes)

    def is_kind(self, kind: str | Kind | set[str | Kind]) -> bool:
        kinds = kind if isinstance(kind, set) else {kind}
        return self.kind in {Kind(str(k.value if isinstance(k, Kind) else k)) for k in kinds}

    is_folder = property(lambda self: self._raw.is_folder)
    is_namespace = property(lambda self: self._raw.is_namespace)
    is_class = property(lambda self: self._raw.is_class)
    is_function = property(lambda self: self._raw.is_function)
    is_script = property(lambda self: self._raw.is_script)
    is_property = property(lambda self: self._raw.is_property or self._raw.is_enumeration)

    # members ----------------------------------------------------------------

    @property
    def members(self) -> dict[str, Object]:
        return {
            name: wrap(raw, self._paths_collection, parent=self)
            for name, raw in self._raw.members.items()
        }

    @property
    def inherited_members(self) -> dict[str, Alias]:
        return {}

    @property
    def all_members(self) -> dict[str, Object | Alias]:
        return {**self.inherited_members, **self.members}

    def __bool__(self) -> bool:
        return True

    def __len__(self) -> int:
        return len(self._raw.members)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.name!r}, {self.lineno!r}, {self.endlineno!r})"


class Folder(Object):
    """A plain folder, or a class folder."""

    @property
    def canonical_path(self) -> str:
        return self._raw.path


class Namespace(Object):
    """A package (`+pkg`)."""

    @property
    def path(self) -> str:
        return "+" + self.canonical_path

    @property
    def is_subnamespace(self) -> bool:
        return "." in self.canonical_path


class Script(Object):
    """A script."""


class Property(Object):
    """A class property or an enumeration member."""

    @property
    def type(self) -> Expr | None:
        return _expr(getattr(self._raw, "type", None))

    @property
    def dimensions(self) -> list[str] | None:
        dims = getattr(self._raw, "dimensions", None)
        return list(dims) if dims else None

    @property
    def validators(self) -> Expr | None:
        return _expr(getattr(self._raw, "validators", None))

    @property
    def default(self) -> Expr | None:
        value = getattr(self._raw, "default", None)
        if value is None:
            value = getattr(self._raw, "value", None)
        return _expr(value)

    @property
    def getter(self) -> Function | None:
        raw = getattr(self._raw, "getter", None)
        return (
            None
            if raw is None
            else cast("Function", wrap(raw, self._paths_collection, parent=self))
        )

    @property
    def setter(self) -> Function | None:
        raw = getattr(self._raw, "setter", None)
        return (
            None
            if raw is None
            else cast("Function", wrap(raw, self._paths_collection, parent=self))
        )


class Function(Object):
    """A function or a method."""

    @property
    def arguments(self) -> Arguments:
        return Arguments(*(Argument(a, self) for a in self._raw.arguments))

    @property
    def returns(self) -> Arguments:
        return Arguments(*(Argument(a, self) for a in self._raw.returns))

    @property
    def is_method(self) -> bool:
        parent = self.parent
        return parent is not None and parent.kind is Kind.CLASS

    @property
    def is_constructor_method(self) -> bool:
        parent = self.parent
        return self.is_method and parent is not None and self.name == parent.name

    @property
    def is_getter(self) -> bool:
        return bool(self._raw.is_getter)

    @property
    def is_setter(self) -> bool:
        return bool(self._raw.is_setter)


class Class(Object):
    """A class (a file, or a class folder)."""

    @property
    def bases(self) -> list[Expr]:
        return [Expr(str(base)) for base in self._raw.bases]

    @property
    def resolved_bases(self) -> list[Object]:
        resolved = []
        for base in self.bases:
            found = self._paths_collection.get_member(str(base))
            if found is not None:
                resolved.append(found)
        return resolved

    @property
    def mro(self) -> list[Class]:
        return [cast("Class", wrap(raw, self._paths_collection)) for raw in self._raw.mro[1:]]

    @property
    def constructor(self) -> Function | None:
        member = self.members.get(self.name)
        return member if isinstance(member, Function) else None

    @property
    def arguments(self) -> Arguments:
        constructor = self.constructor
        return constructor.arguments if constructor is not None else Arguments()

    @property
    def inherited_members(self) -> dict[str, Alias]:
        return {
            name: Alias(name, wrap(raw.target, self._paths_collection), self, inherited=True)
            for name, raw in self._raw.inherited_members.items()
        }


class Alias(_MembersByKind):
    """A member inherited from a base class: the same object under a new parent."""

    is_alias = True
    inherited = True
    is_collection = False

    def __init__(
        self, name: str, target: Object, parent: Object | Alias, *, inherited: bool = False
    ) -> None:
        self.name = name
        self._target = target
        self.parent = parent
        # An inherited member keeps the path of the member it was inherited from.
        self._inherited = inherited

    @property
    def target(self) -> Object:
        return self._target

    @property
    def path(self) -> str:
        if self._inherited:
            return self._target.path
        return f"{self.parent.path}.{self.name}"

    @property
    def canonical_path(self) -> str:
        return self._target.path

    @property
    def members(self) -> dict[str, Object | Alias]:
        return {
            name: Alias(name, member, self) if not isinstance(member, Alias) else member
            for name, member in self._target.members.items()
        }

    @property
    def inherited_members(self) -> dict[str, Alias]:
        return {}

    @property
    def all_members(self) -> dict[str, Object | Alias]:
        return {**self.inherited_members, **self.members}

    def __getattr__(self, item: str) -> Any:
        return getattr(self._target, item)

    def __bool__(self) -> bool:
        return True

    def __len__(self) -> int:
        return len(self._target)

    def __repr__(self) -> str:
        return f"Alias({self.name!r}, {self._target!r})"


_CLASSES: dict[str, type[Object]] = {
    "folder": Folder,
    "namespace": Namespace,
    "class": Class,
    "function": Function,
    "script": Script,
    "live_script": Script,
    "property": Property,
    "enumeration": Property,
}


def wrap(raw: Any, paths_collection: PathsCollection, *, parent: Object | None = None) -> Object:
    """Wrap an index object in the model class of its kind."""
    return _CLASSES.get(str(raw.kind), Object)(raw, paths_collection, parent=parent)
