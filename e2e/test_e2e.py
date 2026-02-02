"""Test suite for end-to-end."""

from pathlib import Path

import pytest
from docutils.core import publish_string

import rst2typst

# --
# Tests for convert by CLI arguments.
# --

_cli_cases_dir = Path(__file__).parent / "cases-cli"


@pytest.mark.parametrize("source", _cli_cases_dir.glob("*.rst"))
def test_cli(source: Path):
    ret = publish_string(
        source.read_text(),
        writer=rst2typst.Writer(),
    )
    assert ret == b""
