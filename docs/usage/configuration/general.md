---
toc_depth: 2
---

# General options

## `show_bases`

- **:octicons-package-24: Type [`bool`][] :material-equal: `True`{ title="default value" }**
<!-- - **:octicons-project-template-24: Template :material-null:** (contained in [`class.html`][class template]) -->

Show the base classes of a class.

```yaml title="in mkdocs.yml (global configuration)"
plugins:
- mkdocstrings:
    handlers:
      matlab:
        options:
          show_bases: true
```

```md title="or in docs/some_page.md (local configuration)"
::: matlab_callable
    options:
        show_bases: false
```

??? code ":material-file-code: `myClass.m`"

    ```matlab
    --8<-- "docs/snippets/myClass.m"
    ```

???+ preview

    === "with bases" 

        ```markdown
        ::: myClass
            options:
                show_bases: true
        ```

        ::: myClass
            options:
                show_bases: true

    === "without bases"
        
        ```markdown
        ::: myClass
            options:
                show_bases: false
        ```

        ::: myClass
            options:
                show_bases: false

## `show_inheritance_diagram`


- **:octicons-package-24: Type [`bool`][] :material-equal: `False`{ title="default value" }**
<!-- - **:octicons-project-template-24: Template :material-null:** (contained in [`class.html`][class template]) -->

Show the inheritance diagram of a class using [Mermaid](https://mermaid.js.org/).

With this option enabled, an inheritance diagram (as a flowchart) will be displayed after a class  signature. Each node will act as a cross-reference and will bring you to the relevant class' documentation when clicking on it.

It should work out of the box with [Material for MkDocs](https://squidfunk.github.io), but it is recommended to follow the [setup guide](https://squidfunk.github.io/mkdocs-material/reference/diagrams/#other-diagram-types) for optimal support in Material for Mkdocs. For other themes, you must either setup [mkdocs-mermaid2](https://mkdocs-mermaid2.readthedocs.io/en/latest), or include Mermaid's Javascript code manually:

```yaml title="mkdocs.yml"
extra_javascript:
- https://unpkg.com/mermaid@10.9.0/dist/mermaid.min.js
```

```yaml title="in mkdocs.yml (global configuration)"
plugins:
- mkdocstrings:
    handlers:
      matlab:
        options:
          show_inheritance_diagram: true
```

```md title="or in docs/some_page.md (local configuration)"
::: matlab_callable
    options:
        show_inheritance_diagram: false
```

??? code ":material-file-code: Source files"

    ```matlab title='myClass.m'
    --8<-- "docs/snippets/myClass.m"
    ```

    ```matlab title='myParent.m'
    --8<-- "docs/snippets/myParent.m"
    ```

???+ preview

    ::: myClass
        options:
            show_bases: false
            show_inheritance_diagram: true
            show_root_heading: false
            show_root_toc_entry: false

## `show_source`

- **:octicons-package-24: Type [`bool`][] :material-equal: `True`{ title="default value" }**
<!-- - **:octicons-project-template-24: Template :material-null:** (contained in [`class.html`][class template] and  [`function.html`][function template]) -->

Show the source code of this object.

```yaml title="in mkdocs.yml (global configuration)"
plugins:
- mkdocstrings:
    handlers:
      matlab:
        options:
          show_source: true
```

```md title="or in docs/some_page.md (local configuration)"
::: matlab_callable
    options:
      show_source: false
```

??? code ":material-file-code: `myfunction.m`"

    ```matlab
    --8<-- "docs/snippets/myfunction.m"
    ```

???+ preview

    === "with source" 
        
        ```markdown
        ::: myfunction
            options:
                show_source: true
        ```

        ::: myfunction
            options:
                show_source: true

    === "without bases"

        ```markdown
        ::: myfunction
            options:
                show_source: false
        ```

        ::: myfunction
            options:
                show_source: false
