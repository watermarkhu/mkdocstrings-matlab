# This module implements rendering utilities.

from __future__ import annotations

import random
import re
import string
import sys
from contextlib import suppress
from dataclasses import replace
from re import Pattern
from typing import TYPE_CHECKING, Any, Callable, ClassVar, Literal

from griffe import (
    AliasResolutionError,
    CyclicAliasError,
    Docstring,
    DocstringAttribute,
    DocstringClass,
    DocstringFunction,
    DocstringModule,
    DocstringSection,
    DocstringSectionAttributes,
    DocstringSectionClasses,
    DocstringSectionFunctions,
    DocstringSectionModules,
    DocstringSectionText,
)
from griffe._internal.docstrings.models import (
    DocstringParameter,
    DocstringReturn,
    DocstringSectionOtherParameters,
    DocstringSectionParameters,
    DocstringSectionReturns,
)
from griffe._internal.docstrings.parsers import DocstringStyle, parse
from jinja2 import pass_context
from markupsafe import Markup
from maxx.enums import ArgumentKind
from maxx.objects import (
    Alias,
    Class,
    Function,
    Namespace,
    Object,
    Property,
)
from mkdocs_autorefs import AutorefsHookInterface
from mkdocstrings import get_logger

if TYPE_CHECKING:
    from collections.abc import Iterator, Sequence

    from jinja2.runtime import Context
    from mkdocstrings import CollectorItem

_logger = get_logger(__name__)


def _sort_key_alphabetical(item: CollectorItem) -> str:
    """
    Sort key function to order items alphabetically by name.

    Args:
        item: The collector item to get sort key for.

    Returns:
        A string representing the sort key (the item's name).
    """
    # `chr(sys.maxunicode)` is a string that contains the final unicode character,
    # so if `name` isn't found on the object, the item will go to the end of the list.
    return item.name or chr(sys.maxunicode)


def _sort_key_source(item: CollectorItem) -> float:
    """
    Sort key function to order items by their position in the source file.

    Args:
        item: The collector item to get sort key for.

    Returns:
        A float representing the line number of the item in the source file.
    """
    # If `lineno` is none, the item will go to the end of the list.
    return item.lineno if item.lineno is not None else float("inf")


Order = Literal["alphabetical", "source"]
"""Ordering methods.

- `alphabetical`: order members alphabetically;
- `source`: order members as they appear in the source file.
"""

_order_map: dict[str, Callable[[Object | Alias], str | float]] = {
    "alphabetical": _sort_key_alphabetical,
    "source": _sort_key_source,
}


class _StashCrossRefFilter:
    stash: ClassVar[dict[str, str]] = {}

    @staticmethod
    def _gen_key(length: int) -> str:
        return "_" + "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(max(1, length - 1))
        )  # noqa: S311

    def _gen_stash_key(self, length: int) -> str:
        key = self._gen_key(length)
        while key in self.stash:
            key = self._gen_key(length)
        return key

    def __call__(self, crossref: str, *, length: int) -> str:
        key = self._gen_stash_key(length)
        self.stash[key] = crossref
        return key


do_stash_crossref = _StashCrossRefFilter()
"""Filter to stash cross-references (and restore them after formatting and highlighting)."""


@pass_context
def do_format_signature(
    context: Context,
    callable_path: Markup,
    function: Function,
    line_length: int,
    *,
    annotations: bool | None = None,
    crossrefs: bool = False,  # noqa: ARG001
) -> str:
    """Format a signature.

    Parameters:
        context: Jinja context, passed automatically.
        callable_path: The path of the callable we render the signature of.
        function: The function we render the signature of.
        line_length: The line length.
        annotations: Whether to show type annotations.
        crossrefs: Whether to cross-reference types in the signature.

    Returns:
        The same code, formatted.
    """
    env = context.environment
    template = env.get_template("signature.html.jinja")

    if annotations is None:
        new_context = context.parent
    else:
        new_context = dict(context.parent)
        new_context["config"] = replace(new_context["config"], show_signature_types=annotations)

    signature = template.render(new_context, function=function, signature=True)
    signature = str(
        env.filters["highlight"](
            Markup.escape(signature),
            language="matlab",
            inline=False,
            classes=["doc-signature"],
            linenums=False,
        ),
    )

    if stash := env.filters["stash_crossref"].stash:
        for key, value in stash.items():
            signature = re.sub(rf"\b{key}\b", value, signature)
        stash.clear()

    return signature


