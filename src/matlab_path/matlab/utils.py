from __future__ import annotations

from textmate_grammar.elements import ContentElement

from . import TM_PARSER
from .data import _load_references
from .nodes import Classdef, Script


def append_comment(elem: ContentElement, docstring: dict[int, str]) -> dict[int, str]:
    """
    Append a comment from the given element to the docstring.

    Parameters:
        elem (ContentElement): The element containing the comment.
        docstring (dict[int, str]): The existing docstring.

    Returns:
        dict[int, str]: The updated docstring with the appended comment.
    """
    content = elem.content[elem.content.index("%") + 1 :]
    pos = list(elem.characters.keys())[0]
    docstring[pos[0]] = content
    return docstring


def append_section_comment(elem: ContentElement, docstring: dict[int, str]) -> dict[int, str]:
    """
    Appends a section comment to the given docstring.

    Args:
        elem (ContentElement): The content element containing the section comment.
        docstring (dict[int, str]): The existing docstring to append the section comment to.

    Returns:
        dict[int, str]: The updated docstring with the section comment appended.
    """
    content = elem.content[elem.content.index("%%") + 2 :]
    pos = list(elem.characters.keys())[0]
    docstring[pos[0]] = content
    return docstring


def append_block_comment(elem: ContentElement, docstring: dict[int, str]) -> dict[int, str]:
    """
    Appends the block comment from the given element to the docstring dictionary.

    Args:
        elem (ContentElement): The element containing the block comment.
        docstring (dict[int, str]): The dictionary to append the block comment to.

    Returns:
        dict[int, str]: The updated docstring dictionary.
    """
    bracket = elem.content.index("%{") + 2
    begin = elem.content[bracket:].index("\n") + bracket + 1
    content = elem.content[begin : elem.content.index("%}")]
    pos = list(elem.characters.keys())[0]
    index = pos[0] + 1
    for i, line in enumerate(content.split("\n")):
        docstring[index + i] = line
    return docstring


def fix_indentation(docstring: dict[int, str]) -> dict[int, str]:
    """
    Fixes the indentation of a multi-line docstring.

    Args:
        docstring (dict[int, str]): A dictionary representing the lines of the docstring.

    Returns:
        str: The fixed docstring with correct indentation.

    """
    if not docstring:
        return {}
    padding = [len(line) - len(line.lstrip()) for line in docstring.values()]
    indent = min(
        [pad for pad, line in zip(padding, docstring.values()) if not (line.isspace() or not line)]
    )

    for (i, line), pad in zip(docstring.items(), padding):
        docstring[i] = line[indent:].rstrip() if len(line) >= pad else line.rstrip()
    return docstring


def analyze_dependency(element: ContentElement, node: Script) -> None:
    """
    Analyzes the dependency of a given element and updates the dependencies of a script node.

    https://mathworks.com/help/compiler/function.html

    Args:
        element (ContentElement): The element to analyze the dependency for.
        node (Script): The script node to update the dependencies for.

    Returns:
        None
    """

    if isinstance(node, Classdef):
        builtins = _load_references()

        for ancestor in node.ancestors:
            if ancestor in builtins:
                node._builtin_dependencies.add(ancestor)
            else:
                node._calls.add(ancestor)

        for class_elem, _ in element.find(
            ["meta.properties.matlab", "meta.methods.matlab"],
            depth=1,
        ):
            if class_elem.token == "meta.properties.matlab":
                for item, _ in class_elem.find(
                    [
                        "storage.type.matlab",
                        "entity.name.function.matlab",
                        "variable.other.readwrite.matlab",
                    ]
                ):
                    if item.content in builtins:
                        node._builtin_dependencies.add(item.content)
                    else:
                        node._calls.add(item.content)
            elif class_elem.token == "meta.methods.matlab":
                for method_elem, _ in class_elem.find("meta.function.matlab", depth=1):
                    fname = next(method_elem.find("entity.name.function.matlab"))[0].content
                    _analyze_dependency_file(method_elem, node.methods[fname])
    else:
        _analyze_dependency_file(element, node)


def _analyze_dependency_file(element: ContentElement, node: Script) -> None:
    builtins = _load_references()

    def add_dependency(name: str):
        if name in builtins:
            node._builtin_dependencies.add(name)
        else:
            node._calls.add(name)

    local_variables: set[str] = set()

    for item, _ in element.find(
        [
            "variable.parameter.input.matlab",
            "storage.type.matlab",
            "comment.line.percentage.matlab",
            "entity.name.namespace.matlab",
            "meta.assignment.variable.single.matlab",
            "meta.assignment.variable.group.matlab",
            "variable.other.readwrite.matlab",
        ]
    ):
        if item.token == "variable.parameter.input.matlab":
            # Function input variables
            local_variables.add(item.content)

        elif item.token in [
            "meta.assignment.variable.single.matlab",
            "meta.assignment.variable.group.matlab",
        ]:
            # Assigned variables
            for variable, _ in item.find("variable.other.readwrite.matlab"):
                local_variables.add(variable.content)

        elif item.token == "storage.type.matlab":
            # Validator type
            add_dependency(item.content)

        elif item.token == "comment.line.percentage.matlab" and item.content.startswith(
            "%#function"
        ):
            # Pragma types https://mathworks.com/help/compiler/function.html
            for pragma in [
                pragma.strip() for pragma in item.content[10:].strip().split(" ") if pragma
            ]:
                add_dependency(pragma)
        elif item.token == "entity.name.namespace.matlab":
            # Namespace imports https://mathworks.com/help/matlab/ref/import.html
            if item.children[-1].content == "*":
                namespace = "".join([child.content for child in item.children[:-2]])
                if namespace in builtins:
                    node._builtin_dependencies.add(namespace)
                else:
                    node._imports.add(namespace)
            else:
                add_dependency("".join([child.content for child in item.children]))

        elif (
            item.token == "variable.other.readwrite.matlab"
            and item.content not in local_variables
            and (
                item.parent is not None
                and item.parent.token
                not in [
                    "meta.assignment.variable.single.matlab",
                    "meta.assignment.variable.group.matlab",
                ]
            )
        ):
            # Function call without parentheses
            add_dependency(item.content)

    token_list = element.flatten()
    for i, (_, content, tokens) in enumerate(token_list):
        if len(tokens) > 2 and tokens[-2:] == [
            "meta.function-call.parens.matlab",
            "entity.name.function.matlab",
        ]:
            # Add function call as dependency (does not add methods)
            if i > 1 and token_list[i - 1][2][-1] != "punctuation.accessor.dot.matlab":
                if content not in local_variables:
                    add_dependency(content)

            # Add full namespace of function call as dependency (does not add class objects)
            else:
                name = content
                while i > 1 and token_list[i - 1][2][-1] == "punctuation.accessor.dot.matlab":
                    namespace_item = token_list[i - 2][1]
                    name = namespace_item + "." + name
                    i -= 2
                if namespace_item not in local_variables:
                    add_dependency(name)

    for name in local_variables:
        if name in node._calls:
            node._calls.remove(name)
