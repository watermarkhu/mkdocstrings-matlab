from __future__ import annotations

from pathlib import Path

from textmate_grammar.elements import ContentBlockElement, ContentElement

from . import TM_PARSER
from .attributes import ArgumentAttributes, ClassdefAttributes, MethodAttributes, PropertyAttributes
from .nodes import (
    App,
    Argument,
    Classdef,
    Enum,
    Function,
    LiveScript,
    Method,
    Mex,
    Node,
    Package,
    Property,
    Script,
)
from .utils import (
    analyze_dependency,
    append_block_comment,
    append_comment,
    append_section_comment,
    fix_indentation,
)

_LEADING_TOKEN = "punctuation.whitespace.comment.leading.matlab"
_COMMENT_TOKENS = [
    "comment.line.percentage.matlab",
    "comment.block.percentage.matlab",
    "comment.line.double-percentage.matlab",
]
_STOP_TOKENS = [
    "meta.function.matlab",  # Nested functions
    "meta.function-call.parens.matlab",  # Function call
    "meta.assignment.variable.single.matlab",  # Assignment
    "meta.assignment.variable.group.matlab",
    "meta.import.matlab",  # Import
]


def get_node(
    path: Path,
    parent: Node | None = None,
    in_class_folder: bool = False,
    dependency_analysis: bool = False,
) -> Script | None:
    """
    Returns a Node object based on the given path.

    Args:
        path (Path): The path to the file or directory.
        parent (Node | None, optional): The parent node. Defaults to None.

    Returns:
        Node: The Node object representing the file or directory.

    Raises:
        Warning: If the file could not be parsed.

    """
    if path.is_file():
        fqdm = _fully_qualified_domain_name(path.stem, parent)
        if path.suffix == ".m":
            try:
                element = TM_PARSER.parse_file(path)
            except IndexError:
                return None

            if element is None:
                return None
            try:
                element = next(element.find("meta.class.matlab", depth=1))[0]
                node = _parse_m_classdef(path, element, parent)  # type: ignore
            except StopIteration:
                generator = element.find(
                    [
                        "comment.line.percentage.matlab",
                        "comment.block.percentage.matlab",
                        "comment.line.double-percentage.matlab",
                        "meta.function.matlab",
                    ],
                    stop_tokens="*",
                    depth=1,
                )
                for item, _ in generator:
                    if item.token == "meta.function.matlab":
                        node = _parse_m_function(path, item, parent, in_class_folder)  # type: ignore
                        break
                else:
                    node = _parse_m_script(path, element, parent)  # type: ignore

            if node is not None and dependency_analysis:
                analyze_dependency(element, node)

            return node

        elif path.suffix == ".p":
            # TODO get docstring from .m helper path
            return Script(name=path.stem, fqdm=fqdm, path=path, parent=parent)
        elif path.suffix == ".mlx":
            # TODO get docstring
            return LiveScript(name=path.stem, fqdm=fqdm, path=path, parent=None)
        elif path.suffix == ".mlapp":
            # TODO get docstring
            return App(name=path.stem, fqdm=fqdm, path=path, parent=None)
        elif path.suffix in [".mex", ".mexa64", ".mexmaci64", ".mexw32", ".mexw64"]:
            return Mex(name=path.stem, fqdm=fqdm, path=path, parent=None)

    elif path.is_dir() and path.stem[0] == "+":
        return _parse_dir_package(path, parent)
    elif path.is_dir() and path.stem[0] == "@":
        return _parse_dir_classdef(path, parent)

    return None


def _parse_dir_classdef(path: Path, parent: Node | None = None) -> Classdef | None:
    """
    Parses a directory classdef and returns a Classdef object.

    Args:
        path (Path): The path to the directory classdef.
        parent (Node | None, optional): The parent node of the directory classdef. Defaults to None.

    Returns:
        Classdef: The parsed directory classdef.

    """
    class_definition = path / f"{path.stem[1:]}.m"

    if class_definition.exists():
        element = TM_PARSER.parse_file(class_definition)
        if element is None:
            return None

        class_elem = next(element.find("meta.class.matlab", depth=1))[0]
        node = _parse_m_classdef(class_definition, class_elem, parent)  # type: ignore
    else:
        fqdm = _fully_qualified_domain_name(path.stem[1:], parent)
        node = Classdef(name=path.stem[1:], fqdm=fqdm, path=path, parent=parent)

    for member in path.iterdir():
        # TODO Private folders?
        if member.is_file() and member != class_definition:
            if member.name == "Contents.m":
                continue

            child = get_node(member, node, in_class_folder=True)

            if isinstance(child, Method):
                node.methods[child.name] = child

    return node


