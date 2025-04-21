"""Functions and classes for collecting MATLAB objects from paths."""

from __future__ import annotations

from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Callable, Sequence, TypeVar

from _griffe.collections import LinesCollection as GLC
from _griffe.collections import ModulesCollection


from mkdocstrings_handlers.matlab.models import (
    Class,
    Classfolder,
    Docstring,
    DocstringSectionText,
    Folder,
    MatlabMixin,
    Namespace,
    PathMixin,
    _ParentGrabber,
)
from mkdocstrings_handlers.matlab.treesitter import FileParser

PathType = TypeVar("PathType", bound=PathMixin)

__all__ = ["LinesCollection", "PathsCollection"]


class LinesCollection(GLC):
    """A simple dictionary containing the modules source code lines."""

    def __init__(self) -> None:
        """Initialize the collection."""
        self._data: dict[str, list[str]] = {}


class PathGlobber:
    """
    A class to recursively glob paths as MATLAB would do it.
    """

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
            elif member.is_file() and member.suffix == ".m" and member.name != "Contents.m":
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


class PathsCollection(ModulesCollection):
    """
    PathsCollection is a class that manages a collection of MATLAB paths and their corresponding models.

    Attributes:
        config (Mapping): Configuration settings for the PathsCollection.
        lines_collection (LinesCollection): An instance of LinesCollection for managing lines.

    Args:
        matlab_path (Sequence[str | Path]): A list of strings or Path objects representing the MATLAB paths.
        recursive (bool, optional): If True, recursively adds all subdirectories of the given paths to the search path. Defaults to False.
        config_path (Path | None, optional): The path to the configuration file. Defaults to None.

    Methods:
        members() -> dict:
            Returns a dictionary of members with their corresponding models.

        resolve(identifier: str, config: Mapping = {}) -> MatlabMixin | None:
            Resolves the given identifier to a model object.

        update_model(model: MatlabMixin, config: Mapping) -> MatlabMixin:
            Updates the given model object with the provided configuration.

        addpath(path: str | Path, to_end: bool = False, recursive: bool = False) -> list[Path]:
            Adds a path to the search path.

        rm_path(path: str | Path, recursive: bool = False) -> list[Path]:
            Removes a path from the search path and updates the namespace and database accordingly.

    """

    def __init__(
        self,
        matlab_path: Sequence[str | Path],
        recursive: bool = False,
        config_path: Path | None = None,
    ) -> None:
        """
        Initialize an instance of PathsCollection.

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
        self._members: dict[Path, list[tuple[str, Path]]] = defaultdict(list)
        self._folders: dict[Path, LazyModel] = {}
        self._config_path = config_path
        self.lines_collection = LinesCollection()

        for path in matlab_path:
            self.addpath(Path(path), to_end=True, recursive=recursive)

    @property
    def members(self):
        return {
            identifier: self._models[paths[0]].model()
            for identifier, paths in self._mapping.items()
        }

    def resolve(self, identifier: str):
        """
        Resolve an identifier to a MatlabMixin model.

        This method attempts to resolve a given identifier to a corresponding
        MatlabMixin model using the internal mapping and models. If the identifier
        is not found directly, it will attempt to resolve it by breaking down the
        identifier into parts and resolving each part recursively.

        Args:
            identifier (str): The identifier to resolve.

        Returns:
            MatlabMixin or None: The resolved MatlabMixin model if found, otherwise None.
        """

        # Find in global database
        if identifier in self._mapping:
            model = self._models[self._mapping[identifier][0]].model()

        elif self._config_path is not None and "/" in identifier:
            absolute_path = (self._config_path / Path(identifier)).resolve()
            if absolute_path.exists():
                if absolute_path.suffix:
                    path, member = absolute_path.parent, absolute_path.stem
                else:
                    path, member = absolute_path, None
                lazymodel = self._folders.get(path, None)

                if lazymodel is not None:
                    model = lazymodel.model()
                    if model is not None and member is not None:
                        model = model.members.get(member, None)
                else:
                    model = None
            else:
                model = None

        else:
            model = None
            name_parts = identifier.split(".")
            if len(name_parts) > 1:
                base = self.resolve(".".join(name_parts[:-1]))
                if base is None or name_parts[-1] not in base.members:
                    model = None
                else:
                    model = base.members[name_parts[-1]]
            else:
                model = None

        if isinstance(model, MatlabMixin):
            return model
        return None

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

        for member in PathGlobber(path, recursive=recursive):
            model = LazyModel(member, self)
            self._models[member] = model
            self._mapping[model.name].append(member)
            self._members[path].append((model.name, member))

            if self._config_path is not None and member.parent.stem[0] not in [
                "+",
                "@",
            ]:
                if member.parent.is_relative_to(self._config_path):
                    if member.parent not in self._folders:
                        self._folders[member.parent] = LazyModel(member.parent, self)
                else:
                    pass  # TODO: Issue warning?

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

        for name, member in self._members.pop(path):
            self._mapping[name].remove(member)
            self._models.pop(member)

        if recursive:
            for subdir in [item for item in self._path if _is_subdirectory(path, item)]:
                self.rm_path(subdir, recursive=False)

    def get_inheritance_diagram(self, model: Class) -> DocstringSectionText | None:
        def get_id(str: str) -> str:
            return str.replace(".", "_")

        def get_nodes(model: Class, nodes: set[str] = set()) -> set[str]:
            nodes.add(f"   {get_id(model.name)}[{model.name}]")
            for base in [str(base) for base in model.bases]:
                super = self.resolve(base)
                if super is None:
                    nodes.add(f"   {get_id(base)}[{base}]")
                else:
                    if isinstance(super, Class):
                        get_nodes(super, nodes)
            return nodes

        def get_links(model: Class, links: set[str] = set()) -> set[str]:
            for base in [str(base) for base in model.bases]:
                super = self.resolve(base)
                if super is None:
                    links.add(f"   {get_id(base)} --> {get_id(model.name)}")
                else:
                    links.add(f"   {get_id(super.name)} --> {get_id(model.name)}")
                    if isinstance(super, Class):
                        get_links(super, links)
            return links

        nodes = get_nodes(model)
        if len(nodes) == 1:
            return None

        nodes_str = "\n".join(list(nodes))
        links_str = "\n".join(list(get_links(model)))
        section = f"```mermaid\nflowchart TB\n{nodes_str}\n{links_str}\n```"

        return DocstringSectionText(section, title="Inheritance Diagram")


def _is_subdirectory(parent_path: Path, child_path: Path) -> bool:
    try:
        child_path.relative_to(parent_path)
    except ValueError:
        return False
    else:
        return True


class LazyModel:
    """
    A class to lazily collect and model MATLAB objects from a given path.

    Methods:
        is_class_folder: Checks if the path is a class folder.
        is_namespace: Checks if the path is a namespace.
        is_in_namespace: Checks if the path is within a namespace.
        name: Returns the name of the MATLAB object, including namespace if applicable.
        model: Collects and returns the MATLAB object model..
    """

    def __init__(self, path: Path, paths_collection: PathsCollection):
        self._path: Path = path
        self._model: MatlabMixin | None = None
        self._paths_collection: PathsCollection = paths_collection
        self._lines_collection: LinesCollection = paths_collection.lines_collection

    @property
    def is_folder(self) -> bool:
        return self._path.is_dir() and self._path.name[0] not in ["+", "@"]

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

    def model(self) -> MatlabMixin | None:
        if not self._path.exists():
            return None

        if self._model is None:
            if self.is_class_folder:
                self._model = self._collect_classfolder(self._path)
            elif self.is_namespace:
                self._model = self._collect_namespace(self._path)
            elif self.is_folder:
                self._model = self._collect_folder(self._path)
            else:
                self._model = self._collect_path(self._path)
        if self._model is not None:
            self._model.parent = self._collect_parent(self._path.parent)
        return self._model

    def _collect_parent(self, path: Path) -> _ParentGrabber | None:
        if self.is_in_namespace:
            grabber: Callable[[], MatlabMixin | None] = self._paths_collection._models[path].model
            parent = _ParentGrabber(grabber)
        else:
            parent = None
        return parent

    def _collect_path(self, path: Path, **kwargs: Any) -> MatlabMixin:
        file = FileParser(path)
        model = file.parse(paths_collection=self._paths_collection, **kwargs)
        self._lines_collection[path] = file.content.split("\n")
        return model

    def _collect_directory(self, path: Path, model: PathType) -> PathType:
        for member in path.iterdir():
            if member.is_dir() and member.name[0] in ["+", "@"]:
                submodel = self._paths_collection._models[member].model()
                if submodel is not None:
                    model.members[submodel.name] = submodel

            elif member.is_file() and member.suffix == ".m":
                if member.name == "Contents.m":
                    contentsfile = self._collect_path(member)
                    model.docstring = contentsfile.docstring
                else:
                    submodel = self._paths_collection._models[member].model()
                    if submodel is not None:
                        model.members[submodel.name] = submodel

        if model.docstring is None:
            model.docstring = self._collect_readme_md(path, model)

        return model

    def _collect_classfolder(self, path: Path) -> Classfolder | None:
        classfile = path / (path.name[1:] + ".m")
        if not classfile.exists():
            return None
        model = self._collect_path(classfile)
        if not isinstance(model, Classfolder):
            return None
        for member in path.iterdir():
            if member.is_file() and member.suffix == ".m" and member != classfile:
                if member.name == "Contents.m" and model.docstring is None:
                    contentsfile = self._collect_path(member)
                    model.docstring = contentsfile.docstring
                else:
                    method = self._collect_path(member)
                    method.parent = model
                    model.members[method.name] = method
        if model.docstring is None:
            model.docstring = self._collect_readme_md(path, model)
        return model

    def _collect_namespace(self, path: Path) -> Namespace:
        name = self.name[1:].split(".")[-1]
        model = Namespace(name, filepath=path, paths_collection=self._paths_collection)
        return self._collect_directory(path, model)

    def _collect_folder(self, path: Path) -> Folder:
        name = path.stem
        model = Folder("/" + name, filepath=path, paths_collection=self._paths_collection)
        return self._collect_directory(path, model)

    def _collect_readme_md(self, path, parent: PathMixin) -> Docstring | None:
        if (path / "README.md").exists():
            readme = path / "README.md"
        elif (path / "readme.md").exists():
            readme = path / "readme.md"
        else:
            return None

        with open(readme, "r") as file:
            content = file.read()
        return Docstring(content, parent=parent)
