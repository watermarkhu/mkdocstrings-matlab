from enum import Enum


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
