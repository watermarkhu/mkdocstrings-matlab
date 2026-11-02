from __future__ import annotations

from html.parser import HTMLParser

from markdown import Markdown

from mkdocstrings_handlers.matlab.highlighting import (
    configure_matlab_highlighting,
    highlight_matlab,
    validate_matlab_fence,
)


class _TextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.text: list[str] = []

    def handle_data(self, data: str) -> None:
        self.text.append(data)


def test_highlight_matlab_emits_textmate_scopes_and_escapes_source() -> None:
    source = "x = '<&>'\n"
    result = highlight_matlab(source, "matlab", "matlab", {}, None, classes=[], attrs={})

    assert 'class="matlab"' in result
    assert "tm-token-string" in result
    assert "tm-string-quoted-single-matlab" in result
    assert "&lt;&amp;&gt;" in result
    assert "'<&>'" not in result

    parser = _TextParser()
    parser.feed(result)
    assert "".join(parser.text) == source


def test_highlight_matlab_preserves_fence_attributes_and_source() -> None:
    source = "x = 42\n\n"
    result = highlight_matlab(
        source,
        "matlab",
        "matlab",
        {},
        None,
        classes=["highlight"],
        id_value="example",
        attrs={"data-title": 'sample "code"'},
    )

    assert 'id="example"' in result
    assert 'class="matlab highlight"' in result
    assert 'data-title="sample &quot;code&quot;"' in result
    assert result.count("\n") >= 2
    assert "tm-constant-numeric-decimal-matlab" in result

    parser = _TextParser()
    parser.feed(result)
    assert "".join(parser.text) == source


def test_superfences_routes_matlab_blocks_to_textmate_formatter() -> None:
    extensions = ["pymdownx.highlight"]
    extension_config = {}
    configure_matlab_highlighting(extensions, extension_config)

    assert "pymdownx.superfences" in extensions
    assert extension_config["pymdownx.superfences"]["custom_fences"] == [
        {
            "name": "matlab",
            "class": "matlab",
            "format": highlight_matlab,
            "validator": validate_matlab_fence,
        }
    ]

    markdown = Markdown(
        extensions=extensions,
        extension_configs=extension_config,
    )

    result = markdown.convert('```matlab title="sample.m"\nx = 42\n```')

    assert 'class="filename">sample.m</span>' in result
    assert "tm-token-number" in result
    assert "tm-constant-numeric-decimal-matlab" in result
    assert '<span class="mi">42</span>' not in result


def test_superfences_configuration_preserves_other_fences_and_is_idempotent() -> None:
    mermaid = {"name": "mermaid", "class": "mermaid"}
    custom_matlab = {"name": "matlab", "class": "custom-matlab", "format": str}
    extensions = ["pymdownx.superfences"]
    extension_config = {"pymdownx.superfences": {"custom_fences": [mermaid, custom_matlab]}}

    configure_matlab_highlighting(extensions, extension_config)
    configure_matlab_highlighting(extensions, extension_config)

    fences = extension_config["pymdownx.superfences"]["custom_fences"]
    assert fences[0] is mermaid
    assert fences[1]["class"] == "custom-matlab"
    assert fences[1]["format"] is highlight_matlab
    assert fences[1]["validator"] is validate_matlab_fence
    assert len(fences) == 2
