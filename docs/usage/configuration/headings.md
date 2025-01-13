---
toc_depth: 2
---

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

--8<-- "docs/snippets/+mynamespace/mynamespace.md"

???+ preview 

    === "With level 3 and root heading"

        <h3><code>mynamespace</code> (3)</h3>
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

With this option enabled, each function/method parameter (including parameters of the constructor methods merged in their parent class with the [`merge_constructor_into_class`][] option) gets a permalink, an entry in the Table of Contents, and an entry in the generated objects inventory. The permalink and inventory entry allow cross-references from internal and external pages.

The identifier used in the permalink and inventory is of the following form: `path.to.function(param_name)`. To manually cross-reference a arameter, you can therefore use this Markdown syntax:

```md
- Class parameter: [`param`][package.module.Class(param)]
- Method parameter: [`param`][package.module.Class.method(param)]
- Function parameter: [`param`][package.module.function(param)]
- Variadic positional parameters: [`*args`][package.module.function(*args)]
- Variadic keyword parameters: [`**kwargs`][package.module.function(**kwargs)]
```

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

--8<-- "docs/snippets/+mynamespace/mynamespace.md"

???+ preview "Preview: Cross-references"

    === "With parameter headings"

        ```markdown
        ::: mynamespace.typed_function
            options:
              parameter_headings: true
        ```

        ::: mynamespace.typed_function
            options:
              parameter_headings: true
              docstring_section_style: list

    === "Without parameter headings"

        ```markdown
        ::: mynamespace.typed_function
            options:
              parameter_headings: false
        ```

        ::: mynamespace.typed_function
            options:
              parameter_headings: false
              docstring_section_style: list

???+ preview "Preview: Parameter sections"

    === "Table style"

        ::: mynamespace.typed_function
            options:
              show_root_heading: false
              show_root_toc_entry: false
              parameter_headings: true
              docstring_section_style: table
              show_docstring_output_arguments: false
              show_docstring_description: false

    === "List style"

        ::: mynamespace.typed_function
            options:
              show_root_heading: false
              show_root_toc_entry: false
              parameter_headings: true
              docstring_section_style: list
              show_docstring_output_arguments: false
              show_docstring_description: false

    === "Spacy style"

        ::: mynamespace.typed_function
            options:
              show_root_heading: false
              show_root_toc_entry: false
              parameter_headings: true
              docstring_section_style: spacy
              show_docstring_output_arguments: false
              show_docstring_description: false

???+ preview "Preview: Table of contents (with symbol types)"

    <code class="doc-symbol doc-symbol-toc doc-symbol-function"></code> typed_function<br>
    <code class="doc-symbol doc-symbol-toc doc-symbol-parameter" style="margin-left: 16px;"></code> input


## `show_root_heading`

- **:octicons-package-24: Type [`bool`][] :material-equal: `False`{ title="default value" }**
<!-- - **:octicons-project-template-24: Template :material-null:** (N/A) -->

Show the heading of the object at the root of the documentation tree (i.e. the object referenced by the identifier after `:::`).

It is pretty common to inject documentation for one module per page. Since each page already has a title, usually being the module's name, we can spare one heading level by not showing the heading for the module itself (heading levels are limited to 6 by the HTML specification).

Sparing that extra level can be helpful when your objects tree is deeply nested (e.g. method in a class in a class in a module). If your objects tree is not deeply nested, and you are injecting documentation for many different objects on a single page, it might be preferable to render the heading of each object.

```yaml title="in mkdocs.yml (global configuration)"
plugins:
- mkdocstrings:
    handlers:
      matlab:
        options:
          show_root_heading: false
```

```md title="or in docs/some_page.md (local configuration)"
::: mynamespace.ClassA
    options:
      show_root_heading: true

::: mynamespace.ClassB
    options:
      show_root_heading: true
```

--8<-- "docs/snippets/+mynamespace/mynamespace.md"

