# %%

from mkdocstrings_handlers.matlab.collect import PathCollection
from pathlib import Path


path = Path(__file__).parent / "src"


path_collection = PathCollection([path])

path_collection.members

# %%
model = path_collection.resolve("DocumentationFramework")
# %%
model.inherited_members
# %%
model = path_collection.resolve("myNamespace.myClass")
model.members["myClass"].lines
# %%
