"""PDF handler."""

import os

import typst
from docutils.frontend import validate_boolean, validate_comma_separated_list

from .package import install_package, package_dir
from .writer import Writer as BaseWriter


class Writer(BaseWriter):
    format = "pdf"

    settings_spec = BaseWriter.settings_spec + (
        "TypstPDF Writer Options",
        None,
        (
            (
                "Install Typst local package forcibly.",
                ["--force-install-package"],
                {
                    "action": "store_true",
                    "dest": "force_install_package",
                    "default": False,
                    "validator": validate_boolean,
                },
            ),
            (
                "List of directories where custom fonts are stored.",
                ["--font-paths"],
                {
                    "action": "append",
                    "dest": "font_paths",
                    "metavar": "<item[,item,...]>",
                    "default": [],
                    "validator": validate_comma_separated_list,
                },
            ),
        ),
    )

    def translate(self):
        super().translate()

        install_package(
            package_dir,
            "rst2typst",
            force=self.document.settings.force_install_package,
        )
        font_paths = self.document.settings.font_paths
        if isinstance(font_paths, str):
            font_paths = [font_paths]
        else:
            font_paths = list(font_paths)
        env_font_paths = os.environ.get("TYPST_FONT_PATHS")
        if env_font_paths:
            font_paths += env_font_paths.split(os.pathsep)
        self.output = typst.compile(self.output.encode(), font_paths=font_paths)

    def display_warnings(self):
        pass
