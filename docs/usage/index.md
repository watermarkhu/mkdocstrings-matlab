# Usage

## Installation

You can install this handler by installing is as a dependency

```shell
uv add mkdocstrings-matlab --group docs
```
or 

```shell
pip install mkdocstrings-matlab
```

## Configuration

The current package serves as an language extension to [mkdocstrings](https://mkdocstrings.github.io/), an auto-documentation framework that is compatible with both MkDocs and [Zensical](https://zensical.org/about/) (a continueation of [Material for MkDocs](https://squidfunk.github.io/mkdocs-material)). MkDocs uses `mkdocs.yml` for the project configuration. Zensical introduces a `zensical.toml`, but is compatible with `mkdocs.yml` as well.

For *mkdocstrings* the default will be the Python handler. You can change the default handler,
or explicitely set the MATLAB handler as default by defining the `default_handler`
configuration option of `mkdocstrings` in `mkdocs.yml` or `zensical.toml`:

=== "mkdocs.yml"

    ```yaml title="mkdocs.yml"
    plugins:
    - mkdocstrings:
        default_handler: matlab
        matlab:
            ...  # the MATLAB handler configuration
    ```
    
=== "zensical.toml"

    ```toml
    [project.plugins.mkdocstrings]
    default_handler = "matlab"
    
    [project.plugins.mkdocstrings.matlab]
    # The MATLAB handler configuration
    ```

## Injecting documentation

With the MATLAB handler installed and configured as default handler, you can inject documentation for a module, class, function, or any other MATLAB object with *mkdocstrings*' `[autodoc syntax]`, in your Markdown pages:

```md
::: path.to.object
```

If another handler was defined as default handler, you can explicitely ask for the MATLAB handler to be used when injecting documentation with the `handler` option:

```md
::: path.to.object
    handler: matlab
```
### Namespaces

Entire [namespaces](https://mathworks.com/help/matlab/matlab_oop/namespaces.html) can be fully documented by prefixing the `+` character to the namespace that is to be documented. E.g. the following namespace 

```text
+mynamespace
├── Contents.m
├── readme.md
├── myclass.m
└── +subnamespace
    └── mfunction.m
```

is documented with:

```md
::: +mynamespace
```

The docstring of the namespace is taken from either the [`Contents.m`](https://mathworks.com/help/matlab/matlab_prog/create-a-help-summary-contents-m.html) or a `readme.md` that resides at the root level of the namespace, with `Contents.m` taking precedence over `readme.md`.

Documenting a nested namespace requires only a single prefixed `+` at the start of the fully resolved path, e.g. 

```md
::: +mynamespace.subnamespace
```

### Folders

Similarly to namepaces, all contents of a folder can be fully documented by specifying the relative path of a folder with respect to the config file. E.g. the following repository

```text
src
└── module
    ├── myfunction.m
    ├── myClass.m
    ├── submodule
    │   └── myfunction.m
    └── +mynamespace
        └── namespacefunction.m
docs
└── index.md
mkdocs.yml # or
zensical.toml
```

is documented with:

```markdown
::: src/module
```

In the case above the function `module/submodule/myfunction.m` overshadows the function `module/myfunction.m` on the MATLAB path. This means that in the global namespace myfunction will always call `module/submodule/myfunction.m`, which is the function to be documented by `::: myfunction`. 

While this kind of behavior is strictly recommended against, mkdocstrings-matlab does support documenting the shadowed function by using its path. The file extension is now stricty required. 

```markdown
::: src/module/myfunction.m
```

!!! tip

    A folder identifier must strictly contain the `/` character. For a folder `foo` that is in the same directory containing `mkdocs.yml` or `zensical.toml`, use `::: ./foo`. 

!!! tip

    If `mkdocs.yml` or `zensical.toml` lives inside of a subdirectly that does not contain source code, use relative paths e.g. `../src/module`. 

!!! tip

    Sub-selecting folder members are possible with the [members](./configuration/members.md) options. 

### Global only options

Some options are **global only**, and go directly under the handler's name. See all global only options [here](./global.md).

### Global and local options

The other options can be used both globally *and* locally, under the `options` key.
For example, globally:

=== "mkdocs.yml"

    ```yaml
    plugins:
    - mkdocstrings:
        handlers:
          matlab:
            options:
              do_something: true
    ```
=== "zensical.toml"

    ```toml
    [project.plugins.mkdocstrings.handlers.matlab.options]
    do_something = true
    ```

...and locally, overriding the global configuration:

```md title="docs/some_page.md"
::: package.module.class
    options:
      do_something: false
```

These options affect how the documentation is collected from sources and rendered.
See the following tables summarizing the options, and get more details for each option
in the following pages:

- [General options](configuration/general.md): various options that do not fit in the other categories
- [Headings options](configuration/headings.md): options related to headings and the table of contents
    (or sidebar, depending on the theme used)
- [Members options](configuration/members.md): options related to filtering or ordering members
    in the generated documentation
- [Docstrings options](configuration/docstrings.md): options related to docstrings (parsing and rendering)
- [Signature options](configuration/signatures.md): options related to signatures and type annotations
