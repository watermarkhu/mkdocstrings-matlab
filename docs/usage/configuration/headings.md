# Headings options

## `heading_level`

- **:octicons-package-24: Type [`int`][] :material-equal: `2`{ title="default value" }**
<!-- - **:octicons-project-template-24: Template :material-null:** (N/A) -->

The initial heading level to use.

When injecting documentation for an object, the object itself and its members are rendered. For each layer of objects, we increase the heading level by 1.

The initial heading level will be used for the first layer. If you set it to 3, then headings will start with `<h3>`.

If the [heading for the root object][show_root_heading] is not shown, then the initial heading level is used for its members.

```yaml title="in mkdocs.yml (global configuration)"
plugins:
- mkdocstrings:
    handlers:
      matlab:
        options:
          heading_level: 2
```

```md title="or in docs/some_page.md (local configuration)"
::: matlab_callable
    options:
      heading_level: 3
```

!!! preview 

    === ":material-file-tree: tree"

        ```
        +mypackage
        |-- ClassA.m
        |-- ClassB.m
        |-- myfunction.m
        ```

    === "With level 3 and root heading"

        <h3><code>mypackage</code> (3)</h3>
        <p>Docstring of the package namespace.</p>
        <h4><code>ClassA</code> (4)</h4>
        <p>Docstring of class A.</p>
        <h4><code>ClassB</code> (4)</h4>
        <p>Docstring of class B.</p>
        <h5><code>myfunction</code> (5)</h5>
        <p>Docstring of the function.</p>

    === "With level 3, without root heading"

        <p>Docstring of the package namespace.</p>
        <h3><code>ClassA</code> (3)</h3>
        <p>Docstring of class A.</p>
        <h3><code>ClassB</code> (3)</h3>
        <p>Docstring of class B.</p>
        <h4><code>myfunction</code> (4)</h4>
        <p>Docstring of the function.</p>


## `parameter_headings`

- **:octicons-package-24: Type [`bool`][] :material-equal: `False`{ title="default value" }**

Whether to render headings for function/method parameters.

With this option enabled, each function/method parameter (including parameters of the constructor methods merged in their parent class with the [`merge_init_into_class`][] option) gets a permalink, an entry in the Table of Contents, and an entry in the generated objects inventory. The permalink and inventory entry allow cross-references from internal and external pages.

The identifier used in the permalink and inventory is of the following form: `path.to.function(param_name)`. To manually cross-reference a arameter, you can therefore use this Markdown syntax:

```md
- Class parameter: [`param`][package.module.Class(param)]
- Method parameter: [`param`][package.module.Class.method(param)]
- Function parameter: [`param`][package.module.function(param)]
- Variadic positional parameters: [`*args`][package.module.function(*args)]
- Variadic keyword parameters: [`**kwargs`][package.module.function(**kwargs)]
```

Enabling this option along with [`signature_crossrefs`][] will automatically render cross-references to parameters in class/function/method signatures and attributes values.

```yaml title="in mkdocs.yml (global configuration)"
plugins:
- mkdocstrings:
    handlers:
      matlab:
        options:
          parameter_headings: false
```

```md title="or in docs/some_page.md (local configuration)"
::: matlab_callable
    options:
      parameter_headings: true
```

!!! preview "Preview: Cross-references"

    ::: typedFunction
        options:
          heading_level: 3
          parameter_headings: true
          parameters_from_arguments: true
          docstring_section_style: list

!!! preview "Preview: Parameter sections"

    === "Table style"

        ::: typedFunction
            options:
              heading_level: 3
              show_root_heading: false
              show_root_toc_entry: false
              parameter_headings: true
              parameters_from_arguments: true
              docstring_section_style: table
              show_docstring_returns: false
              show_docstring_description: false

    === "List style"

        ::: typedFunction
            options:
              heading_level: 3
              show_root_heading: false
              show_root_toc_entry: false
              parameter_headings: true
              parameters_from_arguments: true
              docstring_section_style: list
              show_docstring_returns: false
              show_docstring_description: false

    === "Spacy style"

        ::: typedFunction
            options:
              heading_level: 3
              show_root_heading: false
              show_root_toc_entry: false
              parameter_headings: true
              parameters_from_arguments: true
              docstring_section_style: spacy
              show_docstring_returns: false
              show_docstring_description: false

!!! preview "Preview: Table of contents (with symbol types)"

    <code class="doc-symbol doc-symbol-toc doc-symbol-function"></code> typedFunction<br>
    <code class="doc-symbol doc-symbol-toc doc-symbol-parameter" style="margin-left: 16px;"></code> input

    To customize symbols, see [Customizing symbol types](../customization.md/#symbol-types).


