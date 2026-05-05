"""PDF handler."""

import typst
from docutils.frontend import validate_boolean

from .package import install_package
from .writer import Writer as BaseWriter


class Writer(BaseWriter):
    format = "pdf"

    settings_spec = BaseWriter.settings_spec + (
        "TypstPDF Writer Options",
        None,
        (
            (
                "Install Typst local package forcely.",
                ["--force-install-package"],
                {
                    "action": "store_true",
                    "dest": "force_install_package",
                    "default": False,
                    "validator": validate_boolean,
                },
            ),
        ),
    )

    def translate(self):
        super().translate()
        install_package(force=self.document.settings.force_install_package)
        self.output = typst.compile(self.output.encode())
