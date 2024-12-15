# %%

from _griffe.docstrings.google import _read_block_items_maybe, _get_name_annotation_description, parse_docstring_annotation, _annotation_from_parent 
from mkdocstrings_handlers.matlab.collect import PathCollection
from mkdocstrings_handlers.matlab.models import Docstring
from pathlib import Path


path = Path(__file__).parent / "src"


path_collection = PathCollection([path])


# %%
model = path_collection.resolve("myfunction")
docstring = model.docstring
# %%

text = '\n'.join([
    '% Perform some operation using the input arguments.',
    '%',
    '% Returns:',
    '%   output1: Overruled documentation of output1',
    '%   output2 (double): Overruled documentation of output2',
])
docstring = Docstring(text)
offset = 0
returns_multiple_items = True
returns_named_value = True
options = {}


block, new_offset = _read_block_items_maybe(
    docstring,
    offset=offset,
    multiple=returns_multiple_items,
    **options,
)

for index, (line_number, yield_lines) in enumerate(block):
    try:
        name, annotation, description = _get_name_annotation_description(
            docstring,
            line_number,
            yield_lines,
            named=returns_named_value,
        )
    except ValueError:
        continue

    if annotation:
        # try to compile the annotation to transform it into an expression
        annotation = parse_docstring_annotation(annotation, docstring)
    else:
        # try to retrieve the annotation from the docstring parent
        annotation = _annotation_from_parent(docstring, gen_index=0, multiple=len(block) > 1, index=index)

    print(annotation)
# %%
