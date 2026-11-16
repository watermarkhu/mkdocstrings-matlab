"""Generate the builtin documentation link table from the MATLAB reference index.

MATLAB's `doc` command resolves a name through the reference index that ships with each
installed product, `help/docCatalog/referenceapi/<product>.json`, under the MATLAB root. This
script reads those files and writes `src/mkdocstrings_handlers/matlab/data/builtin_docs.json`,
which maps each documented name to its page under https://www.mathworks.com/help/.

Only the products installed with MATLAB are read: the add-on groups listed under
`supportPackages` in a product's index are skipped. The elementary functions MATLAB documents on
the `double` page (such as `double.sum`) link under their own name when no other page has it.
Other method pages (`containers.Map.keys`, `mexception.rethrow`) are not linked by bare name.

Rerun it when the MATLAB release changes:

    python scripts/gen_builtin_docs.py [--matlabroot /path/to/MATLAB]

The MATLAB root defaults to the one `matlab` on the PATH runs from. The release used for the
committed table is R2026b.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

BASE = "https://www.mathworks.com/help/"
OUTPUT = (
    Path(__file__).resolve().parents[1] / "src/mkdocstrings_handlers/matlab/data/builtin_docs.json"
)

PAGE_TYPES = frozenset(
    {"function", "class", "object", "keyword", "package", "block", "tool", "app"}
)
"""The entity types that name a page of their own."""

IDENTIFIER = re.compile(r"[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*")
PAGE_PATH = re.compile(r"[a-z][a-z-]*/(?:[a-z]+/)?[\w.-]+\.html")


def default_matlabroot() -> Path:
    if (matlab := shutil.which("matlab")) is None:
        sys.exit("matlab is not on the PATH; pass --matlabroot")
    return Path(matlab).resolve().parents[1]


def collect(index: Path) -> tuple[dict[str, str], str]:
    """Map each documented name to its page, preferring MATLAB's own product and then the
    page named after the entity."""
    docset = json.loads((index.parents[1] / "docset.json").read_text(encoding="utf-8"))
    release = docset["documentation_set"]["release"]
    primary: dict[str, set[str]] = defaultdict(set)
    fallback: dict[str, set[str]] = defaultdict(set)
    for path in sorted(index.glob("*.json")):
        product = json.loads(path.read_text(encoding="utf-8"))
        location = product["helpLocation"]
        for item in product.get("refItems", []):
            for entity in item.get("refentity", []):
                name = entity.get("name", "")
                if not IDENTIFIER.fullmatch(name):
                    continue
                page = f"{location}/{item['href']}"
                if entity.get("type") in PAGE_TYPES and entity.get("fcntype") != "instancemethod":
                    primary[name].add(page)
                elif (
                    entity.get("type") == "function"
                    and entity.get("fcntype") == "instancemethod"
                    and "." not in name
                ):
                    fallback[name].add(page)

    def preference(name: str, page: str) -> tuple[bool, bool, str]:
        location, href = page.split("/", 1)
        return (location != "matlab", href != f"ref/{name.lower()}.html", page)

    pages = {
        name: min(candidates, key=lambda page: preference(name, page))
        for name, candidates in primary.items()
    }
    names_lower = {name.lower() for name in pages}
    methods = {}
    for name, candidates in fallback.items():
        base = f"matlab/ref/double.{name.lower()}.html"
        if name not in pages and name.lower() not in names_lower and base in candidates:
            methods[name] = base
    pages.update(methods)
    for name, page in list(pages.items()):
        base = f"matlab/ref/double.{name.lower()}.html"
        if not page.startswith("matlab/") and base in fallback.get(name, ()):
            pages[name] = base
    print(f"names taken from elementary method pages: {len(methods)}", file=sys.stderr)
    return pages, release


def toc_names(index: Path) -> set[str]:
    """The function names MATLAB's function catalog lists (`helpfuncbycat.xml`), for a check."""
    toc = index.parents[1] / "matlab" / "helpfuncbycat.xml"
    return set(
        re.findall(
            r'<tocitem target="ref/[^"]+">\s*<name>([^<]+)</name>', toc.read_text(encoding="utf-8")
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--matlabroot", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    root = args.matlabroot or default_matlabroot()
    index = root / "help" / "docCatalog" / "referenceapi"
    if not index.is_dir():
        sys.exit(f"no reference index under {root}")
    pages, release = collect(index)
    bad = [page for page in pages.values() if not PAGE_PATH.fullmatch(page)]
    if bad:
        sys.exit(f"unexpected page paths: {bad[:5]}")
    lower = {name.lower() for name in pages}
    missing = sorted(
        name
        for name in toc_names(index)
        if IDENTIFIER.fullmatch(name) and name.lower() not in lower
    )
    print(
        f"function catalog names missing from the table: {len(missing)} {missing[:20]}",
        file=sys.stderr,
    )
    data = {"release": release, "base": BASE, "pages": dict(sorted(pages.items()))}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=1, ensure_ascii=True) + "\n", encoding="utf-8")
    print(f"{len(pages)} names from MATLAB {release} written to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
