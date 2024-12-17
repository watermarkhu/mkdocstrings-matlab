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
    "MatlabMixin",
    "Module",
    "Docstring",
    "DocstringSectionText",
    "Namespace",
    "Parameters",
    "Parameter",
    "Property",
    "Script",
]


class Docstring(GriffeDocstring):
    """
    A class to represent a docstring with additional sections.

    This class extends the GriffeDocstring class to include extra sections
    that can be added to the parsed docstring.

    Attributes:
        _extra_sections (list[DocstringSection]): A list to store additional docstring sections.

    Methods:
        parsed: Returns the parsed docstring sections combined with extra sections.
        _parsed: Parses the docstring into structured data.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initializes the Docstring object.

        Args:
            *args (Any): Variable length argument list.
            **kwargs (Any): Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self._extra_sections: list[DocstringSection] = []

    @property
    def parsed(self) -> list[DocstringSection]:
        """
        The docstring sections, parsed into structured data.

        Returns:
            list[DocstringSection]: The combined list of parsed and extra docstring sections.
        """
        return self._parsed + self._extra_sections

    @cached_property
    def _parsed(self) -> list[DocstringSection]:
        """
        Parses the docstring into structured data.

        Returns:
            list[DocstringSection]: The parsed docstring sections.
        """
        return self.parse()


class _ParentGrabber:
    """
    A callable class that wraps a function to grab a parent MatlabObject.

    Attributes:
        _grabber (Callable[[], MatlabObject]): A callable that returns a MatlabObject.

    Methods:
        __call__(): Calls the grabber function and returns a MatlabObject.
    """

    def __init__(self, grabber: "Callable[[], Object]") -> None:
        """
        Initializes the _ParentGrabber with a grabber function.

        Args:
            grabber (Callable[[], MatlabObject]): A function that returns a MatlabObject.
        """
        self._grabber = grabber

    @property
    def parent(self) -> "Object":
        """
        Calls the grabber function and returns a MatlabObject.

        Returns:
            MatlabObject: The MatlabObject returned by the grabber function.
        """
        return self._grabber()


class MatlabObject(Object):
    """
    Represents a Matlab object with associated docstring, path collection, and parent object.

    Attributes:
        path_collection (PathCollection | None): The collection of paths related to the Matlab object.
    """

    def __init__(
        self,
        *args,
        path_collection: "PathCollection | None" = None,
        **kwargs,
    ) -> None:
        """
        Initialize the object with the given parameters.

        Args:
            *args: Variable length argument list.
            path_collection (PathCollection | None): The collection of paths related to the object.
            **kwargs: Arbitrary keyword arguments.
        """

        self.path_collection: "PathCollection | None" = path_collection
        lines_collection = (
            path_collection.lines_collection if path_collection is not None else None
        )
        super().__init__(*args, lines_collection=lines_collection, **kwargs)

    @property
    def canonical_path(self) -> str:
        """
        The full dotted path of this object.

        Returns:
            str: The canonical path of the object.
        """
        if isinstance(self.parent, _Root):
            return self.name

        if isinstance(self.parent, MatlabObject):
            parent = self.parent
        else:
            parent = getattr(self.parent, "model", self.parent)

        if isinstance(parent, Classfolder) and self.name == parent.name:
            if isinstance(parent.parent, _Root) or parent.parent is None:
                return self.name
            else:
                return f"{parent.parent.canonical_path}.{self.name}"
        else:
            return f"{parent.canonical_path}.{self.name}" if parent else self.name


class _Root(MatlabObject):
    """
    A class representing the root object in a MATLAB structure.
    All the objects that have the root object as parent are at the top level,
    and can be called directly.
    """

    def __init__(self) -> None:
        super().__init__("ROOT", parent=None)

    def __repr__(self) -> str:
        return "MATLABROOT"


ROOT = _Root()


class PathMixin(Object):
    """
    A mixin class that provides a filepath attribute and related functionality.

    Attributes:
        filepath (Path | None): The file path associated with the object. It can be None if no file path is provided.
    """

    def __init__(self, *args: Any, filepath: Path | None = None, **kwargs: Any) -> None:
        self._filepath: Path | None = filepath

        super().__init__(*args, **kwargs)

    @property
    def filepath(self) -> Path | None:
        return self._filepath

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"


class MatlabMixin(Object):
    def __init__(
        self,
        *args: Any,
        parent: "Class | Classfolder | Namespace | _Root | None" = None,
        docstring: Docstring | None = None,
        **kwargs: Any,
    ):
        self._parent: "Class | Classfolder | Namespace | _Root | _ParentGrabber | None" = parent
        self._docstring: Docstring | None = docstring
        super().__init__(*args, **kwargs)

    @property
    def parent(self) -> Object:
        if isinstance(self._parent, MatlabMixin):
            return self._parent
        elif isinstance(self._parent, _ParentGrabber):
            return self._parent.parent
        else:
            return ROOT

    @parent.setter
    def parent(self, value):
        if value is not None:
            self._parent = value

    @property
    def docstring(self) -> Docstring | None:
        return self._docstring

    @docstring.setter
    def docstring(self, value: Docstring | None):
        if value is not None:
            self._docstring = value


class Parameter(MatlabMixin, GriffeParameter, MatlabObject):
    """
    Represents a parameter in a MATLAB object.

    Inherits from:
        MatlabObject: Base class for MATLAB objects.
        GriffeParameter: Base class for parameters.

    Attributes:
        kind (ParameterKind | None): The kind of the parameter, which can be of type ParameterKind or None.
    """

    def __init__(
        self, *args: Any, kind: ParameterKind | None = None, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.kind: ParameterKind | None = kind


class Parameters(MatlabMixin, GriffeParameters, MatlabObject):
    """
    A class to represent a collection of parameters.

    Inherits from:
        MatlabObject: Base class for MATLAB objects.
        GriffeParameters: Base class for handling parameters.
    """

    def __init__(self, *parameters: Parameter, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._params: list[Parameter] = list(parameters)


class Script(MatlabMixin, PathMixin, MatlabObject):
    """
    A class representing a MATLAB script.

    This class inherits from `PathMixin` and `MatlabObject` to provide
    functionality specific to MATLAB scripts.
    """

    pass


class Class(MatlabMixin, PathMixin, GriffeClass, MatlabObject):
    """
    Represents a MATLAB class with additional properties and methods for handling
    MATLAB-specific features.

    This class extends `PathMixin`, `MatlabObject`, and `GriffeClass` to provide
    additional functionality for handling MATLAB class properties such as
    abstract, hidden, and sealed attributes. It also provides methods to retrieve
    parameters, inherited members, and labels.

    Attributes:
        abstract (bool): Indicates if the class is abstract.
        hidden (bool): Indicates if the class is hidden.
        sealed (bool): Indicates if the class is sealed.

    Args:
        *args (Any): Variable length argument list.
        Abstract (bool, optional): Indicates if the class is abstract
        Hidden (bool, optional): Indicates if the class is hidden
        Sealed (bool, optional): Indicates if the class is sealed
    """

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
        """
        Retrieve the parameters of the class by grabbing its constructor.

        Returns:
            Parameters: The parameters of the function if the current member is a function,
                        otherwise an empty Parameters object.
        """
        try:
            member = self.all_members.get(self.name)
            if isinstance(member, Function):
                return member.parameters
            return Parameters()
        except KeyError:
            return Parameters()

    @property
    def inherited_members(self) -> dict[str, MatlabObject]:
        """
        Retrieve a dictionary of inherited members from base classes.

        This method iterates over the base classes in reverse order, resolves their models,
        and collects members that are not already present in the current object's members.

        Returns:
            dict[str, MatlabObject]: A dictionary where the keys are member names and the values are the corresponding MatlabObject instances.
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
    """
    A class representing a MATLAB classfolder
    """

    pass


