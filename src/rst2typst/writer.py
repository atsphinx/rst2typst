"""Writer and related classes for docutils."""

from __future__ import annotations

import functools
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

    def block_on_structural(func: Callable):
        def count_linefeed(body: list[str]) -> int:
            if not body:
                return 0
            num = 0
            if body[-1].endswith("\n"):
                num += 1
            if len(body) > 1 and body[-2].startswith("\n"):
                num += 1
            return num

        @functools.wraps(func)
        def _block_on_structural(self, node: nodes.Element):
            required = (
                2
                - count_linefeed(self.body)
                - int(not isinstance(node.parent, nodes.Structural))
            )
            if required > 0:
                self.body.append("\n" * required)

            func(self, node)

        return _block_on_structural

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

    def visit_docinfo(self, node: nodes.docinfo):
        self._hi.push("/ ")

    def depart_docinfo(self, node: nodes.docinfo):
        self._hi.pop()

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

    # Body Elements
    # -------------

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

    def visit_comment(self, node: nodes.comment):
        raise nodes.SkipNode

    @block_on_structural
    def visit_definition_list(self, node: nodes.definition_list):
        self._hi.push("/ ")

    def depart_definition_list(self, node: nodes.definition_list):
        self._hi.pop()

    # Refs: https://typst.app/docs/reference/model/terms/
    @block_on_structural
    def visit_field_list(self, node: nodes.field_list):
        self._hi.push("/ ")

    def depart_field_list(self, node: nodes.field_list):
        self._hi.pop()

    # Refs: https://typst.app/docs/reference/text/raw/
    def visit_literal_block(self, node: nodes.literal_block):
        if "code" in node["classes"]:
            code = node["classes"][-1]
            self.body.append(f"```{code}\n")
            return
        self.body.append("```\n")

    def depart_literal_block(self, node: nodes.literal_block):
        self.body.append("\n```\n\n")

    @block_on_structural
    def visit_option_list(self, node: nodes.option_list):
        self._hi.push("/ ")

    def depart_option_list(self, node: nodes.option_list):
        self._hi.pop()

    def visit_paragraph(self, node: nodes.paragraph):
        pass

    @block_on_structural
    def depart_paragraph(self, node: nodes.paragraph):
        pass

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
        self.body.append(self._hi.prefix)

    def depart_block_quote(self, node: nodes.block_quote):
        self._hi.pop()
        self.body.append("]\n")

    # Refs: https://typst.app/docs/reference/model/list/
    @block_on_structural
    def visit_bullet_list(self, node: nodes.bullet_list):
        self._hi.push("- ")

    def depart_bullet_list(self, node: nodes.bullet_list):
        self._hi.pop()

    @block_on_structural
    def visit_enumerated_list(self, node: nodes.enumerated_list):
        self._hi.push("+ ")

    def depart_enumerated_list(self, node: nodes.enumerated_list):
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

    # Body Subelements
    # ----------------

    def visit_caption(self, node: nodes.caption):
        self.body.append(",\n")
        self.body.append(f"{self._hi.indent}caption: [")

    def depart_caption(self, node: nodes.caption):
        self.body.append("],\n")

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

    @block_on_structural
    def visit_definition_list_item(self, node: nodes.definition_list_item):
        self.body.append(self._hi.prefix)

    def depart_definition_list_item(self, node: nodes.definition_list_item):
        pass

    def visit_description(self, node: nodes.description):
        self.body.append(self._hi.indent)
        pass

    def depart_description(self, node: nodes.description):
        pass

    def visit_field_name(self, node: nodes.field_name):
        pass

    def depart_field_name(self, node: nodes.field_name):
        self.body.append(": ")

    def visit_field(self, node: nodes.field):
        self.body.append(self._hi.prefix)

    def depart_field(self, node: nodes.field):
        pass

    def visit_field_body(self, node: nodes.field_body):
        pass

    def depart_field_body(self, node: nodes.field_body):
        pass

    @block_on_structural
    def visit_list_item(self, node: nodes.list_item):
        self.body.append(self._hi.prefix)

    def depart_list_item(self, node: nodes.list_item):
        pass

    def visit_option_group(self, node: nodes.option_group):
        text = ", ".join([option.astext() for option in node.findall(nodes.option)])
        self.body.append(f"{text}: \\\n")
        raise nodes.SkipNode

    @block_on_structural
    def visit_option_list_item(self, node: nodes.option_list_item):
        self.body.append(self._hi.prefix)

    def depart_option_list_item(self, node: nodes.option_list_item):
        pass

    def visit_term(self, node: nodes.term):
        pass

    def depart_term(self, node: nodes.term):
        pass

    # Inline Elements
    # ---------------
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
