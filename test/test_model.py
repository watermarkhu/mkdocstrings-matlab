"""Tests for the `model` module, the adapter over malt-index's objects."""

from __future__ import annotations

import logging
from pathlib import Path

import pytest
from griffe import Docstring

from mkdocstrings_handlers.matlab import model
from mkdocstrings_handlers.matlab.model import ArgumentKind, Expression, Kind

FIXTURE = Path(__file__).parent / "fixture"


@pytest.fixture
def paths() -> model.PathsCollection:
    return model.PathsCollection([FIXTURE], recursive=True, working_directory=FIXTURE)


def test_expression_renders_its_text_and_tokens() -> None:
    expression = Expression("containers.Map")

    assert str(expression) == "containers.Map"
    assert list(expression) == ["containers", ".", "Map"]
    assert expression.doc == "https://www.mathworks.com/help/matlab/ref/containers.map.html"


def test_builtin_expression_links_its_reference_page() -> None:
    assert Expression("double").doc == "https://www.mathworks.com/help/matlab/ref/double.html"
    assert Expression("uint8(3)").doc == "https://www.mathworks.com/help/matlab/ref/uint8.html"
    assert Expression("Widget").doc == ""


def test_kinds_are_the_template_values() -> None:
    # An enumeration is a class to the templates, as it always was.
    assert Kind("class") is Kind.ENUMERATION
    assert Kind.ENUMERATION is Kind.CLASS
    assert ArgumentKind("keyword-only") is ArgumentKind.keyword_only
    assert ArgumentKind("varargin") is ArgumentKind.varargin


def test_folder_members_are_named_without_the_folder(paths: model.PathsCollection) -> None:
    folder = paths.get_member(str(FIXTURE))

    assert folder is not None
    assert folder.is_folder
    assert folder.path == "/fixture"
    assert folder.members["module_function"].path == "module_function"


def test_namespace_path_keeps_the_plus(paths: model.PathsCollection) -> None:
    namespace = paths.get_member("+moduleNamespace")

    assert namespace is not None
    assert namespace.is_namespace
    assert namespace.path == "+moduleNamespace"
    assert namespace.canonical_path == "moduleNamespace"
    assert namespace.members["namespace_function"].path == "moduleNamespace.namespace_function"


def test_inherited_members_keep_the_base_path(paths: model.PathsCollection) -> None:
    subclass = paths.get_member("subClass")

    assert subclass is not None
    assert subclass.is_class
    assert subclass.bases == ["moduleClass"]
    method = subclass.inherited_members["method1"]
    assert method.inherited
    assert method.is_alias
    assert method.path == "moduleClass.method1"
    assert "method1" in subclass.all_members
    assert "method1" not in subclass.members


def test_constructor_is_the_method_named_after_the_class(paths: model.PathsCollection) -> None:
    moduleclass = paths.get_member("moduleClass")

    assert moduleclass is not None
    assert moduleclass.constructor is not None
    assert moduleclass.constructor.name == "moduleClass"
    assert [argument.name for argument in moduleclass.constructor.arguments] == ["a", "b"]


def test_docstring_is_a_griffe_docstring_with_its_parent(paths: model.PathsCollection) -> None:
    function = paths.get_member("module_function")

    assert function is not None
    assert function.has_docstring
    assert isinstance(function.docstring, Docstring)
    assert function.docstring.parent is function
    assert function.docstring.lineno is not None
    assert function.docstring.parser is None


def test_missing_names_are_none(paths: model.PathsCollection) -> None:
    assert paths.get_member("no_such_name") is None
    assert paths.get_member("") is None
    assert "module_function" in paths
    assert "no_such_name" not in paths


def test_arguments_carry_their_kinds(paths: model.PathsCollection) -> None:
    function = paths.get_member("module_arguments")

    assert function is not None
    kinds = {argument.name: argument.kind for argument in function.arguments}
    assert ArgumentKind.varargin in kinds.values()
    assert ArgumentKind.keyword_only in kinds.values()


def test_source_and_file_follow_the_declaration(paths: model.PathsCollection) -> None:
    function = paths.get_member("module_function")

    assert function is not None
    assert function.source.startswith("function")
    assert function.filepath.resolve() == (FIXTURE / "module_function.m").resolve()
    assert function.relative_filepath is not None
    assert function.relative_filepath.name == "module_function.m"


def test_index_logger_level_follows_the_option() -> None:
    try:
        model.configure_index_logger("ERROR")
        assert logging.getLogger("malt_index").level == logging.ERROR
        model.configure_index_logger("TRACE")
        assert logging.getLogger("malt_index").level == 5
    finally:
        model.configure_index_logger("WARNING")
