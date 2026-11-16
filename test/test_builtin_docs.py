"""Tests for the builtin documentation table and the generator that writes it."""

from __future__ import annotations

import importlib.util
import json
import re
from importlib import resources
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from mkdocstrings_handlers.matlab.model import Expression

ROOT = Path(__file__).parents[1]
GENERATOR = ROOT / "scripts" / "gen_builtin_docs.py"
BASE = "https://www.mathworks.com/help/"
IDENTIFIER = re.compile(r"[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*")
PAGE = re.compile(
    r"(matlab|coder|compiler|fixedpoint|parallel-computing)/(?:[a-z]+/)?[\w.-]+\.html"
)


def _no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    keys = [key for key, _ in pairs]
    assert len(keys) == len(set(keys)), "duplicate key in the table"
    return dict(pairs)


def _load_generator() -> ModuleType:
    spec = importlib.util.spec_from_file_location("gen_builtin_docs", GENERATOR)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _fake_index(root: Path, products: dict[str, list[dict[str, Any]]]) -> Path:
    help_dir = root / "help"
    index = help_dir / "docCatalog" / "referenceapi"
    index.mkdir(parents=True)
    docset = {"documentation_set": {"release": "R2026b"}}
    (help_dir / "docset.json").write_text(json.dumps(docset), encoding="utf-8")
    for location, items in products.items():
        product = {"helpLocation": location, "refItems": items}
        (index / f"{location}.json").write_text(json.dumps(product), encoding="utf-8")
    return index


@pytest.fixture(scope="module")
def table() -> dict[str, Any]:
    text = resources.files("mkdocstrings_handlers.matlab").joinpath("data", "builtin_docs.json")
    return json.loads(text.read_text(encoding="utf-8"), object_pairs_hook=_no_duplicates)


def test_table_is_packaged_with_its_release(table: dict[str, Any]) -> None:
    assert table["release"] == "R2026b"
    assert table["base"] == BASE
    assert len(table["pages"]) > 3000


@pytest.mark.parametrize(
    ("name", "page"),
    [
        ("double", "matlab/ref/double.html"),
        ("char", "matlab/ref/char.html"),
        ("string", "matlab/ref/string.html"),
        ("cell", "matlab/ref/cell.html"),
        ("struct", "matlab/ref/struct.html"),
        ("table", "matlab/ref/table.html"),
        ("int8", "matlab/ref/int8.html"),
        ("function_handle", "matlab/ref/function_handle.html"),
        ("datetime", "matlab/ref/datetime.html"),
        ("categorical", "matlab/ref/categorical.html"),
        ("containers.Map", "matlab/ref/containers.map.html"),
        ("matlab.lang.makeValidName", "matlab/ref/matlab.lang.makevalidname.html"),
        ("if", "matlab/ref/if.html"),
        ("sum", "matlab/ref/double.sum.html"),
        ("fi", "fixedpoint/ref/embedded.fi.html"),
        ("codegen", "coder/ref/codegen.html"),
        ("codistributed", "parallel-computing/codistributed.html"),
    ],
)
def test_known_names_resolve(table: dict[str, Any], name: str, page: str) -> None:
    assert table["pages"][name] == page
    assert Expression(name).doc == BASE + page


@pytest.mark.parametrize("name", ["Widget", "Double", "Map", "gather", "matlab.lang"])
def test_unknown_and_case_sensitive_names_do_not_link(name: str) -> None:
    assert Expression(name).doc == ""


def test_first_builtin_in_the_expression_is_linked() -> None:
    assert Expression("double or char").doc == BASE + "matlab/ref/double.html"
    assert Expression("Widget(uint8)").doc == BASE + "matlab/ref/uint8.html"
    assert Expression("containers.Map(KeyType=char)").doc == (
        BASE + "matlab/ref/containers.map.html"
    )


def test_quoted_text_is_not_a_name() -> None:
    assert Expression('"read"').doc == ""
    assert Expression("'error', double").doc == BASE + "matlab/ref/double.html"


def test_table_is_sorted_and_well_formed(table: dict[str, Any]) -> None:
    pages = table["pages"]
    assert list(pages) == sorted(pages)
    for name, page in pages.items():
        assert IDENTIFIER.fullmatch(name), name
        assert PAGE.fullmatch(page), (name, page)


def test_generator_prefers_matlab_and_its_elementary_pages(tmp_path: Path) -> None:
    generator = _load_generator()
    index = _fake_index(
        tmp_path,
        {
            "matlab": [
                {"href": "ref/plot.html", "refentity": [{"name": "plot", "type": "function"}]},
                {
                    "href": "ref/addpath.html",
                    "refentity": [{"name": "addpath", "type": "function"}],
                },
                {
                    "href": "ref/matlab.project.project.addpath.html",
                    "refentity": [
                        {"name": "addPath", "type": "function", "fcntype": "instancemethod"}
                    ],
                },
                {
                    "href": "ref/double.abs.html",
                    "refentity": [
                        {"name": "abs", "type": "function", "fcntype": "instancemethod"},
                        {"name": "double.abs", "type": "method", "fcntype": "instancemethod"},
                    ],
                },
                {
                    "href": "ref/double.sum.html",
                    "refentity": [{"name": "sum", "type": "function", "fcntype": "instancemethod"}],
                },
                {
                    "href": "ref/containers.map.keys.html",
                    "refentity": [{"name": "containers.Map.keys", "type": "method"}],
                },
                {
                    "href": "ref/mexception.rethrow.html",
                    "refentity": [
                        {"name": "rethrow", "type": "function", "fcntype": "instancemethod"}
                    ],
                },
                {
                    "href": "ref/alphashape.perimeter.html",
                    "refentity": [
                        {"name": "perimeter", "type": "function", "fcntype": "instancemethod"}
                    ],
                },
            ],
            "fixedpoint": [
                {"href": "ref/sum.html", "refentity": [{"name": "sum", "type": "function"}]},
                {"href": "ref/plot.html", "refentity": [{"name": "plot", "type": "function"}]},
                {
                    "href": "ref/polyshape.perimeter.html",
                    "refentity": [
                        {"name": "perimeter", "type": "function", "fcntype": "instancemethod"}
                    ],
                },
            ],
        },
    )

    pages, release = generator.collect(index)

    assert release == "R2026b"
    assert pages["plot"] == "matlab/ref/plot.html"
    assert pages["sum"] == "matlab/ref/double.sum.html"
    assert pages["abs"] == "matlab/ref/double.abs.html"
    assert "containers.Map.keys" not in pages
    assert "perimeter" not in pages
    assert "rethrow" not in pages
    assert pages["addpath"] == "matlab/ref/addpath.html"
    assert "addPath" not in pages
