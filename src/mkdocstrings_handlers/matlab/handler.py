from pathlib import Path
from collections import ChainMap
from markdown import Markdown
from mkdocstrings.handlers.base import BaseHandler, CollectorItem, CollectionError
from mkdocstrings_handlers.python import rendering
from typing import Any, ClassVar, Mapping
from griffe import Docstring, Parameters, Parameter, ParameterKind
from pprint import pprint


import charset_normalizer
import json


from mkdocstrings_handlers.matlab.collections import LinesCollection, ModelsCollection
from mkdocstrings_handlers.matlab_engine import MatlabEngine, MatlabExecutionError
from mkdocstrings_handlers.matlab.models import (
    Function,
    Class,
    Classfolder,
    Namespace,
    Property,
    ROOT,
)
from mkdocstrings_handlers.matlab.parser import MatlabParser


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
        "show_inheritance_diagram": False,  # Insider feature
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
        "merge_init_into_class": False,
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
            paths = ""
        else:
            config_path = Path(config_file_path).parent
            full_paths = [str((config_path / path).resolve()) for path in paths]

        self.engine = MatlabEngine()
        self.engine.addpath(str(Path(__file__).parent / "matlab"))
        self.engine.matlab_startup(full_paths, startup_expression)
        self.models = ModelsCollection()
        self.lines = LinesCollection()
        self.parser = MatlabParser()
        self._locale = locale

    def get_templates_dir(self, handler: str | None = None) -> Path:
        # use the python handler templates
        # (it assumes the python handler is installed)
        return super().get_templates_dir("python")

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
        final_config = ChainMap(config, self.default_config)  # type: ignore[arg-type]
        if identifier in self.models:
            return self.models[identifier]

        try:
            ast_json = self.engine.docstring.resolve(identifier)
        except MatlabExecutionError as error:
            raise CollectionError(error.args[0].strip()) from error
        ast_dict = json.loads(ast_json)

        filepath = Path(ast_dict["path"])
        if filepath not in self.lines:
            lines = str(charset_normalizer.from_path(filepath).best()).splitlines()
            self.lines[filepath] = lines

        match ast_dict["type"]:
            case "function" | "method":
                return self.collect_function(ast_dict, final_config)
            case "class":
                return self.collect_class(ast_dict, final_config)
            case _:
                return None

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

    def get_anchors(self, data: CollectorItem) -> tuple[str, ...]:
        """Return the possible identifiers (HTML anchors) for a collected item.

        Arguments:
            data: The collected data.

        Returns:
            The HTML anchors (without '#'), or an empty tuple if this item doesn't have an anchor.
        """
        anchors = [data.path]
        return tuple(anchors)

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

    def collect_class(self, ast_dict: dict, config: Mapping) -> Class:
        docstring = (
            Docstring(ast_dict["docstring"], parser=config["docstring_style"])
            if ast_dict["docstring"]
            else None
        )

        filepath = Path(ast_dict["path"])

        if config["show_source"]:
            tmObject = self.parser.parse_file(filepath)
            tmClass = next(
                child
                for child in tmObject.children
                if child.token == "meta.class.matlab"
            )
        else:
            tmClass = None

        bases = ast_dict["superclasses"] if isinstance(ast_dict["superclasses"], list) else [ast_dict["superclasses"]]
        bases = [base for base in bases if base != "handle"]

        model = Class(
            ast_dict["name"],
            docstring=docstring,
            parent=self.get_parent(filepath.parent),
            hidden=ast_dict["hidden"],
            sealed=ast_dict["sealed"],
            abstract=ast_dict["abstract"],
            enumeration=ast_dict["enumeration"],
            handle=ast_dict["handle"],
            bases=bases,
            filepath=filepath,
            modules_collection=self.models,
            lines_collection=self.lines,
            lineno=1,
            endlineno=len(self.lines[filepath]),
            textmate=tmClass,
        )

        for property_dict in ast_dict["properties"]:
            name = property_dict.pop("name")
            defining_class = property_dict.pop("class")
            property_doc = property_dict.pop("docstring")
            docstring = (
                Docstring(property_doc, parser=config["docstring_style"])
                if property_doc
                else None
            )
            if (
                defining_class != model.canonical_path
                and not config["inherited_members"]
            ):
                continue

            prop = Property(name, docstring=docstring, parent=model, **property_dict)
            model.members[name] = prop
            self.models[prop.canonical_path] = prop

        for method_dict in ast_dict["methods"]:
            name = method_dict.pop("name")
            defining_class = method_dict.pop("class")
            if (
                defining_class != model.canonical_path
                and not config["inherited_members"]
            ):
                continue

            method = self.collect(f"{defining_class}.{name}", config)
            (method.lineno, method.endlineno) = model.get_lineno_method(name)
            method.parent = model
            method._access = method_dict["access"]
            method._static = method_dict["static"]
            method._abstract = method_dict["abstract"]
            method._sealed = method_dict["sealed"]
            method._hidden = method_dict["hidden"]

            model.members[name] = method
            self.models[method.canonical_path] = method

        if config["merge_init_into_class"] and model.name in model.members:
            constructor = model.members.pop(model.name)
            model.members["__init__"] = constructor
            if constructor.docstring.value == model.docstring.value:
                model.docstring = None

        self.models[model.canonical_path] = model

        return model

    def collect_function(self, ast_dict: dict, config: Mapping) -> Function:
        parameters = []

        inputs = (
            ast_dict["inputs"]
            if isinstance(ast_dict["inputs"], list)
            else [ast_dict["inputs"]]
        )
        for input_dict in inputs:
            if input_dict["name"] == "varargin":
                parameter_kind = ParameterKind.var_positional
            elif input_dict["kind"] == "positional":
                parameter_kind = ParameterKind.positional_only
            else:
                parameter_kind = ParameterKind.keyword_only

            parameters.append(
                Parameter(
                    input_dict["name"],
                    kind=parameter_kind,
                    annotation=input_dict["class"],
                    default=input_dict["default"] if input_dict["default"] else None,
                )
            )

        filepath = Path(ast_dict["path"])
        model = Function(
            ast_dict["name"],
            parameters=Parameters(*parameters),
            docstring=Docstring(
                ast_dict["docstring"],
                parser=config["docstring_style"],
                parser_options=config["docstring_options"],
            )
            if ast_dict["docstring"]
            else None,
            parent=self.get_parent(filepath.parent),
            filepath=filepath,
            modules_collection=self.models,
            lines_collection=self.lines,
            lineno=1,
            endlineno=len(self.lines[filepath]),
        )

        self.models[model.canonical_path] = model
        return model

    def get_parent(self, path: Path) -> Namespace | Classfolder:
        if path.stem[0] == "+":
            parent = Namespace(
                path.stem[1:], filepath=path, parent=self.get_parent(path.parent)
            )
            identifier = parent.canonical_path
            if identifier in self.models:
                parent = self.models[identifier]
            else:
                self.models[identifier] = parent

        elif path.stem[0] == "@":
            parent = Classfolder(
                path.stem[1:], filepath=path, parent=self.get_parent(path.parent)
            )
            identifier = parent.canonical_path
            if identifier in self.models:
                parent = self.models[identifier]
            else:
                self.models[identifier] = parent

        else:
            parent = ROOT
        return parent


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