@pass_context
def do_format_arguments(
    context: Context,
    section_kind: str,
    section: DocstringSectionParameters | DocstringSectionOtherParameters | DocstringSectionReturns,
    *,
    crossrefs: bool = False,
) -> str:
    env = context.environment

    match str(section_kind).strip():
        case "parameters":
            template = env.get_template("docstring/input_arguments.html.jinja")
        case "other parameters":
            template = env.get_template("docstring/name_value_arguments.html.jinja")
        case "returns":
            template = env.get_template("docstring/output_arguments.html.jinja")
        case _:
            raise ValueError(f"Unknown section kind: {section_kind}")

    html = template.render(context.parent, section=section)

    if stash := env.filters["stash_crossref"].stash:
        for key, value in stash.items():
            html = re.sub(rf"\b{key}\b", value, html)
        stash.clear()

    return html


@pass_context
def do_format_property(
    context: Context,
    property_path: Markup,
    property: Property,
    line_length: int,
    *,
    crossrefs: bool = False,  # noqa: ARG001
) -> str:
    """Format an property.

    Parameters:
        context: Jinja context, passed automatically.
        property_path: The path of the callable we render the signature of.
        property: The property we render the signature of.
        line_length: The line length.
        crossrefs: Whether to cross-reference types in the signature.

    Returns:
        The same code, formatted.
    """
    env = context.environment
    template = env.get_template("expression.html.jinja")
    annotations = context.parent["config"].show_signature_types

    signature = str(property_path).strip()
    if annotations and property.type:
        annotation = template.render(
            context.parent,
            expression=property.type,
            signature=True,
            backlink_type="returned-by",
        )
        signature += f": {annotation}"
    if property.default:
        value = template.render(
            context.parent,
            expression=property.default,
            signature=True,
            backlink_type="used-by",
        )
        signature += f" = {value}"

    signature = str(
        env.filters["highlight"](
            Markup.escape(signature),
            language="python",
            inline=False,
            classes=["doc-signature"],
            linenums=False,
        ),
    )

    if stash := env.filters["stash_crossref"].stash:
        for key, value in stash.items():
            signature = re.sub(rf"\b{key}\b", value, signature)
        stash.clear()

    return signature


def do_order_members(
    members: Sequence[Object | Alias],
    order: Order | list[Order],
    members_list: bool | list[str] | None,
) -> Sequence[Object | Alias]:
    """Order members given an ordering method.

    Parameters:
        members: The members to order.
        order: The ordering method.
        members_list: An optional member list (manual ordering).

    Returns:
        The same members, ordered.
    """
    if isinstance(members_list, list) and members_list:
        sorted_members = []
        members_dict = {member.name: member for member in members}
        for name in members_list:
            if name in members_dict:
                sorted_members.append(members_dict[name])
        return sorted_members
    if isinstance(order, str):
        order = [order]
    for method in order:
        with suppress(ValueError):
            return sorted(members, key=_order_map[method])
    return members


def _keep_object(name: str, filters: Sequence[tuple[Pattern, bool]]) -> bool:
    """
    Determine if an object should be kept based on filter patterns.

    Args:
        name: The name of the object.
        filters: A sequence of tuple pairs of (pattern, exclude_flag).

    Returns:
        True if the object should be kept, False otherwise.
    """
    keep = None
    rules = set()
    for regex, exclude in filters:
        rules.add(exclude)
        if regex.search(name):
            keep = not exclude
    if keep is None:
        # When we only include stuff, no match = reject.
        # When we only exclude stuff, or include and exclude stuff, no match = keep.
        return rules != {False}
    return keep


def _parents(obj: Alias) -> set[str]:
    """
    Get the full set of parent paths for an object.

    This function collects all parent paths in the inheritance hierarchy
    including paths for both direct parents and their alias targets.

    Args:
        obj: The alias object to get parents for.

    Returns:
        A set of parent path strings.
    """
    parent: Object | Alias = obj.parent  # type: ignore[assignment]
    parents = {parent.path}
    while parent.parent:
        parent = parent.parent
        parents.add(parent.path)
    return parents


