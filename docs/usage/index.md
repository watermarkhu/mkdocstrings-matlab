# Usage

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

For *mkdocstrings* the default will be the Python handler. You can change the default handler,
or explicitely set the MATLAB handler as default by defining the `default_handler`
configuration option of `mkdocstrings` in `mkdocs.yml`:

```yaml title="mkdocs.yml"
plugins:
- mkdocstrings:
    default_handler: matlab
```

## Injecting documentation

With the MATLAB handler installed and configured as default handler,
you can inject documentation for a module, class, function, or any other MATLAB object
with *mkdocstrings*' [autodoc syntax], in your Markdown pages:

```md
::: path.to.object
```

If another handler was defined as default handler, 
you can explicitely ask for the MATLAB handler to be used when injecting documentation
with the `handler` option:

```md
::: path.to.object
    handler: matlab
```

## Configuration

When installed, the MATLAB handler becomes the default *mkdocstrings* handler.
You can configure it in `mkdocs.yml`:

```yaml title="mkdocs.yml"
plugins:
- mkdocstrings:
    handlers:
      python:
        ...  # the Python handler configuration
```

### Global-only options

Some options are **global only**, and go directly under the handler's name.



#### `paths`

This option is used to set the [MATLAB search path](https://mathworks.com/help/matlab/matlab_env/what-is-the-matlab-search-path.html). 
The MATLAB search path is a subset of all the folders in the file system.
The order of folders on the search path is important. 
When files with the same name appear in multiple folders on the search path, 
MATLAB uses the one found in the folder nearest to the top of the search path.

Non-absolute paths are computed as relative to MkDocs configuration file. Example:

```yaml title="mkdocs.yml"
plugins:
- mkdocstrings:
    handlers:
      matlab:
        paths: [src]  # search files in the src folder
```


#### `load_external_modules`

This option allows you to specify whether the handler should recursively search through the directories specified in the `paths` option. When set to `true`, the handler will look for MATLAB files in all subdirectories of the specified paths.

Example:

```yaml title="mkdocs.yml"
plugins:
- mkdocstrings:
    handlers:
      matlab:
        paths: [src]  # search files in the src folder
        paths_recursive: true  # search recursively in subfolders
```



### Global/local options

The other options can be used both globally *and* locally, under the `options` key.
For example, globally:

```yaml title="mkdocs.yml"
plugins:
- mkdocstrings:
    handlers:
      python:
        options:
          do_something: true
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

#### Options summary

::: mkdocstrings_handlers.matlab.handler.MatlabHandler.default_config
    handler: python
    options:
      show_root_heading: false
      show_root_toc_entry: false
