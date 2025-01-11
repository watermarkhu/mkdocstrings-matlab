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

<div class="result" markdown>

![Image title](img/preview_dark.png#only-dark){ align=left width=400 }

![Image title](img/preview_light.png#only-light){ align=left width=400 }

Given the function above, the rendered documentation here is created from the following markdown document file,

```markdown title="docs/api.md"
::: mynamespace.typed_function
    options:
      parse_arguments: true
```

</div>

--8<-- "README.md:footer"
