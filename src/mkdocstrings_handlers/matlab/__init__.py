"""MATLAB handler for mkdocstrings."""

from mkdocstrings_handlers.matlab.handler import get_handler
from mkdocstrings_handlers.matlab import collect, handler, models, treesitter
from _griffe.enumerations import DocstringSectionKind
from _griffe.docstrings import numpy, google

__all__ = ["get_handler", "collect", "handler", "models", "treesitter"]


# Add custom sections to the numpy and google docstring parsers
extensions = {
    "arguments": DocstringSectionKind.parameters,
    "input arguments": DocstringSectionKind.parameters,
    "outputs": DocstringSectionKind.returns,
    "output arguments": DocstringSectionKind.returns,
    "name value arguments": DocstringSectionKind.other_parameters,
    "name-value arguments": DocstringSectionKind.other_parameters,
    "name value pairs": DocstringSectionKind.other_parameters,
    "name-value pairs": DocstringSectionKind.other_parameters,
    "properties": DocstringSectionKind.attributes,
    "namespaces": DocstringSectionKind.modules,
    "packages": DocstringSectionKind.modules,
}

google._section_kind.update(extensions)
numpy._section_kind.update(extensions)