def _parse_dir_package(path: Path, parent: Node | None = None) -> Package:
    """
    Parses a directory package and returns a Package object.

    Args:
        path (Path): The path to the directory package.
        parent (Node | None, optional): The parent node of the directory package. Defaults to None.

    Returns:
        Package: The parsed directory package.

    """
    fqdm = _fully_qualified_domain_name(path.stem[1:], parent)
    node = Package(name=path.stem[1:], fqdm=fqdm, path=path, parent=parent)

    for member in path.iterdir():
        if member.is_file():
            child = get_node(member, node)

            if member.name == "Contents.m" and isinstance(child, Script):
                node.docstring = child.docstring
            if isinstance(child, Function):
                node.functions.append(child)
            elif isinstance(child, Classdef):
                node.classes.append(child)
        elif member.is_dir() and member.stem[0] == "+":
            child = _parse_dir_package(member, node)
            if child is not None:
                node.packages.append(child)
        elif member.is_dir() and member.stem[0] == "@":
            child = _parse_dir_classdef(member, node)
            if child is not None:
                node.classes.append(child)

    return node


def _fully_qualified_domain_name(name: str, parent: Node | None) -> str:
    """
    Resolves the fully qualified name by appending the parent names.

    Args:
        name (str): The name to be resolved.
        parent (Node | None): The parent node.

    Returns:
        str: The fully qualified name.
    """
    while parent:
        name = f"{parent.name}.{name}"
        parent = parent.parent
    return name


def _line_comment_to_docstring(element: ContentElement, docstring: dict[int, str]):
    """
    Converts a line comment to a docstring.

    Args:
        element (ContentElement): The line comment element.
        docstring (dict[int, str]): The dictionary representing the docstring.

    Returns:
        None
    """
    first_charater_position = next(iter(element.characters))[0]
    docstring[first_charater_position] = element.content[element.content.index("%") + 1 :]


def _validate_token(element: ContentElement, token: str) -> None:
    """
    Validates the token of a given ContentElement.

    Args:
        element (ContentElement): The ContentElement to validate.
        token (str): The token to compare against the element's token.

    Raises:
        ValueError: If the element's token does not match the provided token.
    """
    if element.token != token:
        raise ValueError(f"Expected token {token}, got {element.token}")


