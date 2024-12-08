# %%
from tree_sitter import Language, Parser, Node, TreeCursor
import tree_sitter_matlab as tsmatlab

from pathlib import Path

import charset_normalizer

import mkdocstrings_handlers.matlab.models as models

LANGUAGE = Language(tsmatlab.language())
parser = Parser(LANGUAGE)


def _dedent_lines(lines: list[str]) -> list[str]:
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


def comment_node_docstring(node: Node) -> list[str]:
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
                docstring += _dedent_lines(comment_lines)
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
            docstring += _dedent_lines(comment_block[1:])

        elif line[0] == "%":
            comment_lines.append(line[1:])
        else:
            raise LookupError

    if comment_lines:
        docstring += _dedent_lines(comment_lines)

    return docstring

#%%

def parse_function(cursor: TreeCursor) -> models.Function:

    docstring = []
    doclineno, docendlineno = 0, 0
    used_arguments = False
    kwargs = dict(lineno=cursor.node.start_point.row, endlineno=cursor.node.end_point.row)

    cursor.goto_first_child()

    while cursor.goto_next_sibling():
        match cursor.node.type:
            case "function_output":
                cursor.goto_first_child()
                if cursor.node.type == "identifier":
                    returns = [models.Parameter(cursor.node.text.decode(encoding))]
                else:
                    cursor.goto_first_child()
                    returns = []
                    while cursor.goto_next_sibling():
                        if cursor.node.type == "identifier":
                            returns.append(models.Parameter(cursor.node.text.decode(encoding)))
                    cursor.goto_parent()
                kwargs["returns"] = models.Parameters(*returns)
                cursor.goto_parent()

            case "identifier":
                identifier = cursor.node.text.decode(encoding)

            case "function_arguments":
                cursor.goto_first_child()
                parameters = []
                while cursor.goto_next_sibling():
                    if cursor.node.type == "identifier":
                        parameters.append(models.Parameter(cursor.node.text.decode(encoding)))
                kwargs["parameters"] = models.Parameters(*parameters)
                cursor.goto_parent()

            case "comment":
                if used_arguments: 
                    continue
                if not doclineno:
                    doclineno = cursor.node.start_point.row
                docendlineno = cursor.node.end_point.row 
                docstring += comment_node_docstring(cursor.node)

            case "arguments_statement":
                used_arguments = True
                
                arguments_type = "parameters"
                cursor.goto_first_child()
                while cursor.goto_next_sibling():
                    if cursor.node.type == "attributes":
                        if 'Output' in cursor.node.text.decode(encoding):
                            arguments_type = "returns"
                    elif cursor.node.type == "property":
                        
                        parameters = kwargs[arguments_type]

                        cursor.goto_first_child()
                        identifier = cursor.node.text.decode(encoding)

                        if '.' in identifier:
                            kwargsvar = identifier.split('.')[0]
                            kwargsparameter = next((p for p in parameters if p.name == kwargsvar), None)
                            if kwargsparameter:
                                parameters._params.remove(kwargsparameter)
                            identifier = identifier.split('.')[-1]
                            parameter = models.Parameter(identifier, kind=models.ParameterKind.keyword_only)
                            parameters._params.append(parameter)
                        else:
                            parameter = next((p for p in parameters if p.name == identifier), None)
                            if identifier == "varargin":
                                parameter.kind=models.ParameterKind.var_keyword
                            else:
                                parameter.kind=models.ParameterKind.positional

                        while cursor.goto_next_sibling():
                            match cursor.node.type:
                                case 'dimensions':
                                    # Do nothing with dimensions for now
                                    continue
                                case 'identifier':
                                    parameter.annotation = cursor.node.text.decode(encoding)
                                case 'validation_functions':
                                    # Do nothing with validation functions for now
                                    continue
                                case 'default_value':
                                    parameter.default = cursor.node.text.decode(encoding)[1:].strip()
                                    if parameter.kind is models.ParameterKind.positional:
                                        parameter.kind = models.ParameterKind.optional
                                case 'comment':
                                    parameter.docstring = '\n'.join(comment_node_docstring(cursor.node))
                        cursor.goto_parent()
                cursor.goto_parent()

            case "end" | "block":
                break

    if docstring:
        kwargs["docstring"] = models.Docstring('\n'.join(docstring), lineno=doclineno, endlineno=docendlineno)

    return models.Function(identifier, **kwargs, )


# %%
filepath = Path(__file__).parents[3] / "test" / "src" / "myfunction.m"
encoding = charset_normalizer.from_path(filepath).best().encoding
with open(filepath, "rb") as f:
    content = f.read()

tree = parser.parse(content)
cursor = tree.walk()
cursor.goto_first_child()

header_comment = []
doclineno, docendlineno = 0, 0

while True:
    if cursor.node.type == "function_definition":
        model = parse_function(cursor)
        break
    elif cursor.node.type == "class_definition":
        print("Must be a class")
        break
    elif cursor.node.type == "comment":
        header_comment += comment_node_docstring(cursor.node)
        if not doclineno:
            doclineno = cursor.node.start_point.row
        docendlineno = cursor.node.end_point.row
    else:
        print(f"Must be a script: {cursor.node.type}")
        break

    if not cursor.goto_next_sibling():
        break

if not model.docstring:
    model.docstring = models.Docstring('\n'.join(header_comment), lineno=doclineno, endlineno=docendlineno)

# %%
