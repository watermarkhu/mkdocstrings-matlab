from pathlib import Path

from mkdocstrings_handlers.matlab.treesitter import FileParser

file = (
    Path(__file__).parent.parent
    / "docs"
    / "snippets"
    / "+mynamespace"
    / "typed_function.m"
)
parser = FileParser(file.resolve())
parser.parse()

# https://github.com/mkdocstrings/python/compare/1.13.0...1.16.2
