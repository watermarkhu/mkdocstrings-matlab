from copy import deepcopy
from collections import defaultdict, deque
from pathlib import Path
from typing import Mapping

from _griffe.collections import LinesCollection as GLC, ModulesCollection


from mkdocstrings_handlers.matlab.models import (
    Class,
    Classfolder,
    DocstringSectionText,
    Function,
    MatlabObject,
    Namespace,
    Script,
    ROOT,
)
from mkdocstrings_handlers.matlab.treesitter import parse_file


__all__ = ["LinesCollection", "PathCollection"]


class LinesCollection(GLC):
    """A simple dictionary containing the modules source code lines."""

    def __init__(self) -> None:
        """Initialize the collection."""
        self._data: dict[str, list[str]] = {}


class PathGlobber:
    def __init__(self, path: Path, recursive: bool = False):
        self._idx = 0
        self._paths: list[Path] = []
        self._glob(path, recursive)

    def _glob(self, path: Path, recursive: bool = False):
        for member in path.iterdir():
            if (
                member.is_dir()
                and recursive
                and member.stem[0] not in ["+", "@"]
                and member.stem != "private"
            ):
                self._glob(member, recursive=True)
            elif member.is_dir() and member.stem[0] == "+":
                self._paths.append(member)
                self._glob(member)
            elif member.is_dir() and member.stem[0] == "@":
                self._paths.append(member)
            elif (
                member.is_file()
                and member.suffix == ".m"
                and member.name != "Contents.m"
            ):
                self._paths.append(member)

    def max_stem_length(self) -> int:
        return max(len(path.stem) for path in self._paths)

    def __len__(self):
        return len(self._paths)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            item = self._paths[self._idx]
        except IndexError as err:
            raise StopIteration from err
        self._idx += 1
        return item


class PathCollection(ModulesCollection):
    """
    Represents a search path for MATLAB paths.
    """

    def __init__(
        self,
        matlab_path: list[str | Path],
        config: Mapping = {},
    ) -> None:
        """
        Initialize an instance of PathCollection.

        Args:
            matlab_path (list[str | Path]): A list of strings or Path objects representing the MATLAB paths.

        Raises:
            TypeError: If any element in matlab_path is not a string or Path object.

        """
        for path in matlab_path:
            if not isinstance(path, (str, Path)):
                raise TypeError(f"Expected str or Path, got {type(path)}")

        self._path: deque[Path] = deque()
        self._mapping: dict[str, deque[Path]] = defaultdict(deque)
        self._models: dict[Path, LazyModel] = {}
        self.config = config
        self.lines_collection = LinesCollection()

        for path in matlab_path:
            self.addpath(Path(path), to_end=True)

    @property
    def members(self):
        return {
            name: self._models[paths[0]].model for name, paths in self._mapping.items()
        }

    def resolve(
        self,
        name: str,
        config: Mapping = {},
    ) -> MatlabObject | None:
        """
        Resolves the given name to a model object.
        """

        # Find in global database
        if name not in self._mapping:
            return None

        model = self._models[self._mapping[name][0]].model

        if isinstance(model, Class) and "Inheritance Diagram" not in model.docstring.parsed:
            model.docstring.parsed.append(self.get_inheritance_diagram(model))
                
        self.update_member_docstring_attributes(model, config)

        return model
    
    def update_member_docstring_attributes(self, model: MatlabObject, config: Mapping):
        if hasattr(model, "docstring") and model.docstring is not None:
            model.docstring.parser = config.get("docstring_style", "google")
            model.docstring.parser_options = config.get("docstring_options", {})
            model.docstring.section_style = config.get("docstring_section_style", "table")

        for member in getattr(model, "members", {}).values():
            self.update_member_docstring_attributes(member, config)
            


    def addpath(self, path: str | Path, to_end: bool = False, recursive: bool = False):
        """
        Add a path to the search path.

        Args:
            path (str | Path): The path to be added.
            to_end (bool, optional): Whether to add the path to the end of the search path. Defaults to False.

        Returns:
            list[Path]: The previous search path before adding the new path.
        """
        if isinstance(path, str):
            path = Path(path)

        if path in self._path:
            self._path.remove(path)

        if to_end:
            self._path.append(path)
        else:
            self._path.appendleft(path)

        members = PathGlobber(path, recursive=recursive)
        for member in members:
            model = LazyModel(member, self)
            self._models[member] = model
            self._mapping[model.name].append(member)

    def rm_path(self, path: str | Path, recursive: bool = False):
        """
        Removes a path from the search path and updates the namespace and database accordingly.

        Args:
            path (str | Path): The path to be removed from the search path.
            recursive (bool, optional): If True, recursively removes all subdirectories of the given path from the search path. Defaults to False.

        Returns:
            list[Path]: The previous search path before the removal.

        """
        if isinstance(path, str):
            path = Path(path)

        if path not in self._path:
            return list(self._path)

        self._path.remove(path)

        for name, member in self._path_members.pop(path):
            self._mapping[name].remove(member)
            self._models.pop(member)

        if recursive:
            for subdir in [item for item in self._path if _is_subdirectory(path, item)]:
                self.rm_path(subdir, recursive=False)

    def get_inheritance_diagram(self, model: Class) -> DocstringSectionText:
        def get_id(str: str) -> str:
            return str.replace(".", "_")

        def get_nodes(model: Class, nodes: set[str] = set()) -> set[str]:
            nodes.add(f"   {get_id(model.name)}[{model.name}]")
            for base in model.bases:
                super = self.resolve(base)
                if super is None:
                    nodes.add(f"   {get_id(base)}[{base}]")
                else:
                    get_nodes(super, nodes)
            return nodes

        def get_links(model: Class, links: set[str] = set()) -> set[str]:
            for base in model.bases:
                super = self.resolve(base)
                if super is None:
                    links.add(f"   {get_id(model.name)} --> {get_id(base)}")
                else:
                    links.add(f"   {get_id(model.name)} --> {get_id(super.name)}")
                    get_links(super, links)
            return links

        nodes_str = "\n".join(list(get_nodes(model)))
        links_str = "\n".join(list(get_links(model)))
        section = f"## Inheritance Diagram\n\n```mermaid\nflowchart BT\n{nodes_str}\n{links_str}\n```"

        return DocstringSectionText(section, title="Inheritance Diagram")