def _remove_cycles(objects: list[Object | Alias]) -> Iterator[Object | Alias]:
    """
    Filter objects to remove those that create cycles in the inheritance graph.

    Args:
        objects: List of objects to check for cycles.

    Returns:
        An iterator yielding objects that don't create inheritance cycles.
    """
    suppress_errors = suppress(AliasResolutionError, CyclicAliasError)
    for obj in objects:
        if obj.is_alias:
            with suppress_errors:
                if obj.parent and obj.path in _parents(obj):  # type: ignore[arg-type,union-attr]
                    continue
        yield obj


def do_filter_objects(
    objects_dictionary: dict[str, Object | Alias],
    *,
    filters: Sequence[tuple[Pattern, bool]] | None = None,
    members_list: bool | list[str] | None = None,
    inherited_members: bool | list[str] = False,
    private_members: bool | list[str] = False,
    hidden_members: bool | list[str] = False,
    keep_no_docstrings: bool = True,
) -> list[Object | Alias]:
    """Filter a dictionary of objects based on their docstrings.

    Parameters:
        objects_dictionary: The dictionary of objects.
        filters: Filters to apply, based on members' names.
            Each element is a tuple: a pattern, and a boolean indicating whether
            to reject the object if the pattern matches.
        members_list: An optional, explicit list of members to keep.
            When given and empty, return an empty list.
            When given and not empty, ignore filters and docstrings presence/absence.
        inherited_members: Whether to keep inherited members or exclude them.
        private_members: Whether to keep private members or exclude them.
        hidden_members: Whether to keep hidden members or exclude them.
        keep_no_docstrings: Whether to keep objects with no/empty docstrings (recursive check).

    Returns:
        A list of objects.
    """
    inherited_members_specified = False
    if inherited_members is True:
        # Include all inherited members.
        objects = list(objects_dictionary.values())
    elif inherited_members is False:
        # Include no inherited members.
        objects = [obj for obj in objects_dictionary.values() if not obj.inherited]
    else:
        # Include specific inherited members.
        inherited_members_specified = True
        objects = [
            obj
            for obj in objects_dictionary.values()
            if not obj.inherited or obj.name in set(inherited_members)
        ]

    if isinstance(private_members, bool) and not private_members:
        objects = [obj for obj in objects if not obj.is_private]
    elif isinstance(private_members, list):
        objects = [
            obj
            for obj in objects
            if not obj.is_private or (obj.is_private and obj.name in private_members)
        ]

    if isinstance(hidden_members, bool) and not hidden_members:
        objects = [obj for obj in objects if not obj.is_hidden]
    elif isinstance(hidden_members, list):
        objects = [
            obj
            for obj in objects
            if not obj.is_hidden or (obj.is_hidden and obj.name in hidden_members)
        ]

    if members_list is True:
        # Return all pre-selected members.
        return objects

    if members_list is False or members_list == []:
        # Return selected inherited members, if any.
        return [obj for obj in objects if obj.inherited]

    if members_list is not None:
        # Return selected members (keeping any pre-selected inherited members).
        return [
            obj
            for obj in objects
            if obj.name in set(members_list) or (inherited_members_specified and obj.inherited)
        ]

    # Use filters and docstrings.
    if filters:
        objects = [
            obj
            for obj in objects
            if _keep_object(obj.name, filters) or (inherited_members_specified and obj.inherited)
        ]
    if not keep_no_docstrings:
        objects = [
            obj
            for obj in objects
            if obj.has_docstring or (inherited_members_specified and obj.inherited)
        ]

    # Prevent infinite recursion.
    if objects:
        objects = list(_remove_cycles(objects))

    return objects


def do_get_template(obj: Object) -> str:
    """Get the template name used to render an object.

    Parameters:
        env: The Jinja environment, passed automatically.
        obj: A Griffe object, or a template name.

    Returns:
        A template name.
    """
    name = obj
    if isinstance(obj, (Alias, Object)):
        extra_data = getattr(obj, "extra", {}).get("mkdocstrings", {})
        if name := extra_data.get("template", ""):
            return name
        name = obj.kind.value
    return f"{name}.html.jinja"


@pass_context
def do_as_properties_section(
    context: Context,  # noqa: ARG001
    properties: Sequence[Property],
    *,
    check_public: bool = True,
) -> DocstringSectionAttributes:
    """Build an properties section from a list of properties.

    Parameters:
        properties: The properties to build the section from.
        check_public: Whether to check if the property is public.

    Returns:
        An properties docstring section (attributes in Python)
    """

    def _parse_docstring_summary(property: Property) -> str:
        if property.docstring is None:
            return ""
        line = property.docstring.value.split("\n", 1)[0]
        if ":" in line and property.docstring.parser_options.get(
            "returns_type_in_property_summary", False
        ):
            _, line = line.split(":", 1)
        return line

    return DocstringSectionAttributes(
        [
            DocstringAttribute(
                name=property.name,
                description=_parse_docstring_summary(property),
                annotation=str(property.type),
                value=property.default,  # type: ignore[arg-type]
            )
            for property in properties
            if not check_public or not property.is_private
        ],
    )


