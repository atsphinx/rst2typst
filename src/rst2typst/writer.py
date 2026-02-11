"""Writer and related classes for docutils."""

from __future__ import annotations

from typing import TYPE_CHECKING

from docutils import nodes
from docutils.writers import Writer as BaseWriter

from .frontend import validate_comma_separated_int

if TYPE_CHECKING:
    from typing import Any


class Writer(BaseWriter):
    supported = ("typst",)

    settings_spec = BaseWriter.settings_spec + (
        "Typst Writer Options",
        None,
        (
            (
                "Section level for page-break",
                ["--page-break-level"],
                {
                    "metavar": "<int>(,<int>)",
                    "validator": validate_comma_separated_int,
                },
            ),
        ),
    )

    settings_defaults = {"page_break_level": []}

    config_section = "typst writer"

    def __init__(self):
        super().__init__()
        self.translator_class = TypstTranslator

    def translate(self):
        visitor: TypstTranslator = self.translator_class(self.document)
        self.document.walkabout(visitor)  # type: ignore[possibly-missing-attribute]
        self.output = "".join(visitor.body)


class HanglingIndent(list[str]):
    """Controller for line prefixes.

    This class works to render Typst documents for correctly and human readability.
    """

    def __init__(self):
        super().__init__()
        self.append("")

    def push(self, text: str):
        self.append(text)

    def pop(self) -> str:  # type: ignore[invalid-method-override]]
        return super().pop()

    @property
    def prefix(self) -> str:
        """Retrieve prefix with indent for first line of a block."""
        space = " " * sum(len(s) for s in self[:-1])
        return f"{space}{self[-1]}"

    @property
    def indent(self) -> str:
        """Retrieve hangling indent for subsequent lines of a block."""
        return " " * sum(len(s) for s in self)

    def is_indent_only(self) -> bool:
        return self.prefix == self.indent


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
        self._hi = HanglingIndent()

    # --
    # For base syntax
    # --

    def visit_Text(self, node: nodes.Text):
        self.body.append(f"\n{self._hi.indent}".join(node.astext().split("\n")))

    def depart_Text(self, node: nodes.Text):
        pass

    # For doctree nodes
    # =================
    #
    # This section collects visit/depart methods for built-in doctree nodes.
    # Methods are sorted by these rules:
    #
    #   * The order of "Element Categories" of `doctree page`_.
    #   * The order of classification of each categories: "empty", "simple", "compound".
    #   * Alphabetical order of nodes.
    #   * ``visit_`` is first, and ``depart_`` is second if it is exists.
    #
    # It adds reference to pages of typst before definition of each ``visit_`` methods.
    #
    # .. _doctree page: https://www.docutils.org/docs/ref/doctree.html

    # Root Element
    # ------------

    def visit_document(self, node: nodes.document):
        pass

    def depart_document(self, node: nodes.document):
        pass

    # Structural Elements
    # -------------------

    def visit_section(self, node: nodes.section):
        self.section_level += 1
        if (
            self.document.settings.page_break_level
            and self.section_level in self.document.settings.page_break_level
        ):
            self.body.append("#pagebreak()\n\n")

    def depart_section(self, node: nodes.section):
        self.section_level -= 1

    # Structural Subelements
    # ----------------------

    # Refs: https://typst.app/docs/reference/model/title/
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

    # Decorative Elements
    # -------------------
    #
    # Currently, there are not defined.

    # Bibliographic Elements
    # ----------------------
    #
    # Currently, there are not defined.

    # Body Elements
    # -------------

    def visit_image(self, node: nodes.image):
        if self._hi.is_indent_only:
            self.body.append(self._hi.prefix)
        prefix = "#"
        suffix = "\n\n"
        if isinstance(node.parent, nodes.figure):
            prefix = ""
            suffix = ",\n"
        self.body.append(f"{prefix}image(\n")
        self._hi.push("  ")
        self.body.append(f'{self._hi.indent}"{node["uri"]}",\n')
        if "alt" in node:
            self.body.append(f'{self._hi.indent}alt: "{node["alt"]}",\n')
        if "width" in node:
            self.body.append(f"{self._hi.indent}width: {node['width']},\n")
        self._hi.pop()
        self.body.append(f"{self._hi.indent}){suffix}")

    def visit_comment(self, node: nodes.comment):
        raise nodes.SkipNode

    # Refs: https://typst.app/docs/reference/text/raw/
    def visit_literal_block(self, node: nodes.literal_block):
        if "code" in node["classes"]:
            code = node["classes"][-1]
            self.body.append(f"```{code}\n")
            return
        self.body.append("```\n")

    def depart_literal_block(self, node: nodes.literal_block):
        self.body.append("\n```\n\n")

    def visit_paragraph(self, node: nodes.paragraph):
        if self._hi.is_indent_only():
            self.body.append(self._hi.indent)

    def depart_paragraph(self, node: nodes.paragraph):
        self.body.append("\n")
        if isinstance(node.parent, (nodes.document, nodes.section)):
            self.body.append("\n")

    def visit_raw(self, node: nodes.raw):
        if "format" in node and node["format"] == "typst":
            # NOTE: ``self.body.append(node.astext())`` does not work as expected.
            for line in node.astext().split("\n"):
                self.body.append(f"{line}\n")
            self.body.append("\n")
        raise nodes.SkipNode

    def visit_reference(self, node: nodes.reference):
        # TODO: Add case for internal links if exists.
        href = node["refuri"]
        self.body.append(f'#link("{href}")[')

    def depart_reference(self, node: nodes.reference):
        self.body.append("]")

    # Refs: https://typst.app/docs/reference/model/quote/
    def visit_block_quote(self, node: nodes.block_quote):
        self._hi.push("  ")
        args = []
        attrs = list(node.findall(nodes.attribution))
        if attrs:
            args.append(f"attribution: [{attrs[0].astext()}]")
            for a in attrs:
                node.remove(a)
        self.body.append(f"#quote({' '.join(args)})[\n")

    def depart_block_quote(self, node: nodes.block_quote):
        self._hi.pop()
        self.body.append("]\n")

    # Refs: https://typst.app/docs/reference/model/list/
    def visit_bullet_list(self, node: nodes.bullet_list):
        self._hi.push("- ")

    def depart_bullet_list(self, node: nodes.bullet_list):
        self._hi.pop()
        if isinstance(node.parent, (nodes.document, nodes.section)):
            self.body.append("\n")

    # Refs: https://typst.app/docs/reference/model/enum/
    def visit_enumerated_list(self, node: nodes.enumerated_list):
        self._hi.push("+ ")

    def depart_enumerated_list(self, node: nodes.enumerated_list):
        self._hi.pop()
        if isinstance(node.parent, (nodes.document, nodes.section)):
            self.body.append("\n")

    def visit_figure(self, node: nodes.figure):
        if self._hi.is_indent_only:
            self.body.append(self._hi.prefix)
        self.body.append("#figure(\n")
        self._hi.push("  ")
        # Remove reference node between <figure> and <image>
        if isinstance(node.children[0], nodes.reference):
            ref = node.children[0]
            node.remove(ref)
            for child in reversed(ref.children):
                node.insert(0, child)

    def depart_figure(self, node: nodes.figure):
        self._hi.pop()
        self.body.append(f"{self._hi.indent})\n")

    # Body Subelements
    # ----------------

    def visit_caption(self, node: nodes.caption):
        self.body.append(f"{self._hi.indent}caption: [")

    def depart_caption(self, node: nodes.caption):
        self.body.append("],\n")

    def visit_list_item(self, node: nodes.list_item):
        self.body.append(self._hi.prefix)

    def depart_list_item(self, node: nodes.list_item):
        pass

    # Inline Elements
    # ---------------

    # Refs: https://typst.app/docs/reference/model/emph/
    def visit_emphasis(self, node: nodes.emphasis):
        self.body.append("_")

    def depart_emphasis(self, node: nodes.emphasis):
        self.body.append("_")

    # Refs: https://typst.app/docs/reference/model/raw/
    def visit_literal(self, node: nodes.literal):
        # TODO: Correct way to detect language
        if "code" in node["classes"]:
            code = node["classes"][-1]
            self.body.append(f"```{code} ")
            return
        self.body.append("`")

    def depart_literal(self, node: nodes.literal):
        # TODO: Reserve appending text after visit
        if "code" in node["classes"]:
            self.body.append("```")
            return
        self.body.append("`")

    # Refs: https://typst.app/docs/reference/model/strong/
    def visit_strong(self, node: nodes.strong):
        self.body.append("*")

    def depart_strong(self, node: nodes.strong):
        self.body.append("*")
