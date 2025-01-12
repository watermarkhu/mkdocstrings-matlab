"""Functions and classes for collecting MATLAB objects from paths."""

from collections import defaultdict, deque
from copy import copy, deepcopy
from pathlib import Path
from typing import Mapping, Sequence, Callable, TypeVar

from _griffe.collections import LinesCollection as GLC, ModulesCollection
from _griffe.docstrings.models import (
    DocstringSectionOtherParameters,
    DocstringSectionParameters,
    DocstringSectionReturns,
    DocstringParameter,
    DocstringReturn,
)
from _griffe.enumerations import DocstringSectionKind
from _griffe.expressions import Expr

from mkdocstrings_handlers.matlab.enums import ParameterKind
from mkdocstrings_handlers.matlab.models import (
    _ParentGrabber,
    Class,
    Classfolder,
    Docstring,
    DocstringSectionText,
    Function,
    Folder,
    MatlabMixin,
    Namespace,
    PathMixin,
)
from mkdocstrings_handlers.matlab.treesitter import FileParser


PathType = TypeVar("PathType", bound=PathMixin)

__all__ = ["LinesCollection", "PathCollection"]


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
    PathCollection is a class that manages a collection of MATLAB paths and their corresponding models.

    Attributes:
        config (Mapping): Configuration settings for the PathCollection.
        lines_collection (LinesCollection): An instance of LinesCollection for managing lines.

    Args:
        matlab_path (Sequence[str | Path]): A list of strings or Path objects representing the MATLAB paths.
        recursive (bool, optional): If True, recursively adds all subdirectories of the given paths to the search path. Defaults to False.
        config (Mapping, optional): Configuration settings for the PathCollection. Defaults to {}.
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

        get_inheritance_diagram(model: Class) -> DocstringSectionText | None:
            Generates an inheritance diagram for the given class model.
    """

    def __init__(
        self,
        matlab_path: Sequence[str | Path],
        recursive: bool = False,
        config: Mapping = {},
        config_path: Path | None = None,
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
        self._members: dict[Path, list[tuple[str, Path]]] = defaultdict(list)
        self._folders: dict[str, LazyModel] = {}
        self._config_path = config_path

        self.config = config
        self.lines_collection = LinesCollection()

        for path in matlab_path:
            self.addpath(Path(path), to_end=True, recursive=recursive)

    @property
    def members(self):
        return {
            identifier: self._models[paths[0]].model()
            for identifier, paths in self._mapping.items()
        }

    def resolve(
        self,
        identifier: str,
        config: Mapping = {},
    ):
        """
        Resolve an identifier to a MatlabMixin model.

        This method attempts to resolve a given identifier to a corresponding
        MatlabMixin model using the internal mapping and models. If the identifier
        is not found directly, it will attempt to resolve it by breaking down the
        identifier into parts and resolving each part recursively.

        Args:
            identifier (str): The identifier to resolve.
            config (Mapping, optional): Configuration options to update the model. Defaults to an empty dictionary.

        Returns:
            MatlabMixin or None: The resolved MatlabMixin model if found, otherwise None.
        """

        # Find in global database
        if identifier in self._mapping:
            model = self._models[self._mapping[identifier][0]].model()
            if model is not None:
                model = self.update_model(model, config)

        elif self._config_path is not None and "/" in identifier:
            absolute_path = (self._config_path / Path(identifier)).resolve()
            if absolute_path.exists():
                path = absolute_path.relative_to(self._config_path)
                if path.suffix:
                    path, member = path.parent, path.stem
                else:
                    member = None
                lazymodel = self._folders.get(str(path), None)

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
                base = self.resolve(".".join(name_parts[:-1]), config=config)
                if base is None or name_parts[-1] not in base.members:
                    model = None
                else:
                    model = base.members[name_parts[-1]]
            else:
                model = None

        if isinstance(model, MatlabMixin):
            return model
        return None

    def update_model(self, model: MatlabMixin, config: Mapping) -> MatlabMixin:
        """
        Update the given model based on the provided configuration.

        This method updates the docstring parser and parser options for the model,
        patches return annotations for MATLAB functions, and optionally creates
        docstring sections from argument blocks. It also recursively updates
        members of the model and handles special cases for class constructors
        and inheritance diagrams.

        Args:
            model (MatlabMixin): The model to update.
            config (Mapping): The configuration dictionary.

        Returns:
            MatlabMixin: The updated model.
        """

        # Update docstring parser and parser options
        if hasattr(model, "docstring") and model.docstring is not None:
            model.docstring.parser = config.get("docstring_style", "google")
            model.docstring.parser_options = config.get("docstring_options", {})

        # Patch docstring section titles
        if model.docstring is not None:
            for section in model.docstring.parsed:
                match section.kind:
                    case DocstringSectionKind.attributes:
                        section.title = "Properties:"
                    case DocstringSectionKind.modules:
                        section.title = "Namespaces:"
                    case DocstringSectionKind.parameters:
                        section.title = "Input arguments:"
                    case DocstringSectionKind.returns:
                        section.title = "Output arguments:"
                    case DocstringSectionKind.other_parameters:
                        section.title = "Name-Value Arguments:"

        # Patch returns annotation
        # In _griffe.docstrings.<parser>.py the function _read_returns_section will enforce an annotation
        # on the return parameter. This annotation is grabbed from the parent. For MATLAB this is invalid.
        # Thus the return annotation needs to be patched back to a None.
        if (
            isinstance(model, Function)
            and model.docstring is not None
            and any(
                isinstance(doc, DocstringSectionReturns)
                for doc in model.docstring.parsed
            )
        ):
            section = next(
                doc
                for doc in model.docstring.parsed
                if isinstance(doc, DocstringSectionReturns)
            )
            for returns in section.value:
                if not isinstance(returns.annotation, Expr):
                    returns.annotation = None

        # previous updates do not edit the model attributes persistently
        # However, the following updates do edit the model attributes persistently
        # such as adding new sections to the docstring or editing its members.abs
        # Thus, we need to copy the model to avoid editing the original model
        alias = copy(model)
        alias.docstring = (
            deepcopy(model.docstring) if model.docstring is not None else None
        )
        alias.members = {key: value for key, value in model.members.items()}
        if isinstance(alias, Class):
            alias._inherited_members = None

        for name, member in getattr(alias, "members", {}).items():
            alias.members[name] = self.update_model(member, config)

        # Merge constructor docstring into class
        if (
            isinstance(alias, Class)
            and config.get("merge_constructor_into_class", False)
            and alias.name in alias.members
            and alias.members[alias.name].docstring is not None
        ):
            constructor = alias.members.pop(alias.name)
            if constructor.docstring is not None:
                if alias.docstring is None:
                    alias.docstring = Docstring("", parent=alias)

                if config.get("merge_constructor_ignore_summary", False):
                    alias.docstring._suffixes.extend(constructor.docstring.parsed[1:])
                else:
                    alias.docstring._suffixes.extend(constructor.docstring.parsed)

        # Hide hidden members (methods and properties)
        hidden_members = config.get("hidden_members", False)
        if isinstance(hidden_members, bool):
            filter_hidden = not hidden_members
            show_hidden = []
        else:
            filter_hidden = True
            show_hidden: list[str] = hidden_members
        if isinstance(alias, Class) and filter_hidden:
            alias.members = {
                key: value
                for key, value in alias.members.items()
                if not getattr(value, "Hidden", False)
                or (
                    show_hidden
                    and getattr(value, "Hidden", False)
                    and key in show_hidden
                )
            }
            alias._inherited_members = {
                key: value
                for key, value in alias.inherited_members.items()
                if not getattr(value, "Hidden", False)
                or (
                    show_hidden
                    and getattr(value, "Hidden", False)
                    and key in show_hidden
                )
            }

        # Hide private members (methods and properties)
        private_members = config.get("private_members", False)
        if isinstance(private_members, bool):
            filter_private = not private_members
            show_private = []
        else:
            filter_private = True
            show_private: list[str] = private_members
        if isinstance(alias, Class) and filter_private:
            alias.members = {
                key: value
                for key, value in alias.members.items()
                if not getattr(value, "Private", False)
                or (
                    show_private
                    and getattr(value, "Private", False)
                    and key in show_private
                )
            }
            alias._inherited_members = {
                key: value
                for key, value in alias.inherited_members.items()
                if not getattr(value, "Private", False)
                or (
                    show_private
                    and getattr(value, "Private", False)
                    and key in show_private
                )
            }

        # Create parameters and returns sections from argument blocks
        if (
            isinstance(alias, Function)
            and alias.docstring is not None
            and config.get("parse_arguments", True)
            and (
                config.get("show_docstring_input_arguments", True)
                or config.get("show_docstring_name_value_arguments", True)
                or config.get("show_docstring_output_arguments", True)
            )
        ):
            docstring_parameters = any(
                isinstance(doc, DocstringSectionParameters)
                for doc in alias.docstring.parsed
            )
            docstring_returns = any(
                isinstance(doc, DocstringSectionReturns)
                for doc in alias.docstring.parsed
            )

            if not docstring_parameters and alias.parameters:
                arguments_parameters = any(
                    param.docstring is not None for param in alias.parameters
                )
            else:
                arguments_parameters = False

            if not docstring_returns and alias.returns:
                arguments_returns = any(
                    ret.docstring is not None for ret in alias.returns
                )
            else:
                arguments_returns = False

            document_parameters = not docstring_parameters and arguments_parameters
            document_returns = not docstring_returns and arguments_returns

            standard_parameters = [
                param
                for param in alias.parameters
                if param.kind is not ParameterKind.keyword_only
            ]

            keyword_parameters = [
                param
                for param in alias.parameters
                if param.kind is ParameterKind.keyword_only
            ]

            if (
                config.get("show_docstring_input_arguments", True)
                and document_parameters
                and standard_parameters
            ):
                alias.docstring._suffixes.append(
                    DocstringSectionParameters(
                        [
                            DocstringParameter(
                                name=param.name,
                                value=str(param.default)
                                if param.default is not None
                                else None,
                                annotation=param.annotation,
                                description=param.docstring.value
                                if param.docstring is not None
                                else "",
                            )
                            for param in standard_parameters
                        ]
                    )
                )

            if (
                config.get("show_docstring_name_value_arguments", True)
                and document_parameters
                and keyword_parameters
            ):
                alias.docstring._suffixes.append(
                    DocstringSectionOtherParameters(
                        [
                            DocstringParameter(
                                name=param.name,
                                value=str(param.default)
                                if param.default is not None
                                else None,
                                annotation=param.annotation,
                                description=param.docstring.value
                                if param.docstring is not None
                                else "",
                            )
                            for param in keyword_parameters
                        ],
                        title="Name-Value Arguments:",
                    )
                )

            if config.get("show_docstring_output_arguments", True) and document_returns:
                returns = DocstringSectionReturns(
                    [
                        DocstringReturn(
                            name=param.name,
                            value=str(param.default)
                            if param.default is not None
                            else None,
                            annotation=param.annotation,
                            description=param.docstring.value
                            if param.docstring is not None
                            else "",
                        )
                        for param in alias.returns or []
                    ]
                )
                alias.docstring._suffixes.append(returns)

        # Add inheritance diagram to class docstring
        if (
            isinstance(alias, Class)
            and config.get("show_inheritance_diagram", False)
            and (
                (
                    alias.docstring is not None
                    and "Inheritance Diagram" not in alias.docstring.parsed
                )
                or alias.docstring is None
            )
        ):
            diagram = self.get_inheritance_diagram(alias)
            if diagram is not None:
                if alias.docstring is None:
                    alias.docstring = Docstring("", parent=alias)
                alias.docstring._prefixes.append(diagram)

        return alias

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
                    relative_path = member.parent.relative_to(self._config_path)
                    if member.parent not in self._folders:
                        self._folders[str(relative_path)] = LazyModel(
                            member.parent, self
                        )
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

    def __init__(self, path: Path, path_collection: PathCollection):
        self._path: Path = path
        self._model: MatlabMixin | None = None
        self._path_collection: PathCollection = path_collection
        self._lines_collection: LinesCollection = path_collection.lines_collection

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
            grabber: Callable[[], MatlabMixin | None] = self._path_collection._models[
                path
            ].model
            parent = _ParentGrabber(grabber)
        else:
            parent = None
        return parent

    def _collect_path(self, path: Path) -> MatlabMixin:
        file = FileParser(path)
        model = file.parse(path_collection=self._path_collection)
        self._lines_collection[path] = file.content.split("\n")
        return model

    def _collect_directory(self, path: Path, model: PathType) -> PathType:
        for member in path.iterdir():
            if member.is_dir() and member.name[0] in ["+", "@"]:
                submodel = self._path_collection._models[member].model()
                if submodel is not None:
                    model.members[submodel.name] = submodel

            elif member.is_file() and member.suffix == ".m":
                if member.name == "Contents.m":
                    contentsfile = self._collect_path(member)
                    model.docstring = contentsfile.docstring
                else:
                    submodel = self._path_collection._models[member].model()
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
        model = Namespace(name, filepath=path, path_collection=self._path_collection)
        return self._collect_directory(path, model)

    def _collect_folder(self, path: Path) -> Folder:
        name = path.stem
        model = Folder(name, filepath=path, path_collection=self._path_collection)
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
