"""The mkdocstrings handler for processing MATLAB code documentation."""

from __future__ import annotations 

import re
from pathlib import Path
from pprint import pprint
from typing import TYPE_CHECKING, Any, ClassVar

from jinja2.loaders import FileSystemLoader
from markdown import Markdown
from mkdocs.exceptions import PluginError

from mkdocstrings import BaseHandler, CollectionError, CollectorItem, HandlerOptions, Inventory, get_logger
from mkdocstrings_handlers.matlab.collect import LinesCollection, PathsCollection
from mkdocstrings_handlers.matlab.config import MatlabConfig, MatlabOptions
from mkdocstrings_handlers.python import rendering

if TYPE_CHECKING:
    from collections.abc import Iterator, Mapping, MutableMapping, Sequence
    from mkdocs.config.defaults import MkDocsConfig

class MatlabHandler(BaseHandler):
    """The `MatlabHandler` class is a handler for processing Matlab code documentation."""

    name: ClassVar[str] = "matlab"
    """The MATLAB handler class."""
    
    domain: ClassVar[str] = "mat"  # to match Sphinx's default domain
    """The cross-documentation domain/language for this handler."""
    
    enable_inventory: ClassVar[bool] = True
    """Whether this handler is interested in enabling the creation of the `objects.inv` Sphinx inventory file."""
    fallback_theme: ClassVar[str] = "material"
    """The fallback theme."""

    fallback_config: ClassVar[dict] = {
        "fallback": True,
    }

    def __init__(
        self,
        config: MatlabConfig,
        base_dir: Path,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the handler with the given configuration.

        Args:
            config: The handler configuration.
            base_dir: The base directory of the project.
            **kwargs: Arguments passed to the parent constructor.

        Returns:
            None
        """
        super().__init__(**kwargs)

        self.config = config
        self.base_dir = base_dir
        self.global_options = config.options

        theme_path = Path(__file__).resolve().parent / "templates" / self.theme
        if theme_path.exists() and isinstance(self.env.loader, FileSystemLoader):
            # Insert our templates directory at the beginning of the search path to overload the Python templates
            self.env.loader.searchpath.insert(0, str(theme_path))
        css_path = theme_path / "style.css"
        if css_path.exists():
            self.extra_css += "\n" + css_path.read_text(encoding="utf-8")

        if config.paths:
            full_paths = [
                (base_dir / path).resolve()
                for path in config.paths
            ]
        else:
            full_paths = []

        if pathIds := [str(path) for path in full_paths if not path.is_dir()]:
            raise PluginError(
                "The following paths do not exist or are not directories: "
                + ", ".join(pathIds)
            )

        self._path_collection: PathsCollection = PathsCollection(
            full_paths, recursive=config.paths_recursive, config_path=base_dir
        )
        self._lines_collection: LinesCollection = self._path_collection.lines_collection


    def get_templates_dir(self, *args, **kwargs) -> Path:
        # use the python handler templates
        # (it assumes the python handler is installed)
        return super().get_templates_dir("python")

    def get_options(self, local_options: Mapping[str, Any]) -> HandlerOptions:
        """Get combined default, global and local options.

        Arguments:
            local_options: The local options.

        Returns:
            The combined options.
        """

        extra = {**self.global_options.get("extra", {}), **local_options.get("extra", {})}
        options = {**self.global_options, **local_options, "extra": extra}
        try:
            # YORE: Bump 2: Replace `opts =` with `return` within line.
            opts = MatlabOptions.from_data(**options)
        except Exception as error:
            raise PluginError(f"Invalid options: {error}") from error

        return opts

    def render(self, data: CollectorItem, config: dict[str, Any]) -> str:
        """Render a template using provided data and configuration options.

        Arguments:
            data: The collected data to render.
            config: The handler's configuration options.

        Returns:
            The rendered template as HTML.
        """

        template_name = rendering.do_get_template(self.env, data)
        template = self.env.get_template(template_name)

        heading_level = config["heading_level"]

        try:
            config["members_order"] = rendering.Order(config["members_order"])
        except ValueError as error:
            choices = "', '".join(item.value for item in rendering.Order)
            raise PluginError(
                f"Unknown members_order '{config['members_order']}', choose between '{choices}'.",
            ) from error

        if config["filters"]:
            config["filters"] = [
                (re.compile(filtr.lstrip("!")), filtr.startswith("!"))
                for filtr in config["filters"]
            ]

        summary = config["summary"]
        if summary is True:
            config["summary"] = {
                "attributes": True,
                "functions": True,
                "classes": True,
                "modules": True,
            }
        elif summary is False:
            config["summary"] = {
                "attributes": False,
                "functions": False,
                "classes": False,
                "modules": False,
            }
        else:
            config["summary"] = {
                "attributes": summary.get(
                    "properties", False
                ),  # Map properties (MATLAB) to attributes (Python)
                "functions": summary.get("functions", False),
                "classes": summary.get("classes", False),
                "modules": summary.get(
                    "namespaces", False
                ),  # Map namespaces (MATLAB) to modules (Python)
            }

        # Map docstring options
        config["show_docstring_attributes"] = config.get(
            "show_docstring_properties", True
        )
        config["show_docstring_modules"] = config.get("show_docstring_namespaces", True)
        config["show_docstring_parameters"] = config.get(
            "show_docstring_input_arguments", True
        )
        config["show_docstring_other_parameters"] = config.get(
            "show_docstring_name_value_arguments", True
        )
        config["show_docstring_returns"] = config.get(
            "show_docstring_output_arguments", True
        )

        # These settings must be present to avoid errors
        for setting in [
            "merge_init_into_class",
            "show_docstring_raises",
            "show_docstring_receives",
            "show_docstring_yields",
            "show_docstring_warns",
        ]:
            config[setting] = False
        config["line_length"] = 88

        return template.render(
            **{
                "config": config,
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
        self.env.filters["stash_crossref"] = rendering.do_stash_crossref
        self.env.filters["get_template"] = rendering.do_get_template
        self.env.filters["as_attributes_section"] = rendering.do_as_attributes_section
        self.env.filters["as_functions_section"] = rendering.do_as_functions_section
        self.env.filters["as_classes_section"] = rendering.do_as_classes_section
        self.env.filters["as_modules_section"] = rendering.do_as_modules_section
        self.env.globals["AutorefsHook"] = rendering.AutorefsHook
        self.env.tests["existing_template"] = (
            lambda template_name: template_name in self.env.list_templates()
        )

    def collect(self, identifier: str, config: dict[str, Any]) -> CollectorItem:
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

        final_config = self.get_options(config)
        try:
            model = self._path_collection.resolve(identifier, config=final_config)
        except SyntaxError as ex:
            msg = str(ex)
            if ex.text:
                msg += ":\n" + ex.text
            raise CollectionError(msg) from ex
        except Exception as ex:
            raise CollectionError(str(ex)) from ex

        if model is None:
            raise CollectionError(f"Identifier '{identifier}' not found")
        return model


def get_handler(
    handler_config: MutableMapping[str, Any],
    tool_config: MkDocsConfig,
    **kwargs: Any,
) -> MatlabHandler:
    """
    Create and return a MatlabHandler object with the specified configuration.

    Parameters:
         handler_config: The handler configuration.
        tool_config: The tool (SSG) configuration.

    Returns:
        MatlabHandler: An instance of MatlabHandler configured with the provided parameters.
    """
    base_dir = Path(tool_config.config_file_path or "./mkdocs.yml").parent
    return MatlabHandler(
        config=MatlabConfig.from_data(**handler_config),
        base_dir=base_dir,
        **kwargs,
    )


if __name__ == "__main__":
    handler = get_handler(theme="material")
    pprint(handler.collect("matlab_startup", {}).docstring.parse("google"))
