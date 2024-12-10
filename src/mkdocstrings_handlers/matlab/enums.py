from enum import Enum


class ParameterKind(str, Enum):
    """Enumeration of the different parameter kinds."""

    positional: str = "positional"
    """Positional-only parameter."""
    # positional_or_keyword: str = "positional or keyword"
    # """Positional or keyword parameter."""
    # var_positional: str = "variadic positional"
    # """Variadic positional parameter."""

    optional: str = "optional"
    """Optional parameter."""
    keyword_only: str = "keyword-only"
    """Keyword-only parameter."""
    var_keyword: str = "variadic keyword"
    """Variadic keyword parameter."""


class AccessEnum(str, Enum):
    PUBLIC: str = "public"
    PROTECTED: str = "protected"
    PRIVATE: str = "private"
    IMMUTABLE: str = "immutable"
