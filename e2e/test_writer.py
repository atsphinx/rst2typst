"""Test suite for end-to-end."""

from pathlib import Path

import pytest
from docutils.core import publish_parts

from rst2typst import writer

# --
# Tests for convert by CLI arguments.
# --

_cli_cases_dir = Path(__file__).parent / "output"


@pytest.mark.parametrize("source", _cli_cases_dir.glob("*.rst"))
def test_translate_output(source: Path):
    expected = source.with_suffix(".typ").read_text().strip()
    parts = publish_parts(source.read_text(), writer=writer.Writer())
    assert parts["body"].strip() == expected
