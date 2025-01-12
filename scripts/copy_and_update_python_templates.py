"""A script to copy the modules and attributes templates from 
the python handler to the matlab handler and update the names"""

from mkdocstrings_handlers.python.handler import PythonHandler
from pathlib import Path

# Get the templates directory of the python handler
pythonHandler = PythonHandler('python', 'material')
templatesDir = pythonHandler.get_templates_dir()
targetDir = Path(__file__).parent.parent / "src" / "mkdocstrings_handlers" / "matlab" / "templates" / "matlab"

# Copy the namespace and module templates
moduleTemplate = templatesDir / "material" / "_base" / "module.html.jinja"

targetFile = targetDir / "material" /  "folder.html.jinja"
content = moduleTemplate.read_text().replace("doc-symbol-module", "doc-symbol-folder")
targetFile.write_text(content)

targetFile = targetDir / "material" /  "namespace.html.jinja"
content = moduleTemplate.read_text().replace("doc-symbol-module", "doc-symbol-namespace")
targetFile.write_text(content)

# Copy the class and function templates
attributeTemplate = templatesDir / "material" / "_base" / "attribute.html.jinja"
targetFile = targetDir / "material" /  "property.html.jinja"
content = attributeTemplate.read_text().replace("doc-symbol-attribute", "doc-symbol-property")
targetFile.write_text(content)