def _common_function_method(
    node: Function | Method, element: ContentBlockElement, parent: Node | None = None
):
    """
    This function is a helper function used internally in the parser module of the MATLAB path library.
    It processes a common function or method and extracts input and output arguments, as well as any associated docstrings.

    Parameters:
        node (Function | Method): The function or method node to process.
        element (ContentBlockElement): The content block element representing the function or method.
        parent (Node | None, optional): The parent node of the function or method. Defaults to None.

    Returns:
        None

    Raises:
        None
    """
    # Function implementation goes here

    def _add_argument(
        arg_element: ContentBlockElement,
        attributes: ArgumentAttributes,
        arg_docstring: dict[int, str],
    ):
        _validate_token(arg_element, "meta.assignment.definition.property.matlab")
        name = arg_element.begin[0].content

        if attributes.Output:
            argument = node.output[name]
        else:
            if "." in name:
                node.input.pop(name.split(".")[0], None)

                option_name = name.split(".")[1]
                argument = Argument(name=option_name, path=node.path, parent=node)
                node.options[option_name] = argument
            else:
                argument = node.input[name]

        argument.attributes = attributes
        _common_property_argument(argument, arg_element, arg_docstring)

    docstring: dict[int, str] = {}

    for function_item, _ in element.find(
        ["meta.function.declaration.matlab", "meta.arguments.matlab"] + _COMMENT_TOKENS,
        stop_tokens=_STOP_TOKENS,
        depth=1,
    ):
        if function_item.token == "meta.function.declaration.matlab":
            # Get input and output arguments from function declaration

            for variable, _ in function_item.find(
                ["variable.parameter.output.matlab", "variable.parameter.input.matlab"]
            ):
                if variable.token == "variable.parameter.input.matlab":
                    node.input[variable.content] = Argument(
                        name=variable.content, path=node.path, parent=node
                    )
                else:
                    node.output[variable.content] = Argument(
                        name=variable.content, path=node.path, parent=node
                    )

        elif function_item.token == "comment.block.percentage.matlab":
            append_block_comment(function_item, docstring)

        elif function_item.token == "comment.line.percentage.matlab":
            append_comment(function_item, docstring)

        elif function_item.token == "comment.line.double-percentage.matlab":
            append_section_comment(function_item, docstring)

        else:  # meta.arguments.matlab
            modifiers = {
                m.content: True
                for m, _ in function_item.findall(
                    "storage.modifier.arguments.matlab", attribute="begin"
                )
            }
            attributes = ArgumentAttributes.from_dict(modifiers)

            arg_elem: ContentBlockElement | None = None
            arg_docstring: dict[int, str] = {}
            for arg_item, _ in function_item.find(
                [
                    "meta.assignment.definition.property.matlab",
                    "comment.line.percentage.matlab",
                ],
                depth=1,
            ):
                if arg_item.token == "meta.assignment.definition.property.matlab":
                    if arg_elem:
                        _add_argument(arg_elem, attributes, arg_docstring)

                    arg_docstring = {}
                    arg_elem = arg_item  # type: ignore
                else:
                    _line_comment_to_docstring(arg_item, arg_docstring)

            else:
                if arg_elem:
                    _add_argument(arg_elem, attributes, arg_docstring)

    node.docstring = fix_indentation(docstring)


def _common_property_argument(
    node: Property | Argument, element: ContentBlockElement, docstring: dict[int, str]
):
    """
    Parses a common property or argument element and extracts relevant information.

    Args:
        node (Property | Argument): The node to store the extracted information.
        element (ContentBlockElement): The element to parse.
        docstring (dict[int, str]): The dictionary to store the extracted docstring.

    Returns:
        None
    """

    if element.end:
        default_elements = element.findall(
            "*",
            stop_tokens=_COMMENT_TOKENS,
            attribute="end",
            depth=1,
        )
        if (
            default_elements
            and default_elements[0][0].token == "keyword.operator.assignment.matlab"
        ):
            node.default = "".join([el.content for el, _ in default_elements[1:]])

        doc_elements = element.findall("comment.line.percentage.matlab", attribute="end")

        for el, _ in doc_elements:
            _line_comment_to_docstring(el, docstring)

    node.docstring = fix_indentation(docstring)

    for expression, _ in element.find(
        [
            "storage.type.matlab",
            "meta.parens.size.matlab",
            "meta.block.validation.matlab",
        ],
        depth=1,
    ):
        if expression.token == "storage.type.matlab":
            node.type = expression.content
        elif expression.token == "meta.parens.size.matlab":
            node.size = expression.content.split(",")
        else:
            node.validators = [validator.content for validator in expression.children]


def _parse_m_script(path: Path, element: ContentBlockElement, parent: Node | None = None) -> Script:
    """
    Parse an m-script file and return a Script object.

    Args:
        path (Path): The path to the m-script file.
        element (ContentBlockElement): The content block element representing the m-script.
        **kwargs: Additional keyword arguments.

    Returns:
        Script: The parsed Script object.

    """
    docstring: dict[int, str] = {}
    for function_item, _ in element.find(
        _COMMENT_TOKENS + [_LEADING_TOKEN], stop_tokens="*", depth=1
    ):
        if function_item.token == "comment.line.percentage.matlab":
            append_comment(function_item, docstring)
        elif function_item.token == "comment.line.double-percentage.matlab":
            append_section_comment(function_item, docstring)
        elif function_item.token == "comment.block.percentage.matlab":
            # Block comments will take precedence over single % comments
            append_block_comment(function_item, docstring)
            break
    fix_indentation(docstring)
    return Script(name=path.stem, fqdm=path.stem, path=path, parent=None, docstring=docstring)


