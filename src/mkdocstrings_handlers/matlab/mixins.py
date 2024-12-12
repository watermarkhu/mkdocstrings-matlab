from typing import Any
from pathlib import Path


__all__ = ["PathMixin"]


class PathMixin:
    def __init__(self, *args: Any, filepath: Path | None = None, **kwargs: Any) -> None:
        self._filepath: Path | None = filepath
        super().__init__(*args, **kwargs)

    @property
    def filepath(self) -> Path | None:
        return self._filepath
