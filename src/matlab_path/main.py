from __future__ import annotations

from collections import defaultdict, deque
from pathlib import Path

from tqdm import tqdm

from .matlab.nodes import Classdef, Package, Script
from .matlab.parser import get_node


class _PathGlobber:
    def __init__(self, path: Path, recursive: bool = False):
        self._idx = 0
        self._paths: list[Path] = []
        self._glob(path, recursive)

    def _glob(self, path: Path, recursive: bool = False):
        for member in path.iterdir():
            if recursive and member.is_dir() and member.stem[0] not in ["+", "@"]:
                self._glob(member, recursive=True)
                continue

            if member.is_file() and member.name == "Contents.m":
                # ignore contents.m files except in package/class folders
                continue

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


class SearchPath:
    """
    Represents a search path for MATLAB paths.

    Attributes:
        _search_path (deque[Path]): A deque of Path objects representing the search path.
        _path_members (dict[Path, list[tuple[str, Path]]]): A dictionary mapping each path to a list of tuples containing the name and member Path objects.
        _namespace (dict[str, deque[Path]]): A dictionary mapping each name to a deque of member Path objects.
        _local_namespaces (dict[Path, dict[str, Path]]): A dictionary mapping each path to a dictionary of local names to member Path objects.
        _database (dict[Path, Node]): A dictionary mapping each member Path object to its corresponding Node object.

    """

    def __init__(
        self,
        matlab_path: list[str | Path],
        dependency_analysis: bool = False,
        show_progressbar: bool = False,
    ) -> None:
        """
        Initialize an instance of SearchPath.

        Args:
            matlab_path (list[str | Path]): A list of strings or Path objects representing the MATLAB paths.

        Raises:
            TypeError: If any element in matlab_path is not a string or Path object.

        """
        for path in matlab_path:
            if not isinstance(path, (str, Path)):
                raise TypeError(f"Expected str or Path, got {type(path)}")

        self._search_path: deque[Path] = deque()
        self._path_members: dict[Path, list[tuple[str, Path]]] = defaultdict(list)
        self._namespace: dict[str, deque[Path]] = defaultdict(deque)
        self._local_namespaces: dict[Path, dict[str, Path]] = defaultdict(dict)
        self._database: dict[Path, Script] = {}
        self._dependency_analysis = dependency_analysis
        self._show_progressbar = show_progressbar

        for path in matlab_path:
            self.addpath(Path(path), to_end=True)

    def resolve(self, name: str, local_namespaces: list[Path] | None = None) -> Script | None:
        """
        Resolves the given name to a Node object.

        Args:
            name (str): The name to resolve.
            local_namespaces (list[str | Path] | None, optional): A list of local namespaces to search in. Defaults to None.

        Returns:
            Node | None: The resolved Node object, or None if the name is not found.
        """
        # Resolve local namespaces first
        if local_namespaces is not None:
            for str_path in local_namespaces:
                path = Path(str_path)
                if path in self._local_namespaces and name in self._local_namespaces[path]:
                    return self._database[self._local_namespaces[path][name]]

        # Find in global database
        if name in self._namespace:
            return self._database[self._namespace[name][0]]
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

        if path in self._search_path:
            self._search_path.remove(path)

        if to_end:
            self._search_path.append(path)
        else:
            self._search_path.appendleft(path)

        members = _PathGlobber(path, recursive=recursive)
        postfix_length = members.max_stem_length()

        for member in (pbar := tqdm(members)) if self._show_progressbar else members:
            if self._show_progressbar:
                pbar.set_postfix_str("." * (postfix_length - len(member.stem)) + member.stem)

            node = get_node(member, dependency_analysis=self._dependency_analysis)
            if node is None:
                continue
            self._path_members[path].append((node.fqdm, member))
            self._database[member] = node

            if path.stem == "private":
                self._local_namespaces[path.parent][node.fqdm] = member
            else:
                if to_end:
                    self._namespace[node.fqdm].append(member)
                else:
                    self._namespace[node.fqdm].appendleft(member)

            if isinstance(node, Package):
                self._add_package_to_local_namespace(member, node, to_end=to_end)

    def _add_package_to_local_namespace(self, path: Path, package: Package, to_end: bool = False):
        """
        Adds a package and its contents to the local namespace.

        Args:
            path (Path): The path of the package.
            package (Package): The package object containing classes, functions, and sub-packages.
            to_end (bool, optional): Determines whether to add the package to the end of the namespace.
                Defaults to False, which adds the package to the beginning of the namespace.

        Returns:
            None
        """
        for item in package.classes + package.functions + package.packages:
            self._local_namespaces[path][item.name] = item.path
            if to_end:
                self._namespace[item.fqdm].append(item.path)
            else:
                self._namespace[item.fqdm].appendleft(item.path)
            self._database[item.path] = item
        for subpackage in package.packages:
            self._add_package_to_local_namespace(subpackage.path, subpackage)

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

        if path not in self._search_path:
            return list(self._search_path)

        self._search_path.remove(path)

        for name, member in self._path_members.pop(path):
            self._namespace[name].remove(member)
            self._database.pop(member)

        if recursive:
            for subdir in [item for item in self._search_path if _is_subdirectory(path, item)]:
                self.rm_path(subdir, recursive=False)

    def resolve_dependencies(self) -> None:
        """
        Resolves the dependencies for each node in the database.

        This method iterates over each node in the database and resolves its dependencies.
        It updates the dependencies of each node by removing any dependencies that could not be resolved.
        It also updates the dependants of each resolved dependency.

        Returns:
            None
        """
        nodes = self._database.values()

        for node in nodes:
            if not isinstance(node, Script):
                continue
            self._resolve_node(node)

    def _resolve_node(self, node):
        # Get paths of imported namespaces
        packages = [self.resolve(pkg, local_namespaces=[node.path.parent]) for pkg in node._imports]
        package_paths = [pkg.path for pkg in packages if pkg is not None]
        package_paths.reverse()

        # Try to resolve all dependencies
        namespace = package_paths + [node.path.parent]
        for name in node._calls:
            dependency = self.resolve(name, local_namespaces=namespace)
            if dependency is None and "." in name:
                # classdef method
                dependency = self.resolve(name.split(".")[0], local_namespaces=package_paths)
            if dependency is None:
                node._unresolved_dependencies.add(name)
            else:
                node.dependencies.add(dependency)

        for dependency in node.dependencies:
            dependency.dependants.add(node)

        if isinstance(node, Classdef):
            for method in node.methods.values():
                self._resolve_node(method)


def _is_subdirectory(parent_path: Path, child_path: Path) -> bool:
    try:
        child_path.relative_to(parent_path)
    except ValueError:
        return False
    else:
        return True
