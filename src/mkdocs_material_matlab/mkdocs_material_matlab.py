from mkdocs.plugins import BasePlugin
import os


class MkdocsMaterialMatlabPlugin(BasePlugin):
    def on_config(self, config):
        # Ensure the custom CSS file is included in the extra_css list
        css_path = "css/style.css"
        if css_path not in config["extra_css"]:
            config["extra_css"].append(css_path)
        return config

    def on_post_build(self, *, config):
        # Ensure the custom CSS file is copied to the output directory
        css_src_path = os.path.join(os.path.dirname(__file__), "css", "style.css")
        css_dest_path = os.path.join(config["site_dir"], "css", "style.css")
        os.makedirs(os.path.dirname(css_dest_path), exist_ok=True)
        with open(css_src_path, "rb") as src_file:
            with open(css_dest_path, "wb") as dest_file:
                dest_file.write(src_file.read())
