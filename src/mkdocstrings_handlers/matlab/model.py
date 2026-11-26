"""The documentation model: `malt_index` objects dressed for the templates.

`malt_index` knows the MATLAB side: paths, members, inherited members, constructors,
builtin documentation links. What it does not know is Griffe: the templates and the
rendering helpers want a parsed `Docstring` attached to each object, an `extra` dictionary,
a `Kind` enumeration, and the member views as wrapped objects. This module wraps the index
objects with just that. Nothing here reads files or parses MATLAB.
"""

from __future__ import annotations

from collections.abc import Iterator
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

import malt_index
from griffe import Docstring
from malt_index import Expr

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
        self.type: Expr | None = raw.type_expr
        self.dimensions = list(raw.dimensions) if raw.dimensions else None
        self.validators: Expr | None = raw.validators_expr
        self.default: Expr | None = raw.default_expr
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


class Object:
    """A documented object: a folder, namespace, class, function, script or property."""

    is_collection = False

    def __init__(
        self, raw: Any, paths_collection: PathsCollection, *, parent: Object | None = None
    ) -> None:
        self._raw = raw
        self._paths_collection = paths_collection
        self._parent = parent
        self.docstring: Docstring | None = _docstring(raw, self)
        self.extra: dict[str, dict[str, Any]] = {}

    def _wrap_all(self, raws: dict[str, Any]) -> dict[str, Object]:
        return {name: wrap(raw, self._paths_collection, parent=self) for name, raw in raws.items()}

    # identity ---------------------------------------------------------------

    @property
    def name(self) -> str:
        return self._raw.name

    @property
    def path(self) -> str:
        return self._raw.canonical_path

    @property
    def canonical_path(self) -> str:
        return self._raw.canonical_path

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
        return bool(self._raw.is_alias)

    @property
    def inherited(self) -> bool:
        """Whether the object is a member inherited from a base class."""
        return bool(self._raw.is_alias)

    @property
    def target(self) -> Object:
        return wrap(self._raw.target, self._paths_collection, parent=self._parent)

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
        return bool(self._raw.is_internal)

    @property
    def is_private(self) -> bool:
        return bool(self._raw.is_private)

    @property
    def is_hidden(self) -> bool:
        return bool(self._raw.is_hidden)

    @property
    def has_docstring(self) -> bool:
        return bool(self.docstring)

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
        return self._wrap_all(self._raw.members)

    @property
    def inherited_members(self) -> dict[str, Object]:
        return self._wrap_all(getattr(self._raw, "inherited_members", {}))

    @property
    def all_members(self) -> dict[str, Object]:
        return self._wrap_all(self._raw.all_members)

    @property
    def folders(self) -> dict[str, Object]:
        return self._wrap_all(self._raw.folders)

    @property
    def namespaces(self) -> dict[str, Object]:
        return self._wrap_all(self._raw.namespaces)

    @property
    def scripts(self) -> dict[str, Object]:
        return self._wrap_all(self._raw.scripts)

    @property
    def classes(self) -> dict[str, Object]:
        return self._wrap_all(self._raw.classes)

    @property
    def functions(self) -> dict[str, Object]:
        return self._wrap_all(self._raw.functions)

    @property
    def properties(self) -> dict[str, Object]:
        # Enumeration members are rendered as properties, in member order.
        wanted = {*self._raw.properties, *self._raw.enumerations}
        return self._wrap_all({n: m for n, m in self._raw.all_members.items() if n in wanted})

    def __bool__(self) -> bool:
        return True

    def __len__(self) -> int:
        return len(self._raw.members)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.name!r}, {self.lineno!r}, {self.endlineno!r})"


# Inherited members are objects too: `is_alias` and `target` tell them apart.
Alias = Object


class Folder(Object):
    """A plain folder, or a class folder."""


class Namespace(Object):
    """A package (`+pkg`)."""

    @property
    def path(self) -> str:
        return "+" + self.canonical_path


class Script(Object):
    """A script."""


class Property(Object):
    """A class property or an enumeration member."""

    @property
    def type(self) -> Expr | None:
        return getattr(self._raw, "type_expr", None)

    @property
    def dimensions(self) -> list[str] | None:
        dims = getattr(self._raw, "dimensions", None)
        return list(dims) if dims else None

    @property
    def validators(self) -> Expr | None:
        return getattr(self._raw, "validators_expr", None)

    @property
    def default(self) -> Expr | None:
        return getattr(self._raw, "default_expr", None) or getattr(self._raw, "value_expr", None)

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
        return bool(self._raw.is_method)

    @property
    def is_constructor_method(self) -> bool:
        return bool(self._raw.is_constructor_method)

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
        return list(self._raw.bases_expr)

    @property
    def resolved_bases(self) -> list[Object]:
        return [wrap(raw, self._paths_collection) for raw in self._raw.resolved_bases]

    @property
    def constructor(self) -> Function | None:
        raw = self._raw.constructor
        return (
            None
            if raw is None
            else cast("Function", wrap(raw, self._paths_collection, parent=self))
        )

    @property
    def arguments(self) -> Arguments:
        constructor = self.constructor
        return constructor.arguments if constructor is not None else Arguments()


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
