<h1 align="center">mkdocstrings-matlab</h1>

<p align="center">A MATLAB handler for <a href="https://github.com/mkdocstrings/mkdocstrings"><i>mkdocstrings</i></a>.</p>


---

<p align="center"><img src="logo.png"></p>

The MATLAB handler uses [Tree-sitter](https://tree-sitter.github.io/tree-sitter/) and its [MATLAB parser](https://github.com/acristoffers/tree-sitter-matlab) to collect documentation from MATLAB source code. Via the python bindings the Abstract Syntax Tree (AST) of the source code is traversed to extract useful information. The imported objected are imported as custom [Griffe](https://mkdocstrings.github.io/griffe/) objects and mocked for the [python handler](https://mkdocstrings.github.io/python/). 

## Installation

You can install this handler by specifying it as a dependency:

```toml title="pyproject.toml"
# PEP 621 dependencies declaration
# adapt to your dependencies manager
[project]
dependencies = [
    "mkdocstrings-matlab>=0.3",
]
```

## Features

- **Data collection from source code**: collection of the object-tree and the docstrings is done thanks to
  [Tree-sitter](https://tree-sitter.github.io/tree-sitter/).

- **Support for argument validation blocks:** Tree-sitter collects your [function and method argument validation](https://mathworks.com/help/matlab/matlab_prog/function-argument-validation-1.html)
   blocks to display input and output argument types and default values. 
   It is even able to automatically add cross-references o other objects from your API.

- **Recursive documentation of MATLAB [namespaces](https://mathworks.com/help/matlab/matlab_oop/namespaces.html):** 
  just add `+` to the identifer, and you get the full namespace docs. You don't need to inject documentation for each class, function, and script.

- **Support for documented properties:** properties definitions followed by a docstring will be recognized in classes. 

- **Multiple docstring-styles support:** common support for Google-style, Numpydoc-style,
  and Sphinx-style docstrings. See [Griffe's documentation](https://mkdocstrings.github.io/griffe/docstrings/) on docstrings support.

- **Admonition support in Google docstrings:** blocks like `Note:` or `Warning:` will be transformed
  to their [admonition](https://squidfunk.github.io/mkdocs-material/reference/admonitions/) equivalent.
  *We do not support nested admonitions in docstrings!*

- **Every object has a TOC entry:** we render a heading for each object, meaning *MkDocs* picks them into the Table
  of Contents, which is nicely displayed by the Material theme. Thanks to *mkdocstrings* cross-reference ability,
  you can reference other objects within your docstrings, with the classic Markdown syntax:
  `[this object][namespace.subnamespace.object]` or directly with `[namespace.subnamespace.object][]`

- **Source code display:** *mkdocstrings* can add a collapsible div containing the highlighted source code of the MATLAB object.