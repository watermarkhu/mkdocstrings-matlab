"""MATLAB handler for mkdocstrings."""

from _griffe.docstrings import google, numpy
from _griffe.enumerations import DocstringSectionKind

from mkdocstrings_handlers.matlab import collect, models, treesitter
from mkdocstrings_handlers.matlab.handler import MatlabHandler, get_handler
from mkdocstrings_handlers.matlab.config import MatlabConfig, MatlabOptions

__all__ = [
    "MatlabHandler",
    "MatlabConfig",
    "MatlabOptions",
    "get_handler",
    "collect",
    "models",
    "treesitter",
]


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
