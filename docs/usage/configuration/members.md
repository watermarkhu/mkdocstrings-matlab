# Members options

## `members`

- **:octicons-package-24: Type <code><autoref identifier="list" optional>list</autoref>[<autoref identifier="str" optional>str</autoref>] |
    <autoref identifier="bool" optional>bool</autoref> | None</code>  :material-equal: `None`{ title="default value" }**
<!-- - **:octicons-project-template-24: Template :material-null:** (N/A) -->

An explicit list of members to render.

Only members declared in this list will be rendered. A member without a docstring will still be rendered, even if [`show_if_no_docstring`][] is set to false.

The members will be rendered in the specified order, regardless of the value of [`members_order`][]. **Note that members will still be grouped by category, according to the [`group_by_category`][] option.**

Passing a falsy value (`no`, `false` in YAML) or an empty list (`[]`) will tell the Python handler not to render any member. Passing a truthy value (`yes`, `true` in YAML) will tell the Python handler to render every member.

Any given value, except for an explicit `None` (`null` in YAML) will tell the handler to ignore [`filters`][] for the object's members. Filters will still be applied to the next layers of members (grand-children).

```yaml title="in mkdocs.yml (global configuration)"
plugins:
- mkdocstrings:
    handlers:
      matlab:
        options:
          members:
          - hello  # (1)
```

1. :warning: Most of the time it won't make sense to use this option at the global level.

```md title="or in docs/some_page.md (local configuration)"
::: +mymembers
    options:
      members:
      - ThisClass
      - this_function
```

--8<-- "docs/snippets/+mymembers/mymembers.md"

!!! prevew

    === "With `members: true`"

        ::: +mymembers
            options:
              members: true

    === "With `members: false` or `members: []`"

        ::: +mymembers
            options:
              members: false

    === "With `members: [ThisClass]`"

        ::: +mymembers
            options:
              members: [ThisClass]


!!! info

    The default behavior (with unspecified `members` or `members: null`) is to use [`filters`][].
