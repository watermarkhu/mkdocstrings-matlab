from __future__ import annotations

from dataclasses import dataclass, field


class Attributes:
    @classmethod
    def from_dict(cls, settings: dict):
        for key, value in settings.items():
            if value is None:
                settings[key] = True
                continue
            annotation = cls.__annotations__.get(key, bool)
            if annotation == "str":
                settings[key] = value
            elif annotation == "bool":
                if value in ["True", "true", "t", 1]:
                    settings[key] = True
                else:
                    settings[key] = False
            elif annotation == "int":
                settings[key] = int(value)
            elif annotation == "str":
                settings[key] = value
            elif annotation == "list[str]":
                raise NotImplementedError
            else:
                raise NotImplementedError
        return cls(**settings)


@dataclass
class ArgumentAttributes(Attributes):
    """Argument block attributes"""

    # https://mathworks.com/help/matlab/ref/arguments.html
    Input: bool = True
    Output: bool = False
    Repeating: bool = False

    @property
    def is_input(self):
        if self.Output:
            return False
        return self.Input


@dataclass
class PropertyAttributes(Attributes):
    """Class property attributes"""

    # https://mathworks.com/help/matlab/matlab_oop/property-attributes.html
    Abortset: bool = False
    Abstract: bool = False
    Access: str = "public"
    Constant: bool = False
    Dependent: bool = False
    GetAccess: str = "public"
    GetObservable = False
    Hidden: bool = False
    NonCopyable: bool = False
    PartialMatchPriority: int = 1
    SetAccess: str = "public"
    SetObservable: bool = False
    Transient: bool = False

    # https://mathworks.com/help/matlab/matlab_prog/define-property-attributes-1.html
    DiscreteState: bool = False
    NonTunable: bool = False

    # https://mathworks.com/help/matlab/ref/matlab.unittest.testcase-class.html/
    TestParameter: bool = False
    MethodSetupParameter: bool = False
    ClassSetupParameter: bool = False


@dataclass
class MethodAttributes(Attributes):
    """Class method attributes"""

    # https://mathworks.com/help/matlab/matlab_oop/method-attributes.html
    Abstract: bool = False
    Access: str = "public"
    Hidden: bool = False
    Sealed: bool = False
    Static: bool = False

    # https://mathworks.com/help/matlab/ref/matlab.unittest.testcase-class.html
    Test: bool = False
    TestMethodSetup: bool = False
    TestMethodTeardown: bool = False
    TestClassSetup: bool = False
    TestClassTeardown: bool = False
    ParameterCombination: str = "exhaustive"
    TestParameterDefinition: str = ""
    TestTags: list[str] = field(default_factory=list)


@dataclass
class ClassdefAttributes(Attributes):
    """Class attributes"""

    # https://mathworks.com/help/matlab/matlab_oop/class-attributes.html
    Abstract: bool = False
    AllowedSubclasses: str = ""
    ConstructOnLoad: bool = False
    HandleCompatible: bool = False
    Hidden: bool = False
    InferiorClasses: str = ""
    Sealed: bool = False

    # https://mathworks.com/help/matlab/ref/matlab.unittest.testcase-class.html
    SharedTestFixtures: list[str] = field(default_factory=list)
    TestTags: list[str] = field(default_factory=list)
