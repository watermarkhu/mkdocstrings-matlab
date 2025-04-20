"""This module defines enumerations used by the MATLAB handler."""

from __future__ import annotations

from enum import Enum


class Kind(str, Enum):
    """
    An enumeration representing different kinds of MATLAB code elements.
    This enumeration is a subclass of the Griffe `Kind` enumeration, and extends it with additional values.
    """

    FOLDER = "folder"
    """folders"""
    NAMESPACE = "namespace"
    """namespaces"""
    CLASS = "class"
    """Classes."""
    FUNCTION = "function"
    """Functions and methods."""
    SCRIPT = "script"
    """Scripts."""
    PROPERTY = "property"
    """Class properties."""
    ALIAS = "alias"
    """Aliases (imported objects)."""


class ParameterKind(str, Enum):
    """
    An enumeration representing different kinds of function parameters.

    Attributes:
        positional (str): Positional-only parameter.
        optional (str): Optional parameter.
        keyword_only (str): Keyword-only parameter.
        varargin (str): Varargin parameter.
    """

    positional_only = "positional-only"
    optional = "optional"
    keyword_only = "keyword-only"
    varargin = "varargin"


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
