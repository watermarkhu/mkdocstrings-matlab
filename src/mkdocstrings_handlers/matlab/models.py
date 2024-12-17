from typing import Any, TYPE_CHECKING, Callable
from functools import cached_property
from pathlib import Path
from griffe import (
    Attribute,
    Function as GriffeFunction,
    Class as GriffeClass,
    Docstring as GriffeDocstring,
    DocstringSection,
    DocstringSectionText,
    Module,
    Object,
    Parameters as GriffeParameters,
    Parameter as GriffeParameter,
)

from mkdocstrings_handlers.matlab.enums import AccessEnum, ParameterKind

if TYPE_CHECKING:
    from mkdocstrings_handlers.matlab.collect import PathCollection

__all__ = [
    "Attribute",
    "Class",
    "Classfolder",
    "Function",
    "MatlabObject",
    "Module",
    "Docstring",
    "DocstringSectionText",
    "Namespace",
    "PathMixin",
    "Parameters",
    "Parameter",
    "Property",
    "Script",
]


class Docstring(GriffeDocstring):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._extra_sections: list[DocstringSection] = []

    @property
    def parsed(self) -> list[DocstringSection]:
        """The docstring sections, parsed into structured data."""
        return self._parsed + self._extra_sections

    @cached_property
    def _parsed(self) -> list[DocstringSection]:
        return self.parse()


class _ParentGrabber:
    def __init__(self, grabber: "Callable[[], MatlabObject]") -> None:
        self._grabber = grabber

    def __call__(self) -> "MatlabObject":
        return self._grabber()


class MatlabObject(Object):
    def __init__(
        self,
        *args,
        docstring: Docstring | None = None,
        path_collection: "PathCollection | None" = None,
        parent: "Class | Classfolder | Namespace | _Root | None" = None,
        **kwargs,
    ) -> None:
        self._docstring: Docstring | None = docstring
        self.path_collection: "PathCollection | None" = path_collection
        self._parent: "Class | Classfolder | Namespace | _Root | _ParentGrabber | None" = parent
        lines_collection = (
            path_collection.lines_collection if path_collection is not None else None
        )
        super().__init__(*args, lines_collection=lines_collection, **kwargs)

    @property
    def canonical_path(self) -> str:
        """The full dotted path of this object.

        The canonical path is the path where the object was defined (not imported).
        """
        if isinstance(self.parent, _Root):
            return self.name

        if isinstance(self.parent, MatlabObject):
            parent = self.parent
        else:
            parent = getattr(self.parent, "model", self.parent)

        if isinstance(parent, Classfolder) and self.name == parent.name:
            if isinstance(parent.parent, _Root):
                return self.name
            else:
                return f"{parent.parent.canonical_path}.{self.name}"
        else:
            return f"{parent.canonical_path}.{self.name}" if parent else self.name

    @property
    def docstring(self) -> Docstring | None:
        return self._docstring

    @docstring.setter
    def docstring(self, value: Docstring | None):
        if value is not None:
            self._docstring = value

    @property
    def parent(self) -> "MatlabObject":
        if isinstance(self._parent, MatlabObject):
            return self._parent
        elif isinstance(self._parent, _ParentGrabber):
            return self._parent()
        else:
            return ROOT

    @parent.setter
    def parent(self, value):
        if value is not None:
            self._parent = value


class _Root(MatlabObject):
    def __init__(self) -> None:
        super().__init__("ROOT", parent=None)

    def __repr__(self) -> str:
        return "MATLABROOT"


ROOT = _Root()


class PathMixin(Object):
    def __init__(self, *args: Any, filepath: Path | None = None, **kwargs: Any) -> None:
        self._filepath: Path | None = filepath
        self._parent = ROOT
        super().__init__(*args, **kwargs)

    @property
    def filepath(self) -> Path | None:
        return self._filepath

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"


