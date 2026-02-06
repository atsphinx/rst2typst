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
        visitor: TypstTranslator = self.translator_class(self.document)
        self.document.walkabout(visitor)
        self.output = "".join(visitor.body)


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

    # Refs:
    #   - https://www.docutils.org/docs/ref/doctree.html#comment
    def visit_comment(self, node: nodes.comment):
        raise nodes.SkipNode

    # Refs:
    #   - https://www.docutils.org/docs/ref/doctree.html#emphasis
    #   - https://typst.app/docs/reference/model/emph/
    def visit_emphasis(self, node: nodes.emphasis):
        self.body.append("_")

    def depart_emphasis(self, node: nodes.emphasis):
        self.body.append("_")

    # Refs:
    #   - https://www.docutils.org/docs/ref/doctree.html#literal
    #   - https://typst.app/docs/reference/model/raw/
    def visit_literal(self, node: nodes.literal):
        # TODO: Correct way to detect language
        if "code" in node["classes"]:
            code = node["classes"][-1]
            self.body.append(f"```{code} ")
            return
        self.body.append("`")

    # Refs:
    #   - https://www.docutils.org/docs/ref/doctree.html#paragraph
    def visit_paragraph(self, node: nodes.paragraph):
        pass

    def depart_paragraph(self, node: nodes.paragraph):
        self.body.append("\n\n")

    def depart_literal(self, node: nodes.literal):
        # TODO: Reserve appending text after visit
        if "code" in node["classes"]:
            self.body.append("```")
            return
        self.body.append("`")

    # Refs:
    #   - https://www.docutils.org/docs/ref/doctree.html#reference
    def visit_reference(self, node: nodes.reference):
        # TODO: Add case for internal links if exists.
        href = node["refuri"]
        self.body.append(f'#link("{href}")[')

    def depart_reference(self, node: nodes.reference):
        self.body.append("]")

    # Refs:
    #   - https://www.docutils.org/docs/ref/doctree.html#strong
    #   - https://typst.app/docs/reference/model/strong/
    def visit_strong(self, node: nodes.strong):
        self.body.append("*")

    def depart_strong(self, node: nodes.strong):
        self.body.append("*")
