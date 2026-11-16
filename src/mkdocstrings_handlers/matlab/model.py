"""The models the handler and the templates use, built on malt-index.

malt-index reads the MATLAB path and returns plain facts: names, spans, the text of the
comments, and types and defaults as text. The classes here wrap those facts in the shape
the templates and the rendering code expect: griffe docstrings built from the comment text,
expressions that link MATLAB builtins, and the member views (`all_members`, `functions`,
and so on). Nothing here parses MATLAB; griffe parses the docstrings when the handler asks
for their sections.
"""

from __future__ import annotations

import json
import logging
import re
from enum import Enum
from functools import cached_property, lru_cache
from importlib import resources
from pathlib import Path
from typing import TYPE_CHECKING, Any, NoReturn

import malt_index
from griffe import Docstring
from malt_index import FilePathError, NameResolutionError

if TYPE_CHECKING:
    from collections.abc import Iterator


__all__ = [
    "Argument",
    "ArgumentKind",
    "Class",
    "Expression",
    "Folder",
    "Function",
    "Kind",
    "LiveScript",
    "Namespace",
    "Object",
    "PathsCollection",
    "Property",
    "Script",
    "configure_index_logger",
]


class Kind(str, Enum):
    """The kinds of objects. The values are the ones the templates use (`obj.kind.value`)."""

    FOLDER = "folder"
    NAMESPACE = "namespace"
    CLASS = "class"
    ENUMERATION = "class"
    """An enumeration is rendered as a class, as it always was."""
    FUNCTION = "function"
    SCRIPT = "script"
    PROPERTY = "property"
    LIVE_SCRIPT = "live_script"


class ArgumentKind(str, Enum):
    """How an argument is passed."""

    positional_only = "positional-only"
    optional = "optional"
    keyword_only = "keyword-only"
    varargin = "varargin"


_KINDS: dict[str, Kind] = {
    "folder": Kind.FOLDER,
    "namespace": Kind.NAMESPACE,
    "class": Kind.CLASS,
    "enumeration": Kind.ENUMERATION,
    "function": Kind.FUNCTION,
    "script": Kind.SCRIPT,
    "live_script": Kind.LIVE_SCRIPT,
    "property": Kind.PROPERTY,
}

