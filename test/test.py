# %%

from mkdocstrings_handlers.matlab.collect import PathCollection
from pathlib import Path


path = Path(__file__).parent / "src"


path_collection = PathCollection([path])

print(path_collection.members)

# %%
model = path_collection.resolve("myfunction")