def _parse_m_function(
    path: Path,
    element: ContentBlockElement,
    parent: Node | None = None,
    in_class_folder: bool = False,
) -> Function:
    """
    Parses an m-function from the given path and element.

    Args:
        path (Path): The path to the m-function file.
        element (ContentBlockElement): The element representing the m-function.
        parent (Node | None, optional): The parent node of the m-function. Defaults to None.

    Returns:
        Function: The parsed m-function node.

    Raises:
        ValidationError: If the element is not a valid m-function.

    """
    _validate_token(element, "meta.function.matlab")
    fqdm = _fully_qualified_domain_name(path.stem, parent)
    if not in_class_folder:
        node = Function(name=path.stem, fqdm=fqdm, path=path, parent=parent)
    else:
        node = Method(name=path.stem, fqdm=fqdm, path=path, parent=parent)
    _common_function_method(node, element, parent)
    return node


def _parse_method(
    parent: Classdef, element: ContentBlockElement, attributes: MethodAttributes
) -> Method:
    """
    Parses a method from the given element and returns a Method object.

    Args:
        parent (Classdef): The parent Classdef object.
        element (ContentBlockElement): The element to parse.
        attributes (MethodAttributes): The attributes of the method.

    Returns:
        Method: The parsed Method object.
    """
    _validate_token(element, "meta.function.matlab")
    declaration = next(element.find("meta.function.declaration.matlab", depth=1))[0]
    name = next(declaration.find("entity.name.function.matlab"))[0].content
    fqdm = _fully_qualified_domain_name(name, parent)
    node = Method(name=name, fqdm=fqdm, attributes=attributes, parent=parent, path=parent.path)
    _common_function_method(node, element, parent)
    return node


_CLASS_TOKENS = [
    "meta.class.declaration.matlab",
    "meta.properties.matlab",
    "meta.enum.matlab",
    "meta.methods.matlab",
]


