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


## `inherited_members`

- **:octicons-package-24: Type <code><autoref identifier="list" optional>list</autoref>[<autoref identifier="str" optional>str</autoref>] |
    <autoref identifier="bool" optional>bool</autoref></code>  :material-equal: `False`{ title="default value" }**
<!-- - **:octicons-project-template-24: Template :material-null:** (N/A) -->

An explicit list of inherited members (for classes) to render.

Inherited members are always fetched from classes that are in the same namespace as the currently rendered class. Otherwise, it must be ensured that the paths to the parent is included in [paths](../index.md#paths). This is also the case for MATLAB built-in classes. 

Passing a falsy value (`no`, `false` in YAML) or an empty list (`[]`) will tell the Python handler not to render any inherited member. Passing a truthy value (`yes`, `true` in YAML) will tell the Python handler to render every inherited member.

When all inherited members are selected with `inherited_members: true`, it is possible to specify both members and inherited members in the `members` list:

```yaml
inherited_members: true
members:
- inherited_member_a
- inherited_member_b
- member_x
- member_y
```

The alternative is not supported:

```yaml
inherited_members:
- inherited_member_a
- inherited_member_b
members:
- member_x
- member_y
```

...because it would make members ordering ambiguous/unspecified.

You can render inherited members *only* by setting `inherited_members: true` (or a list of inherited members) and setting `members: false`:

```yaml
inherited_members: true
members: false
```

```yaml
inherited_members:
- inherited_member_a
- inherited_member_b
members: false
```

You can render *all declared members* and all or specific inherited members by leaving `members` as null (default):

```yaml
inherited_members:
- inherited_member_a
- inherited_member_b
# members: null  # (1)
```

1. In this case, only declared members will be subject to further filtering with [`filters`][filters] and [`docstrings`][show_if_no_docstring].

```yaml
inherited_members: true  # (1)
# members: null
```

1. In this case, both declared and inherited members will be subject to further filtering with [`filters`][filters] and [`docstrings`][show_if_no_docstring].

You can render *all declared members* and all or specific inherited members, avoiding further filtering with [`filters`][filters] and [`docstrings`][show_if_no_docstring] by setting `members: true`:

```yaml
inherited_members: true
members: true
```

```yaml
inherited_members:
- inherited_member_a
- inherited_member_b
members: true
```

The general rule is that declared or inherited members specified in lists are never filtered out.

```yaml title="in mkdocs.yml (global configuration)"
plugins:
- mkdocstrings:
    handlers:
      matlab:
        options:
          inherited_members: false
```

```md title="or in docs/some_page.md (local configuration)"
::: mymembers.ThisClass
    options:
      inherited_members: true
```

--8<-- "docs/snippets/+mymembers/mymembers.md"

!!! preview

    === "With inherited members"

        ::: mymembers.ThisClass
            options:
              inherited_members: true

    === "Without inherited members"

        ::: mymembers.ThisClass
            options:
              inherited_members: false

## `members_order`

- **:octicons-package-24: Type [`str`][] :material-equal: `"alphabetical"`{ title="default value" }**
<!-- - **:octicons-project-template-24: Template :material-null:** (N/A) -->

The members ordering to use. Possible values:

- `alphabetical`: order by the members names.
- `source`: order members as they appear in the source file.

The order applies for all members, recursively.
The order will be ignored for members that are explicitely sorted using the [`members`][] option.
**Note that members will still be grouped by category,
according to the [`group_by_category`][] option.**

```yaml title="in mkdocs.yml (global configuration)"
plugins:
- mkdocstrings:
    handlers:
      matlab:
        options:
          members_order: alphabetical
```

```md title="or in docs/some_page.md (local configuration)"
::: mymembers.ThisClass
    options:
      members_order: source
```

--8<-- "docs/snippets/+mymembers/mymembers.md"

!!! prevew

    === "With alphabetical order"

        ::: +mymembers.ThisClass
            options:
              members: true
              members_order: alphabetical

    === "With source order"

        ::: +mymembers.ThisClass
            options:
              members: true
              members_order: source