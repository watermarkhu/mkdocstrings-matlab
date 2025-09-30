"""The mkdocstrings handler for processing MATLAB code documentation."""

from __future__ import annotations

from contextlib import suppress
from dataclasses import asdict
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar

from griffe import AliasResolutionError, Parser
from maxx.collection import LinesCollection, PathsCollection
from mkdocs.exceptions import PluginError
from mkdocstrings import (
    BaseHandler,
    CollectionError,
    CollectorItem,
    HandlerOptions,
    get_logger,
)

from mkdocstrings_handlers.matlab import rendering
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
            for theme_dir in base_dir.joinpath(self.custom_templates, "matlab").iterdir():
                if theme_dir.joinpath("_base").is_dir():
                    _logger.warning(
                        f"Overriding base template '{theme_dir.name}/_base/<template>.html.jinja' is not supported, "
                        f"override '{theme_dir.name}/<template>.html.jinja' instead",
                    )

        if config.paths:
            full_paths = []
            for path in config.paths:
                if "*" in path:
                    full_paths.extend([d for d in base_dir.glob(path) if d.is_dir()])
                else:
                    full_paths.append((base_dir / path).resolve())
        else:
            full_paths = []

        if path_ids := [str(path) for path in full_paths if not path.is_dir()]:
            raise PluginError(
                "The following paths do not exist or are not directories: " + ", ".join(path_ids)
            )

        self._paths = full_paths
        self._paths_collection: PathsCollection = PathsCollection(
            full_paths, recursive=config.paths_recursive, working_directory=base_dir
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
            return MatlabOptions.from_data(**options)
        except Exception as error:
            raise PluginError(f"Invalid options: {error}") from error

    def render(self, data: CollectorItem, options: MatlabOptions) -> str:
        """Render a template using provided data and configuration options.

        Arguments:
            data: The collected data to render.
            options: The handler's configuration options.

        Returns:
            The rendered template as HTML.
        """

        template_name = rendering.do_get_template(data)
        template = self.env.get_template(template_name)

        if hasattr(data, "docstring") and data.docstring is not None:
            data.docstring.parse()

        heading_level = options.heading_level

        html = template.render(
            **{
                "config": options,
                data.kind.value: data,
                "heading_level": heading_level,
                "root": True,
                "locale": self.config.locale,
            },
        )

        if self.env.filters["stash_crossref"].stash:
            pass

        return html

    def update_env(self, config: Any) -> None:  # noqa: ARG002
        """Update the Jinja environment with custom filters and tests.

        Parameters:
            config: The SSG configuration.
        """
        self.env.trim_blocks = True
        self.env.lstrip_blocks = True
        self.env.keep_trailing_newline = False
        self.env.filters["order_members"] = rendering.do_order_members
        self.env.filters["format_signature"] = rendering.do_format_signature
        self.env.filters["format_property"] = rendering.do_format_property
        self.env.filters["format_arguments"] = rendering.do_format_arguments
        self.env.filters["filter_objects"] = rendering.do_filter_objects
        self.env.filters["stash_crossref"] = rendering.do_stash_crossref
        self.env.filters["get_template"] = rendering.do_get_template
        self.env.filters["function_docstring"] = rendering.do_function_docstring
        self.env.filters["parse_docstring"] = rendering.do_parse_docstring
        self.env.filters["as_properties_section"] = rendering.do_as_properties_section
        self.env.filters["as_functions_section"] = rendering.do_as_functions_section
        self.env.filters["as_classes_section"] = rendering.do_as_classes_section
        self.env.filters["as_namespaces_section"] = rendering.do_as_namespaces_section
        self.env.filters["as_inheritance_diagram_section"] = (
            rendering.do_as_inheritance_diagram_section
        )
        self.env.globals["AutorefsHook"] = rendering.AutorefsHook
        self.env.tests["existing_template"] = (
            lambda template_name: template_name in self.env.list_templates()
        )
        # The following is required since in MATLAB there is a concept called namespace
        # This is used as a variable in Jinja templates and would overwrite the namespace macro
        # Thus we create an alias for this.
        self.env.globals["jinja_namespace"] = self.env.globals["namespace"]
        self.env.globals["paths_collection"] = self._paths_collection

    def collect(self, identifier: str, options: MatlabOptions) -> CollectorItem:
        """Collect data given an identifier and user configuration.

        In the implementation, you typically call a subprocess that returns JSON, and load that JSON again into
        a Python dictionary for example, though the implementation is completely free.

        Arguments:
            identifier: An identifier for which to collect data.
            options: The handler's configuration options.

        Returns:
            CollectorItem
        """
        if identifier == "":
            raise CollectionError("Empty identifier")

        if options == {}:
            options = self.get_options({})

        try:
            if "/" in identifier:
                # If the identifier contains a slash, it is a path to a file.
                # We use the lines collection to get the model.
                path = (self.base_dir / identifier).resolve()
                if path in self._paths_collection._folders:
                    # If the path is a folder, we return the folder model.
                    model = self._paths_collection._folders[path]
                else:
                    raise CollectionError(
                        f"Path '{identifier}' is not a valid path in the collection"
                    )
            else:
                model = self._paths_collection.get_member(identifier)
        except SyntaxError as ex:
            msg = str(ex)
            if ex.text:
                msg += ":\n" + str(ex.text)
            raise CollectionError(msg) from ex
        except KeyError as ex:
            raise CollectionError(str(ex)) from ex
        except AliasResolutionError as ex:
            raise CollectionError(str(ex)) from ex

        if model is None:
            raise CollectionError(f"Identifier '{identifier}' not found")

        parser_name = options.docstring_style
        parser = parser_name and Parser(parser_name)
        parser_options = options.docstring_options and asdict(
            options.docstring_options  # ty: ignore[invalid-argument-type]
        )

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