_LOG_LEVELS: dict[str, int] = {
    "TRACE": 5,
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "SUCCESS": 25,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


def configure_index_logger(level: str = "WARNING") -> None:
    """Set the level of the records malt-index writes (the `malt_index` logger).

    Parameters:
        level: The level name, as the `tree_sitter_logging_level` option gives it.
    """
    logging.getLogger("malt_index").setLevel(_LOG_LEVELS[level])


_TOKEN = re.compile(r"\w+|[^\w\s]")
_STRING = re.compile(r"\"[^\"]*\"|'[^']*'")
_NAME = re.compile(r"[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*")


@lru_cache(maxsize=1)
def _builtin_docs() -> dict[str, str]:
    """The documentation URL of each builtin name, read once from the packaged table.

    The table is generated from MATLAB's reference index (`scripts/gen_builtin_docs.py`).
    """
    table = resources.files("mkdocstrings_handlers.matlab").joinpath("data", "builtin_docs.json")
    data = json.loads(table.read_text(encoding="utf-8"))
    return {name: data["base"] + page for name, page in data["pages"].items()}


class Expression:
    """A type, default, validator or base class, as written in the source.

    It renders as its text. A MATLAB builtin in it, such as a function, class or data type
    that MATLAB documents, links to its documentation (`doc`). Iterating it gives its tokens.
    """

    def __init__(self, text: str) -> None:
        """Initialize the expression.

        Parameters:
            text: The expression text.
        """
        self.text = text
        """The expression text."""

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return f"Expression({self.text!r})"

    def __iter__(self) -> Iterator[str]:
        return iter(_TOKEN.findall(self.text))

    @property
    def doc(self) -> str:
        """The documentation URL of a builtin in the expression, or an empty string.

        Quoted text is not a name: in `"text", double`, `double` is the builtin.
        """
        docs = _builtin_docs()
        for name in _NAME.findall(_STRING.sub(" ", self.text)):
            if (url := docs.get(name)) is not None:
                return url
        return ""


def _expression(text: str | None) -> Expression | None:
    return None if text is None else Expression(text)


def _docstring(
    text: str | None, lineno: int | None, endlineno: int | None, parent: Any
) -> Docstring | None:
    if text is None:
        return None
    return Docstring(text, lineno=lineno, endlineno=endlineno, parent=parent)


class Object:
    """A MATLAB object on the search path: a folder, namespace, class, function, and so on.

    The subclasses add what their kind has. An inherited member is an `Object` with
    `inherited` set. Its path is its base's, as the templates have always shown it.
    """

    def __init__(
        self,
        inner: Any,
        collection: PathsCollection,
        *,
        parent: Object | None = None,
        path: str | None = None,
        inherited: bool = False,
    ) -> None:
        """Initialize the object.

        Parameters:
            inner: The malt-index object.
            collection: The search path the object belongs to.
            parent: The object this one is a member of, if any.
            path: The dotted path of a member; malt-index's path when not given.
            inherited: Whether this object is an inherited member.
        """
        self._inner = inner
        self._collection = collection
        self.kind: Kind = _KINDS[inner.kind]
        """The kind of the object."""
        self.parent = parent
        """The object this one is a member of, or `None`."""
        self._canonical_path: str = inner.path if path is None else path
        self.inherited = inherited
        """Whether this object is a member inherited from a base class."""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name!r}, {self.lineno!r}, {self.endlineno!r})"

    @property
    def name(self) -> str:
        """The name of the object."""
        return self._inner.name

    @property
    def canonical_path(self) -> str:
        """The dotted path of the object, as its name is written in the source (no `+`)."""
        return self._canonical_path

    @property
    def path(self) -> str:
        """The path the templates use as the object's id (a folder's is `/name`)."""
        return self.canonical_path

    @property
    def module(self) -> NoReturn:
        """Stands in for griffe's module lookup, which MATLAB objects do not have.

        Raises:
            ValueError: Always. griffe catches it when it resolves annotations.
        """
        raise ValueError("Object does not have a module")

    @property
    def lineno(self) -> int | None:
        """The first line of the declaration (1-based)."""
        return self._inner.lineno

    @property
    def endlineno(self) -> int | None:
        """The last line of the declaration (1-based, inclusive)."""
        return self._inner.endlineno

    @property
    def attributes(self) -> set[str]:
        """The attributes, such as `Hidden` or `Access=private`."""
        return set(self._inner.attributes)

    @property
    def is_alias(self) -> bool:
        """Whether this object is an inherited member, which stands for its base's member."""
        return self._inner.is_alias

    @property
    def target(self) -> Object:
        """The object this one stands for: itself, as malt-index's copies are."""
        return self

    @property
    def is_private(self) -> bool:
        """Whether the object is private."""
        return self._inner.is_private

    @property
    def is_hidden(self) -> bool:
        """Whether the object is hidden."""
        return self._inner.is_hidden

    @property
    def is_namespace(self) -> bool:
        """Whether this object is a namespace (a package)."""
        return self.kind is Kind.NAMESPACE

    @property
    def is_folder(self) -> bool:
        """Whether this object is a folder."""
        return self.kind is Kind.FOLDER

    @property
    def is_class(self) -> bool:
        """Whether this object is a class (an enumeration is one too)."""
        return self.kind is Kind.CLASS

    @property
    def is_function(self) -> bool:
        """Whether this object is a function or a method."""
        return self.kind is Kind.FUNCTION

    @property
    def is_script(self) -> bool:
        """Whether this object is a script."""
        return self.kind is Kind.SCRIPT

    @property
    def is_property(self) -> bool:
        """Whether this object is a property."""
        return self.kind is Kind.PROPERTY

    @property
    def is_internal(self) -> bool:
        """Whether the object is in a `+internal` package."""
        filepath = self._inner.filepath
        return filepath is not None and "+internal" in Path(filepath).parts

    @property
    def filepath(self) -> Path:
        """The file that declares the object, or its parent's.

        Raises:
            FilePathError: When neither the object nor its parent has a file.
        """
        if (filepath := self._inner.filepath) is not None:
            return Path(filepath)
        if self.parent is not None:
            return self.parent.filepath
        raise FilePathError(self.name)

    @property
    def relative_filepath(self) -> Path | None:
        """The file that declares the object, relative to the working directory when it is below it."""
        if (filepath := self._inner.filepath) is None:
            return None
        path = Path(filepath)
        try:
            return path.relative_to(Path.cwd())
        except ValueError:
            return path

    @cached_property
    def docstring(self) -> Docstring | None:
        """The comment next to the declaration, as a griffe docstring (not parsed)."""
        return _docstring(
            self._inner.docstring,
            self._inner.docstring_lineno,
            self._inner.docstring_endlineno,
            parent=self,
        )

    @property
    def has_docstring(self) -> bool:
        """Whether the object has a docstring, empty or not."""
        return self.docstring is not None

    @property
    def lines(self) -> list[str]:
        """The source lines of the declaration."""
        return self._inner.lines

    @property
    def source(self) -> str:
        """The source of the declaration, dedented."""
        return self._inner.source

    @property
    def lines_collection(self) -> malt_index.LinesCollection:
        """The source lines of the files on the search path."""
        return self._inner.lines_collection

    @property
    def paths_collection(self) -> PathsCollection:
        """The search path the object belongs to."""
        return self._collection

    def _member_path(self, name: str) -> str:
        # The members of a folder are named by their own name: the folder is not in their path.
        if self.is_folder:
            return name
        return f"{self.canonical_path}.{name}"

    @cached_property
    def members(self) -> dict[str, Object]:
        """The declared members: properties, methods, local functions, files and packages."""
        return {
            name: _wrap(
                member,
                self._collection,
                parent=self,
                path=self._member_path(member.name),
            )
            for name, member in self._inner.members.items()
        }

    @cached_property
    def inherited_members(self) -> dict[str, Object]:
        """The members inherited from base classes (none unless this is a class)."""
        return {}

    @property
    def all_members(self) -> dict[str, Object]:
        """All members, declared and inherited."""
        if self.is_class:
            return {**self.inherited_members, **self.members}
        return self.members

    def _of_kind(self, kind: Kind, members: dict[str, Object]) -> dict[str, Object]:
        return {name: member for name, member in members.items() if member.kind is kind}

    @property
    def folders(self) -> dict[str, Object]:
        """The folder members."""
        return self._of_kind(Kind.FOLDER, self.all_members)

    @property
    def namespaces(self) -> dict[str, Object]:
        """The namespace members."""
        return self._of_kind(Kind.NAMESPACE, self.all_members)

    @property
    def scripts(self) -> dict[str, Object]:
        """The script members (declared ones only)."""
        return self._of_kind(Kind.SCRIPT, self.members)

    @property
    def classes(self) -> dict[str, Object]:
        """The class members, enumerations included."""
        return self._of_kind(Kind.CLASS, self.all_members)

    @property
    def functions(self) -> dict[str, Object]:
        """The function members."""
        return self._of_kind(Kind.FUNCTION, self.all_members)

    @property
    def properties(self) -> dict[str, Object]:
        """The property members."""
        return self._of_kind(Kind.PROPERTY, self.all_members)


