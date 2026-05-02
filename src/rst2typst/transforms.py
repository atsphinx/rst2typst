from __future__ import annotations

from docutils import nodes
from docutils.transforms import Transform


class RemapFootnotes(Transform):
    default_priority = 700

    def apply(self, **kwargs):
        footnotes = {}
        for f in list(self.document.findall(nodes.footnote)):
            f.parent.remove(f)
            for id in f.attributes.get("ids", []):
                label_idx = f.first_child_matching_class(nodes.label)
                if label_idx is not None:
                    label = f.children[label_idx]
                    f["label"] = (
                        f"{'footnote-' if not id.startswith('footnote-') else ''}{id}"
                    )
                    label.parent.remove(label)
                footnotes[id] = f
        for ref in self.document.findall(nodes.footnote_reference):
            refid = ref["refid"]
            label_id = (
                f"{'footnote-' if not refid.startswith('footnote-') else ''}{refid}"
            )
            if refid in footnotes:
                footnote = footnotes.pop(refid)
                idx = ref.parent.index(ref)
                ref.parent.insert(idx, footnote)
            ref.remove(ref.children[0])
            ref.append(nodes.Text(label_id))


class AssignLiteralLanguage(Transform):
    """Transformer to inject 'language' attribute into all <literal> and <literal_block> nodes."""

    default_priority = 400

    def _assign_language(self, node: nodes.Element):
        if "language" in node:
            return
        if "classes" not in node:
            return
        if "code" not in node["classes"]:
            return
        if len(node["classes"]) < 2:
            return
        node["language"] = node["classes"][-1]

    def apply(self, **kwargs):
        for node in self.document.findall(nodes.literal):
            self._assign_language(node)
        for node in self.document.findall(nodes.literal_block):
            self._assign_language(node)
