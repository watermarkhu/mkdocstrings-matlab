"""SuperFences formatter backed by textmate-grammar-python."""

from __future__ import annotations

import html
import re
from collections.abc import Mapping, MutableMapping, MutableSequence, Sequence
from typing import Any

from textmate_grammar.parsers.matlab import matlab_grammar

_CATEGORIES = (
    ("constant.numeric", "number"),
    ("constant.character", "string"),
    ("entity.name.function", "function"),
    ("entity.name.type", "type"),
    ("support.function", "function"),
    ("support.type", "type"),
    ("keyword", "keyword"),
    ("storage", "keyword"),
    ("string", "string"),
    ("comment", "comment"),
    ("constant", "constant"),
    ("variable", "variable"),
    ("invalid", "error"),
)


def validate_matlab_fence(
    language: str,
    inputs: dict[str, Any],
    options: dict[str, Any],
    attrs: dict[str, str],
    md: Any,
) -> bool:
    """Accept fence options without falling back to Pygments highlighting."""
    del language, attrs, md
    options.update(inputs)
    return True


def configure_matlab_highlighting(mdx: Sequence[Any], mdx_config: Mapping[str, Any]) -> None:
    """Register the TextMate formatter on the site's SuperFences extension."""
    if not isinstance(mdx, MutableSequence) or not isinstance(mdx_config, MutableMapping):
        raise TypeError("MkDocs must provide mutable Markdown extension configuration")

    extension_name = "pymdownx.superfences"
    if not any(
        extension == extension_name or type(extension).__module__.startswith(extension_name)
        for extension in mdx
    ):
        mdx.append(extension_name)

    extension_config = mdx_config.setdefault(extension_name, {})
    if not isinstance(extension_config, MutableMapping):
        raise TypeError("The SuperFences configuration must be mutable")
    custom_fences = extension_config.setdefault("custom_fences", [])
    if not isinstance(custom_fences, MutableSequence):
        raise TypeError("SuperFences custom_fences must be a mutable sequence")

    for fence in custom_fences:
        if isinstance(fence, MutableMapping) and fence.get("name") == "matlab":
            fence["class"] = fence.get("class") or "matlab"
            fence["format"] = highlight_matlab
            fence["validator"] = validate_matlab_fence
            break
    else:
        custom_fences.append(
            {
                "name": "matlab",
                "class": "matlab",
                "format": highlight_matlab,
                "validator": validate_matlab_fence,
            }
        )


def highlight_matlab(
    source: str,
    language: str,
    class_name: str,
    options: dict[str, Any],
    md: Any,
    **kwargs: Any,
) -> str:
    """Format a MATLAB fenced block using TextMate scopes.

    The signature matches ``pymdownx.superfences`` custom fence formatters.
    Existing fence classes, ids, and attributes are retained.
    """
    del md

    grammar = matlab_grammar()
    state = None
    lines = source.split("\n")
    rendered: list[str] = []
    final_scopes = (grammar.root_scope_name,)

    for index, line in enumerate(lines):
        result = grammar.tokenize_line(line, state)
        state = result.ruleStack
        for token in result.tokens:
            value = line[token.startIndex : token.endIndex]
            if not value:
                continue
            final_scopes = tuple(token.scopes)
            classes = _scope_classes(final_scopes)
            rendered.append(
                f'<span class="{html.escape(" ".join(classes), quote=True)}">'
                f"{html.escape(value, quote=False)}</span>"
            )
        if index < len(lines) - 1:
            classes = _scope_classes(final_scopes)
            rendered.append(f'<span class="{html.escape(" ".join(classes), quote=True)}">\n</span>')

    classes = list(kwargs.get("classes", []))
    if class_name:
        classes.insert(0, class_name)
    class_attr = f' class="{html.escape(" ".join(classes), quote=True)}"' if classes else ""
    id_value = kwargs.get("id_value")
    id_attr = f' id="{html.escape(str(id_value), quote=True)}"' if id_value else ""
    attrs = kwargs.get("attrs", {})
    attrs_attr = "".join(
        f' {html.escape(str(name), quote=True)}="{html.escape(str(value), quote=True)}"'
        for name, value in attrs.items()
    )
    title = options.get("title")
    title_markup = (
        f'<span class="filename">{html.escape(str(title), quote=False)}</span>' if title else ""
    )
    wrapper_classes = f' class="language-{_css_name(language)} highlight"'
    return (
        f"<div{wrapper_classes}>{title_markup}"
        f"<pre{id_attr}{class_attr}{attrs_attr}><code>{''.join(rendered)}</code></pre></div>"
    )


def _scope_classes(scopes: tuple[str, ...]) -> list[str]:
    classes = [f"tm-{_css_name(scope)}" for scope in scopes if scope]
    for scope in reversed(scopes):
        for prefix, category in _CATEGORIES:
            if scope == prefix or scope.startswith(f"{prefix}."):
                classes.append(f"tm-token-{category}")
                return list(dict.fromkeys(classes))
    return list(dict.fromkeys(classes))


def _css_name(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "-", value).strip("-").lower()


__all__ = ["configure_matlab_highlighting", "highlight_matlab", "validate_matlab_fence"]