class Parameter(MatlabObject, GriffeParameter):
    def __init__(
        self, *args: Any, kind: ParameterKind | None = None, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.kind: ParameterKind | None = kind


class Parameters(MatlabObject, GriffeParameters):
    def __init__(self, *parameters: Parameter) -> None:
        self._params: list[Parameter] = list(parameters)


class Script(PathMixin, MatlabObject):
    pass


class Class(PathMixin, MatlabObject, GriffeClass):
    def __init__(
        self,
        *args: Any,
        Abstract: bool = False,
        Hidden: bool = False,
        Sealed: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.abstract: bool = Abstract
        self.hidden: bool = Hidden
        self.sealed: bool = Sealed

    @property
    def parameters(self) -> Parameters:
        """The parameters of this class' `__init__` method, if any.

        This property fetches inherited members,
        and therefore is part of the consumer API:
        do not use when producing Griffe trees!
        """
        try:
            return self.all_members[self.name].parameters  # type: ignore[union-attr]
        except KeyError:
            return Parameters()

    @property
    def inherited_members(self) -> dict[str, MatlabObject]:
        """Members that are inherited from base classes.

        This method is part of the consumer API:
        do not use when producing Griffe trees!
        """

        inherited_members = {}
        for base in reversed(self.bases):
            model = (
                self.path_collection.resolve(str(base))
                if self.path_collection
                else None
            )
            if model is None:
                # TODO Perhaps issue a warning here?
                continue

            for name, member in model.members.items():
                if name not in self.members:
                    inherited_members[name] = member
        return inherited_members

    @property
    def labels(self) -> set[str]:
        labels = set()
        if self.abstract:
            labels.add("abstract")
        if self.hidden:
            labels.add("hidden")
        if self.sealed:
            labels.add("sealed")
        return labels

    @labels.setter
    def labels(self, *args):
        pass

    @property
    def is_private(self) -> bool:
        return self.hidden

    @property
    def canonical_path(self) -> str:
        if isinstance(self.parent, Classfolder):
            return self.parent.canonical_path
        else:
            return super().canonical_path


class Classfolder(Class):
    pass


class Property(MatlabObject, Attribute):
    def __init__(
        self,
        *args: Any,
        AbortSet: bool = False,
        Abstract: bool = False,
        Constant: bool = False,
        Dependent: bool = False,
        GetObservable: bool = False,
        Hidden: bool = False,
        NonCopyable: bool = False,
        SetObservable: bool = False,
        Transient: bool = False,
        WeakHandle: bool = False,
        GetAccess: AccessEnum = AccessEnum.PUBLIC,
        SetAccess: AccessEnum = AccessEnum.PUBLIC,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.abort_set: bool = AbortSet
        self.abstract: bool = Abstract
        self.constant: bool = Constant
        self.dependent: bool = Dependent
        self.get_observable: bool = GetObservable
        self.hidden: bool = Hidden
        self.non_copyable: bool = NonCopyable
        self.set_observable: bool = SetObservable
        self.transient: bool = Transient
        self.weak_handle: bool = WeakHandle
        self.get_access: AccessEnum = GetAccess
        self.set_access: AccessEnum = SetAccess

        self.getter: Function | None = None
        """The getter linked to this property."""

    @property
    def is_private(self) -> bool:
        set_public = (
            self.set_access == AccessEnum.PUBLIC
            or self.set_access == AccessEnum.IMMUTABLE
        )
        get_public = self.get_access == AccessEnum.PUBLIC
        return (set_public or get_public) and not self.hidden

    @property
    def labels(self) -> set[str]:
        labels = set()
        for attr in [
            "abort_set",
            "abstract",
            "constant",
            "dependent",
            "get_observable",
            "hidden",
            "non_copyable",
            "set_observable",
            "transient",
            "weak_handle",
        ]:
            if getattr(self, attr):
                labels.add(attr)
        for attr in ["get_access", "set_access"]:
            if getattr(self, attr) != AccessEnum.PUBLIC:
                labels.add(f"{attr}={str(getattr(self, attr)).lower()}")
        return labels

    @labels.setter
    def labels(self, *args):
        pass


class Function(PathMixin, MatlabObject, GriffeFunction):
    def __init__(
        self,
        *args: Any,
        returns: Parameters | None = None,
        Abstract: bool = False,
        Access: AccessEnum = AccessEnum.PUBLIC,
        Hidden: bool = False,
        Sealed: bool = False,
        Static: bool = False,
        setter: bool = False,
        getter: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.returns: Parameters | None = returns
        self.access: AccessEnum = Access
        self.static: bool = Static
        self.abstract: bool = Abstract
        self.sealed: bool = Sealed
        self.hidden: bool = Hidden
        self._is_setter: bool = setter
        self._is_getter: bool = getter

    @property
    def is_private(self) -> bool:
        public = self.access == AccessEnum.PUBLIC or self.access == AccessEnum.IMMUTABLE
        return public and not self.hidden

    @property
    def labels(self) -> set[str]:
        labels = set()
        for attr in ["abstract", "hidden", "sealed", "static"]:
            if getattr(self, attr):
                labels.add(attr)
        if self.access != AccessEnum.PUBLIC:
            labels.add(f"access={str(self.access).lower()}")
        return labels

    @labels.setter
    def labels(self, *args):
        pass


class Namespace(PathMixin, MatlabObject, Module):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._access: AccessEnum = AccessEnum.PUBLIC

    def __repr__(self) -> str:
        return f"Namespace({self.path!r})"
