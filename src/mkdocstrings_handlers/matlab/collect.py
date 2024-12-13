from collections import defaultdict, deque
from pathlib import Path
from typing import Mapping

from _griffe.collections import LinesCollection as GLC, ModulesCollection


from mkdocstrings_handlers.matlab.models import (
    MatlabObject,
    DocstringSectionText,
    Function,
    Class,
    Script,
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

        model.docstring.parser = config.get("docstring_style", "google")
        model.docstring.parser_options = config.get("docstring_options", {})

        match model:
            case Script():
                pass
            case Function():
                pass
            case Class():
                if config.get("show_inheritance_diagram"):
                    model.docstring.parsed.append(self.get_inheritance_diagram(model))

                if config.get("merge_init_into_class") and model.name in model.members:
                    constructor = model.members.pop(model.name)
                    model.docstring.parsed.extend(constructor.docstring.parsed)
            case _:
                return None, []

        return model

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
            id = get_id(model.name)
            nodes.add(f"   {id}[{model.name}]")
            for base in [self.resolve(base) for base in model.bases]:
                if base is not None:
                    get_nodes(base, nodes)
            return nodes

        def get_links(model: Class, links: set[str] = set()) -> set[str]:
            for base in [self.resolve(base) for base in model.bases]:
                if base is not None:
                    links.add(f"   {get_id(model.name)} --> {get_id(base.name)}")
                    get_links(base, links)
            return links

        nodes_str = "\n".join(list(get_nodes(model)))
        links_str = "\n".join(list(get_links(model)))
        section = f"```mermaid\nflowchart BT\n{nodes_str}\n{links_str}\n```"

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

        if self.is_class_folder:
            return namespace + self._path.name[1:]
        else:
            return namespace + self._path.stem

    @property
    def model(self):
        if not self._path.exists():
            return None

        if self._model is None:
            if self.is_class_folder:
                classfile = self._path / (self._path.name[1:] + ".m")
                if not classfile.exists():
                    return None
                self._model, self._lines_collection[classfile] = self.collect_path(
                    classfile
                )

                for member in self._path.iterdir():
                    if (
                        member.is_file()
                        and member.suffix == ".m"
                        and member.name != "Contents.m"
                        and member != classfile
                    ):
                        method, lines = self.collect_path(member)
                        self._model.members[method.name] = method
                        self._lines_collection[method.filepath] = lines
            else:
                self._model, self._lines_collection[self._path] = self.collect_path(
                    self._path
                )

        return self._model

    def collect_path(self, path: Path) -> tuple[MatlabObject, list[str]]:
        model, content = parse_file(path, path_collection=self._path_collection)
        lines = content.split("\n")
        return model, lines
