"""Test cases using spec documents.

``spec`` pages in documentation includes example how does it convert from reStructuredText to Typst.
This file run tests using documents as "Spec of visitor/departer".
"""

from pathlib import Path

import pytest
from docutils.core import publish_parts

from rst2typst import writer

SPEC_DIR = (Path(__file__).parent.parent / "docs" / "spec").resolve()


def fetch_all_cases():
    """Fetch all test cases from spec documents."""
    ids = []
    cases = []
    for rst in SPEC_DIR.glob("**/*.rst.txt"):
        group = rst.relative_to(SPEC_DIR).parent
        name = rst.name[:-8]
        typ = rst.parent / f"{name}.typ.txt"
        cases.append((rst.read_text(), typ.read_text()))
        ids.append(f"{group.name}__{name}")
    return ids, cases


ids, all_cases = fetch_all_cases()


@pytest.mark.parametrize("source,expected", all_cases, ids=ids)
def test_translate(source, expected):
    parts = publish_parts(source, writer=writer.Writer())
    assert parts["body"].strip() == expected.strip()
