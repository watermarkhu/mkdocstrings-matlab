from enum import Enum
from _griffe.enumerations import Kind as GriffeKind


class Kind(str, Enum):
    """
    An enumeration representing different kinds of MATLAB code elements.
    This enumeration is a subclass of the Griffe `Kind` enumeration, and extends it with additional values.
    """
    MODULE = "module"
    """Modules."""
    CLASS = "class"
    """Classes."""
    FUNCTION = "function"
    """Functions and methods."""
    ATTRIBUTE = "attribute"
    """Attributes and properties."""
    ALIAS = "alias"
    """Aliases (imported objects)."""
    SCRIPT = "script"


class ParameterKind(str, Enum):
    """
    An enumeration representing different kinds of function parameters.

    Attributes:
        positional (str): Positional-only parameter.
        optional (str): Optional parameter.
        keyword_only (str): Keyword-only parameter.
        var_keyword (str): Variadic keyword parameter.
    """

    positional_only = "positional-only"
    optional = "optional"
    keyword_only = "keyword-only"
    var_keyword = "variadic keyword"


class AccessEnum(str, Enum):
    """
    An enumeration representing different access levels for MATLAB code elements.

    Attributes:
        public (str): Represents public access level.
        protected (str): Represents protected access level.
        private (str): Represents private access level.
        immutable (str): Represents immutable access level.
    """

    public = "public"
    protected = "protected"
    private = "private"
    immutable = "immutable"
