# %%
from collections import OrderedDict
from tree_sitter import Language, Parser, Node, TreeCursor
import tree_sitter_matlab as tsmatlab

from pathlib import Path

import charset_normalizer

from mkdocstrings_handlers.matlab.models import (
    AccessEnum,
    Class,
    Docstring,
    Function,
    MatlabObject,
    Parameters,
    Parameter,
    Property,
    Script,
)
from mkdocstrings_handlers.matlab.models import PathMixin
from mkdocstrings_handlers.matlab.enums import ParameterKind


__all__ = ["FileParser"]


LANGUAGE = Language(tsmatlab.language())

PARSER = Parser(LANGUAGE)

FILE_QUERY = LANGUAGE.query("""(source_file
    (comment)* @header .
    (function_definition)? @function .
    (class_definition)? @class
)
""")


FUNCTION_QUERY = LANGUAGE.query("""(function_definition .
    ("function") .
    (function_output . 
        [
            (identifier) @output
            (multioutput_variable .
                ((identifier) @output (",")?)+
            )
        ]
    )? .
    (identifier) .
    (function_arguments .
        ((identifier) @input (",")?)*
    )? .
    (comment)* @docstring .
    (arguments_statement)* @arguments
)""")


ARGUMENTS_QUERY = LANGUAGE.query("""(arguments_statement .
    ("arguments") .
    (attributes
        (identifier) @attributes
    )? .
    ("\\n")? .
    (property)+ @arguments
)""")


PROPERTY_QUERY = LANGUAGE.query("""(property . 
    [
        (identifier) @name
        (property_name
            (identifier) @options .
            (".") .
            (identifier) @name
        )
    ] .
    (dimensions)? @dimentions .
    (identifier)? @class .
    (validation_functions)? @validators .
    (default_value
        ("=") .
        _+ @default
    )? .
    (comment)* @comment              
)""")


def _strtobool(value: str) -> bool:
    if value.lower() in ["true", "1"]:
        return True
    else:
        return False


def _dedent(lines: list[str]) -> list[str]:
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


