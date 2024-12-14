from pathlib import Path
from collections import ChainMap
from markdown import Markdown
from mkdocstrings.handlers.base import BaseHandler, CollectorItem, CollectionError
from mkdocstrings_handlers.python import rendering
from typing import Any, ClassVar, Mapping
from pprint import pprint


from mkdocstrings_handlers.matlab.collect import LinesCollection, PathCollection
from mkdocstrings_handlers.matlab.models import (
    Function,
    Class,
    Script,
)


class MatlabHandler(BaseHandler):
    """The `MatlabHandler` class is a handler for processing Matlab code documentation.

    Attributes:
        name (str): The handler's name.
        domain (str): The cross-documentation domain/language for this handler.
        enable_inventory (bool): Whether this handler is interested in enabling the creation of the `objects.inv` Sphinx inventory file.
        fallback_theme (str): The fallback theme.
        fallback_config (ClassVar[dict]): The configuration used to collect item during autorefs fallback.
        default_config (ClassVar[dict]): The default configuration for the handler.

    Methods:
        __init__(self, *args, config_file_path=None, paths=None, startup_expression="", locale="en", **kwargs): Initializes a new instance of the `MatlabHandler` class.
        get_templates_dir(self, handler=None): Returns the templates directory for the handler.
        collect(self, identifier, config): Collects the documentation for the given identifier.
        render(self, data, config): Renders the collected documentation data.
        update_env(self, md, config): Updates the Jinja environment with custom filters and tests.
    """

    name: str = "matlab"
    """The handler's name."""
    domain: str = "mat"  # to match Sphinx's default domain
    """The cross-documentation domain/language for this handler."""
    enable_inventory: bool = True
    """Whether this handler is interested in enabling the creation of the `objects.inv` Sphinx inventory file."""
    fallback_theme = "material"
    """The fallback theme."""
    fallback_config: ClassVar[dict] = {"fallback": True}
    """The configuration used to collect item during autorefs fallback."""
    default_config: ClassVar[dict] = {
        # https://mkdocstrings.github.io/python/usage/
        # General options
        # "find_stubs_package": False,
        # "allow_inspection": True,
        "show_bases": True,
        "show_inheritance_diagram": True,
        "inheritance_diagram_show_builtin": False,
        "show_source": True,
        # "preload_modules": None,
        # Heading options
        "heading_level": 2,
        "parameter_headings": False,
        "show_root_heading": False,
        "show_root_toc_entry": True,
        "show_root_full_path": True,
        "show_root_members_full_path": False,
        "show_object_full_path": False,
        "show_category_heading": False,
        "show_symbol_type_heading": False,
        "show_symbol_type_toc": False,
        # Member options
        "inherited_members": False,
        "members": None,
        "members_order": rendering.Order.alphabetical,
        "filters": [],
        "group_by_category": True,
        "show_submodules": False,
        "summary": False,
        "show_labels": True,
        # Docstring options
        "docstring_style": "google",
        "docstring_options": {},
        "docstring_section_style": "table",
        "create_from_argument_blocks": True,
        "show_if_no_docstring": False,
        "show_docstring_attributes": True,
        "show_docstring_functions": True,
        "show_docstring_classes": True,
        "show_docstring_modules": True,
        "show_docstring_description": True,
        "show_docstring_examples": True,
        "show_docstring_other_parameters": True,
        "show_docstring_parameters": True,
        "show_docstring_raises": True,
        "show_docstring_receives": True,
        "show_docstring_returns": True,
        "show_docstring_warns": True,
        "show_docstring_yields": True,
        # Signature options
        "annotations_path": "brief",
        "line_length": 60,
        "show_signature": True,
        "show_signature_annotations": False,
        "signature_crossrefs": False,
        "separate_signature": False,
        "unwrap_annotated": False,
        "modernize_annotations": False,
    }

    def __init__(
        self,
        *args: Any,
        config_file_path: str | None = None,
        paths: list[str] | None = None,
        startup_expression: str = "",
        locale: str = "en",
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)

        if paths is None:
            full_paths = ""
        else:
            config_path = Path(config_file_path).parent
            full_paths = [str((config_path / path).resolve()) for path in paths]

        self.paths: PathCollection = PathCollection(full_paths)
        self.lines: LinesCollection = self.paths.lines_collection
        self._locale: str = locale

    def get_templates_dir(self, handler: str | None = None) -> Path:
        # use the python handler templates
        # (it assumes the python handler is installed)
        return super().get_templates_dir("python")

    def render(self, data: CollectorItem, config: Mapping[str, Any]) -> str:
        """Render a template using provided data and configuration options.

        Arguments:
            data: The collected data to render.
            config: The handler's configuration options.

        Returns:
            The rendered template as HTML.
        """
        final_config = ChainMap(config, self.default_config)  # type: ignore[arg-type]

        template_name = rendering.do_get_template(self.env, data)
        template = self.env.get_template(template_name)

        heading_level = final_config["heading_level"]

        return template.render(
            **{
                "config": final_config,
                data.kind.value: data,
                "heading_level": heading_level,
                "root": True,
                "locale": self._locale,
            },
        )

    def update_env(self, md: Markdown, config: dict) -> None:
        """Update the Jinja environment with custom filters and tests.

        Parameters:
            md: The Markdown instance.
            config: The configuration dictionary.
        """
        super().update_env(md, config)
        self.env.trim_blocks = True
        self.env.lstrip_blocks = True
        self.env.keep_trailing_newline = False
        self.env.filters["split_path"] = rendering.do_split_path
        self.env.filters["crossref"] = rendering.do_crossref
        self.env.filters["multi_crossref"] = rendering.do_multi_crossref
        self.env.filters["order_members"] = rendering.do_order_members
        self.env.filters["format_code"] = rendering.do_format_code
        self.env.filters["format_signature"] = rendering.do_format_signature
        self.env.filters["format_attribute"] = rendering.do_format_attribute
        self.env.filters["filter_objects"] = rendering.do_filter_objects
        self.env.filters["stash_crossref"] = lambda ref, length: ref
        self.env.filters["get_template"] = rendering.do_get_template
        self.env.filters["as_attributes_section"] = rendering.do_as_attributes_section
        self.env.filters["as_functions_section"] = rendering.do_as_functions_section
        self.env.filters["as_classes_section"] = rendering.do_as_classes_section
        self.env.filters["as_modules_section"] = rendering.do_as_modules_section
        self.env.tests["existing_template"] = (
            lambda template_name: template_name in self.env.list_templates()
        )

    def collect(self, identifier: str, config: Mapping[str, Any]) -> CollectorItem:
        """Collect data given an identifier and user configuration.

        In the implementation, you typically call a subprocess that returns JSON, and load that JSON again into
        a Python dictionary for example, though the implementation is completely free.

        Arguments:
            identifier: An identifier for which to collect data.
            config: The handler's configuration options.

        Returns:
            CollectorItem
        """
        if identifier == "":
            raise CollectionError("Empty identifier")

        final_config = ChainMap(config, self.default_config)  # type: ignore[arg-type]
        return self.paths.resolve(identifier, config=final_config)


def get_handler(
    *,
    theme: str,
    custom_templates: str | None = None,
    config_file_path: str | None = None,
    paths: list[str] | None = None,
    startup_expression: str = "",
    **config: Any,
) -> MatlabHandler:
    """
    Returns a MatlabHandler object.

    Parameters:
        theme (str): The theme to use.
        custom_templates (str | None, optional): Path to custom templates. Defaults to None.
        config_file_path (str | None, optional): Path to configuration file. Defaults to None.
        paths (list[str] | None, optional): List of paths to include. Defaults to None.
        startup_expression (str, optional): Startup expression. Defaults to "".
        **config (Any): Additional configuration options.

    Returns:
        MatlabHandler: The created MatlabHandler object.
    """
    return MatlabHandler(
        handler="matlab",
        theme=theme,
        custom_templates=custom_templates,
        config_file_path=config_file_path,
        paths=paths,
        startup_expression=startup_expression,
    )


if __name__ == "__main__":
    handler = get_handler(theme="material")
    pprint(handler.collect("matlab_startup", {}).docstring.parse("google"))
