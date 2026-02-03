"""Test suite for end-to-end."""

import subprocess
from pathlib import Path

import pytest

# --
# Tests for convert by CLI arguments.
# --

_cli_cases_dir = Path(__file__).parent / "cases-cli"


@pytest.mark.parametrize("source", _cli_cases_dir.glob("*.rst"))
def test_cli(source: Path):
    """Test convert by CLI arguments.

    This case has three processes.

    1. Convert rst to typ by rst2typst.
    2. Compare converted Typst source and expected Typst source.
    3. Try compile converted Typst source to pdf by typst.
    """
    expected = source.with_suffix(".typ").read_text().strip()
    proc_rst2typst = subprocess.run(
        ["rst2typst", str(source)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert proc_rst2typst.returncode == 0
    assert not proc_rst2typst.stderr
    assert proc_rst2typst.stdout == expected
    proc_typst = subprocess.run(
        ["typst", "c", "-", "-"],
        input=proc_rst2typst.stdout.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert proc_typst.returncode == 0
    assert not proc_typst.stderr
