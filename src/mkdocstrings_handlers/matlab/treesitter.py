# %%
from tree_sitter import Language, Parser, Node, TreeCursor
import tree_sitter_matlab as tsmatlab

from pathlib import Path

import charset_normalizer

from mkdocstrings_handlers.matlab.models import (
    AccessEnum,
    Class,
    Docstring,
    Function,
    Parameters,
    Parameter,
    Property,
    Script,
)
from mkdocstrings_handlers.matlab.models import PathMixin
from mkdocstrings_handlers.matlab.enums import ParameterKind


__all__ = ["parse_file"]


LANGUAGE = Language(tsmatlab.language())
PARSER = Parser(LANGUAGE)


def strtobool(value: str) -> bool:
    if value.lower() in ["true", "1"]:
        return True
    else:
        return False


def dedent_lines(lines: list[str]) -> list[str]:
    """
    Dedent a list of strings by removing the minimum common leading whitespace.

    Args:
        lines (list[str]): A list of strings to be dedented.

    Returns:
        list[str]: A list of strings with the common leading whitespace removed.
    """
    indents = [len(line) - len(line.lstrip()) for line in lines if line.strip()]
    indent = min(indents)
    if indent == 0:
        return lines
    else:
        return [line[indent:] if line.strip() else line for line in lines]


def comment_node_docstring(node: Node, encoding: str) -> list[str]:
    """
    Extracts and processes docstring comments from a given node.
    This function iterates over the lines of text within the provided node,
    identifying and processing lines that are marked as docstring comments.
    It supports both single-line and multi-line comment blocks, denoted by
    specific markers ("%{", "%%", and "%}").

    Args:
        node (Node): The node containing the text to be processed.
    Returns:
        list[str]: A list of strings representing the extracted and processed
                   docstring comments.
    Raises:
        LookupError: If a line does not conform to the expected comment format.
    """

    docstring, comment_lines = [], []

    lines = iter(node.text.decode(encoding).splitlines())
    while True:
        try:
            line = next(lines).lstrip()
        except StopIteration:
            break

        if line[:2] == "%{" or line[:2] == "%%":
            if comment_lines:
                docstring += dedent_lines(comment_lines)
                comment_lines = []
            if line[:2] == "%%":
                docstring.append(line[2:].lstrip())
                continue

            comment_block = []
            line = line[2:]
            while "%}" not in line:
                comment_block.append(line)
                try:
                    line = next(lines)
                except StopIteration:
                    break
            else:
                last_line = line[: line.index("%}")]
                if last_line:
                    comment_block.append(last_line)
            docstring.append(comment_block[0])
            docstring += dedent_lines(comment_block[1:])

        elif line[0] == "%":
            comment_lines.append(line[1:])
        else:
            raise LookupError

    if comment_lines:
        docstring += dedent_lines(comment_lines)

    return docstring


def parse_function(
    cursor: TreeCursor, encoding: str, filepath: Path, **kwargs
) -> Function:
    docstring = []
    doclineno, docendlineno = 0, 0
    used_arguments = False
    kwargs["lineno"] = cursor.node.start_point.row + 1
    kwargs["endlineno"] = cursor.node.end_point.row + 1

    cursor.goto_first_child()

    while cursor.goto_next_sibling():
        match cursor.node.type:
            case "function_output":
                cursor.goto_first_child()
                if cursor.node.type == "identifier":
                    returns = [Parameter(cursor.node.text.decode(encoding))]
                else:
                    cursor.goto_first_child()
                    returns = []
                    while cursor.goto_next_sibling():
                        if cursor.node.type == "identifier":
                            returns.append(Parameter(cursor.node.text.decode(encoding)))
                    cursor.goto_parent()
                kwargs["returns"] = Parameters(*returns)
                cursor.goto_parent()

            case "set.":
                kwargs["setter"] = True

            case "get.":
                kwargs["getter"] = True

            case "identifier":
                identifier = cursor.node.text.decode(encoding)
                if kwargs.get("setter", False):
                    identifier = f"set.{identifier}"
                elif kwargs.get("getter", False):
                    identifier = f"get.{identifier}"

            case "function_arguments":
                cursor.goto_first_child()
                parameters = []
                while cursor.goto_next_sibling():
                    if cursor.node.type == "identifier":
                        parameters.append(Parameter(cursor.node.text.decode(encoding)))
                kwargs["parameters"] = Parameters(*parameters)
                cursor.goto_parent()

            case "comment":
                if used_arguments:
                    continue
                if not doclineno:
                    doclineno = cursor.node.start_point.row
                docendlineno = cursor.node.end_point.row
                docstring += comment_node_docstring(cursor.node, encoding)

            case "arguments_statement":
                used_arguments = True

                arguments_type = "parameters"
                cursor.goto_first_child()
                while cursor.goto_next_sibling():
                    if cursor.node.type == "attributes":
                        if "Output" in cursor.node.text.decode(encoding):
                            arguments_type = "returns"
                    elif cursor.node.type == "property":
                        parameters = kwargs[arguments_type]

                        cursor.goto_first_child()
                        argument = cursor.node.text.decode(encoding)

                        if "." in argument:
                            kwargsvar = argument.split(".")[0]
                            kwargsparameter = next(
                                (p for p in parameters if p.name == kwargsvar), None
                            )
                            if kwargsparameter:
                                parameters._params.remove(kwargsparameter)
                            argument = argument.split(".")[-1]
                            parameter = Parameter(
                                argument, kind=ParameterKind.keyword_only
                            )
                            parameters._params.append(parameter)
                        else:
                            parameter = next(
                                (p for p in parameters if p.name == argument), None
                            )
                            if argument == "varargin":
                                parameter.kind = ParameterKind.var_keyword
                            else:
                                parameter.kind = ParameterKind.positional

                        while cursor.goto_next_sibling():
                            match cursor.node.type:
                                case "dimensions":
                                    # Do nothing with dimensions for now
                                    continue
                                case "identifier":
                                    parameter.annotation = cursor.node.text.decode(
                                        encoding
                                    )
                                case "validation_functions":
                                    # Do nothing with validation functions for now
                                    continue
                                case "default_value":
                                    parameter.default = cursor.node.text.decode(
                                        encoding
                                    )[1:].strip()
                                    if parameter.kind is ParameterKind.positional:
                                        parameter.kind = ParameterKind.optional
                                case "comment":
                                    parameter.docstring = "\n".join(
                                        comment_node_docstring(cursor.node, encoding)
                                    )
                        cursor.goto_parent()
                cursor.goto_parent()

            case "end" | "block":
                break

    cursor.goto_parent()

    if docstring:
        kwargs["docstring"] = Docstring(
            "\n".join(docstring), lineno=doclineno + 1, endlineno=docendlineno + 1
        )

    return Function(identifier, filepath=filepath, **kwargs)