class Property(MatlabMixin, Attribute, MatlabObject):
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
        GetAccess: AccessEnum = AccessEnum.public,
        SetAccess: AccessEnum = AccessEnum.public,
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

    @property
    def is_private(self) -> bool:
        set_public = (
            self.set_access == AccessEnum.public
            or self.set_access == AccessEnum.immutable
        )
        get_public = self.get_access == AccessEnum.public
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
            if getattr(self, attr) != AccessEnum.public:
                labels.add(f"{attr}={str(getattr(self, attr))}")
        return labels

    @labels.setter
    def labels(self, *args):
        pass


class Function(MatlabMixin, PathMixin, GriffeFunction, MatlabObject):
    """
    Represents a MATLAB function with various attributes and properties.

    Attributes:
        parameters (Parameters): The parameters of the function.
        returns (Parameters | None): The return parameters of the function.
        access (AccessEnum): The access level of the function.
        static (bool): Indicates if the function is static.
        abstract (bool): Indicates if the function is abstract.
        sealed (bool): Indicates if the function is sealed.
        hidden (bool): Indicates if the function is hidden.
        _is_setter (bool): Indicates if the function is a setter.
        _is_getter (bool): Indicates if the function is a getter.

    Args:
        *args (Any): Variable length argument list.
        returns (Parameters | None, optional): The return parameters of the function. Defaults to None.
        Abstract (bool, optional): Indicates if the function is abstract. Defaults to False.
        Access (AccessEnum, optional): The access level of the function. Defaults to AccessEnum.public.
        Hidden (bool, optional): Indicates if the function is hidden. Defaults to False.
        Sealed (bool, optional): Indicates if the function is sealed. Defaults to False.
        Static (bool, optional): Indicates if the function is static. Defaults to False.
        setter (bool, optional): Indicates if the function is a setter. Defaults to False.
        getter (bool, optional): Indicates if the function is a getter. Defaults to False.
    """

    def __init__(
        self,
        *args: Any,
        returns: Parameters | None = None,
        Abstract: bool = False,
        Access: AccessEnum = AccessEnum.public,
        Hidden: bool = False,
        Sealed: bool = False,
        Static: bool = False,
        setter: bool = False,
        getter: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.parameters: Parameters = Parameters()
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
        public = self.access == AccessEnum.public or self.access == AccessEnum.immutable
        return public and not self.hidden

    @property
    def labels(self) -> set[str]:
        labels = set()
        for attr in ["abstract", "hidden", "sealed", "static"]:
            if getattr(self, attr):
                labels.add(attr)
        if self.access != AccessEnum.public:
            labels.add(f"access={str(self.access)}")
        return labels

    @labels.setter
    def labels(self, *args):
        pass


class Namespace(MatlabMixin, PathMixin, Module, MatlabObject):
    """
    A class representing a namespace in a MATLAB project.

    Inherits from:
        - PathMixin: A mixin class providing path-related functionality.
        - MatlabObject: A base class for MATLAB objects.
        - Module: A class representing a module.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._access: AccessEnum = AccessEnum.public

    def __repr__(self) -> str:
        return f"Namespace({self.path!r})"

    @property
    def is_internal(self) -> bool:
        return any(part == "+internal" for part in self.filepath.parts) if self.filepath else False
