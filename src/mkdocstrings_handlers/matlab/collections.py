from _griffe.collections import LinesCollection as _LinesCollection, ModulesCollection
from _griffe.models import Object


class LinesCollection(_LinesCollection):
    pass


class ModelsCollection(ModulesCollection):
    def __init__(self):
        self.members: dict[str, Object] = {}

    def __setitem__(self, key: str, value: Object):
        self.members[key] = value

    def __getitem__(self, key: str):
        return self.members[key]
