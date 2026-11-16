# Credits

This project owes its existence to the incredible [`mkdocstrings`](https://mkdocstrings.github.io/) and its primary handler [`mkdocstrings-python`](https://mkdocstrings.github.io/python/). The MATLAB handler has been very much a re-implementation of the python handler, adapted where necessary for MATLAB. Special thanks to [@paramoy](https://fosstodon.org/@pawamoy) for his efforts.

Moreover, `mkdocstrings` itself extends [`mkdocs`](https://www.mkdocs.org/) and [`mkdocs-material`](https://squidfunk.github.io/mkdocs-material/), which form the foundation of the entire mkdoc* suite of documentation tools.

Finally, MATLAB source code is read by [malt-index](https://github.com/watermarkhu/malt), the native index of the MATLAB path in malt, which requires [Tree-sitter](https://tree-sitter.github.io/tree-sitter/) and its [MATLAB parser](https://github.com/acristoffers/tree-sitter-matlab). These libraries enable the parsing of MATLAB source code with exceptional speed and accuracy.

Thanks also to [maxx](https://github.com/watermarkhu/maxx), the MATLAB collector this handler used before malt-index. malt-index was written from scratch; it does not contain maxx's code.

The links from MATLAB builtins to their documentation come from the reference index that MATLAB ships with its documentation (`help/docCatalog/referenceapi`). The table in `src/mkdocstrings_handlers/matlab/data/builtin_docs.json` is generated from it by `scripts/gen_builtin_docs.py`, for the MATLAB release recorded in the file.
