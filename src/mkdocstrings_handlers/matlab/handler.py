"""The mkdocstrings handler for processing MATLAB code documentation."""

from __future__ import annotations

from contextlib import suppress
from dataclasses import asdict
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar

from griffe import Parser, AliasResolutionError
from mkdocs.exceptions import PluginError
from mkdocstrings import (
    BaseHandler,
    CollectionError,
    CollectorItem,
    HandlerOptions,
    get_logger,
)
from mkdocstrings_handlers.matlab import rendering
from mkdocstrings_handlers.matlab.collect import LinesCollection, PathsCollection
from mkdocstrings_handlers.matlab.config import MatlabConfig, MatlabOptions

if TYPE_CHECKING:
    from collections.abc import Mapping, MutableMapping
    from mkdocs.config.defaults import MkDocsConfig


_logger = get_logger(__name__)


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

        # Warn if user overrides base templates.
        if self.custom_templates:
            for theme_dir in base_dir.joinpath(self.custom_templates, "python").iterdir():
                if theme_dir.joinpath("_base").is_dir():
                    _logger.warning(
                        f"Overriding base template '{theme_dir.name}/_base/<template>.html.jinja' is not supported, "
                        f"override '{theme_dir.name}/<template>.html.jinja' instead",
                    )

        if config.paths:
            full_paths = [(base_dir / path).resolve() for path in config.paths]
        else:
            full_paths = []

        if path_ids := [str(path) for path in full_paths if not path.is_dir()]:
            raise PluginError(
                "The following paths do not exist or are not directories: " + ", ".join(path_ids)
            )

        self._paths = full_paths
        self._paths_collection: PathsCollection = PathsCollection(
            full_paths, recursive=config.paths_recursive, config_path=base_dir
        )
        self._lines_collection: LinesCollection = self._paths_collection.lines_collection

    def get_options(self, local_options: Mapping[str, Any]) -> HandlerOptions:
        """Get combined default, global and local options.

        Arguments:
            local_options: The local options.

        Returns:
            The combined options.
        """

        extra = {
            **self.global_options.get("extra", {}),
            **local_options.get("extra", {}),
        }
        options = {**self.global_options, **local_options, "extra": extra}
        try:
            # YORE: Bump 2: Replace `opts =` with `return` within line.
            opts = MatlabOptions.from_data(**options)
        except Exception as error:
            raise PluginError(f"Invalid options: {error}") from error

        return opts

    def render(self, data: CollectorItem, options: MatlabOptions) -> str:
        """Render a template using provided data and configuration options.

        Arguments:
            data: The collected data to render.
            config: The handler's configuration options.

        Returns:
            The rendered template as HTML.
        """

        template_name = rendering.do_get_template(self.env, data)
        template = self.env.get_template(template_name)

        heading_level = options.heading_level

        return template.render(
            **{
                "config": options,
                data.kind.value: data,
                "heading_level": heading_level,
                "root": True,
                "locale": self.config.locale,
            },
        )

    def update_env(self, config: Any) -> None:  # noqa: ARG002
        """Update the Jinja environment with custom filters and tests.

        Parameters:
            config: The SSG configuration.
        """
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
        self.env.filters["as_properties_section"] = rendering.do_as_properties_section
        self.env.filters["as_functions_section"] = rendering.do_as_functions_section
        self.env.filters["as_classes_section"] = rendering.do_as_classes_section
        self.env.filters["as_namespaces_section"] = rendering.do_as_namespaces_section
        self.env.filters["as_inheritance_diagram_section"] = rendering.do_as_inheritance_diagram_section
        self.env.filters["backlink_tree"] = rendering.do_backlink_tree
        self.env.globals["AutorefsHook"] = rendering.AutorefsHook
        self.env.tests["existing_template"] = (
            lambda template_name: template_name in self.env.list_templates()
        )

    def collect(self, identifier: str, options: MatlabOptions) -> CollectorItem:
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

        if options == {}:
            options = self.get_options({})
        try:
            model = self._paths_collection.resolve(identifier)
        except SyntaxError as ex:
            msg = str(ex)
            if ex.text:
                msg += ":\n" + ex.text
            raise CollectionError(msg) from ex
        except KeyError as ex:
            raise CollectionError(str(ex)) from ex
        except AliasResolutionError as ex:
            raise CollectionError(str(ex)) from ex

        if model is None:
            raise CollectionError(f"Identifier '{identifier}' not found")
        
        parser_name = options.docstring_style
        parser = parser_name and Parser(parser_name)
        parser_options = options.docstring_options and asdict(options.docstring_options)

        with suppress(AliasResolutionError):
            if model.docstring is not None:
                model.docstring.parser = parser
                model.docstring.parser_options = parser_options or {}

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
