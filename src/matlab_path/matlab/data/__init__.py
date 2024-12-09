import json
from pathlib import Path

_FILE = Path(__file__).parent / "references.json"
_REFERENCES: dict[str, str] = {}


def _load_references() -> dict[str, str]:
    global _REFERENCES
    if not _REFERENCES:
        with open(_FILE) as file:
            _REFERENCES = json.load(file)
    return _REFERENCES
