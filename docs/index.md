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

![Image title](img/preview_dark.png#only-dark){ align=right width=400 }

![Image title](img/preview_light.png#only-light){ align=right width=400 }

With the following syntax in the source markdown document file,

```markdown title="source markdown document"
::: mynamespace.typed_function
    options:
      parse_arguments: true
```

The function `typed_function` will be auto-documented as displayed on the right. 

</div>

--8<-- "README.md:footer"
