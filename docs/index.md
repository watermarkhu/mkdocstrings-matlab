---
hide:
- feedback
---

--8<-- "README.md:header"

## Preview

Let's us quickly see how auto-documentation works with mkdocstrings-matlab:

```matlab title="Function making use of Argument Validation in namespace +mynamespace"
--8<-- "docs/src/snippets/+mynamespace/typed_function.m"
```

Given the function above, the rendered documentation here is created from the following markdown document file,

```markdown title="docs/api.md"
::: mynamespace.typed_function
    options:
      parse_arguments: true
      separate_signature: true
      show_signature_types: true
      signature_crossrefs: true
```

<div class="result" markdown>

::: mynamespace.typed_function
    options:
      parse_arguments: true
      separate_signature: true
      show_signature_types: true
      signature_crossrefs: true
      docstring_section_style: list

</div>

!!! note

    MATLAB code blocks are highlighted using the bundled TextMate grammar from `textmate-grammar-python`, with classes derived from its scopes. The `matlab` fence formatter is registered in the documentation configuration, so examples and snippets use the same highlighter.

--8<-- "README.md:footer"
