"""PDF handler."""

import os

import typst
from docutils.frontend import validate_boolean

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
                "List of directories stored custom fonts.",
                ["--font-paths"],
                {
                    "action": "store",
                    "dest": "font_paths",
                    "default": [],
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
        font_paths = list(self.document.settings.font_paths)
        if "TYPST_FONT_PATHS" in os.environ:
            font_paths += os.environ["TYPST_FONT_PATHS"].split(os.pathsep)
        self.output = typst.compile(self.output.encode(), font_paths=font_paths)

    def display_warnings(self):
        pass
