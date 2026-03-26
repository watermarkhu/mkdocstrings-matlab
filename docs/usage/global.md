# Global-only options

## `paths`

This option is used to set the [MATLAB search path](https://mathworks.com/help/matlab/matlab_env/what-is-the-matlab-search-path.html).  The MATLAB search path is a subset of all the folders in the file system. The order of folders on the search path is important.  When files with the same name appear in multiple folders on the search path,  MATLAB uses the one found in the folder nearest to the top of the search path.

Non-absolute paths are computed as relative to MkDocs configuration file. Example:

```yaml title="mkdocs.yml"
plugins:
- mkdocstrings:
    handlers:
      matlab:
        paths: [src]  # search files in the src folder
```


## `paths_recursive`

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

## `tree_sitter_logging_level`

This option controls the logging level for tree-sitter parsing. The tree-sitter parser is used to extract documentation from MATLAB source files. Adjusting this level can help with debugging parsing issues.

Possible values (from most to least verbose):

- `"TRACE"`: Very detailed logging, including all parsing steps
- `"DEBUG"`: Detailed logging for debugging
- `"INFO"`: General informational messages
- `"SUCCESS"`: Success messages only
- `"WARNING"`: Warnings and errors (default)
- `"ERROR"`: Errors only
- `"CRITICAL"`: Critical errors only

Example:

```yaml title="mkdocs.yml"
plugins:
- mkdocstrings:
    handlers:
      matlab:
        tree_sitter_logging_level: DEBUG  # show debug messages during parsing
```


## `docstring_before_properties`

- **:octicons-package-24: Type [`bool`][] :material-equal: `False`{ title="default value" }**

If `True`, docstrings for class properties must come **BEFORE** the property definition. If `False` (default), docstrings come **AFTER** the property definition.

By default, mkdocstrings-matlab expects comments to appear after property definitions:

```matlab
classdef MyClass
    properties
        Property1
            % This is the docstring for Property1 (default behavior)
        Property2
            % This is the docstring for Property2 (default behavior)
    end
end
```

When `docstring_before_properties` is set to `True`, comments must appear before the property they document:

```matlab
classdef MyClass
    properties
        % This is the docstring for Property1 (before mode)
        Property1
        % This is the docstring for Property2 (before mode)
        Property2
    end
end
```

```yaml title="in mkdocs.yml (global configuration)"
plugins:
- mkdocstrings:
    handlers:
      matlab:
        options:
          docstring_before_properties: true
```

```md title="or in docs/some_page.md (local configuration)"
::: matlab_class
    options:
      docstring_before_properties: true
```

## `docstring_before_arguments`

- **:octicons-package-24: Type [`bool`][] :material-equal: `False`{ title="default value" }**

If `True`, docstrings for function arguments must come **BEFORE** the argument definition. If `False` (default), docstrings come **AFTER** the argument definition.

By default, mkdocstrings-matlab expects comments to appear after argument definitions in `arguments` blocks:

```matlab
function result = myFunction(arg1, arg2)
    arguments
        arg1 double
            % This is the docstring for arg1 (default behavior)
        arg2 string
            % This is the docstring for arg2 (default behavior)
    end
    ...
end
```

When `docstring_before_arguments` is set to `True`, comments must appear before the argument they document:

```matlab
function result = myFunction(arg1, arg2)
    arguments
        % This is the docstring for arg1 (before mode)
        arg1 double
        % This is the docstring for arg2 (before mode)
        arg2 string
    end
    ...
end
```

```yaml title="in mkdocs.yml (global configuration)"
plugins:
- mkdocstrings:
    handlers:
      matlab:
        options:
          docstring_before_arguments: true
```

```md title="or in docs/some_page.md (local configuration)"
::: matlab_function
    options:
      docstring_before_arguments: true
```

## `docstring_before_enumerations`

- **:octicons-package-24: Type [`bool`][] :material-equal: `False`{ title="default value" }**

If `True`, docstrings for enumeration members must come **BEFORE** the enumeration definition. If `False` (default), docstrings come **AFTER** the enumeration definition.

By default, mkdocstrings-matlab expects comments to appear after enumeration member definitions:

```matlab
classdef MyEnum
    enumeration
        Member1
            % This is the docstring for Member1 (default behavior)
        Member2
            % This is the docstring for Member2 (default behavior)
    end
end
```

When `docstring_before_enumerations` is set to `True`, comments must appear before the enumeration member they document:

```matlab
classdef MyEnum
    enumeration
        % This is the docstring for Member1 (before mode)
        Member1
        % This is the docstring for Member2 (before mode)
        Member2
    end
end
```

```yaml title="in mkdocs.yml (global configuration)"
plugins:
- mkdocstrings:
    handlers:
      matlab:
        options:
          docstring_before_enumerations: true
```

```md title="or in docs/some_page.md (local configuration)"
::: matlab_enumeration
    options:
      docstring_before_enumerations: true
```
