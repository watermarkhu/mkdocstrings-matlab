from enum import Enum


class ParameterKind(str, Enum):
    """Enumeration of the different parameter kinds."""

    positional = "positional"
    """Positional-only parameter."""
    # positional_or_keyword: str = "positional or keyword"
    # """Positional or keyword parameter."""
    # var_positional: str = "variadic positional"
    # """Variadic positional parameter."""

    optional = "optional"
    """Optional parameter."""
    keyword_only = "keyword-only"
    """Keyword-only parameter."""
    var_keyword = "variadic keyword"
    """Variadic keyword parameter."""


class AccessEnum(str, Enum):
    PUBLIC = "public"
    PROTECTED = "protected"
    PRIVATE = "private"
    IMMUTABLE = "immutable"
