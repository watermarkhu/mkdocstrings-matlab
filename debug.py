import argparse
from pathlib import Path

from mkdocs.commands.serve import serve


def serve_mkdocs(mkdocs_dir: str = "", dev_addr: str = "127.0.0.1:8000"):
    """
    Runs the 'mkdocs serve' command programmatically.

    Args:
        mkdocs_dir: The directory containing the mkdocs.yml file.
                    If None, uses the current working directory.
        dev_addr: The address and port to serve on (e.g., '127.0.0.1:8000').
    """
    dir = Path(mkdocs_dir) if mkdocs_dir else Path.cwd()
    config_file = dir / "mkdocs.yml"
    if not config_file.exists():
        raise FileNotFoundError(f"mkdocs.yml not found in {dir}")

    serve(str(config_file), watch=[mkdocs_dir])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Serve an MkDocs site.")
    parser.add_argument(
        "mkdocs_dir",
        nargs="?",
        default=None,
        help="Optional: The directory containing the mkdocs.yml file. Defaults to the current working directory.",
    )
    parser.add_argument(
        "--addr",
        dest="dev_addr",
        default="127.0.0.1:8000",
        help="IP address and port to serve documentation locally (default: 127.0.0.1:8000)",
    )

    args = parser.parse_args()

    serve_mkdocs(mkdocs_dir=args.mkdocs_dir, dev_addr=args.dev_addr)

    # Example command-line usage:
    # python your_script_name.py
    # python your_script_name.py /path/to/your/mkdocs/project
    # python your_script_name.py --addr 0.0.0.0:8080
    # python your_script_name.py /path/to/your/mkdocs/project --addr 0.0.0.0:8080