class Folder(Object):
    """A folder on the search path, and its files, packages, class folders and subfolders."""


class Namespace(Object):
    """A package (`+pkg`)."""

    @property
    def path(self) -> str:
        """The path with its `+`, as the templates use it for the id."""
        return "+" + self.canonical_path


class Script(Object):
    """A script: a file of commands, with local functions."""


class LiveScript(Object):
    """A live script (`.mlx`, or plain-text live code)."""

    @property
    def sections(self) -> list[Any]:
        """The sections, each with `kind` (`text` or `code`), `content`, and its lines."""
        return self._inner.sections


class Class(Object):
    """A class: a classdef, or a class folder (`@cls`)."""

    @property
    def bases(self) -> list[str]:
        """The base classes, as written."""
        return list(self._inner.bases)

    @cached_property
    def inherited_members(self) -> dict[str, Object]:
        """The members inherited from base classes: the nearest base's member wins.

        Raises:
            CyclicAliasError: When the superclasses lead back to this class.
        """
        return {
            name: _wrap(
                member,
                self._collection,
                parent=self,
                inherited=True,
            )
            for name, member in self._inner.inherited_members.items()
        }

    @cached_property
    def constructor(self) -> Function | None:
        """The constructor: the method named after the class, declared or inherited."""
        for members in (self.members, self.inherited_members):
            member = members.get(self.name)
            if isinstance(member, Function):
                return member
        return None

    @property
    def arguments(self) -> list[Argument]:
        """The arguments of the constructor."""
        constructor = self.constructor
        return [] if constructor is None else constructor.arguments


