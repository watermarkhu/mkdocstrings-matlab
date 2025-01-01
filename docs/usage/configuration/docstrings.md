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

!!! preview

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

!!! preview


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

## `merge_constructor_into_class` and `merge_constructor_ignore_summary`

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
::: path.to.module
    options:
      merge_constructor_into_class: true
      merge_constructor_ignore_summary: true
```

??? code ":material-file-code: `Thing.m`"

    ```matlab
    --8<-- "docs/snippets/Thing.m"
    ```

!!! preview

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


