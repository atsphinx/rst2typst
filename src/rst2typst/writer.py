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
        self.section_level = 0
        self._line_prefixes = [""]

    # --
    # State controls
    # ---

    def _push_prefix(self, text: str):
        self._line_prefixes.append(text)

    def _pop_prefix(self):
        self._line_prefixes.pop()

    # --
    # For base syntax
    # --

    def visit_Text(self, node: nodes.Text):
        prefix_ = " " * sum([len(prefix) for prefix in self._line_prefixes[:-1]])
        midfix_ = self._line_prefixes[-1]
        lines = [
            (
                f"{prefix_}{midfix_}{t}"
                if idx == 0
                else f"{prefix_}{' ' * len(midfix_)}{t}"
            )
            for idx, t in enumerate(node.astext().split("\n"))
        ]
        self.body.append("\n".join(lines))

    def depart_Text(self, node: nodes.Text):
        pass

    # --
    # For doctree nodes
    # --

    # Refs:
    #   - https://www.docutils.org/docs/ref/doctree.html#block-quote
    #   - https://typst.app/docs/reference/model/quote/
    def visit_block_quote(self, node: nodes.block_quote):
        self._push_prefix("  ")
        args = []
        attrs = list(node.findall(nodes.attribution))
        if attrs:
            args.append(f"attribution: [{attrs[0].astext()}]")
            for a in attrs:
                node.remove(a)
        self.body.append(f"#quote({' '.join(args)})[\n")

    def depart_block_quote(self, node: nodes.block_quote):
        self._pop_prefix()
        self.body.append("]\n")

    # Refs:
    #   - https://www.docutils.org/docs/ref/doctree.html#bullet-list
    #   - https://typst.app/docs/reference/model/list/
    def visit_bullet_list(self, node: nodes.bullet_list):
        self._push_prefix("- ")

    def depart_bullet_list(self, node: nodes.bullet_list):
        self._pop_prefix()
        if isinstance(node.parent, (nodes.document, nodes.section)):
            self.body.append("\n")

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
    #   - https://www.docutils.org/docs/ref/doctree.html#enumerated-list
    #   - https://typst.app/docs/reference/model/enum/
    def visit_enumerated_list(self, node: nodes.enumerated_list):
        self._push_prefix("+ ")

    def depart_enumerated_list(self, node: nodes.enumerated_list):
        self._pop_prefix()
        if isinstance(node.parent, (nodes.document, nodes.section)):
            self.body.append("\n")

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
    #   - https://www.docutils.org/docs/ref/doctree.html#literal-block
    #   - https://typst.app/docs/reference/text/raw/
    def visit_literal_block(self, node: nodes.literal_block):
        if "code" in node["classes"]:
            code = node["classes"][-1]
            self.body.append(f"```{code}\n")
            return
        self.body.append("```\n")

    def depart_literal_block(self, node: nodes.literal_block):
        self.body.append("\n```\n\n")

    # Refs:
    #   - https://www.docutils.org/docs/ref/doctree.html#paragraph
    def visit_paragraph(self, node: nodes.paragraph):
        pass

    def depart_paragraph(self, node: nodes.paragraph):
        self.body.append("\n")
        if isinstance(node.parent, (nodes.document, nodes.section)):
            self.body.append("\n")

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

    def visit_section(self, node: nodes.section):
        self.section_level += 1

    def depart_section(self, node: nodes.section):
        self.section_level -= 1

    # Refs:
    #   - https://www.docutils.org/docs/ref/doctree.html#strong
    #   - https://typst.app/docs/reference/model/strong/
    def visit_strong(self, node: nodes.strong):
        self.body.append("*")

    def depart_strong(self, node: nodes.strong):
        self.body.append("*")

    def visit_title(self, node: nodes.title):
        if isinstance(node.parent, nodes.document):
            self.body.append("#title([")
        else:
            prefix = "=" * self.section_level
            self.body.append(f"{prefix} ")

    def depart_title(self, node: nodes.title):
        if isinstance(node.parent, nodes.document):
            self.body.append("])\n\n")
        else:
            self.body.append("\n\n")
