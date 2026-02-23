"""PDF handler."""

import typst

from .writer import Writer as BaseWriter


class Writer(BaseWriter):
    format = "pdf"

    def translate(self):
        super().translate()
        self.output = typst.compile(self.output.encode())
