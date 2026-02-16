"""Test cases using spec documents.

``spec`` pages in documentation includes example how does it convert from reStructuredText to Typst.
This file run tests using documents as "Spec of visitor/departer".
"""

from pathlib import Path

import pytest
from docutils import nodes
from docutils.core import publish_doctree, publish_parts

from rst2typst import writer

SPEC_DIR = (Path(__file__).parent.parent / "docs" / "spec").resolve()


def fetch_all_cases():
    """Fetch all test cases from spec documents."""
    ids = []
    cases = []
    for file in SPEC_DIR.glob("*.rst"):
        doctree = publish_doctree(file.read_text())
        for t1_ in doctree.findall(nodes.title):
            if t1_.astext() != "Examples":
                continue
            for section in t1_.parent.findall(nodes.section, include_self=False):
                title = list(section.findall(nodes.title))[0].astext()
                case_id = f"{file.stem}__{title.lower().replace(' ', '_')}"
                ids.append(case_id)
                cases.append(
                    [
                        literal.astext()
                        for literal in section.findall(nodes.literal_block)
                    ]
                )
    return ids, cases


ids, all_cases = fetch_all_cases()


@pytest.mark.parametrize("source,expected", all_cases, ids=ids)
def test_translate(source, expected):
    parts = publish_parts(source, writer=writer.Writer())
    assert parts["body"].strip() == expected.strip()
