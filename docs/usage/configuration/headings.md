# Headings options

## `heading_level`

- **:octicons-package-24: Type [`int`][] :material-equal: `2`{ title="default value" }**
<!-- - **:octicons-project-template-24: Template :material-null:** (N/A) -->

The initial heading level to use.

When injecting documentation for an object,
the object itself and its members are rendered.
For each layer of objects, we increase the heading level by 1.

The initial heading level will be used for the first layer.
If you set it to 3, then headings will start with `<h3>`.

If the [heading for the root object][show_root_heading] is not shown,
then the initial heading level is used for its members.

```yaml title="in mkdocs.yml (global configuration)"
plugins:
- mkdocstrings:
    handlers:
      python:
        options:
          heading_level: 2
```

```md title="or in docs/some_page.md (local configuration)"
::: path.to.module
    options:
      heading_level: 3
```

/// admonition | Preview
    type: preview

//// tab | With level 3 and root heading
<h3><code>module</code> (3)</h3>
<p>Docstring of the module.</p>
<h4><code>ClassA</code> (4)</h4>
<p>Docstring of class A.</p>
<h4><code>ClassB</code> (4)</h4>
<p>Docstring of class B.</p>
<h5><code>method_1</code> (5)</h5>
<p>Docstring of the method.</p>
////

//// tab | With level 3, without root heading
<p>Docstring of the module.</p>
<h3><code>ClassA</code> (3)</h3>
<p>Docstring of class A.</p>
<h3><code>ClassB</code> (3)</h3>
<p>Docstring of class B.</p>
<h4><code>method_1</code> (4)</h4>
<p>Docstring of the method.</p>
////
///

