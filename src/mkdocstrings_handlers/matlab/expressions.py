from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

from griffe import Expr as GriffeExpr

__all__ = ["CallableExpr", "BuiltinExpr", "MATLAB_BUILTINS"]


def _load_matlab_builtins():
    json_path = Path(__file__).parent / "matlab_builtins.json"
    with open(json_path, "r") as file:
        return json.load(file)


MATLAB_BUILTINS: dict = _load_matlab_builtins()
MATHWORKS_DOC_URL = "https://www.mathworks.com/help/matlab"


@dataclass
class CallableExpr(GriffeExpr):
    name: str

    def __str__(self) -> str:
        """Return the string representation of the builtin expression."""
        return f"{self.name}"


@dataclass
class BuiltinExpr(CallableExpr):
    @property
    def doc(self) -> str:
        """Return the link for the builtin expression."""
        return f"{MATHWORKS_DOC_URL}/{MATLAB_BUILTINS[self.name]}"
