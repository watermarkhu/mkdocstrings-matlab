---
hide:
- feedback
---

--8<-- "README.md:header"

## Preview 

Let's us quickly see how auto-documentation works with mkdocstrings-matlab:

```matlab title="Function making use of Argument Validation in namespace +mynamespace"
--8<-- "docs/snippets/+mynamespace/typed_function.m"
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

    Syntax highlighting of argument blocks will be incorrect with the default configuration due to the outdated MATLAB lexer in [Pygments](https://github.com/pygments/pygments/) and will be resolved after [our PR](https://github.com/pygments/pygments/pull/2887) is merged. 

    In the meantime, the correct syntax highlighing can be configured by adding our branch as the dependency in `pyproject.toml`
    
    ```toml title="pyproject.toml"
    dependencies = [
        "pygments @ git+https://github.com/watermarkhu/pygments.git@matlab",
    ]
    ```

--8<-- "README.md:footer"
