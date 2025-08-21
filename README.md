<!-- --8<-- [start:header] -->

<h1 align="center">mkdocstrings-matlab</h1>

<p align="center">A MATLAB handler for <a href="https://github.com/mkdocstrings/mkdocstrings"><i>mkdocstrings</i></a>.</p>

<p align="center"><img width=300px src="logo.png"></p>

[![Qualify](https://github.com/watermarkhu/mkdocstrings-matlab/actions/workflows/qualify.yaml/badge.svg?branch=main)](https://github.com/watermarkhu/mkdocstrings-matlab/actions/workflows/qualify.yaml)
[![documentation](https://img.shields.io/badge/docs-mkdocs-708FCC.svg?style=flat)](https://watermarkhu.nl/mkdocstrings-matlab)
[![pypi version](https://img.shields.io/pypi/v/mkdocstrings-matlab.svg)](https://pypi.org/project/mkdocstrings-matlab/)

The MATLAB handler uses [maxx](https://github.com/watermarkhu/maxx) to collect documentation from MATLAB source code, which in turn uses [Tree-sitter](https://tree-sitter.github.io/tree-sitter/) and its [MATLAB parser](https://github.com/acristoffers/tree-sitter-matlab).

You can install this handler by specifying it as a dependency:

```toml title="pyproject.toml"
# PEP 621 dependencies declaration
# adapt to your dependencies manager
[project]
dependencies = [
    "mkdocstrings-matlab>=0.X.Y",
]
```

<!-- --8<-- [end:header] -->
<!-- --8<-- [start:footer] -->

## Features

- 🤖 **Data collection from source code**: collection of the object-tree and the docstrings is done thanks to
  [Tree-sitter](https://tree-sitter.github.io/tree-sitter/).

- ✨ **Support for argument validation blocks:** Tree-sitter collects your [function and method argument validation](https://mathworks.com/help/matlab/matlab_prog/function-argument-validation-1.html)
   blocks to display input and output argument types and default values. 
   It is even able to automatically add cross-references to other objects from your API, and links to MathWorks documentation are generated for MATLAB builtin classes. 

- 🔁 **Recursive documentation of MATLAB [namespaces](https://mathworks.com/help/matlab/matlab_oop/namespaces.html) and folders:** 
  just add `+` to the identifer for namespaces or the relative path for folder, and you get documentation for the entire directory. You don't need to inject documentation for each class, function, and script. Additionaly, the directory documentation will be either extracted from the `Contents.m` or the `readme.md` file at the root of the namespace or folder.

- 📄 **Multiple docstring-styles support:** common support for Google-style, Numpydoc-style,
  and Sphinx-style docstrings. See [Griffe's documentation](https://mkdocstrings.github.io/griffe/docstrings/) on docstrings support.

- ⚠️ **Admonition support in Google docstrings:** blocks like `Note:` or `Warning:` will be transformed
  to their [admonition](https://squidfunk.github.io/mkdocs-material/reference/admonitions/) equivalent.
  *We do not support nested admonitions in docstrings!*

- 🔗 **Every object has a TOC entry:** we render a heading for each object, meaning *MkDocs* picks them into the Table
  of Contents, which is nicely displayed by the Material theme. Thanks to *mkdocstrings* cross-reference ability,
  you can reference other objects within your docstrings, with the classic Markdown syntax:
  `[this object][namespace.subnamespace.object]` or directly with `[namespace.subnamespace.object][]`

- 📺 **Source code display:** *mkdocstrings* can add a collapsible div containing the highlighted source code of the MATLAB object.

<!-- --8<-- [end:footer] -->
