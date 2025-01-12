from contextlib import contextmanager
from mkdocs.commands import serve
from pathlib import Path

import os


@contextmanager
def set_directory(path: Path):
    origin = Path().absolute()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(origin)


config_path = Path(__file__).parent.parent.resolve() / "mkdocs.yml"

kwargs = {
    "dev_addr": None,
    "open_in_browser": False,
    "livereload": False,
    "build_type": None,
    "watch_theme": True,
    "config_file": str(config_path),
    "strict": None,
    "use_directory_urls": None,
}

with set_directory(config_path.parent):
    serve.serve(**kwargs)
