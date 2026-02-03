"""Writer for docutils."""

from __future__ import annotations

from typing import TYPE_CHECKING

from docutils import nodes
from docutils.writers import Writer as BaseWriter

if TYPE_CHECKING:
    from typing import Any


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
        def __contains__(self, item: Any):
            return True

    def __init__(self, document: nodes.document):
        super().__init__(document)
        self.document = document
        self.optional = self.WarningOnly()
        self.body = []

    # --
    # For base syntax
    # --

    def visit_Text(self, node: nodes.Text):
        self.body.append(node.astext())

    def depart_Text(self, node: nodes.Text):
        pass

    # --
    # For doctree nodes
    # --

    # Refs: https://www.docutils.org/docs/ref/doctree.html#comment
    def visit_comment(self, node: nodes.comment):
        raise nodes.SkipNode