def parse_class(cursor: TreeCursor, encoding: str, filepath: Path, **kwargs) -> Class:
    docstring: list[str] = []
    docstrings: list[Docstring] = []
    doclineno, docendlineno = 0, 0
    comment_for_docstring: bool = True

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
                                        _strtobool(cursor.node.text.decode(encoding))
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
                docstring += uncommented(cursor.node, encoding)

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
                                    plineno = cursor.node.start_point.row + 1
                                    plinendlineno = cursor.node.end_point.row + 1
                                    text = "\n".join(
                                        uncommented(cursor.node, encoding)
                                    )
                                    prop.docstring = Docstring(
                                        text, lineno=plineno, endlineno=plinendlineno
                                    )
                                    docstrings.append(prop.docstring)

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
                                                _strtobool(
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
                                                _strtobool(
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

    for docstring in docstrings:
        docstring.parent = model

    for prop in properties:
        prop.parent = model
        model[prop.name] = prop

    for method in methods:
        method.parent = model
        if method._is_getter or method._is_setter:
            prop = model.all_members.get(method.name.split(".")[1], None)
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


class FileParser(object):
    def __init__(self, filepath: Path):
        self.filepath: Path = filepath
        self.encoding: str = charset_normalizer.from_path(filepath).best().encoding
        with open(filepath, "rb") as f:
            self._content: bytes = f.read()

    @property
    def content(self):
        return self._content.decode(self.encoding)

    def parse(self, **kwargs) -> PathMixin:
        tree = PARSER.parse(self._content)
        cursor = tree.walk()

        captured = FILE_QUERY.captures(cursor.node)

        if "function" in captured:
            model = self._parse_function(captured["function"][0], **kwargs)
        elif "class" in captured:
            model = self._parse_class(captured["class"][0], **kwargs)
        else:
            model = Script(self.filepath.stem, filepath=self.filepath, **kwargs)

        if not model.docstring:
            model.docstring = self._comment_docstring(
                captured.get("header", None), parent=model
            )

        return model
    
    def _parse_class(self, node: Node, **kwargs) -> Class:

        model = Class(self.filepath.stem)
        return model

    def _parse_function(self, node: Node, **kwargs) -> Function:
        captured: dict = FUNCTION_QUERY.captures(node)

        input_names = self._decode(captured, "input")
        parameters: dict = (
            OrderedDict(
                (name, Parameter(name, kind=ParameterKind.positional))
                for name in input_names
            )
            if input_names
            else {}
        )
        output_names = self._decode(captured, "output")
        returns: dict = (
            OrderedDict(
                (name, Parameter(name, kind=ParameterKind.positional))
                for name in output_names
            )
            if output_names
            else {}
        )

        model = Function(
            self.filepath.stem,
            filepath=self.filepath,
            docstring=self._comment_docstring(captured.get("docstring", None)),
            **kwargs,
        )

        captured_arguments = [
            ARGUMENTS_QUERY.captures(node) for node in captured["arguments"]
        ]
        for arguments in captured_arguments:
            attributes = self._decode(arguments, "attributes")
            is_input = "Input" in attributes or "Output" not in attributes
            # is_repeating = "Repeating" in attributes

            captured_argument = [
                PROPERTY_QUERY.captures(node) for node in arguments["arguments"]
            ]
            for argument in captured_argument:
                name = self._decode(argument, "name", True)

                if "options" in argument:
                    options_name = self._decode(argument, "options", True)
                    parameters.pop(options_name, None)
                    parameter = parameters[name] = Parameter(
                        name, kind=ParameterKind.keyword_only
                    )
                else:
                    if is_input:
                        parameter = parameters.get(name, Parameter(name))
                    else:
                        parameter = returns.get(name, Parameter(name))

                    if "default" in argument:
                        parameter.kind = ParameterKind.optional
                    else:
                        parameter.kind = ParameterKind.positional

                parameter.annotation = self._decode(argument, "class", True)
                parameter.default = self._decode(argument, "default", True)
                parameter.comment = self._comment_docstring(
                    argument.get("comment", None), parent=model
                )

        model.parameters = (
            Parameters(*list(parameters.values())) if parameters else None
        )
        model.returns = Parameters(*list(returns.values())) if returns else None

        return model

    def _decode(
        self, capture: dict[str, list[Node]], key: str, first: bool = False
    ) -> list[str] | str | None:
        if key not in capture:
            return None
        else:
            decoded = [element.text.decode(self.encoding) for element in capture[key]]
            if first:
                return decoded[0]
            else:
                return decoded

    def _comment_docstring(
        self, nodes: list[Node] | Node | None, parent: MatlabObject | None = None
    ) -> Docstring | None:
        
        if nodes is None:
            return None
        elif isinstance(nodes, list):
            lineno = nodes[0].range.start_point.row + 1
            endlineno = nodes[-1].range.end_point.row + 1
            lines = iter(
                [
                    line
                    for lines in [
                        node.text.decode(self.encoding).splitlines() for node in nodes
                    ]
                    for line in lines
                ]
            )
        else:
            lineno = nodes.range.start_point.row + 1
            endlineno = nodes.range.end_point.row + 1
            lines = iter(nodes.text.decode(self.encoding).splitlines())

        docstring, uncommented = [], []

        while True:
            try:
                line = next(lines).lstrip()
            except StopIteration:
                break

            if "--8<--" in line:
                break

            if line[:2] == "%{" or line[:2] == "%%":
                if uncommented:
                    docstring += _dedent(uncommented)
                    uncommented = []
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
                docstring += _dedent(comment_block[1:])

            elif line[0] == "%":
                uncommented.append(line[1:])
            else:
                raise LookupError

        if uncommented:
            docstring += _dedent(uncommented)

        return Docstring(
            "\n".join(docstring),
            lineno=lineno,
            endlineno=endlineno,
            parent=parent,
        )
