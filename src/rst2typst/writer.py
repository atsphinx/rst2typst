"""Writer and related classes for docutils."""

from __future__ import annotations

import functools
from pathlib import Path
from typing import TYPE_CHECKING

from docutils import nodes
from docutils.writers import Writer as BaseWriter

from .frontend import validate_comma_separated_int

if TYPE_CHECKING:
    from typing import Any, Callable, Literal


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

    visitor_attributes = {"body", "includes"}

    def __init__(self):
        super().__init__()
        self.translator_class = TypstTranslator

    def translate(self):
        visitor: TypstTranslator = self.translator_class(self.document)
        self.document.walkabout(visitor)  # type: ignore[possibly-missing-attribute]
        self.parts["body"] = "".join(visitor.body)
        self.parts["includes"] = {i: i.read_text() for i in visitor.includes}
        self.output = "\n".join(self.parts["includes"].values())
        self.output += "\n"
        self.output += self.parts["body"]


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
        self.includes: set[Path] = set()
        self.body = []
        self.section_level = 0
        self._hi = HanglingIndent()

    def block_on_structural(func: Callable):
        @functools.wraps(func)
        def _block_on_structural(self, node: nodes.Element):
            if isinstance(node.parent, nodes.Structural):
                self.body.append("\n")

            func(self, node)

        return _block_on_structural

    # ========================================
    # The visitors and deparers for plain text
    # ========================================

    def visit_Text(self, node: nodes.Text):
        self.body.append(f"\n{self._hi.indent}".join(node.astext().split("\n")))

    def depart_Text(self, node: nodes.Text):
        pass

    # ===========================================================
    # The visitors and deparers for basic reStructuredText syntax
    # ===========================================================
    #
    # They are sorted by these rules:
    #
    #   * The order from "Syntax details" of `reStructuredText Markup Specification`_.
    #   * When the node has children node types, write it nearby the parent node type.
    #   * ``visit_`` is first, and ``depart_`` is second if it is exists.
    #
    # .. _reStructuredText Markup Specification: https://docutils.org/docs/ref/rst/restructuredtext.html

    # Document Structure
    # ==================
    def visit_document(self, node: nodes.document):
        pass

    def depart_document(self, node: nodes.document):
        pass

    def visit_section(self, node: nodes.section):
        self.section_level += 1
        if (
            self.document.settings.page_break_level
            and self.section_level in self.document.settings.page_break_level
        ):
            self.body.append("#pagebreak()\n\n")

    def depart_section(self, node: nodes.section):
        self.section_level -= 1

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

    # Body Elements
    # =============
    @block_on_structural
    def visit_paragraph(self, node: nodes.paragraph):
        pass

    @block_on_structural
    def depart_paragraph(self, node: nodes.paragraph):
        pass

    # Bullet Lists and Enumerated Lists
    # ---------------------------------
    # Refs: https://typst.app/docs/reference/model/list/
    @block_on_structural
    def visit_bullet_list(self, node: nodes.bullet_list):
        self._hi.push("- ")
        if isinstance(node.parent, nodes.list_item):
            self.body.append("\n")

    def depart_bullet_list(self, node: nodes.bullet_list):
        self._hi.pop()

    @block_on_structural
    def visit_enumerated_list(self, node: nodes.enumerated_list):
        self._hi.push("+ ")
        if isinstance(node.parent, nodes.list_item):
            self.body.append("\n")

    def depart_enumerated_list(self, node: nodes.enumerated_list):
        self._hi.pop()

    def visit_list_item(self, node: nodes.list_item):
        self.body.append(self._hi.prefix)

    def depart_list_item(self, node: nodes.list_item):
        if (
            node.first_child_matching_class((nodes.bullet_list, nodes.enumerated_list))
            is None
        ):
            self.body.append("\n")

    # Definition Lists
    # ----------------
    @block_on_structural
    def visit_definition_list(self, node: nodes.definition_list):
        self._hi.push("/ ")

    def depart_definition_list(self, node: nodes.definition_list):
        self._hi.pop()

    def visit_definition_list_item(self, node: nodes.definition_list_item):
        self.body.append(self._hi.prefix)

    def depart_definition_list_item(self, node: nodes.definition_list_item):
        self.body.append("\n")

    def visit_term(self, node: nodes.term):
        pass

    def depart_term(self, node: nodes.term):
        pass

    def visit_classifier(self, node: nodes.classifier):
        self.body.append(" \\<")

    def depart_classifier(self, node: nodes.classifier):
        self.body.append("\\>")

    def visit_definition(self, node: nodes.definition):
        self.body.append(": \\\n")
        self.body.append(self._hi.indent)
        pass

    def depart_definition(self, node: nodes.definition):
        pass

    # Field Lists
    # -----------
    # Refs: https://typst.app/docs/reference/model/terms/
    @block_on_structural
    def visit_field_list(self, node: nodes.field_list):
        self.body.append("#table(\n")
        self._hi.push("  ")
        self.body.append(f"{self._hi.indent}columns: (1fr, auto),\n")

    def depart_field_list(self, node: nodes.field_list):
        self._hi.pop()
        self.body.append(")")

    def visit_field(self, node: nodes.field):
        pass

    def depart_field(self, node: nodes.field):
        pass

    def visit_field_name(self, node: nodes.field_name):
        if isinstance(node.parent.parent, nodes.docinfo):
            self.body.append("/ ")
            return
        self.body.append(self._hi.indent)
        self.body.append("[")

    def depart_field_name(self, node: nodes.field_name):
        if isinstance(node.parent.parent, nodes.docinfo):
            self.body.append(": ")
            return
        self.body.append("],\n")

    def visit_field_body(self, node: nodes.field_body):
        if isinstance(node.parent.parent, nodes.docinfo):
            return
        self.body.append(self._hi.indent)
        self.body.append("[")

    def depart_field_body(self, node: nodes.field_body):
        if isinstance(node.parent.parent, nodes.docinfo):
            return
        self.body.append("],\n")

    # Bibliographic Fields
    # --------------------
    def visit_docinfo(self, node: nodes.docinfo):
        self._hi.push("/ ")

    def depart_docinfo(self, node: nodes.docinfo):
        self._hi.pop()

    def _visit_bibliographic(self, node: nodes.Bibliographic):
        title = node.__class__.__name__.title()
        self.body.append(f"{self._hi.prefix}{title}: ")

    def _depart_bibliographic(self, node: nodes.Bibliographic):
        self.body.append("\n")

    # Refs: https://typst.app/docs/reference/model/terms/
    visit_address = _visit_bibliographic
    depart_address = _depart_bibliographic
    visit_author = _visit_bibliographic
    depart_author = _depart_bibliographic
    visit_contact = _visit_bibliographic
    depart_contact = _depart_bibliographic
    visit_copyright = _visit_bibliographic
    depart_copyright = _depart_bibliographic
    visit_date = _visit_bibliographic
    depart_date = _depart_bibliographic
    visit_organization = _visit_bibliographic
    depart_organization = _depart_bibliographic
    visit_revision = _visit_bibliographic
    depart_revision = _depart_bibliographic
    visit_status = _visit_bibliographic
    depart_status = _depart_bibliographic
    visit_version = _visit_bibliographic
    depart_version = _depart_bibliographic

    # Option Lists
    # ------------
    @block_on_structural
    def visit_option_list(self, node: nodes.option_list):
        self._hi.push("/ ")

    def depart_option_list(self, node: nodes.option_list):
        self._hi.pop()

    def visit_option_list_item(self, node: nodes.option_list_item):
        self.body.append(self._hi.prefix)

    def depart_option_list_item(self, node: nodes.option_list_item):
        self.body.append("\n")

    def visit_option_group(self, node: nodes.option_group):
        text = ", ".join([option.astext() for option in node.findall(nodes.option)])
        self.body.append(f"{text}: \\\n")
        raise nodes.SkipNode

    def visit_description(self, node: nodes.description):
        self.body.append(self._hi.indent)

    def depart_description(self, node: nodes.description):
        pass

    # Literal Blocks
    # --------------
    # Refs: https://typst.app/docs/reference/text/raw/
    def visit_literal_block(self, node: nodes.literal_block):
        if "code" in node["classes"]:
            code = node["classes"][-1]
            self.body.append(f"```{code}\n")
            return
        self.body.append("```\n")

    def depart_literal_block(self, node: nodes.literal_block):
        self.body.append("\n```\n\n")

    # Line Blocks
    # -----------
    # TODO: Implement after

    # Block Quotes
    # ------------
    # Refs: https://typst.app/docs/reference/model/quote/
    @block_on_structural
    def visit_block_quote(self, node: nodes.block_quote):
        self._hi.push("  ")
        args = []
        attrs = list(node.findall(nodes.attribution))
        if attrs:
            args.append(f"attribution: [{attrs[0].astext()}]")
            for a in attrs:
                node.remove(a)
        self.body.append(f"#quote({' '.join(args)})[\n")
        self.body.append(self._hi.prefix)

    def depart_block_quote(self, node: nodes.block_quote):
        self._hi.pop()
        self.body.append("\n]\n")

    # Doctest Blocks
    # --------------
    # TODO: Implement after

    # Tables
    # ------
    @block_on_structural
    def visit_table(self, node: nodes.table):
        figure_opts = {}
        if isinstance(node.children[0], nodes.title):
            figure_opts["caption"] = node.children[0].astext()
            node.remove(node.children[0])
        if figure_opts:
            node["figure_opts"] = figure_opts
            self.body.append("#figure([\n")
            self._hi.push("  ")
        self.body.append(f"{self._hi.indent}#table(\n")
        self._hi.push("  ")

    def depart_table(self, node: nodes.table):
        self._hi.pop()
        self.body.append(f"{self._hi.indent})")
        if "figure_opts" in node:
            opts = node["figure_opts"]
            self.body.append("],")
            if "caption" in opts:
                self.body.append(f"\n{self._hi.indent}caption: [{opts['caption']}],\n")
            self._hi.pop()
            self.body.append(")")
        self.body.append("\n")

    def visit_tgroup(self, node: nodes.tgroup):
        cols = [
            f"{colspec['colwidth']}fr" if colspec != "auto" else "auto"
            for colspec in node.findall(nodes.colspec)
        ]
        self.body.append(f"{self._hi.indent}columns: ({', '.join(cols)}),\n")

    def depart_tgroup(self, node: nodes.tgroup):
        pass

    def visit_colspec(self, node: nodes.colspec):
        raise nodes.SkipNode

    def visit_thead(self, node: nodes.tbody):
        self.body.append(f"{self._hi.indent}table.header(\n")
        self._hi.push("  ")

    def depart_thead(self, node: nodes.tbody):
        self._hi.pop()
        self.body.append(f"{self._hi.indent}),\n")

    def visit_tbody(self, node: nodes.tbody):
        pass

    def depart_tbody(self, node: nodes.tbody):
        pass

    def depart_row(self, node: nodes.tbody):
        pass

    def departt_row(self, node: nodes.row):
        pass

    def visit_entry(self, node: nodes.entry):
        morerows = node.get("morerows", 0)
        morecols = node.get("morecols", 0)
        prefix = ""
        if morerows or morecols:
            prefix = "table.cell("
            if morerows:
                prefix += f"rowspan: {morerows + 1},"
            if morecols:
                prefix += f"colspan: {morecols + 1},"
            prefix += ")"

        self.body.append(f"{self._hi.indent}{prefix}[")

    def depart_entry(self, node: nodes.entry):
        self.body.append("],\n")

    # Explicit Markup Blocks
    # ----------------------
    def visit_comment(self, node: nodes.comment):
        raise nodes.SkipNode

    #
    # Inline Markup
    # =============
    def _enclose_content(wrapper: str):
        def _enclose(self, node: nodes.Inline):
            self.body.append(wrapper)

        return _enclose, _enclose

    # Refs: https://typst.app/docs/reference/model/emph/
    visit_emphasis, depart_emphasis = _enclose_content("_")
    # Refs: https://typst.app/docs/reference/model/strong/
    visit_strong, depart_strong = _enclose_content("*")

    def _enclose_literal(walk: Literal["visit", "depart"]):
        def _enclose(self, node: nodes.literal):
            closure = "`"
            # TODO: Correct way to detect language
            if "code" not in node["classes"]:
                pass
            elif walk == "depart":
                closure = "```"
            else:
                closure = f"```{node['classes'][-1]} "
            self.body.append(closure)

        return _enclose

    # Refs: https://typst.app/docs/reference/model/raw/
    visit_literal = _enclose_literal("visit")
    depart_literal = _enclose_literal("depart")

    def visit_reference(self, node: nodes.reference):
        # TODO: Add case for internal links if exists.
        href = node["refuri"]
        self.body.append(f'#link("{href}")[')

    def depart_reference(self, node: nodes.reference):
        self.body.append("]")

    # =========================================================
    # The visitors and deparers for reStructuredText Directives
    # =========================================================
    #
    # They are sorted by these rules:
    #
    #   * The order from contents of `reStructuredText Directives`_.
    #   * When the node has children node types, write it nearby the parent node type.
    #   * ``visit_`` is first, and ``depart_`` is second if it is exists.
    #
    # .. _reStructuredText Directives: https://docutils.org/docs/ref/rst/directives.html

    # Admonitions
    # ===========
    def _enclose_admonition(node_name: str, title: str | None = None):
        def _visit(self, node: nodes.Element):
            module_path = Path(__file__).parent / "admonition.typ"
            self.includes.add(module_path)

            nonlocal title
            if isinstance(node.parent, nodes.Structural):
                self.body.append("\n")

            title_idx = node.first_child_matching_class(nodes.title)
            if title_idx is not None:
                title = node.children[title_idx].astext()
                node.remove(node.children[title_idx])

            self.body.append(f"{self._hi.indent}#admonition-callout(\n")
            self._hi.push("  ")
            self.body.append(f'{self._hi.indent}"{node_name}", "{title}",\n')
            self.body.append(f"{self._hi.indent}[")

        def _depart(self, node: nodes.Element):
            self.body.append("],\n")
            self._hi.pop()
            self.body.append(f"{self._hi.indent})\n")

        return _visit, _depart

    visit_attention, depart_attention = _enclose_admonition("attention", "Attention")
    visit_caution, depart_caution = _enclose_admonition("caution", "Caution")
    visit_danger, depart_danger = _enclose_admonition("danger", "Danger")
    visit_error, depart_error = _enclose_admonition("error", "Error")
    visit_hint, depart_hint = _enclose_admonition("hint", "Hint")
    visit_important, depart_important = _enclose_admonition("important", "Important")
    visit_note, depart_note = _enclose_admonition("note", "Note")
    visit_tip, depart_tip = _enclose_admonition("tip", "Tip")
    visit_warning, depart_warning = _enclose_admonition("warning", "Warning")
    visit_admonition, depart_admonition = _enclose_admonition("admonition")

    # Images
    # ======
    def visit_image(self, node: nodes.image):
        # FIXME: Implement is too complex.
        prefix = self._hi.indent
        suffix = "\n\n"
        if isinstance(node.parent, nodes.figure):
            prefix = f"{prefix}"
            suffix = "]"
        elif isinstance(node.parent, nodes.reference):
            prefix = f"\n{prefix}"
            suffix = "]"
        self.body.append(f"{prefix}#image(\n")
        self._hi.push("  ")
        self.body.append(f'{self._hi.indent}"{node["uri"]}",\n')
        if "alt" in node:
            self.body.append(f'{self._hi.indent}alt: "{node["alt"]}",\n')
        if "width" in node:
            self.body.append(f"{self._hi.indent}width: {node['width']},\n")
        self._hi.pop()
        self.body.append(f"{self._hi.indent}){suffix}")
        if isinstance(node.parent, nodes.reference):
            self._hi.pop()

    def visit_figure(self, node: nodes.figure):
        # FIXME: Implement is complex.
        if self._hi.is_indent_only:
            self.body.append(self._hi.prefix)
        self.body.append("#figure([\n")
        self._hi.push("  ")
        if node.first_child_matching_class(nodes.reference) is not None:
            self.body.append(f"{self._hi.indent}")
            self._hi.push("  ")

    def depart_figure(self, node: nodes.figure):
        self._hi.pop()
        self.body.append(f"{self._hi.indent})\n\n")

    def visit_caption(self, node: nodes.caption):
        self.body.append(",\n")
        self.body.append(f"{self._hi.indent}caption: [")

    def depart_caption(self, node: nodes.caption):
        self.body.append("],\n")

    # Miscellaneous
    # =============
    def visit_raw(self, node: nodes.raw):
        if "format" in node and node["format"] == "typst":
            # NOTE: ``self.body.append(node.astext())`` does not work as expected.
            for line in node.astext().split("\n"):
                self.body.append(f"{line}\n")
            self.body.append("\n")
        raise nodes.SkipNode
