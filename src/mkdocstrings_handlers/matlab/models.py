"""Classes to represent MATLAB objects and their properties."""

from typing import Any, TYPE_CHECKING, Callable
from functools import cached_property
from pathlib import Path
from griffe import (
    Alias,
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
        _suffixes (list[DocstringSection]): A list to store additional docstring sections.

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
        self._prefixes: list[DocstringSection] = []
        self._suffixes: list[DocstringSection] = []

    @property
    def parsed(self) -> list[DocstringSection]:
        """
        The docstring sections, parsed into structured data.

        Returns:
            list[DocstringSection]: The combined list of parsed and extra docstring sections.
        """
        return self._prefixes + self._parsed + self._suffixes

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

    def __init__(self, grabber: "Callable[[], MatlabMixin | None]") -> None:
        """
        Initializes the _ParentGrabber with a grabber function.

        Args:
            grabber (Callable[[], MatlabObject]): A function that returns a MatlabObject.
        """
        self._grabber = grabber

    @property
    def parent(self) -> "MatlabMixin | None":
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
    def namespaces(self) -> dict[str, "Namespace"]:
        return {}

    @property
    def is_namespace(self) -> bool:
        return False

    @property
    def is_folder(self) -> bool:
        return False

    @property
    def canonical_path(self) -> str:
        """
        The full dotted path of this object.

        Returns:
            str: The canonical path of the object.
        """
        if self.parent is None:
            return self.name

        if isinstance(self.parent, MatlabObject):
            parent = self.parent
        else:
            parent = getattr(self.parent, "model", self.parent)

        if isinstance(parent, Classfolder) and self.name == parent.name:
            if parent.parent is None:
                return self.name
            else:
                return f"{parent.parent.canonical_path}.{self.name}"
        else:
            return f"{parent.canonical_path}.{self.name}" if parent else self.name


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
        parent: "Class | Classfolder | Namespace | None" = None,
        docstring: Docstring | None = None,
        **kwargs: Any,
    ):
        self._parent: "Class | Classfolder | Namespace | _ParentGrabber | None" = parent
        self._docstring: Docstring | None = docstring
        super().__init__(*args, **kwargs)

    @property
    def parent(self) -> Object | None:
        if isinstance(self._parent, MatlabMixin):
            return self._parent
        elif isinstance(self._parent, _ParentGrabber):
            return self._parent.parent
        else:
            return None

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
        self.Abstract: bool = Abstract
        self.Hidden: bool = Hidden
        self.Sealed: bool = Sealed
        self._inherited_members: dict[str, MatlabObject] | None = None

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
        if self._inherited_members is not None:
            return self._inherited_members

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
                    inherited_members[name] = Alias(
                        name, target=member, parent=self, inherited=True
                    )

        self._inherited_members = inherited_members
        return inherited_members

    @property
    def labels(self) -> set[str]:
        labels = set()
        if self.Abstract:
            labels.add("Abstract")
        if self.Hidden:
            labels.add("Hidden")
        if self.Sealed:
            labels.add("Sealed")
        return labels

    @labels.setter
    def labels(self, *args):
        pass

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
        Access: AccessEnum = AccessEnum.public,
        GetAccess: AccessEnum = AccessEnum.public,
        SetAccess: AccessEnum = AccessEnum.public,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.AbortSet: bool = AbortSet
        self.Abstract: bool = Abstract
        self.Constant: bool = Constant
        self.Dependent: bool = Dependent
        self.GetObservable: bool = GetObservable
        self.Hidden: bool = Hidden
        self.NonCopyable: bool = NonCopyable
        self.SetObservable: bool = SetObservable
        self.Transient: bool = Transient
        self.WeakHandle: bool = WeakHandle
        self.Access = Access
        self.GetAccess: AccessEnum = GetAccess
        self.SetAccess: AccessEnum = SetAccess
        self.getter: Function | None = None

        self.extra["mkdocstrings"] = {"template": "property.html.jinja"}

    @property
    def Private(self) -> bool:
        private = self.Access != AccessEnum.public
        set_private = (
            self.SetAccess != AccessEnum.public
            and self.SetAccess != AccessEnum.immutable
        )
        get_private = self.GetAccess != AccessEnum.public
        return private or set_private or get_private

    @property
    def is_private(self) -> bool:
        return self.Private or self.Hidden

    @property
    def labels(self) -> set[str]:
        labels = set()
        for attr in [
            "AbortSet",
            "Abstract",
            "Constant",
            "Dependent",
            "GetObservable",
            "Hidden",
            "NonCopyable",
            "SetObservable",
            "Transient",
            "WeakHandle",
        ]:
            if getattr(self, attr):
                labels.add(attr)
        for attr in ["Access", "GetAccess", "SetAccess"]:
            if getattr(self, attr) != AccessEnum.public:
                labels.add(f"{attr}={getattr(self, attr).value}")
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
        self.Access: AccessEnum = Access
        self.Static: bool = Static
        self.Abstract: bool = Abstract
        self.Sealed: bool = Sealed
        self.Hidden: bool = Hidden
        self._is_setter: bool = setter
        self._is_getter: bool = getter

    @property
    def Private(self) -> bool:
        return self.Access != AccessEnum.public and self.Access != AccessEnum.immutable

    @property
    def is_private(self) -> bool:
        return self.Private or self.Hidden

    @property
    def labels(self) -> set[str]:
        labels = set()
        for attr in ["Abstract", "Hidden", "Sealed", "Static"]:
            if getattr(self, attr):
                labels.add(attr)
        if self.Access != AccessEnum.public:
            labels.add(f"Access={self.Access.value}")
        return labels

    @labels.setter
    def labels(self, *args):
        pass


class Folder(MatlabMixin, PathMixin, Module, MatlabObject):
    """
    A class representing a Folder in a MATLAB project.

    Inherits from:
        - MatlabMixin: A mixin class providing MATLAB-specific functionality.
        - PathMixin: A mixin class providing path-related functionality.
        - Module: A class representing a module.
        - MatlabObject: A base class for MATLAB objects.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.extra["mkdocstrings"] = {"template": "folder.html.jinja"}

    def __repr__(self) -> str:
        return f"Folder({self.filepath!r})"

    @property
    def namespaces(self) -> dict[str, "Namespace"]:
        return {
            name: member
            for name, member in self.members.items()
            if isinstance(member, Namespace)
        }

    @property
    def is_folder(self) -> bool:
        return True


class Namespace(MatlabMixin, PathMixin, Module, MatlabObject):
    """
    A class representing a namespace in a MATLAB project.

    Inherits from:
        - MatlabMixin: A mixin class providing MATLAB-specific functionality.
        - PathMixin: A mixin class providing path-related functionality.
        - Module: A class representing a module.
        - MatlabObject: A base class for MATLAB objects.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._access: AccessEnum = AccessEnum.public
        self.extra["mkdocstrings"] = {"template": "namespace.html.jinja"}

    def __repr__(self) -> str:
        return f"Namespace({self.path!r})"

    @property
    def is_internal(self) -> bool:
        return (
            any(part == "+internal" for part in self.filepath.parts)
            if self.filepath
            else False
        )

    @property
    def is_namespace(self) -> bool:
        return True