???+ preview

    === "With root heading"
    
        ::: mynamespace.classA
            options:
              show_root_heading: true

        ::: mynamespace.classB
            options:
              show_root_heading: true
              members: true

    === "Without root heading"
    
        ::: mynamespace.classA
            options:
              show_root_heading: false

        ::: mynamespace.classB
            options:
              show_root_heading: false

## `show_root_toc_entry`

- **:octicons-package-24: Type [`bool`][] :material-equal: `True`{ title="default value" }**
<!-- - **:octicons-project-template-24: Template :material-null:** (N/A) -->

If the root heading is not shown, at least add a ToC entry for it.

If you inject documentation for an object in the middle of a page, after long paragraphs, and without showing the [root heading][show_root_heading], then you will not be able to link to this particular object as it won't have a permalink and will be "lost" in the middle of text. In that case, it is useful to add a hidden anchor to the document, which will also appear in the table of contents.

In other cases, you might want to disable the entry to avoid polluting the ToC. It is not possible to show the root heading *and* hide the ToC entry.

```yaml title="in mkdocs.yml (global configuration)"
plugins:
- mkdocstrings:
    handlers:
      matlab:
        options:
          show_root_toc_entry: true
```

```md title="or in docs/some_page.md (local configuration)"
## Some heading

Lots of text.

::: matlab_callable
    options:
      show_root_toc_entry: false

## Other heading.

More text.
```