def _parse_m_classdef(
    path: Path, element: ContentBlockElement, parent: Node | None = None
) -> Classdef:
    """
    Parses a MATLAB class definition.

    Args:
        path (Path): The path of the MATLAB file containing the class definition.
        element (ContentBlockElement): The content block element representing the class definition.
        parent (Node | None, optional): The parent node of the class definition. Defaults to None.

    Returns:
        Classdef: The parsed class definition.

    Raises:
        None

    """

    def _add_property(
        element: ContentBlockElement, attributes: PropertyAttributes, docstring: dict[int, str]
    ):
        _validate_token(element, "meta.assignment.definition.property.matlab")
        name = element.begin[0].content
        prop = Property(name=name, parent=node, path=node.path)
        prop.attributes = attributes
        _common_property_argument(prop, element, docstring)
        node.properties[name] = prop

    _validate_token(element, "meta.class.matlab")

    fqdm = _fully_qualified_domain_name(path.stem, parent)
    node = Classdef(name=path.stem, fqdm=fqdm, path=path, parent=parent)

    docstring: dict[int, str] = {}

    for class_item, _ in element.find(_CLASS_TOKENS, depth=1):
        if class_item.token == "meta.class.declaration.matlab":
            modifiers = {}
            current_modifier, current_value = "", "true"

            for attribute_item, _ in class_item.find(
                "*",
                start_tokens="punctuation.section.parens.begin.matlab",
                stop_tokens="punctuation.section.parens.end.matlab",
                depth=1,
            ):
                if attribute_item.token == "punctuation.section.parens.begin.matlab":
                    continue
                elif attribute_item.token == "storage.modifier.class.matlab":
                    current_modifier = attribute_item.content
                elif attribute_item.token == "keyword.operator.assignment.matlab":
                    current_value = ""
                elif attribute_item.token == "punctuation.separator.modifier.comma.matlab":
                    modifiers[current_modifier], current_value = current_value, "true"
                elif attribute_item.token not in _COMMENT_TOKENS:
                    current_value += attribute_item.content
            else:
                if current_modifier:
                    modifiers[current_modifier] = current_value

            node.attributes = ClassdefAttributes.from_dict(modifiers)

            declation_tokens = [
                "entity.name.type.class.matlab",
                "meta.inherited-class.matlab",
                "punctuation.definition.comment.matlab",
            ]

            for declation_item, _ in class_item.find(
                declation_tokens, start_tokens=declation_tokens, depth=1
            ):
                if declation_item.token == "entity.name.type.class.matlab":
                    node.name = declation_item.content
                elif declation_item.token == "meta.inherited-class.matlab":
                    node.ancestors.append(declation_item.content)
                elif declation_item.token == "punctuation.definition.comment.matlab":
                    _line_comment_to_docstring(class_item, docstring)

        elif class_item.token == "meta.properties.matlab":
            modifiers = {}
            current_modifier, current_value = "", "true"
            for modifier_item, _ in class_item.findall(
                "*", start_tokens="storage.modifier.properties.matlab", attribute="begin"
            ):
                if modifier_item.token == "storage.modifier.properties.matlab":
                    if current_modifier:
                        modifiers[current_modifier], current_value = current_value, "true"
                    current_modifier = modifier_item.content
                elif modifier_item.token == "keyword.operator.assignment.matlab":
                    current_value = ""
                elif modifier_item.token not in _COMMENT_TOKENS:
                    current_value += modifier_item.content
            else:
                if current_modifier:
                    modifiers[current_modifier] = current_value

            attributes = PropertyAttributes.from_dict(modifiers)

            prop_elem = None
            prop_docstring: dict[int, str] = {}
            for prop_item, _ in class_item.find(
                [
                    "meta.assignment.definition.property.matlab",
                    "comment.line.percentage.matlab",
                ],
                depth=1,
            ):
                if prop_item.token == "meta.assignment.definition.property.matlab":
                    if prop_elem:
                        _add_property(prop_elem, attributes, prop_docstring)

                    prop_docstring = {}
                    prop_elem = prop_item
                else:
                    _line_comment_to_docstring(prop_item, prop_docstring)
            else:
                if prop_elem:
                    _add_property(prop_elem, attributes, prop_docstring)  # type: ignore

        elif class_item.token == "meta.enum.matlab":
            enum_docstring: dict[int, str] = {}
            enum_name: str = ""
            enum_value: str = ""
            for enum_item, _ in class_item.find(
                [
                    "meta.assignment.definition.enummember.matlab",
                    "meta.parens.matlab",
                    "comment.line.percentage.matlab",
                ],
                attribute="children",
            ):
                if enum_item.token == "meta.assignment.definition.enummember.matlab":
                    if enum_name:
                        enum_doc = fix_indentation(enum_docstring)
                        enum = Enum(
                            name=enum_name,
                            value=enum_value,
                            docstring=enum_doc,
                            parent=node,
                            path=node.path,
                        )
                        node.enumeration.append(enum)
                        enum_docstring, enum_value = {}, ""

                    enum_name = next(enum_item.find("variable.other.enummember.matlab"))[0].content

                elif enum_item.token == "meta.parens.matlab":
                    enum_value = enum_item.content
                else:
                    append_comment(enum_item, enum_docstring)
            else:
                if enum_name:
                    enum_doc = fix_indentation(enum_docstring)
                    enum = Enum(
                        name=enum_name,
                        value=enum_value,
                        docstring=enum_doc,
                        parent=node,
                        path=node.path,
                    )
                    node.enumeration.append(enum)

        else:  # meta.methods.matlab
            modifiers = {}
            current_modifier, current_value = "", "true"
            for modifier_item, _ in class_item.findall(
                ["storage.modifier.methods.matlab", "storage.modifier.access.matlab"],
                attribute="begin",
            ):
                if modifier_item.token == "storage.modifier.methods.matlab":
                    if current_modifier:
                        modifiers[current_modifier], current_value = current_value, "true"
                    current_modifier = modifier_item.content
                else:
                    current_value = modifier_item.content
            else:
                if current_modifier:
                    modifiers[current_modifier] = current_value

            attributes = MethodAttributes.from_dict(modifiers)

            for method_elem, _ in class_item.find("meta.function.matlab", depth=1):
                method = _parse_method(node, method_elem, attributes)  # type: ignore
                node.methods[method.name] = method

    for class_item, _ in element.find(_COMMENT_TOKENS, stop_tokens=_CLASS_TOKENS, depth=1):
        if class_item.token == "comment.block.percentage.matlab":
            append_block_comment(class_item, docstring)
        elif class_item.token == "comment.line.percentage.matlab":
            append_comment(class_item, docstring)
        elif class_item.token == "comment.line.double-percentage.matlab":
            append_section_comment(class_item, docstring)

    node.docstring = fix_indentation(docstring)
    return node