def parse_class(cursor: TreeCursor, encoding: str, filepath: Path, **kwargs) -> Class:
    docstring = []
    doclineno, docendlineno = 0, 0
    comment_for_docstring = True

    savedKwargs = {key: value for key, value in kwargs.items()}
    kwargs["lineno"] = cursor.node.start_point.row + 1
    kwargs["endlineno"] = cursor.node.end_point.row + 1
    methods, properties = [], []

    cursor.goto_first_child()

    while cursor.goto_next_sibling():
        match cursor.node.type:
            case "attributes":
                # https://mathworks.com/help/matlab/matlab_oop/class-attributes.html

                cursor.goto_first_child()
                while cursor.goto_next_sibling():
                    if cursor.node.type == "attribute":
                        cursor.goto_first_child()
                        attributeIdentifier = cursor.node.text.decode(encoding)
                        if attributeIdentifier in ["Sealed", "Abstract", "Hidden"]:
                            value = True
                            while cursor.goto_next_sibling():
                                if cursor.node.type == "boolean":
                                    value = bool(
                                        strtobool(cursor.node.text.decode(encoding))
                                    )
                            kwargs[attributeIdentifier] = value
                        cursor.goto_parent()
                cursor.goto_parent()

            case "identifier":
                identifier = cursor.node.text.decode(encoding)

            case "superclasses":
                cursor.goto_first_child()
                kwargs["bases"] = []
                while cursor.goto_next_sibling():
                    if cursor.node.type == "property_name":
                        kwargs["bases"].append(cursor.node.text.decode(encoding))
                cursor.goto_parent()

            case "comment":
                if not comment_for_docstring:
                    continue
                if not doclineno:
                    doclineno = cursor.node.start_point.row
                docendlineno = cursor.node.end_point.row
                docstring += comment_node_docstring(cursor.node, encoding)

            case "properties":
                comment_for_docstring = False

                cursor.goto_first_child()
                property_kwargs = {key: value for key, value in savedKwargs.items()}

                while cursor.goto_next_sibling():
                    if cursor.node.type == "property":
                        cursor.goto_first_child()
                        prop = Property(
                            cursor.node.text.decode(encoding), **property_kwargs
                        )
                        while cursor.goto_next_sibling():
                            match cursor.node.type:
                                case "dimensions":
                                    # Do nothing with dimensions for now
                                    continue
                                case "identifier":
                                    prop.annotation = cursor.node.text.decode(encoding)
                                case "validation_functions":
                                    # Do nothing with validation functions for now
                                    continue
                                case "default_value":
                                    prop.value = cursor.node.text.decode(encoding)[
                                        1:
                                    ].strip()
                                case "comment":
                                    prop.docstring = "\n".join(
                                        comment_node_docstring(cursor.node, encoding)
                                    )
                        properties.append(prop)
                        cursor.goto_parent()

                    elif cursor.node.type == "attributes":
                        # https://mathworks.com/help/matlab/matlab_oop/property-attributes.html

                        cursor.goto_first_child()
                        while cursor.goto_next_sibling():
                            if cursor.node.type == "attribute":
                                cursor.goto_first_child()
                                attributeIdentifier = cursor.node.text.decode(encoding)
                                if attributeIdentifier in [
                                    "AbortSet",
                                    "Abstract",
                                    "Constant",
                                    "Dependant",
                                    "GetObservable",
                                    "Hidden",
                                    "NonCopyable",
                                    "SetObservable",
                                    "Transient",
                                    "WeakHandle",
                                ]:
                                    value = True
                                    while cursor.goto_next_sibling():
                                        if cursor.node.type == "boolean":
                                            value = bool(
                                                strtobool(
                                                    cursor.node.text.decode(encoding)
                                                )
                                            )
                                    property_kwargs[attributeIdentifier] = value

                                elif attributeIdentifier in ["GetAccess", "SetAccess"]:
                                    cursor.goto_next_sibling()
                                    cursor.goto_next_sibling()
                                    access = cursor.node.text.decode(encoding)
                                    if access in [
                                        "public",
                                        "protected",
                                        "private",
                                        "immutable",
                                    ]:
                                        property_kwargs[attributeIdentifier] = (
                                            AccessEnum(access)
                                        )
                                cursor.goto_parent()
                        cursor.goto_parent()

                cursor.goto_parent()

            case "methods":
                comment_for_docstring = False

                cursor.goto_first_child()
                is_abstract = False
                function_kwargs = {key: value for key, value in savedKwargs.items()}

                while cursor.goto_next_sibling():
                    if cursor.node.type == "function_definition":
                        method = parse_function(
                            cursor, encoding, filepath, **function_kwargs
                        )

                        if method.name != identifier and not is_abstract:
                            # Remove self from first method argument
                            method.parameters._params = method.parameters._params[1:]
                        methods.append(method)

                    elif cursor.node.type == "attributes":
                        # https://mathworks.com/help/matlab/matlab_oop/method-attributes.html

                        cursor.goto_first_child()
                        while cursor.goto_next_sibling():
                            if cursor.node.type == "attribute":
                                cursor.goto_first_child()
                                attributeIdentifier = cursor.node.text.decode(encoding)

                                if attributeIdentifier in [
                                    "Abstract",
                                    "Hidden",
                                    "Sealed",
                                    "Static",
                                ]:
                                    value = True
                                    while cursor.goto_next_sibling():
                                        if cursor.node.type == "boolean":
                                            value = bool(
                                                strtobool(
                                                    cursor.node.text.decode(encoding)
                                                )
                                            )
                                    function_kwargs[attributeIdentifier] = value
                                elif attributeIdentifier == "Access":
                                    cursor.goto_next_sibling()
                                    cursor.goto_next_sibling()
                                    access = cursor.node.text.decode(encoding)
                                    if access in [
                                        "public",
                                        "protected",
                                        "private",
                                        "immutable",
                                    ]:
                                        function_kwargs[attributeIdentifier] = (
                                            AccessEnum(access)
                                        )
                                cursor.goto_parent()

                        is_abstract = function_kwargs.get("abstract", False)
                        cursor.goto_parent()

                cursor.goto_parent()

            case "enumeration":
                comment_for_docstring = False
                # Do nothing with enumerations for now
                continue

    if docstring:
        kwargs["docstring"] = Docstring(
            "\n".join(docstring), lineno=doclineno + 1, endlineno=docendlineno + 1
        )

    model = Class(identifier, filepath=filepath, **kwargs)
    for prop in properties:
        prop.parent = model
        model[prop.name] = prop

    for method in methods:
        method.parent = model
        if method._is_getter or method._is_setter:
            prop = model.members.get(
                method.name.split(".")[1], None
            )  # TODO replace with all_members
            if prop:
                if method._is_getter:
                    prop.getter = method
                else:
                    prop.setter = method
            else:
                # Some warning needs to be issued that this getter/setter has no property to be linked to
                pass
        else:
            model[method.name] = method

    return model


def parse_file(filepath: Path, **kwargs) -> tuple[PathMixin, str]:
    encoding = charset_normalizer.from_path(filepath).best().encoding
    with open(filepath, "rb") as f:
        content = f.read()

    tree = PARSER.parse(content)
    cursor = tree.walk()
    cursor.goto_first_child()

    header_comment = []
    doclineno, docendlineno = 0, 0

    while True:
        if cursor.node.type == "function_definition":
            model = parse_function(
                cursor, encoding, filepath=filepath, **kwargs
            )
            break
        elif cursor.node.type == "class_definition":
            model = parse_class(
                cursor, encoding, filepath=filepath, **kwargs
            )
            break
        elif cursor.node.type == "comment":
            header_comment += comment_node_docstring(cursor.node, encoding)
            if not doclineno:
                doclineno = cursor.node.start_point.row
            docendlineno = cursor.node.end_point.row
        else:
            model = Script(filepath.stem, filepath=filepath, **kwargs)
            break

        if not cursor.goto_next_sibling():
            break

    if not model.docstring:
        model.docstring = Docstring(
            "\n".join(header_comment), lineno=doclineno, endlineno=docendlineno
        )

    return model, content.decode(encoding)


# %%
