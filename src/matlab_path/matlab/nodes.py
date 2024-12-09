from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass, field
from pathlib import Path

from .attributes import ArgumentAttributes, ClassdefAttributes, MethodAttributes, PropertyAttributes


@dataclass(repr=False, eq=False)
class Node:
    """
    Represents a node in the MATLAB path.

    Attributes:
        name (str): The name of the node.
        path (Path): The path associated with the node.
        parent (Node | None): The parent node of the current node, if any.
    """

    name: str
    path: Path
    parent: Node | None = None

    @property
    def nodetype(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name}: path={self.path})"

    def __hash__(self) -> int:
        return hash(self.path)


@dataclass(repr=False, eq=False)
class Script(Node):
    """
    Represents a MATLAB script.

    Attributes:
        fqdm (str): The fully qualified name of the script.
        docstring (dict[int, str]): A dictionary mapping line numbers to docstrings.
    """

    fqdm: str = ""
    docstring: dict[int, str] = field(default_factory=dict)

    _imports: set[str] = field(default_factory=set)
    _calls: set[str] = field(default_factory=set)
    _builtin_dependencies: set[str] = field(default_factory=set)
    _unresolved_dependencies: set[str] = field(default_factory=set)
    dependencies: set[Script] = field(default_factory=set)
    dependants: set[Script] = field(default_factory=set)


@dataclass(repr=False, eq=False)
class Property(Node):
    """
    Represents a property in a MATLAB class.

    Attributes:
        type (str): The type of the property.
        default (str): The default value of the property.
        size (list[str]): The size of the property.
        validators (list[str]): The validators for the property.
        attributes (PropertyAttributes): The attributes of the property.
        docstring (dict[int, str]): The docstring of the property.
    """

    type: str = ""
    default: str = ""
    size: list[str] = field(default_factory=list)
    validators: list[str] = field(default_factory=list)
    attributes: PropertyAttributes = field(default_factory=PropertyAttributes)
    docstring: dict[int, str] = field(default_factory=dict)


@dataclass(repr=False, eq=False)
class Argument(Node):
    """
    Represents an argument in a MATLAB function or method.

    Attributes:
        type (str): The type of the argument.
        default (str): The default value of the argument.
        size (list[str]): The size of the argument.
        validators (list[str]): The validators applied to the argument.
        attributes (ArgumentAttributes): The attributes of the argument.
        docstring (dict[int, str]): The documentation strings for the argument.
    """

    type: str = ""
    default: str = ""
    size: list[str] = field(default_factory=list)
    validators: list[str] = field(default_factory=list)
    attributes: ArgumentAttributes = field(default_factory=ArgumentAttributes)
    docstring: dict[int, str] = field(default_factory=dict)


@dataclass(repr=False, eq=False)
class Enum(Node):
    """
    Represents an enumeration node.

    Attributes:
        value (str): The value of the enumeration.
        docstring (dict[int, str]): A dictionary mapping integer keys to string values representing the documentation for each enumeration value.
    """

    value: str = ""
    docstring: dict[int, str] = field(default_factory=dict)


@dataclass(repr=False, eq=False)
class Function(Script):
    """
    Represents a function in MATLAB.

    Attributes:
        input (OrderedDict[str, Argument]): The input arguments of the function.
        output (OrderedDict[str, Argument]): The output arguments of the function.
        options (dict[str, Argument]): Additional options for the function.
    """

    input: OrderedDict[str, Argument] = field(default_factory=OrderedDict)
    output: OrderedDict[str, Argument] = field(default_factory=OrderedDict)
    options: dict[str, Argument] = field(default_factory=dict)


@dataclass(repr=False, eq=False)
class Method(Function):
    """
    Represents a method in MATLAB.

    Inherits from the Function class and adds additional attributes specific to methods.
    """

    attributes: MethodAttributes = field(default_factory=MethodAttributes)


@dataclass(repr=False, eq=False)
class Classdef(Script):
    """
    Represents a MATLAB class definition.

    Attributes:
        isclassfolder (bool): Indicates if the class is defined in a class folder.
        ancestors (list[str]): List of ancestor classes.
        enumeration (list[Enum]): List of enumeration definitions.
        methods (dict[str, Method]): Dictionary of method definitions, where the key is the method name and the value is an instance of the Method class.
        properties (dict[str, Property]): Dictionary of property definitions, where the key is the property name and the value is an instance of the Property class.
        attributes (ClassdefAttributes): Instance of the ClassdefAttributes class representing additional attributes of the class.
    """

    isclassfolder: bool = False
    ancestors: list[str] = field(default_factory=list)
    enumeration: list[Enum] = field(default_factory=list)
    methods: dict[str, Method] = field(default_factory=dict)
    properties: dict[str, Property] = field(default_factory=dict)
    attributes: ClassdefAttributes = field(default_factory=ClassdefAttributes)


@dataclass(repr=False, eq=False)
class Package(Script):
    """
    Represents a MATLAB package.

    Attributes:
        classes (list[Classdef]): List of Classdef objects in the package.
        functions (list[Function]): List of Function objects in the package.
        packages (list[Package]): List of nested Package objects in the package.
    """

    classes: list[Classdef] = field(default_factory=list)
    functions: list[Function] = field(default_factory=list)
    packages: list[Package] = field(default_factory=list)


@dataclass(repr=False, eq=False)
class LiveScript(Script):
    """
    Represents a live script in MATLAB.
    """

    ...


@dataclass(repr=False, eq=False)
class App(Script):
    """
    Represents a MATLAB application in the MATLAB path.
    """

    ...


@dataclass(repr=False, eq=False)
class Mex(Script):
    """
    Represents a MATLAB MEX file.
    """

    ...
