from typing import Any
from pathlib import Path
from griffe import Object


__all__ = ["CanonicalPathMixin", "PathMixin", "ROOT"]

class _Root(Object):
    def __init__(self) -> None:
        super().__init__("ROOT", parent=None)

    def __repr__(self) -> str:
        return "MATLABROOT"


ROOT = _Root()


class CanonicalPathMixin:
    @property
    def canonical_path(self) -> str:
        """The full dotted path of this object.

        The canonical path is the path where the object was defined (not imported).
        """
        if isinstance(self.parent, _Root):
            return self.name
        return f"{self.parent.path}.{self.name}"


class PathMixin:
    def __init__(self, *args: Any, filepath: Path | None = None, **kwargs: Any) -> None:
        self._filepath: Path | None = filepath
        super().__init__(*args, **kwargs)

    @property
    def filepath(self) -> Path | None:
        return self._filepath