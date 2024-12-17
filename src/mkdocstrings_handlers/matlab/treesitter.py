# %%
from collections import OrderedDict
from typing import Any

from tree_sitter import Language, Parser, Node
import tree_sitter_matlab as tsmatlab

from pathlib import Path

import charset_normalizer

from mkdocstrings_handlers.matlab.models import (
    AccessEnum,
    Class,
    Classfolder,
    Docstring,
    Function,
    MatlabObject,
    Parameters,
    Parameter,
    Property,
    Script,
)
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
    [
        ("set.") @setter
        ("get.") @getter
    ]? .
    (identifier) @name .
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
    (dimensions)? @dimensions .
    (identifier)? @class .
    (validation_functions)? @validators .
    (default_value
        ("=") .
        _+ @default
    )? .
    (comment)* @comment              
)""")


ATTRIBUTE_QUERY = LANGUAGE.query("""(attribute
    (identifier) @name .
    (
        ("=") .
        _+ @value
    )?
)""")


CLASS_QUERY = LANGUAGE.query("""("classdef" .
    (attributes
        (attribute) @attributes
    )? .
    (identifier) @name ?
    (superclasses
        (property_name)+ @bases             
    )? .
    (comment)* @docstring .
    ("\\n")? .
    [
        (methods) @methods
        (properties) @properties
        (enumeration) @enumeration
    ]*
)""")


METHODS_QUERY = LANGUAGE.query("""("methods" .
    (attributes
        (attribute) @attributes
    )? .
    ("\\n")? .
    (function_definition)* @methods
)""")

PROPERTIES_QUERY = LANGUAGE.query("""("properties" .
    (attributes
        (attribute) @attributes
    )? .
    ("\\n")? .
    (property)* @properties
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


class FileParser(object):
    def __init__(self, filepath: Path):
        self.filepath: Path = filepath
        result = charset_normalizer.from_path(filepath).best()
        self.encoding: str = result.encoding if result else "utf-8"
        with open(filepath, "rb") as f:
            self._content: bytes = f.read()

    @property
    def content(self):
        return self._content.decode(self.encoding)

    def parse(self, **kwargs) -> MatlabObject:
        tree = PARSER.parse(self._content)
        cursor = tree.walk()

        if cursor.node is None:
            raise ValueError(f"The file {self.filepath} could not be parsed.")
        captures = FILE_QUERY.captures(cursor.node)

        if "function" in captures:
            model = self._parse_function(captures["function"][0], **kwargs)
        elif "class" in captures:
            model = self._parse_class(captures["class"][0], **kwargs)
        else:
            model = Script(self.filepath.stem, filepath=self.filepath, **kwargs)

        if not model.docstring:
            model.docstring = self._comment_docstring(
                captures.get("header", None), parent=model
            )

        return model

    def _parse_class(self, node: Node, **kwargs) -> Class:
        saved_kwargs = {key: value for key, value in kwargs.items()}
        captures = CLASS_QUERY.captures(node)

        bases = self._decode_from_capture(captures, "bases")
        docstring = self._comment_docstring(captures.get("docstring", None))

        attribute_pairs = [
            self._parse_attribute(node) for node in captures.get("attributes", [])
        ]
        for key, value in attribute_pairs:
            if key in ["Sealed", "Abstract", "Hidden"]:
                kwargs[key] = value

        if self.filepath.parent.stem[0] == "@":
            model = Classfolder(
                self.filepath.stem,
                bases=bases,
                docstring=docstring,
                filepath=self.filepath,
                **kwargs,
            )
        else:
            model = Class(
                self.filepath.stem,
                bases=bases,
                docstring=docstring,
                filepath=self.filepath,
                **kwargs,
            )

        for property_captures in [
            PROPERTIES_QUERY.captures(node) for node in captures.get("properties", [])
        ]:
            property_kwargs = {key: value for key, value in saved_kwargs.items()}
            attribute_pairs = [
                self._parse_attribute(node)
                for node in property_captures.get("attributes", [])
            ]
            for key, value in attribute_pairs:
                if key in [
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
                    property_kwargs[key] = value
                elif key in ["GetAccess", "SetAccess"]:
                    if value in ["public", "protected", "private", "immutable"]:
                        property_kwargs[key] = AccessEnum(value)
                    else:
                        property_kwargs[key] = AccessEnum.PRIVATE
            for property_node in property_captures.get("properties", []):
                property_captures = PROPERTY_QUERY.captures(property_node)

                prop = Property(
                    self._first_from_capture(property_captures, "name"),
                    annotation=self._first_from_capture(property_captures, "class"),
                    value=self._decode_from_capture(property_captures, "default"),
                    docstring=self._comment_docstring(
                        property_captures.get("comment", None)
                    ),
                    parent=model,
                )
                model.members[prop.name] = prop

        for method_captures in [
            METHODS_QUERY.captures(node) for node in captures.get("methods", [])
        ]:
            method_kwargs = {key: value for key, value in saved_kwargs.items()}
            attribute_pairs = [
                self._parse_attribute(node)
                for node in method_captures.get("attributes", [])
            ]
            for key, value in attribute_pairs:
                if key in [
                    "Abstract",
                    "Hidden",
                    "Sealed",
                    "Static",
                ]:
                    method_kwargs[key] = value
                elif key in ["GetAccess", "SetAccess"]:
                    if value in ["public", "protected", "private", "immutable"]:
                        method_kwargs[key] = AccessEnum(value)
                    else:
                        method_kwargs[key] = AccessEnum.PRIVATE
            for method_node in method_captures.get("methods", []):
                method = self._parse_function(
                    method_node, method=True, parent=model, **method_kwargs
                )
                if (
                    method.name != self.filepath.stem
                    and not method.static
                    and method.parameters
                ):
                    # Remove self from first method argument
                    method.parameters._params = method.parameters._params[1:]
                if method._is_getter and method.name in model.members:
                    prop = model.members[method.name]
                    if isinstance(prop, Property):
                        prop.getter = method
                    else:
                        # This can be either an error or that it is a getter in an inherited class
                        pass
                elif method._is_setter and method.name in model.members:
                    prop = model.members[method.name]
                    if isinstance(prop, Property):
                        prop.setter = method
                    else:
                        # This can be either an error or that it is a setter in an inherited class
                        pass
                else:
                    model.members[method.name] = method

        return model

    def _parse_attribute(self, node: Node) -> tuple[str, Any]:
        captures = ATTRIBUTE_QUERY.captures(node)

        key = self._first_from_capture(captures, "name")
        if "value" not in captures:
            value = True
        elif captures["value"][0].type == "boolean":
            value = _strtobool(self._first_from_capture(captures, "value"))
        else:
            value = self._first_from_capture(captures, "value")

        return (key, value)

    def _parse_function(self, node: Node, method: bool = False, **kwargs) -> Function:
        captures: dict = FUNCTION_QUERY.captures(node)

        input_names = self._decode_from_capture(captures, "input")
        parameters: dict = (
            OrderedDict(
                (name, Parameter(name, kind=ParameterKind.positional))
                for name in input_names
            )
            if input_names
            else {}
        )
        output_names = self._decode_from_capture(captures, "output")
        returns: dict = (
            OrderedDict(
                (name, Parameter(name, kind=ParameterKind.positional))
                for name in output_names
            )
            if output_names
            else {}
        )
        if method:
            name = self._first_from_capture(captures, "name")
        else:
            name = self.filepath.stem

        model = Function(
            name,
            filepath=self.filepath,
            docstring=self._comment_docstring(captures.get("docstring", None)),
            getter="getter" in captures,
            setter="setter" in captures,
            **kwargs,
        )

        captures_arguments = [
            ARGUMENTS_QUERY.captures(node) for node in captures.get("arguments", [])
        ]
        for arguments in captures_arguments:
            attributes = self._decode_from_capture(arguments, "attributes")
            is_input = (
                attributes is None
                or "Input" in attributes
                or "Output" not in attributes
            )
            # is_repeating = "Repeating" in attributes

            captures_argument = [
                PROPERTY_QUERY.captures(node) for node in arguments["arguments"]
            ]
            for argument in captures_argument:
                name = self._first_from_capture(argument, "name")

                if "options" in argument:
                    options_name = self._first_from_capture(argument, "options")
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

                parameter.annotation = self._first_from_capture(argument, "class")
                parameter.default = self._first_from_capture(argument, "default")
                parameter.docstring = self._comment_docstring(
                    argument.get("comment", None), parent=model
                )

        model.parameters = Parameters(*list(parameters.values()))
        model.returns = Parameters(*list(returns.values())) if returns else None

        return model

    def _decode(self, node: Node) -> str:
        return (
            node.text.decode(self.encoding)
            if node is not None and node.text is not None
            else ""
        )

    def _decode_from_capture(
        self, capture: dict[str, list[Node]], key: str
    ) -> list[str]:
        if key not in capture:
            return []
        else:
            return [self._decode(element) for element in capture[key]]

    def _first_from_capture(self, capture: dict[str, list[Node]], key: str) -> str:
        decoded = self._decode_from_capture(capture, key)
        if decoded:
            return decoded[0]
        else:
            return ""

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
                    for lines in [self._decode(node).splitlines() for node in nodes]
                    for line in lines
                ]
            )
        else:
            lineno = nodes.range.start_point.row + 1
            endlineno = nodes.range.end_point.row + 1
            lines = iter(self._decode(nodes).splitlines())

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
