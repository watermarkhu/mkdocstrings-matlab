# Credits

This project owes its existence to the incredible [`mkdocstrings`](https://mkdocstrings.github.io/) and its primary handler [`mkdocstrings-python`](https://mkdocstrings.github.io/python/). The MATLAB handler has been very much a re-implementation of the python handler, adapted where necessary for MATLAB. Special thanks to [@paramoy](https://fosstodon.org/@pawamoy) for his efforts.

Moreover, `mkdocstrings` itself extends [`mkdocs`](https://www.mkdocs.org/) and [`mkdocs-material`](https://squidfunk.github.io/mkdocs-material/), which form the foundation of the entire mkdoc* suite of documentation tools.

Finally, the parsing of MATLAB docstrings is powered by [maxx](https://github.com/watermarkhu/maxx), which in turn requires [Tree-sitter](https://tree-sitter.github.io/tree-sitter/) and its [MATLAB parser](https://github.com/acristoffers/tree-sitter-matlab). These libraries enable the parsing of MATLAB source code with exceptional speed and accuracy.
