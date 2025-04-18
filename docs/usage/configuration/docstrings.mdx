---
toc_depth: 2
---

# Docstrings options

## `docstring_style`

- **:octicons-package-24: Type [`str`][] :material-equal: `"google"`{ title="default value" }**
<!-- - **:octicons-project-template-24: Template :material-null:** (N/A) -->

The docstring style to expect when parsing docstrings.

Possible values:

- `"google"`: see [Google style](../docstrings/google.md).
- `"numpy"`: see [Numpy style](../docstrings/numpy.md).
- `"sphinx"`: see [Sphinx style](../docstrings/sphinx.md).
- `None` (`null` or `~` in YAML): no style at all, parse as regular text.

```yaml title="in mkdocs.yml (global configuration)"
plugins:
- mkdocstrings:
    handlers:
      matlab:
        options:
          docstring_style: google
```

```md title="or in docs/some_page.md (local configuration)"
::: matlab_callable
    options:
      docstring_style: numpy
```

???+ preview

    Every style gets rendered the same way. Here are some docstring examples.

    === "Google"

        ```matlab
        function message = greet(name)
            % Greet someone.
            %  
            % Parameters:
            %     name: The name of the person to greet.
            % 
            % Returns:
            %     message: A greeting message.
            
            message = sprintf("Hello %s!", name)
        end
        ```

    === "Numpy"

        ```matlab
        function message = greet(name)
            % Greet someone.
            %  
            % Parameters
            % ----------
            % name
            %    The name of the person to greet.
            % 
            % Returns
            % -------
            % message
            %    A greeting message.
            
            message = sprintf("Hello %s!", name)
        end
        ```

    === "Sphinx"

        ```matlab
        function message = greet(name)
            % Greet someone.
            %  
            % :param name: The name of the person to greet.
            % :return: A greeting message.
            
            message = sprintf("Hello %s!", name)
        end
        ```

## `docstring_options`

- **:octicons-package-24: Type [`dict`][] :material-equal: `{}`{ title="default value" }**
<!-- - **:octicons-project-template-24: Template :material-null:** (N/A) -->

The options for the docstring parser.

