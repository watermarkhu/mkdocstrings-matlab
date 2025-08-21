"""MATLAB handler for mkdocstrings."""

from __future__ import annotations

import logging

from griffe._internal.docstrings import google, numpy
from griffe._internal.enumerations import DocstringSectionKind

from mkdocstrings_handlers.matlab.config import MatlabConfig, MatlabOptions
from mkdocstrings_handlers.matlab.handler import MatlabHandler, get_handler

__all__: list = [
    "MatlabHandler",
    "MatlabConfig",
    "MatlabOptions",
    "get_handler",
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


# Filter griffe logger to remove return type warnings, as this is possible in MATLAB
class ReturnTypeWarningFilter(logging.Filter):
    def filter(self, record):
        if hasattr(record, "msg"):
            message = str(record.msg)
            if "No type or annotation for returned value" in message:
                return False
        return True


griffe_logger: logging.Logger = logging.getLogger("mkdocs.plugins.griffe")
griffe_logger.addFilter(ReturnTypeWarningFilter())