@pass_context
def do_as_functions_section(
    context: Context,
    functions: Sequence[Function],
    *,
    check_public: bool = True,
) -> DocstringSectionFunctions:
    """Build a functions section from a list of functions.

    Parameters:
        functions: The functions to build the section from.
        check_public: Whether to check if the function is public.

    Returns:
        A functions docstring section.
    """
    keep_constructor_method = not context.parent["config"].merge_constructor_into_class
    return DocstringSectionFunctions(
        [
            DocstringFunction(
                name=function.name,
                description=function.docstring.value.split("\n", 1)[0]
                if function.docstring
                else "",
            )
            for function in functions
            if (not check_public or not function.is_private)
            and (
                keep_constructor_method
                or not function.parent
                or not function.parent.is_class
                or function.name != function.parent.name
            )
        ],
    )


@pass_context
def do_as_classes_section(
    context: Context,  # noqa: ARG001
    classes: Sequence[Class],
    *,
    check_public: bool = True,
) -> DocstringSectionClasses:
    """Build a classes section from a list of classes.

    Parameters:
        classes: The classes to build the section from.
        check_public: Whether to check if the class is public.

    Returns:
        A classes docstring section.
    """
    return DocstringSectionClasses(
        [
            DocstringClass(
                name=cls.name,
                description=cls.docstring.value.split("\n", 1)[0] if cls.docstring else "",
            )
            for cls in classes
            if not check_public or not cls.is_private
        ],
    )


@pass_context
def do_as_namespaces_section(
    context: Context,  # noqa: ARG001
    namespaces: Sequence[Namespace],
    *,
    check_public: bool = True,
) -> DocstringSectionModules:
    """Build a namespaces section from a list of namespaces.

    Parameters:
        namespaces: The namespaces to build the section from.
        check_public: Whether to check if the namespace is public.

    Returns:
        A namespaces docstring section. (modules in Python)
    """
    return DocstringSectionModules(
        [
            DocstringModule(
                name=namespace.name,
                description=namespace.docstring.value.split("\n", 1)[0]
                if namespace.docstring
                else "",
            )
            for namespace in namespaces
            if not check_public or not namespace.is_internal
        ],
    )


def do_parse_docstring(
    docstring: Docstring | None,
    docstring_style: DocstringStyle,
    docstring_options: dict[str, Any] | None,
) -> list[DocstringSection]:
    if docstring is None:
        return []
    options = docstring_options or {}
    return parse(docstring, docstring_style, **options)


def do_function_docstring(
    function: Function,
    parse_arguments: bool,
    show_docstring_input_arguments: bool,
    show_docstring_name_value_arguments: bool,
    show_docstring_output_arguments: bool,
    docstring_style: DocstringStyle,
    docstring_options: dict[str, Any] | None,
) -> list[DocstringSection]:
    if function.docstring is None:
        return []

    docstring_sections = do_parse_docstring(function.docstring, docstring_style, docstring_options)
    if not parse_arguments or not (
        show_docstring_input_arguments
        or show_docstring_name_value_arguments
        or show_docstring_output_arguments
    ):
        return docstring_sections

    docstring_arguments = any(
        isinstance(doc, DocstringSectionParameters) for doc in docstring_sections
    )
    docstring_returns = any(isinstance(doc, DocstringSectionReturns) for doc in docstring_sections)

    if not docstring_arguments and function.arguments:
        arguments_arguments = any(param.docstring is not None for param in function.arguments)
    else:
        arguments_arguments = False

    if not docstring_returns and function.returns:
        arguments_returns = any(ret.docstring is not None for ret in function.returns)
    else:
        arguments_returns = False

    document_arguments = not docstring_arguments and arguments_arguments
    document_returns = not docstring_returns and arguments_returns

    standard_arguments = [
        param for param in function.arguments if param.kind is not ArgumentKind.keyword_only
    ]

    keyword_arguments = [
        param for param in function.arguments if param.kind is ArgumentKind.keyword_only
    ]

    if show_docstring_input_arguments and document_arguments and standard_arguments:
        docstring_sections.append(
            DocstringSectionParameters(
                [
                    DocstringParameter(
                        name=param.name,
                        value=str(param.default) if param.default is not None else None,
                        annotation=param.type,
                        description=param.docstring.value if param.docstring is not None else "",
                    )
                    for param in standard_arguments
                ],
                title="",
            )
        )

    if show_docstring_name_value_arguments and document_arguments and keyword_arguments:
        docstring_sections.append(
            DocstringSectionOtherParameters(
                [
                    DocstringParameter(
                        name=param.name,
                        value=str(param.default) if param.default is not None else None,
                        annotation=param.type,
                        description=param.docstring.value if param.docstring is not None else "",
                    )
                    for param in keyword_arguments
                ],
                title="",
            )
        )

    if show_docstring_output_arguments and document_returns:
        returns = DocstringSectionReturns(
            [
                DocstringReturn(
                    name=param.name,
                    value=str(param.default) if param.default is not None else None,
                    annotation=param.type,
                    description=param.docstring.value if param.docstring is not None else "",
                )
                for param in function.returns or []
            ],
            title="",
        )
        docstring_sections.append(returns)

    return docstring_sections


