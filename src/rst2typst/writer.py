"""Writer for docutils."""

from __future__ import annotations

from docutils import nodes
from docutils.writers import Writer as BaseWriter


class Writer(BaseWriter):
    def __init__(self):
        super().__init__()
        self.translator_class = TypstTranslator

    def translate(self):
        visitor = self.translator_class(self.document)
        self.document.walkabout(visitor)
        self.output = "\n".join(visitor.body)


class TypstTranslator(nodes.NodeVisitor):
    # NOTE: Guard for NotImplementedError for unknown nodes. Remove as soon as possible.
    class WarningOnly:
        def __contains__(self, item):
            return True

    def __init__(self, document):
        super().__init__(document)
        self.document = document
        self.optional = self.WarningOnly()
        self.body = []