???+ preview

    === "With ToC entry"

        ```markdown
        ::: matlab_callable
            options:
              show_root_toc_entry: true
        ```

        **Table of contents**  
        [Some heading](#permalink-to-some-heading){ title="#permalink-to-some-heading" }  
        [`matlab_callable`](#permalink-to-object){ title="#permalink-to-object" }   
        [Other heading](#permalink-to-other-heading){ title="#permalink-to-other-heading" } 

    === "Without ToC entry"

        ```markdown
        ::: matlab_callable
            options:
              show_root_toc_entry: false
        ```

        **Table of contents**  
        [Some heading](#permalink-to-some-heading){ title="#permalink-to-some-heading" }  
        [Other heading](#permalink-to-other-heading){ title="#permalink-to-other-heading" }

## `show_root_full_path`

- **:octicons-package-24: Type [`bool`][] :material-equal: `True`{ title="default value" }**
<!-- - **:octicons-project-template-24: Template :material-null:** (N/A) -->

Show the full namespace path for the root object heading.

The namespace path of a MATLAB object is the dot-separated list of names under which it is accessible, for example `namespace.Class.method`.

With this option you can choose to show the full path of the object you inject documentation for, or just its name. This option impacts only the object you specify, not its members. For members, see the two other options [`show_root_members_full_path`][] and [`show_object_full_path`][].

```yaml title="in mkdocs.yml (global configuration)"
plugins:
- mkdocstrings:
    handlers:
      matlab:
        options:
          show_root_full_path: true
```

```md title="or in docs/some_page.md (local configuration)"
::: mynamespace.classA
    options:
      show_root_full_path: false
```

--8<-- "docs/snippets/+mynamespace/mynamespace.md"

???+ preview

    === "With root full path"

        ```markdown
        ::: mynamespace.classA
            options:
              show_root_full_path: true
        ```

        ::: mynamespace.classA
            options:
              show_root_full_path: true

    === "Without root full path"

        ```markdown
        ::: mynamespace.classA
            options:
              show_root_full_path: false
        ```

        ::: mynamespace.classA
            options:
              show_root_full_path: false

## `show_root_members_full_path`

- **:octicons-package-24: Type [`bool`][] :material-equal: `False`{ title="default value" }**
<!-- - **:octicons-project-template-24: Template :material-null:** (N/A) -->

Show the full namespace path of the root members.

This option does the same thing as [`show_root_full_path`][], but for direct members  of the root object instead of the root object itself.

To show the full path for every member recursively, see [`show_object_full_path`][].

```yaml title="in mkdocs.yml (global configuration)"
plugins:
- mkdocstrings:
    handlers:
      matlab:
        options:
          show_root_members_full_path: true
```

```md title="or in docs/some_page.md (local configuration)"
::: mynamespace.classA
    options:
      show_root_members_full_path: false
```

--8<-- "docs/snippets/+mynamespace/mynamespace.md"

???+ preview

    === "With root members full path"

        ```markdown
        ::: mynamespace.classA
            options:
              show_root_members_full_path: true
        ```

        ::: mynamespace.classA
            options:
              show_root_members_full_path: true

    === "Without root members full path"

        ```markdown
        ::: mynamespace.classA
            options:
              show_root_members_full_path: false
        ```

        ::: mynamespace.classA
            options:
              show_root_members_full_path: false

## `show_object_full_path`

- **:octicons-package-24: Type [`bool`][] :material-equal: `False`{ title="default value" }**
<!-- - **:octicons-project-template-24: Template :material-null:** (N/A) -->

Show the full namespace path of every object.

Same as for [`show_root_members_full_path`][], but for every member, recursively. This option takes precedence over [`show_root_members_full_path`][]:

`show_root_members_full_path` | `show_object_full_path` | Direct root members path
----------------------------- | ----------------------- | ------------------------
False                         | False                   | Name only
False                         | True                    | Full
True                          | False                   | Full
True                          | True                    | Full

```yaml title="in mkdocs.yml (global configuration)"
plugins:
- mkdocstrings:
    handlers:
      matlab:
        options:
          show_object_full_path: true
```

```md title="or in docs/some_page.md (local configuration)"
::: +mynamespace
    options:
      show_object_full_path: false
```

???+ preview

    === "With object full path"

        ```markdown
        ::: +mynamespace
            options:
              show_object_full_path: true
        ```

        ::: +mynamespace
            options:
              show_object_full_path: true
              show_docstring_input_arguments: false
              show_docstring_output_arguments: false

    === "Without object full path"
        
        ```markdown
        ::: +mynamespace
            options:
              show_object_full_path: false
        ```

        ::: +mynamespace
            options:
              show_object_full_path: false
              show_docstring_input_arguments: false
              show_docstring_output_arguments: false

## `show_category_heading`

- **:octicons-package-24: Type [`bool`][] :material-equal: `False`{ title="default value" }**
<!-- - **:octicons-project-template-24: Template :material-null:** (N/A) -->

When [grouped by categories][group_by_category], show a heading for each category.
These category headings will appear in the table of contents,
allowing you to link to them using their permalinks.

!!! warning "Not recommended with deeply nested object"

    When injecting documentation for deeply nested objects, you'll quickly run out of heading levels, and the objects at the bottom of the tree risk all getting documented using H6 headings, which might decrease the readability of your API docs. 

```yaml title="in mkdocs.yml (global configuration)"
plugins:
- mkdocstrings:
    handlers:
      matlab:
        options:
          group_by_category: true
          show_category_heading: true
```

```md title="or in docs/some_page.md (local configuration)"
::: matlab_callable
    options:
      group_by_category: true
      show_category_heading: false
```

--8<-- "docs/snippets/+mynamespace/mynamespace.md"

???+ preview

    === "With category headings"

        ```markdown
        ::: +mynamespace
            options:
              group_by_category: true
              show_category_heading: true
        ```
        
        ::: +mynamespace
            options:
              group_by_category: true
              show_category_heading: true
              show_docstring_input_arguments: false
              show_docstring_output_arguments: false

    === "Without category headings"

        ```markdown
        ::: +mynamespace
            options:
              group_by_category: true
              show_category_heading: false
        ```

        ::: +mynamespace
            options:
              group_by_category: true
              show_category_heading: false
              show_docstring_input_arguments: false
              show_docstring_output_arguments: false

## `show_symbol_type_heading`

- **:octicons-package-24: Type [`bool`][] :material-equal: `False`{ title="default value" }**
<!-- - **:octicons-project-template-24: Template :material-null:** (N/A) -->

Show the symbol type in headings.

This option will prefix headings with
<code class="doc-symbol doc-symbol-attribute"></code>,
<code class="doc-symbol doc-symbol-function"></code>,
<code class="doc-symbol doc-symbol-method"></code>,
<code class="doc-symbol doc-symbol-class"></code> or
<code class="doc-symbol doc-symbol-module"></code> types.
See also [`show_symbol_type_toc`][show_symbol_type_toc].

```yaml title="in mkdocs.yml (global configuration)"
plugins:
- mkdocs-material-matlab # (1)
- mkdocstrings:
    handlers:
      matlab:
        options:
          show_symbol_type_heading: true
```

1. :warning: When using material theme, make sure to also enable the plugin `mkdocs-material-matlab` such that the right heading types are displayed. Otherwise, <code class="doc-symbol doc-symbol-attribute"></code> will be shown as `attr` and <code class="doc-symbol doc-symbol-module"></code> will be shown as `mod`, as the mkdocstrings-matlab plugin is reusing assets from mkdocstrings-python. 

```md title="or in docs/some_page.md (local configuration)"
::: matlab_callable
    options:
      show_symbol_type_heading: false
```

--8<-- "docs/snippets/+mynamespace/mynamespace.md"

???+ preview

    === "With symbol type in headings"

        ```markdown
        ::: docs/snippets
            options:
              members:
                - mynamespace
              show_symbol_type_heading: true
        ```

        ::: docs/snippets
            options:
              members: 
                - mynamespace
              show_symbol_type_heading: true
              show_docstring_input_arguments: false
              show_docstring_output_arguments: false

    === "Without symbol type in headings"

        ```markdown
        ::: docs/snippets
            options:
              members:
                - mynamespace
              show_symbol_type_heading: false
        ```

        ::: docs/snippets
            options:
              members:
                - mynamespace
              show_symbol_type_heading: false
              show_docstring_input_arguments: false
              show_docstring_output_arguments: false

## `show_symbol_type_toc`

- **:octicons-package-24: Type [`bool`][] :material-equal: `False`{ title="default value" }**
<!-- - **:octicons-project-template-24: Template :material-null:** (N/A) -->

Show the symbol type in the Table of Contents.

This option will prefix items in the ToC with
<code class="doc-symbol doc-symbol-property"></code>,
<code class="doc-symbol doc-symbol-function"></code>,
<code class="doc-symbol doc-symbol-method"></code>,
<code class="doc-symbol doc-symbol-class"></code>,
<code class="doc-symbol doc-symbol-namespace"></code> or.
<code class="doc-symbol doc-symbol-folder"></code> types.
See also [`show_symbol_type_heading`][show_symbol_type_heading].

```yaml title="in mkdocs.yml (global configuration)"
plugins:
- mkdocs-material-matlab # (1)
- mkdocstrings:
    handlers:
      matlab:
        options:
          show_symbol_type_toc: true
```

1. :warning: When using material theme, make sure to also enable the plugin `mkdocs-material-matlab` such that the right heading types are displayed. 


```md title="or in docs/some_page.md (local configuration)"
::: matlab_callable
    options:
      show_symbol_type_toc: false
```

???+ preview

    === "With symbol type in ToC"

        <ul style="list-style: none;">
          <li><code class="doc-symbol doc-symbol-folder"></code> folder</li>
          <li><code class="doc-symbol doc-symbol-namespace"></code> namespace</li>
          <li><code class="doc-symbol doc-symbol-function"></code> function</li>
          <li><code class="doc-symbol doc-symbol-class"></code> Class
            <ul style="list-style: none;">
              <li><code class="doc-symbol doc-symbol-method"></code> method</li>
              <li><code class="doc-symbol doc-symbol-property"></code> property</li>
            </ul>
          </li>
        </ul>

    === "Without symbol type in ToC"

        <ul style="list-style: none;">
          <li>folder</li>
          <li>namespace</li>
          <li>function</li>
          <li>Class
            <ul style="list-style: none;">
              <li>method</li>
              <li>property</li>
            </ul>
          </li>
        </ul>