- [Google-style options](https://mkdocstrings.github.io/griffe/docstrings/#parser-options){ .external }
- [Numpydoc-style options](https://mkdocstrings.github.io/griffe/docstrings/#parser-options_1){ .external }

The Sphinx style does not offer any option.

Most of the options in the linked pages will not have an effect to mkdocstrings-matlab, since here the objects are mocked as Python objects are docstrings are injected into the mocked objects. 

```yaml title="in mkdocs.yml (global configuration)"
plugins:
- mkdocstrings:
    handlers:
      matlab:
        options:
          docstring_options:
            warn_unknown_params: false
```

```md title="or in docs/some_page.md (local configuration)"
::: matlab_callable
    options:
      docstring_options:
        warn_unknown_params: false
```

## `docstring_section_style`

- **:octicons-package-24: Type [`str`][] :material-equal: `"table"`{ title="default value" }**
<!-- - **:octicons-project-template-24: Template :material-null:** (N/A) -->

The style used to render docstring sections.

A section is a block of text that has a special meaning in a docstring. There are sections for documenting attributes of an object, parameters of a function, exceptions raised by a function, the return value of a function, etc.

Sections are parsed as structured data and can therefore be rendered in different ways. Possible values:

- `"table"`: a simple table, usually with type, name and description columns
- `"list"`: a simple list, akin to what you get with the [ReadTheDocs Sphinx theme]{ .external }
- `"spacy"`: a poor implementation of the amazing tables in [Spacy's documentation]{ .external }

```yaml title="in mkdocs.yml (global configuration)"
plugins:
- mkdocstrings:
    handlers:
      matlab:
        options:
          docstring_section_style: table
```

```md title="or in docs/some_page.md (local configuration)"
::: matlab_callable
    options:
      docstring_section_style: list
```

???+ preview


    === "Table"

        Tables work well when you have lots of items with short names, type annotations, descriptions, etc.. With longer strings, the columns risk getting squished horizontally. In that case, the Spacy tables can help.

        **Parameters:**

        **Type**   | **Name**    | **Description**          | **Default**
        ---------- | ----------- | ------------------------ | -----------
        [`int`][]  | `threshold` | Threshold for something. | *required*
        [`bool`][] | `flag`      | Enable something.        | `False`

        **Other Parameters:**

        **Type**   | **Name**    | **Description**          | **Default**
        ---------- | ----------- | ------------------------ | -----------
        <code><autoref identifier="list" optional>list</autoref>[<autoref identifier="int" optional>int</autoref> \| <autoref identifier="float" optional>float</autoref>]</code> | `gravity_forces` | Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. | *required*
        <code><autoref identifier="VacuumType" optional>VacuumType</autoref> \| <autoref identifier="typing.Literal" optional>Literal</autoref>["regular"]</code> | `vacuum_type` | Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. | `VacuumType.PLASMA`

    === "List"

        Lists work well whatever the length of names, type annotations, descriptions, etc.

        **Parameters:**

        - `threshold` ([`int`][]) &mdash; Threshold for something.
        - `flag` ([`bool`][]) &mdash; Enable something.

        **Other Parameters:**

        - `gravity_forces` (<code><autoref identifier="list" optional>list</autoref>[<autoref identifier="int" optional>int</autoref> \| <autoref identifier="float" optional>float</autoref>]</code>) &mdash; Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        - `vacuum_type` (<code><autoref identifier="VacuumType" optional>VacuumType</autoref> \| <autoref identifier="typing.Literal" optional>Literal</autoref>["regular"]</code>) &mdash; Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

    === "Spacy"

        Spacy tables work better than regular tables with longer names, type annotations, descriptions, etc., by reserving more horizontal space on the second column.

        **Parameters:**

        **Name**    | **Description**
        ----------- | ---------------
        `threshold` | <span style="display: inline-block; min-width: 400px;">Threshold for something.</span><br>**TYPE:** [`int`][] <span style="float: right;"><b>DEFAULT:</b> <i>required</i></span>
        `flag`      | <span style="display: inline-block; min-width: 400px;">Enable something.</span><br>**TYPE:** [`bool`][] <span style="float: right;"><b>DEFAULT:</b> <code>False</code></span>

        **Other Parameters:**

        **Name**    | **Description**
        ----------- | ---------------
        `gravity_forces` | Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.<br>**TYPE:** <code><autoref identifier="list" optional>list</autoref>[<autoref identifier="int" optional>int</autoref> \| <autoref identifier="float" optional>float</autoref>]</code> <span style="float: right;"><b>DEFAULT:</b> <i>required</i></span>
        `vacuum_type` | Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.<br>**TYPE:**<code><autoref identifier="VacuumType" optional>VacuumType</autoref> \| <autoref identifier="typing.Literal" optional>Literal</autoref>["regular"]</code> <span style="float: right;"><b>DEFAULT:</b> <code>VacuumType.PLASMA</code></span>

## `parse_arguments`

- **:octicons-package-24: Type [`bool`][] :material-equal: `True`{ title="default value" }**

Whether to load inputs and output parameters based on argument validation blocks.

Similarly to Python, MATLAB is by default not a typed language. Function and method arguments are dynamically typed, in most cases. This provides flexibility, but is generally bad behavior if the code is meant for production or is intended to be exposed as an API. 

In MATLAB R2019b the concept of [Argument Definitions](https://mathworks.com/help/matlab/input-and-output-arguments.html) was introduced. Within an [arguments](https://mathworks.com/help/matlab/ref/arguments.html) block, the type, size, or other aspects of the inputs (and outputs since R2022b) can be verified. 

```matlab
function z = mySharedFunction(x,y,NameValueArgs)
   arguments
      x (1,1) double     % scalar
      y double {mustBeVector,mustBePositive} 
      NameValueArgs.A string
      NameValueArgs.B string = "default"
   end 
...
end
```

The mkdocstrings-matlab plugin is able to parse the argument blocks and extract the type and default information, and any comment after each Argument Definition will be parsed as the argument docstring. If if `parse_arguments` is enabled, sections will be rendered for the parameters, name-value pairs and the return arguments of functions and methods. These sections can be individually toggled with [`show_docstring_input_arguments`][], [`show_docstring_name_value_arguments`][] and [`show_docstring_output_arguments`][].


```yaml title="in mkdocs.yml (global configuration)"
plugins:
- mkdocstrings:
    handlers:
      matlab:
        options:
          parse_arguments: true
```

```md title="or in docs/some_page.md (local configuration)"
::: mynamespace.typed_function
    options:
      parse_arguments: true
```

--8<-- "docs/snippets/+mynamespace/mynamespace.md"

???+ preview "Preview: Cross-references"

    === "Parse argument validation"

        ```markdown
        ::: mynamespace.typed_function
            options:
              parse_arguments: true
        ```

        ::: mynamespace.typed_function
            options:
              parse_arguments: true

    === "Don't parse argument validation"

        ```markdown
        ::: mynamespace.typed_function
            options:
              parse_arguments: false
        ```

        ::: mynamespace.typed_function
            options:
              parse_arguments: false

!!! note

    Prior to MATLAB R2019b, the functionality of the arguments blocks was most commonly achieved through [`inputParser`](https://mathworks.com/help/matlab/ref/inputparser.html). The validations created with `inputParser` will not be parsed by mkdocstrings-matlab, since it does not have a strict syntax as opposed to Argument Definitions. 

## `merge_constructor_into_class`

- **:octicons-package-24: Type [`bool`][] :material-equal: `False`{ title="default value" }**
<!-- - **:octicons-project-template-24: Template :material-null:** (N/A) -->

Whether to merge the constructor method into the class' signature and docstring.

By default, only the class name is rendered in headings. When merging, the constructor method parameters are added after the class name, like a signature, and the constructor method docstring is appended to the class' docstring. This option is well used in combination with the `merge_constructor_ignore_summary` option, to discard the first line of the constructor docstring which is not often useful.

```yaml title="in mkdocs.yml (global configuration)"
plugins:
- mkdocstrings:
    handlers:
      matlab:
        options:
          merge_constructor_into_class: true
          merge_constructor_ignore_summary: true
```

```md title="or in docs/some_page.md (local configuration)"
::: matlab_callable
    options:
      merge_constructor_into_class: true
      merge_constructor_ignore_summary: true
```

??? code ":material-file-code: `Thing.m`"

    ```matlab
    --8<-- "docs/snippets/Thing.m"
    ```

???+ preview

    === "Merged, summary discarded"

        ```markdown
        ::: Thing
            options:
              merge_constructor_into_class: true
              merge_constructor_ignore_summary: true
        ```

        ::: Thing
            options:
              merge_constructor_into_class: true
              merge_constructor_ignore_summary: true

    === "Merged, summary kept"

        ```markdown
        ::: Thing
            options:
              merge_constructor_into_class: true
              merge_constructor_ignore_summary: false
        ```

        ::: Thing
            options:
              merge_constructor_into_class: true
              merge_constructor_ignore_summary: false

    === "Unmerged"

        ```markdown
        ::: Thing
            options:
              merge_constructor_into_class: false
        ```
        
        ::: Thing
            options:
              merge_constructor_into_class: false



## `show_if_no_docstring`

- **:octicons-package-24: Type [`bool`][] :material-equal: `False`{ title="default value" }**
<!-- - **:octicons-project-template-24: Template :material-null:** (N/A) -->

Show the object heading even if it has no docstring or children with docstrings.

Without an explicit list of [`members`][], members are selected based on [`filters`][], and then filtered again to keep only those with docstrings. Checking if a member has a docstring is done recursively: if at least one of its direct or indirect members (lower in the tree) has a docstring, the member is rendered. If the member does not have a docstring, and none of its members have a docstring, it is excluded.

With this option you can tell the Python handler to skip the docstring check.

```yaml title="in mkdocs.yml (global configuration)"
plugins:
- mkdocstrings:
    handlers:
      matlab:
        options:
          show_if_no_docstring: false
```

```md title="or in docs/some_page.md (local configuration)"
::: +undocumented
    options:
      show_if_no_docstring: true
```

--8<-- "docs/snippets/+undocumented/undocumented.md"

???+ preview

    === "Show"

        ```markdown
        ::: +undocumented
            options:
              show_if_no_docstring: true
        ```

        ::: +undocumented
            options:
              show_if_no_docstring: true

    === "Don't show"

        ```markdown
        ::: +undocumented
            options:
              show_if_no_docstring: false
        ```
        
        ::: +undocumented
            options:
              show_if_no_docstring: false

## `show_docstring_properties`

- **:octicons-package-24: Type [`bool`][] :material-equal: `True`{ title="default value" }**
<!-- - **:octicons-project-template-24: Template :material-null:** (N/A) -->

Whether to render the "Properties" sections of docstrings.

```yaml title="in mkdocs.yml (global configuration)"
plugins:
- mkdocstrings:
    handlers:
      matlab:
        options:
          show_docstring_properties: true
```

```md title="or in docs/some_page.md (local configuration)"
::: matlab_callable
    options:
      show_docstring_properties: false
```

??? code ":material-file-code: `Class.m`"

    ```matlab
    --8<-- "docs/snippets/Class.m"
    ```

???+ preview

    === "With properties"

        ```markdown
        ::: Class
            options:
              show_docstring_properties: true
        ```

        ::: Class
            options:
              show_docstring_properties: true

    === "Without properties"

        ```markdown
        ::: Class
            options:
              show_docstring_properties: false
        ```

        ::: Class
            options:
              show_docstring_properties: false

## `show_docstring_functions`

- **:octicons-package-24: Type [`bool`][] :material-equal: `True`{ title="default value" }**
<!-- - **:octicons-project-template-24: Template :material-null:** (N/A) -->

Whether to render the "Functions" or "Methods" sections of docstrings.

```yaml title="in mkdocs.yml (global configuration)"
plugins:
- mkdocstrings:
    handlers:
      python:
        options:
          show_docstring_functions: true
```

```md title="or in docs/some_page.md (local configuration)"
::: path.to.module
    options:
      show_docstring_functions: false
```

--8<-- "docs/snippets/+module/module.md"

???+ preview

    === "With methods"

        ```markdown
        ::: module.aClass
            options:
              show_docstring_functions: true
        ```

        ::: module.aClass
            options:
              show_docstring_functions: true

    === "Without methods"

        ```markdown
        ::: module.aClass
            options:
              show_docstring_functions: false
        ```

        ::: module.aClass
            options:
              show_docstring_functions: false

    === "With functions"

        ```markdown
        ::: +module
            options:
              show_docstring_functions: true
              members: false
        ```

        ::: +module
            options:
              show_docstring_functions: true
              members: false

    === "Without functions"

        ```markdown
        ::: +module
            options:
              show_docstring_functions: false
              members: false
        ```

        ::: +module
            options:
              show_docstring_functions: false
              members: false

## `show_docstring_classes`

- **:octicons-package-24: Type [`bool`][] :material-equal: `True`{ title="default value" }**
<!-- - **:octicons-project-template-24: Template :material-null:** (N/A) -->

Whether to render the "Classes" sections of docstrings.

```yaml title="in mkdocs.yml (global configuration)"
plugins:
- mkdocstrings:
    handlers:
      matlab:
        options:
          show_docstring_classes: true
```

```md title="or in docs/some_page.md (local configuration)"
::: +matlab_namespace
    options:
      show_docstring_classes: false
```

--8<-- "docs/snippets/+module/module.md"

???+ preview

    === "With classes"

        ```markdown
        ::: +module
            options:
              show_docstring_classes: true
              members: false
        ```

        ::: +module
            options:
              show_docstring_classes: true
              members: false

    === "Without classes"

        ```markdown
        ::: +module
            options:
              show_docstring_classes: false
              members: false
        ```

        ::: +module
            options:
              show_docstring_classes: false
              members: false


## `show_docstring_namespaces`

- **:octicons-package-24: Type [`bool`][] :material-equal: `True`{ title="default value" }**
<!-- - **:octicons-project-template-24: Template :material-null:** (N/A) -->

Whether to render the "Namespaces" sections of docstrings.

```yaml title="in mkdocs.yml (global configuration)"
plugins:
- mkdocstrings:
    handlers:
      matlab:
        options:
          show_docstring_namespaces: true
```

```md title="or in docs/some_page.md (local configuration)"
::: +matlab_namespace
    options:
      show_docstring_namespaces: false
```

--8<-- "docs/snippets/+module/module.md"

???+ preview

    === "With namespaces"

        ```markdown
        ::: +module
            options:
              show_docstring_namespaces: true
              members: false
        ```

        ::: +module
            options:
              show_docstring_namespaces: true
              members: false

    === "Without namespaces"

        ```markdown
        ::: +module
            options:
              show_docstring_namespaces: false
              members: false
        ```

        ::: +module
            options:
              show_docstring_namespaces: false
              members: false

## `show_docstring_description`

- **:octicons-package-24: Type [`bool`][] :material-equal: `True`{ title="default value" }**
<!-- - **:octicons-project-template-24: Template :material-null:** (N/A) -->

Whether to render the textual blocks (including admonitions) of docstrings.

```yaml title="in mkdocs.yml (global configuration)"
plugins:
- mkdocstrings:
    handlers:
      matlab:
        options:
          show_docstring_description: true
```

```md title="or in docs/some_page.md (local configuration)"
::: matlab_callable
    options:
      show_docstring_description: false
```

??? code ":material-file-code: `Class.m`"

    ```matlab
    --8<-- "docs/snippets/Class.m"
    ```

???+ preview

    === "With description blocks"

        ```markdown
        ::: Class
            options:
              show_docstring_description: true
        ```

        ::: Class
            options:
              show_docstring_description: true

    === "Without description blocks"

        ```markdown
        ::: Class
            options:
              show_docstring_description: false
        ```

        ::: Class
            options:
              show_docstring_description: false

## `show_docstring_examples`

- **:octicons-package-24: Type [`bool`][] :material-equal: `True`{ title="default value" }**
<!-- - **:octicons-project-template-24: Template :material-null:** (N/A) -->

Whether to render the "Examples" sections of docstrings.

```yaml title="in mkdocs.yml (global configuration)"
plugins:
- mkdocstrings:
    handlers:
      matlab:
        options:
          show_docstring_examples: true
```

```md title="or in docs/some_page.md (local configuration)"
::: matlab_callable
    options:
      show_docstring_examples: false
```

??? code ":material-file-code: `print_hello.m`"

    ```matlab
    --8<-- "docs/snippets/print_hello.m"
    ```

???+ preview

    === "With examples"
        
        ```markdown
        ::: print_hello
            options:
              show_docstring_examples: true
        ```

        ::: print_hello
            options:
              show_docstring_examples: true

    === "Without examples"

        ```markdown
        ::: print_hello
            options:
              show_docstring_examples: false
        ```

        ::: print_hello
            options:
              show_docstring_examples: false

## `show_docstring_input_arguments`

- **:octicons-package-24: Type [`bool`][] :material-equal: `True`{ title="default value" }**
<!-- - **:octicons-project-template-24: Template :material-null:** (N/A) -->

Whether to render the "Parameters" sections of docstrings. The accepted title headings are `inputs` or `input arguments` (case-insensitive). 

```yaml title="in mkdocs.yml (global configuration)"
plugins:
- mkdocstrings:
    handlers:
      matlab:
        options:
          show_docstring_input_arguments: true
```

```md title="or in docs/some_page.md (local configuration)"
::: matlab_callable
    options:
      show_docstring_input_arguments: false
```

??? code ":material-file-code: `do_something.m`"

    ```matlab
    --8<-- "docs/snippets/do_something.m"
    ```

???+ preview

    === "With parameters"

        ```markdown
        ::: do_something
            options:
              show_docstring_input_arguments: true
        ```
        
        ::: do_something
            options:
              show_docstring_input_arguments: true

    === "Without parameters"

        ```markdown
        ::: do_something
            options:
              show_docstring_input_arguments: false
        ```

        ::: do_something
            options:
              show_docstring_input_arguments: false

!!! warning

    If a `Input arguments` section is provided in the docstring, the description here will overule the parsed values from the argument validation block (see [`parse_arguments`][]).

## `show_docstring_name_value_arguments`

- **:octicons-package-24: Type [`bool`][] :material-equal: `True`{ title="default value" }**
<!-- - **:octicons-project-template-24: Template :material-null:** (N/A) -->

Whether to render the "Name-value pairs" sections of docstrings. The accepted title headings are `name-value pairs` or `name-value arguments` (case-insensitive). 

```yaml title="in mkdocs.yml (global configuration)"
plugins:
- mkdocstrings:
    handlers:
      matlab:
        options:
          show_docstring_name_value_arguments: true
```

```md title="or in docs/some_page.md (local configuration)"
::: matlab_callable
    options:
      show_docstring_name_value_arguments: false
```

??? code ":material-file-code: `do_varargin.m`"

    ```matlab
    --8<-- "docs/snippets/do_varargin.m"
    ```

???+ preview

    === "With parameters"

        ```markdown
        ::: do_varargin
            options:
              show_docstring_name_value_arguments: true
        ```
        
        ::: do_varargin
            options:
              show_docstring_name_value_arguments: true

    === "Without parameters"

        ```markdown
        ::: do_varargin
            options:
              show_docstring_name_value_arguments: false
        ```

        ::: do_varargin
            options:
              show_docstring_name_value_arguments: false

!!! warning

    If a `Name-value arguments` section is provided in the docstring, the description here will overule the parsed values from the argument validation block (see [`parse_arguments`][]).

## `show_docstring_output_arguments`

- **:octicons-package-24: Type [`bool`][] :material-equal: `True`{ title="default value" }**
<!-- - **:octicons-project-template-24: Template :material-null:** (N/A) -->

Whether to render the "Returns" sections of docstrings. The accepted title headings are `outputs` or `output arguments` (case-insensitive). 

```yaml title="in mkdocs.yml (global configuration)"
plugins:
- mkdocstrings:
    handlers:
      matlab:
        options:
          show_docstring_output_arguments: true
```

```md title="or in docs/some_page.md (local configuration)"
::: matlab_callable
    options:
      show_docstring_output_arguments: false
```

??? code ":material-file-code: `do_output.m`"

    ```matlab
    --8<-- "docs/snippets/do_output.m"
    ```

???+ preview

    === "With parameters"

        ```markdown
        ::: do_output
            options:
              show_docstring_output_arguments: true
        ```
        
        ::: do_output
            options:
              show_docstring_output_arguments: true

    === "Without parameters"

        ```markdown
        ::: do_output
            options:
              show_docstring_output_arguments: false
        ```

        ::: do_output
            options:
              show_docstring_output_arguments: false

!!! warning

    If a `Output arguments` section is provided in the docstring, the description here will overule the parsed values from the argument validation block (see [`parse_arguments`][]).
