from enum import Enum
from typing import Any
from griffe import Function as GriffeFunction, Class as GriffeClass, Module, Attribute
from pathlib import Path
from textmate_grammar.elements import ContentElement


class Access(Enum):
    PUBLIC = "public"
    PROTECTED = "protected"
    PRIVATE = "private"
    IMMUTABLE = "immutable"


class CanonicalPathMixin:
    @property
    def canonical_path(self) -> str:
        """The full dotted path of this object.

        The canonical path is the path where the object was defined (not imported).
        """
        if isinstance(self.parent, _Root):
            return self.name
        return f"{self.parent.path}.{self.name}"


class PathMixin:
    def __init__(self, *args: Any, filepath: Path | None = None, **kwargs: Any) -> None:
        self._filepath: Path | None = filepath
        super().__init__(*args, **kwargs)

    @property
    def filepath(self) -> Path | None:
        return self._filepath


class Class(CanonicalPathMixin, PathMixin, GriffeClass):
    def __init__(
        self,
        *args: Any,
        hidden: bool = False,
        sealed: bool = False,
        abstract: bool = False,
        enumeration: bool = False,
        handle: bool = False,
        textmate: ContentElement | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._hidden: bool = hidden
        self._sealed: bool = sealed
        self._abstract: bool = abstract
        self._enumeration: bool = enumeration
        self._handle: bool = handle
        self._textmate: ContentElement | None = textmate

        self._method_lineno: dict[str, tuple[int, int]] = {}
        if textmate is None:
            return
        for block in [
            block
            for block in self._textmate.children
            if block.token == "meta.methods.matlab"
        ]:
            for method in [c for c in block.children if c.token == "meta.function.matlab"]:
                declaration = next(
                    item
                    for item in method.children
                    if item.token == "meta.function.declaration.matlab"
                )
                name = next(
                    item
                    for item in declaration.children
                    if item.token == "entity.name.function.matlab"
                ).content
                charaters_ids = method.characters.keys()
                lineno = min(charaters_ids, key=lambda p: p[0])[0]
                endlino = max(charaters_ids, key=lambda p: p[0])[0] + 1
                self._method_lineno[name] = (lineno, endlino)

    @property
    def is_private(self) -> bool:
        return self._hidden

    @property
    def canonical_path(self) -> str:
        if isinstance(self.parent, Classfolder):
            return self.parent.canonical_path
        else:
            return super().canonical_path

    def get_lineno_method(self, method_name: str) -> tuple[int, int]:
        return self._method_lineno.get(method_name, (self.lineno, self.endlineno))


class Property(CanonicalPathMixin, Attribute):
    def __init__(
        self,
        *args: Any,
        get_access: Access = Access.PUBLIC,
        set_access: Access = Access.PUBLIC,
        dependent: bool = False,
        constant: bool = False,
        abstract: bool = False,
        transient: bool = False,
        hidden: bool = False,
        get_observable: bool = False,
        set_observable: bool = False,
        abort_set: bool = False,
        non_copyable: bool = False,
        has_default: bool = False,
        size: str | None = None,
        validation: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._get_access: Access = get_access
        self._set_access: Access = set_access
        self._dependent: bool = dependent
        self._constant: bool = constant
        self._abstract: bool = abstract
        self._transient: bool = transient
        self._hidden: bool = hidden
        self._get_observable: bool = get_observable
        self._set_observable: bool = set_observable
        self._abort_set: bool = abort_set
        self._non_copyable: bool = non_copyable
        self._has_default: bool = has_default
        self._size: str | None = size
        self._validation: str | None = validation

    @property
    def is_private(self) -> bool:
        set_public = self._access == Access.PUBLIC | self._access == Access.IMMUTABLE
        get_public = self._access == Access.PUBLIC
        return (set_public or get_public) and not self._hidden


class Function(CanonicalPathMixin, PathMixin, GriffeFunction):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._access: Access = Access.PUBLIC
        self._static: bool = False
        self._abstract: bool = False
        self._sealed: bool = False
        self._hidden: bool = False

    @property
    def is_private(self) -> bool:
        public = self._access == Access.PUBLIC | self._access == Access.IMMUTABLE
        return public and not self._hidden


class Namespace(CanonicalPathMixin, PathMixin, Module):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._access: Access = Access.PUBLIC

    def __repr__(self) -> str:
        return f"Namespace({self.path!r})"


class _Root(Namespace):
    def __init__(self) -> None:
        super().__init__("ROOT", parent=None)

    def __repr__(self) -> str:
        return "MATLABROOT"


ROOT = _Root()


class Classfolder(Class):
    def __repr__(self) -> str:
        return f"Classfolder({self.path!r})"
