# Credits

This project owes its existence to the incredible [`mkdocstrings`](https://mkdocstrings.github.io/), its primary extension [`mkdocstrings-python`](https://mkdocstrings.github.io/python/), and [`griffe`](https://github.com/mkdocstrings/griffe). These tools handle the templating of parsed content into HTML elements using Jinja templates, allowing much of the code and documentation to be reused and adapted for *mkdocstrings-matlab*. Special thanks to [@paramoy](https://fosstodon.org/@pawamoy) for his efforts.

Moreover, `mkdocstrings` itself extends [`mkdocs`](https://www.mkdocs.org/) and [`mkdocs-material`](https://squidfunk.github.io/mkdocs-material/), which form the foundation of the entire mkdoc* suite of documentation tools.

Finally, the parsing of MATLAB docstrings is powered by [Tree-sitter](https://tree-sitter.github.io/tree-sitter/) and its [MATLAB parser](https://github.com/acristoffers/tree-sitter-matlab). These libraries enable the parsing of MATLAB source code with exceptional speed and accuracy.
