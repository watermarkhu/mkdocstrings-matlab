"""A script to copy the modules and attributes templates from
the python handler to the matlab handler and update the names"""

from mkdocstrings_handlers.python.handler import PythonHandler
from pathlib import Path
import re

# Get the templates directory of the python handler
pythonHandler = PythonHandler("python", "material")
templatesDir = pythonHandler.get_templates_dir()
targetDir = (
    Path(__file__).parent.parent
    / "src"
    / "mkdocstrings_handlers"
    / "matlab"
    / "templates"
)


def copy_template(
    sourcePath: str,
    targetPath: str,
    mapping: dict[str, str] = {},
    theme: str = "material",
):
    sourceFile = templatesDir / theme / sourcePath
    targetFile = targetDir / theme / targetPath
    content = sourceFile.read_text()
    pattern = re.compile(
        "|".join([re.escape(k) for k in sorted(mapping, key=len, reverse=True)]),
        flags=re.DOTALL,
    )
    content = pattern.sub(lambda x: mapping[x.group(0)], content)
    targetFile.write_text(content)

    return (targetFile, content)


# Copy the namespace and module templates
copy_template(
    "_base/module.html.jinja",
    "folder.html.jinja",
    {"doc-symbol-module": "doc-symbol-folder"},
)
copy_template(
    "_base/module.html.jinja",
    "namespace.html.jinja",
    {"doc-symbol-module": "doc-symbol-namespace"},
)

# Copy the property template
copy_template(
    "_base/attribute.html.jinja",
    "property.html.jinja",
    {"doc-symbol-attribute": "doc-symbol-property"},
)

# Copy the summary modules template
copy_template(
    "_base/summary.html.jinja",
    "summary.html.jinja",
    {
        "summary/modules": "summary/namespaces",
        "summary/attributes": "summary/properties",
    },
)


## Copy the summary properties template
copy_template(
    "_base/summary/attributes.html.jinja",
    "summary/properties.html.jinja",
    {
        "docstring/attributes": "docstring/properties",
        "Summary of attributes": "Summary of properties",
    },
)
copy_template(
    "_base/docstring/attributes.html.jinja",
    "docstring/properties.html.jinja",
    {
        'lang.t("Attributes:")': '"Properties:"',
        'lang.t("ATTRIBUTE")': '"PROPERTY:"',
        " attributes ": " properties ",
        '"Attributes"': '"Properties"',
    },
)

## Copy the summary namespaces template
copy_template(
    "_base/summary/modules.html.jinja",
    "summary/namespaces.html.jinja",
    {
        "docstring/modules": "docstring/namespaces",
        "Summary of modules": "Summary of namespaces",
    },
)
copy_template(
    "_base/docstring/modules.html.jinja",
    "docstring/namespaces.html.jinja",
    {
        'lang.t("Modules:")': '"Namespaces:"',
        'lang.t("MODULE")': '"NAMESPACE:"',
        " modules ": " namespaces ",
        '"Modules"': '"Namespaces"',
    },
)

## Copy children template
copy_template(
    "_base/children.html.jinja",
    "children.html.jinja",
    {
        "-attributes": "-properties",
        "Attributes": "Properties",
        "-modules": "-namespaces",
        "Modules": "Modules",
        "{% if config.show_submodules %}": "{% if config.show_submodules or obj.is_folder %}",
        "{% elif child.is_module and config.show_submodules %}": "{% elif (child.is_namespace and config.show_submodules) or obj.is_folder %}",
    },
)