def do_as_inheritance_diagram_section(model: Class) -> DocstringSectionText | None:
    """Generate an inheritance diagram section for a class.

    Args:
        model: The class model to create an inheritance diagram for.

    Returns:
        A docstring section with a Mermaid diagram, or None if there's no inheritance.
    """

    if not hasattr(model, "bases") or not model.bases:
        return None

    def get_id(str: str) -> str:
        return str.replace(".", "_")

    def get_nodes(model: Class, nodes: set[str] = set()) -> set[str]:
        nodes.add(f"   {get_id(model.name)}[{model.name}]")
        for base in [str(base) for base in model.bases]:
            super = model.paths_collection.get_member(base) if model.paths_collection else None
            if super is None:
                nodes.add(f"   {get_id(base)}[{base}]")
            else:
                if isinstance(super, Class):
                    get_nodes(super, nodes)
        return nodes

    def get_links(model: Class, links: set[str] = set()) -> set[str]:
        for base in [str(base) for base in model.bases]:
            super = model.paths_collection.get_member(base) if model.paths_collection else None
            if super is None:
                links.add(f"   {get_id(base)} --> {get_id(model.name)}")
            else:
                if isinstance(super, Class):
                    links.add(f"   {get_id(super.name)} --> {get_id(model.name)}")
                    get_links(super, links)
        return links

    nodes = get_nodes(model)
    if len(nodes) == 1:
        return None

    nodes_str = "\n".join(list(nodes))
    links_str = "\n".join(list(get_links(model)))
    section = f"```mermaid\nflowchart TB\n{nodes_str}\n{links_str}\n```"

    return DocstringSectionText(section, title="Inheritance Diagram")


class AutorefsHook(AutorefsHookInterface):
    """Autorefs hook.

    With this hook, we're able to add context to autorefs (cross-references),
    such as originating file path and line number, to improve error reporting.
    """

    def __init__(self, current_object: Object | Alias, config: dict[str, Any]) -> None:
        """Initialize the hook.

        Parameters:
            current_object: The object being rendered.
            config: The configuration dictionary.
        """
        self.current_object = current_object
        """The current object being rendered."""
        self.config = config
        """The configuration options."""

    def expand_identifier(self, identifier: str) -> str:
        """Expand an identifier.

        Parameters:
            identifier: The identifier to expand.

        Returns:
            The expanded identifier.
        """
        return identifier

    def get_context(self) -> AutorefsHookInterface.Context:
        """Get the context for the current object.

        Returns:
            The context.
        """
        role = {
            "property": "prop",
            "class": "class",
            "function": "meth"
            if self.current_object.parent and self.current_object.parent.is_class
            else "func",
            "namespace": "name",
            "script": "script",
        }.get(self.current_object.kind.value.lower(), "obj")
        origin = self.current_object.path
        try:
            filepath = self.current_object.docstring.parent.filepath
            lineno = self.current_object.docstring.lineno or 0
        except AttributeError:
            filepath = self.current_object.filepath
            lineno = 0

        return AutorefsHookInterface.Context(
            domain="mat",
            role=role,
            origin=origin,
            filepath=str(filepath),
            lineno=lineno,
        )
