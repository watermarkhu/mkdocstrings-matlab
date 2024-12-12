from typing import Any, Optional, TYPE_CHECKING
from griffe import (
    Function as GriffeFunction,
    Class as GriffeClass,
    Module,
    Attribute,
    Docstring,
    Object,
    Parameters,
    Parameter,
)

from mkdocstrings_handlers.matlab.enums import AccessEnum
from mkdocstrings_handlers.matlab.mixins import PathMixin

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
    "Parameters",
    "Parameter",
    "Property",
    "Script",
]


class _Root(Object):
    def __init__(self) -> None:
        super().__init__("ROOT", parent=None)

    def __repr__(self) -> str:
        return "MATLABROOT"


ROOT = _Root()


class MatlabObject(Object):
    def __init__(
        self,
        *args,
        path_collection: Optional["PathCollection"] = None,
        **kwargs,
    ) -> None:
        self.path_collection = path_collection
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
        return f"{self.parent.path}.{self.name}"


class Script(PathMixin, MatlabObject):
    pass


class Class(PathMixin, GriffeClass, MatlabObject):
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
            model = self.path_collection.resolve(base)
            if model is None:
                # Perhaps issue a warning here?
                continue

            for name, member in model.members.items():
                if name not in self.members:
                    inherited_members[name] = member
        return inherited_members

    @property
    def is_private(self) -> bool:
        return self.hidden

    @property
    def canonical_path(self) -> str:
        if isinstance(self.parent, Classfolder):
            return self.parent.canonical_path
        else:
            return super().canonical_path

    def get_lineno_method(self, method_name: str) -> tuple[int, int]:
        return self._method_lineno.get(method_name, (self.lineno, self.endlineno))


class Classfolder(Class):
    def __repr__(self) -> str:
        return f"Classfolder({self.path!r})"


class Property(Attribute, MatlabObject):
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
            self._access == AccessEnum.PUBLIC | self._access == AccessEnum.IMMUTABLE
        )
        get_public = self._access == AccessEnum.PUBLIC
        return (set_public or get_public) and not self._hidden


class Function(PathMixin, GriffeFunction, MatlabObject):
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
        public = self.access == AccessEnum.PUBLIC | self.access == AccessEnum.IMMUTABLE
        return public and not self.hidden


# class Namespace(PathMixin, Module, MatlabObject):
#     def __init__(self, *args: Any, **kwargs: Any) -> None:
#         super().__init__(*args, **kwargs)
#         self._access: AccessEnum = AccessEnum.PUBLIC

#     def __repr__(self) -> str:
#         return f"Namespace({self.path!r})"