class Function(Object):
    """A function, a method, or a local or nested function."""

    @cached_property
    def arguments(self) -> list[Argument]:
        """The input arguments, then the `arguments` block's entries."""
        return [Argument(argument) for argument in self._inner.arguments]

    @cached_property
    def returns(self) -> list[Argument]:
        """The output arguments."""
        return [Argument(argument) for argument in self._inner.returns]

    @property
    def is_getter(self) -> bool:
        """Whether this is a property getter (`get.X`)."""
        return self._inner.is_getter

    @property
    def is_setter(self) -> bool:
        """Whether this is a property setter (`set.X`)."""
        return self._inner.is_setter


class Property(Object):
    """A property of a class."""

    @property
    def type(self) -> Expression | None:
        """The type, as written."""
        return _expression(self._inner.type)

    @property
    def dimensions(self) -> list[str] | None:
        """The dimensions, as written."""
        return self._inner.dimensions

    @property
    def validators(self) -> Expression | None:
        """The validators, as written."""
        return _expression(self._inner.validators)

    @property
    def default(self) -> Expression | None:
        """The default value, as written."""
        return _expression(self._inner.default)


class Argument:
    """An input or output argument of a function."""

    def __init__(self, inner: Any) -> None:
        """Initialize the argument.

        Parameters:
            inner: The malt-index argument.
        """
        self._inner = inner
        self.name: str = inner.name
        """The argument name (`~` for an ignored one)."""
        self.kind: ArgumentKind = ArgumentKind(inner.kind)
        """How the argument is passed."""

    def __repr__(self) -> str:
        return f"Argument({self.name!r}, {self.kind.value!r})"

    @property
    def type(self) -> Expression | None:
        """The type, as written."""
        return _expression(self._inner.type)

    @property
    def dimensions(self) -> list[str] | None:
        """The dimensions, as written."""
        return self._inner.dimensions

    @property
    def validators(self) -> Expression | None:
        """The validators, as written."""
        return _expression(self._inner.validators)

    @property
    def default(self) -> Expression | None:
        """The default value, as written."""
        return _expression(self._inner.default)

    @property
    def required(self) -> bool:
        """Whether the argument is a positional input with no default."""
        return self._inner.required

    @cached_property
    def docstring(self) -> Docstring | None:
        """The comment next to the argument, as a griffe docstring (not parsed)."""
        return _docstring(self._inner.docstring, None, None, parent=self)

    @property
    def has_docstring(self) -> bool:
        """Whether the argument has a comment, empty or not."""
        return self.docstring is not None


_WRAPPERS: dict[str, type[Object]] = {
    "folder": Folder,
    "namespace": Namespace,
    "class": Class,
    "enumeration": Object,
    "function": Function,
    "script": Script,
    "live_script": LiveScript,
    "property": Property,
}


def _wrap(
    inner: Any,
    collection: PathsCollection,
    *,
    parent: Object | None = None,
    path: str | None = None,
    inherited: bool = False,
) -> Object:
    cls = _WRAPPERS[inner.kind]
    return cls(inner, collection, parent=parent, path=path, inherited=inherited)


class PathsCollection:
    """The MATLAB search path, with its objects as the models of this module."""

    def __init__(
        self,
        paths: list[Path],
        *,
        recursive: bool = False,
        working_directory: Path | None = None,
        parser_config: malt_index.ParserConfig | None = None,
    ) -> None:
        """Read the folders on the search path.

        Parameters:
            paths: The folders, relative to the working directory or absolute.
            recursive: Whether plain subfolders join the path, as MATLAB's `genpath` does.
            working_directory: The directory relative paths resolve against.
            parser_config: Which comment block documents a declaration.

        Raises:
            FilePathError: When a folder cannot be read.
        """
        self._index = malt_index.PathsCollection(
            [Path(path) for path in paths],
            recursive=recursive,
            working_directory=working_directory,
            parser_config=parser_config,
        )

    def get_member(self, identifier: str) -> Object | None:
        """The object of an identifier, or `None`.

        A plain identifier is a name on the path (`pkg.fn`, `Cls`). An identifier with a
        slash is a folder on the path, or a file in one, relative to the working directory
        or absolute.

        Parameters:
            identifier: The name or path.

        Returns:
            The object, or `None` when nothing on the path matches.
        """
        try:
            inner = self._index.get(identifier)
        except NameResolutionError:
            return None
        return None if inner is None else _wrap(inner, self)

    def __contains__(self, identifier: object) -> bool:
        return isinstance(identifier, str) and self.get_member(identifier) is not None

    @property
    def lines_collection(self) -> malt_index.LinesCollection:
        """The source lines of the files on the path."""
        return self._index.lines_collection
