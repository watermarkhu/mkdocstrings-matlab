"""The mkdocstrings handler for processing MATLAB code documentation."""

from pathlib import Path
from collections import ChainMap
from jinja2.loaders import FileSystemLoader
from markdown import Markdown
from mkdocs.exceptions import PluginError
from mkdocstrings.handlers.base import BaseHandler, CollectorItem, CollectionError
from mkdocstrings_handlers.python import rendering
from typing import Any, ClassVar, Mapping
from pprint import pprint

import re

from mkdocstrings_handlers.matlab.collect import LinesCollection, PathCollection


class MatlabHandler(BaseHandler):
    """The `MatlabHandler` class is a handler for processing Matlab code documentation."""

    name: str = "matlab"
    """The handler's name."""
    domain: str = "mat"  # to match Sphinx's default domain
    """The cross-documentation domain/language for this handler."""
    enable_inventory: bool = True
    """Whether this handler is interested in enabling the creation of the `objects.inv` Sphinx inventory file."""
    fallback_theme = "material"
    """The fallback theme."""
    fallback_config: ClassVar[dict] = {
        "fallback": True,
    }
    """The configuration used to collect item during autorefs fallback."""
    default_config: ClassVar[dict] = {
        # General options
        "show_bases": True,
        "show_inheritance_diagram": False,
        "show_source": True,
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
        "members": None,
        "hidden_members": False,
        "private_members": False,
        "inherited_members": False,
        "members_order": rendering.Order.alphabetical.value,
        "filters": ["!^delete$|^disp$"],
        "group_by_category": True,
        "show_subnamespaces": False,
        "summary": False,
        "show_labels": True,
        # Docstring options
        "docstring_style": "google",
        "docstring_options": {},
        "docstring_section_style": "table",
        "parse_arguments": False,
        "merge_constructor_into_class": False,
        "merge_constructor_ignore_summary": False,
        "show_if_no_docstring": False,
        "show_docstring_propeties": True,
        "show_docstring_functions": True,
        "show_docstring_classes": True,
        "show_docstring_namespaces": True,
        "show_docstring_description": True,
        "show_docstring_examples": True,
        "show_docstring_input_arguments": True,
        "show_docstring_name_value_arguments": True,
        "show_docstring_output_arguments": True,
        # Signature options
        "show_signature": True,
        "show_signature_annotations": False,
        "separate_signature": False,
        "signature_crossrefs": False,
    }
    """Default handler configuration.

    Attributes: General options:
        show_bases (bool): Show the base classes of a class. Default: `True`.
        show_inheritance_diagram (bool): Show the inheritance diagram of a class using Mermaid. Default: `False`.
        show_source (bool): Show the source code of this object. Default: `True`.


    Attributes: Headings options:
        heading_level (int): The initial heading level to use. Default: `2`.
        parameter_headings (bool): Whether to render headings for parameters (therefore showing parameters in the ToC). Default: `False`.
        show_root_heading (bool): Show the heading of the object at the root of the documentation tree
            (i.e. the object referenced by the identifier after `:::`). Default: `False`.
        show_root_toc_entry (bool): If the root heading is not shown, at least add a ToC entry for it. Default: `True`.
        show_root_full_path (bool): Show the full path for the root object heading. Default: `True`.
        show_root_members_full_path (bool): Show the full path of the root members. Default: `False`.
        show_object_full_path (bool): Show the full path of every object. Default: `False`.
        show_category_heading (bool): When grouped by categories, show a heading for each category. Default: `False`.
        show_symbol_type_heading (bool): Show the symbol type in headings (e.g. mod, class, meth, func and attr). Default: `False`.
        show_symbol_type_toc (bool): Show the symbol type in the Table of Contents (e.g. mod, class, methd, func and attr). Default: `False`.

    Attributes: Members options:
        members (list[str] | bool | None): A boolean, or an explicit list of members to render.
            If true, select all members without further filtering.
            If false or empty list, do not render members.
            If none, select all members and apply further filtering with filters and docstrings. Default: `None`.
        hidden_members (list[str] | bool | None): A boolean, or an explicit list of hidden members to render. 
            If true, select all inherited members, which can then be filtered with `members`.
            If false or empty list, do not select any hidden member. Default: `False`.
        private_members (list[str] | bool | None): A boolean, or an explicit list of private members to render. 
            If true, select all inherited members, which can then be filtered with `members`.
            If false or empty list,  do not select any private member.  Default: `False`.
        inherited_members (list[str] | bool | None): A boolean, or an explicit list of inherited members to render.
            If true, select all inherited members, which can then be filtered with `members`.
            If false or empty list, do not select any inherited member. Default: `False`.
        members_order (str): The members ordering to use. Options: `alphabetical` - order by the members names,
            `source` - order members as they appear in the source file. Default: `"alphabetical"`.
        filters (list[str] | None): A list of filters applied to filter objects based on their name.
            A filter starting with `!` will exclude matching objects instead of including them.
            The `members` option takes precedence over `filters` (filters will still be applied recursively
            to lower members in the hierarchy). Default: `["!^delete$|^disp$"]`.
        group_by_category (bool): Group the object's children by categories: properties, classes, functions, and namespaces. Default: `True`.
        show_subnamespaces (bool): When rendering a namespace, show its subnamespaces recursively. Default: `False`.
        summary (bool | dict[str, bool]): Whether to render summaries of namespaces, classes, functions (methods) and properties. Default: `False`.
        show_labels (bool): Whether to show labels of the members. Default: `True`.

    Attributes: Docstrings options:
        docstring_style (str): The docstring style to use: `google`, `numpy`, `sphinx`, or `None`. Default: `"google"`.
        docstring_options (dict): The options for the docstring parser. See [docstring parsers](https://mkdocstrings.github.io/griffe/reference/docstrings/) and their options in Griffe docs.
        docstring_section_style (str): The style used to render docstring sections. Options: `table`, `list`, `spacy`. Default: `"table"`.
        parse_arguments (bool): Whether to load inputs and output parameters based on argument validation blocks. Default: `True`.
        merge_constructor_into_class (bool): Whether to merge the constructor method into the class' signature and docstring. Default: `False`.
        merge_constructor_ignore_summary (bool): Whether to ignore the constructor summary when merging it into the class. Default: `False`.
        show_if_no_docstring (bool): Show the object heading even if it has no docstring or children with docstrings. Default: `False`.
        show_docstring_properties (bool): Whether to display the "Properties" section in the object's docstring. Default: `True`.
        show_docstring_functions (bool): Whether to display the "Functions" or "Methods" sections in the object's docstring. Default: `True`.
        show_docstring_classes (bool): Whether to display the "Classes" section in the object's docstring. Default: `True`.
        show_docstring_namespaces (bool): Whether to display the "Namespaces" section in the object's docstring. Default: `True`.
        show_docstring_description (bool): Whether to display the textual block (including admonitions) in the object's docstring. Default: `True`.
        show_docstring_examples (bool): Whether to display the "Examples" section in the object's docstring. Default: `True`.
        show_docstring_input_arguments (bool): Whether to display the "Input arguments" section in the object's docstring. Default: `True`.
        show_docstring_name_value_arguments (bool): Whether to display the "Name-value pairs" section in the object's docstring. Default: `True`.
        show_docstring_output_arguments (bool): Whether to display the "Output arguments" section in the object's docstring. Default: `True`.

    Attributes: Signatures/annotations options:
        show_signature (bool): Show methods and functions signatures. Default: `True`.
        show_signature_annotations (bool): Show the type annotations in methods and functions signatures. Default: `False`.
        separate_signature (bool): Whether to put the whole signature in a code block below the heading.
        signature_crossrefs (bool): Whether to render cross-references for type annotations in signatures. Default: `False`.
    """

    def __init__(
        self,
        handler: str,
        theme: str,
        custom_templates: str | None = None,
        config_file_path: str | None = None,
        paths: list[str] | None = None,
        paths_recursive: bool = False,
        locale: str = "en",
        **kwargs: Any,
    ) -> None:
        """
        Initialize the handler with the given configuration.

        Args:
            handler: The name of the handler.
            theme: The name of theme to use.
            custom_templates: Directory containing custom templates.
            config_file_path (str | None, optional): Path to the configuration file. Defaults to None.
            paths (list[str] | None, optional): List of paths to include. Defaults to None.
            paths_recursive (bool, optional): Whether to include paths recursively. Defaults to False.
            locale (str, optional): Locale setting. Defaults to "en".
            **kwargs (Any): Arbitrary keyword arguments.

        Returns:
            None
        """

        super().__init__(handler, theme, custom_templates=custom_templates)

        theme_path = Path(__file__).resolve().parent / "templates" / theme
        if theme_path.exists() and isinstance(self.env.loader, FileSystemLoader):
            # Insert our templates directory at the beginning of the search path to overload the Python templates
            self.env.loader.searchpath.insert(0, str(theme_path))
        css_path = theme_path / "style.css"
        if css_path.exists():
            self.extra_css += "\n" + css_path.read_text(encoding="utf-8")

        if paths is None or config_file_path is None:
            config_path = None
            full_paths = []
        else:
            config_path = Path(config_file_path).parent
            full_paths = [(config_path / path).resolve() for path in paths]

        if pathIds := [str(path) for path in full_paths if not path.is_dir()]:
            raise PluginError(
                "The following paths do not exist or are not directories: "
                + ", ".join(pathIds)
            )

        self.paths: PathCollection = PathCollection(
            full_paths, recursive=paths_recursive, config_path=config_path
        )
        self.lines: LinesCollection = self.paths.lines_collection
        self._locale: str = locale

    def get_templates_dir(self, *args, **kwargs) -> Path:
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

        try:
            final_config["members_order"] = rendering.Order(
                final_config["members_order"]
            )
        except ValueError as error:
            choices = "', '".join(item.value for item in rendering.Order)
            raise PluginError(
                f"Unknown members_order '{final_config['members_order']}', choose between '{choices}'.",
            ) from error

        if final_config["filters"]:
            final_config["filters"] = [
                (re.compile(filtr.lstrip("!")), filtr.startswith("!"))
                for filtr in final_config["filters"]
            ]

        summary = final_config["summary"]
        if summary is True:
            final_config["summary"] = {
                "attributes": True,
                "functions": True,
                "classes": True,
                "modules": True,
            }
        elif summary is False:
            final_config["summary"] = {
                "attributes": False,
                "functions": False,
                "classes": False,
                "modules": False,
            }
        else:
            final_config["summary"] = {
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
        final_config["show_docstring_attributes"] = config.get(
            "show_docstring_properties", True
        )
        final_config["show_docstring_modules"] = config.get(
            "show_docstring_namespaces", True
        )
        final_config["show_docstring_parameters"] = config.get(
            "show_docstring_input_arguments", True
        )
        final_config["show_docstring_other_parameters"] = config.get(
            "show_docstring_name_value_arguments", True
        )
        final_config["show_docstring_returns"] = config.get(
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
            final_config[setting] = False
        final_config["line_length"] = 88

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
        model = self.paths.resolve(identifier, config=final_config)
        if model is None:
            raise CollectionError(f"Identifier '{identifier}' not found")
        return model


def get_handler(
    *,
    theme: str,
    custom_templates: str | None = None,
    config_file_path: str | None = None,
    paths: list[str] | None = None,
    paths_recursive: bool = False,
    **config: Any,
) -> MatlabHandler:
    """
    Create and return a MatlabHandler object with the specified configuration.

    Parameters:
        theme (str): The theme to be used by the handler.
        custom_templates (str | None, optional): Path to custom templates. Defaults to None.
        config_file_path (str | None, optional): Path to the configuration file. Defaults to None.
        paths (list[str] | None, optional): List of paths to include. Defaults to None.
        paths_recursive (bool, optional): Whether to include paths recursively. Defaults to False.
        **config (Any): Additional configuration options.

    Returns:
        MatlabHandler: An instance of MatlabHandler configured with the provided parameters.
    """
    return MatlabHandler(
        handler="matlab",
        theme=theme,
        custom_templates=custom_templates,
        config_file_path=config_file_path,
        paths=paths,
        paths_recursive=paths_recursive,
    )


if __name__ == "__main__":
    handler = get_handler(theme="material")
    pprint(handler.collect("matlab_startup", {}).docstring.parse("google"))