def _is_subdirectory(parent_path: Path, child_path: Path) -> bool:
    try:
        child_path.relative_to(parent_path)
    except ValueError:
        return False
    else:
        return True


class LazyModel:
    def __init__(
        self, path: Path, path_collection: PathCollection
    ) -> MatlabObject | None:
        self._path: Path = path
        self._model: MatlabObject | None = None
        self._path_collection: PathCollection = path_collection
        self._lines_collection: LinesCollection = path_collection.lines_collection

    @property
    def is_class_folder(self) -> bool:
        return self._path.is_dir() and self._path.name[0] == "@"

    @property
    def is_namespace(self) -> bool:
        return self._path.name[0] == "+"
    
    @property
    def is_in_namespace(self) -> bool:
        return self._path.parent.name[0] == "+"

    @property
    def name(self):
        if self.is_in_namespace:
            parts = list(self._path.parts)
            item = len(parts) - 2
            nameparts = []
            while item >= 0:
                if parts[item][0] != "+":
                    break
                nameparts.append(parts[item][1:])
                item -= 1
            nameparts.reverse()
            namespace = ".".join(nameparts) + "."
        else:
            namespace = ""

        if self.is_class_folder or self.is_namespace:
            name = namespace + self._path.name[1:]
        else:
            name = namespace + self._path.stem

        if self.is_namespace:
            return "+" + name
        else:
            return name

    @property
    def model(self):
        if not self._path.exists():
            return None

        if self._model is None:
            if self.is_class_folder:
                self._model = self._collect_classfolder(self._path)
            elif self.is_namespace:
                self._model = self._collect_namespace(self._path)
            else:
                self._model = self._collect_path(self._path)
        self._model._parent = self._collect_parent(self._path.parent)
        return self._model
    
    def _collect_parent(self, path: Path):
        if self.is_in_namespace:
            parent = self._path_collection._models[path]
        else:
            parent = ROOT
        return parent

    def _collect_path(self, path: Path) -> MatlabObject:
        model, content = parse_file(path, path_collection=self._path_collection)
        lines = content.split("\n")
        self._lines_collection[path] = lines
        return model
    
    def _collect_classfolder(self, path: Path) -> Classfolder | None: 
        classfile = path / (path.name[1:] + ".m")
        if not classfile.exists():
            return None
        model = self._collect_path(classfile)

        for member in path.iterdir():
            if (
                member.is_file()
                and member.suffix == ".m"
                and member.name != "Contents.m"
                and member != classfile
            ):
                method = self._collect_path(member)
                method.parent = model
                model.members[method.name] = method
        return model

    def _collect_namespace(self, path: Path) -> Namespace:

        name = self.name[1:].split(".")[-1]
        model = Namespace(name, filepath=path, path_collection=self._path_collection)

        for member in path.iterdir():
            if member.is_dir() and member.name[0] in ["+", "@"]:
                submodel = self._path_collection._models[member].model
                if submodel is not None:
                    model.members[submodel.name] = submodel

            elif member.is_file() and member.suffix == ".m":
                if member.name == "Contents.m":
                    contentsfile = self._collect_path(member, path)
                    contentsfile.docstring = model.docstring
                else:
                    submodel = self._path_collection._models[member].model
                    if submodel is not None:
                        model.members[submodel.name] = submodel
        return model