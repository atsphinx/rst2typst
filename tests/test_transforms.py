import textwrap

from docutils import nodes
from docutils.core import publish_doctree

from rst2typst import transforms as t


class Test_AssignLiteralLanguage:
    def test_capture_literal(self):
        source = """
        .. role:: python(code)
           :language: python

        :python:`hello()`
        """
        doctree = publish_doctree(textwrap.dedent(source).strip())
        transform = t.AssignLiteralLanguage(doctree)
        transform.apply()
        node = list(transform.document.findall(nodes.literal))[0]
        assert "language" in node
        assert node["language"] == "python"

    def test_capture_literal_block(self):
        source = """
        .. code:: python

           def hello():
               return "world"
        """
        doctree = publish_doctree(textwrap.dedent(source).strip())
        transform = t.AssignLiteralLanguage(doctree)
        transform.apply()
        node = list(transform.document.findall(nodes.literal_block))[0]
        assert "language" in node
        assert node["language"] == "python"
