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
    print(source)
    proc_rst2typst = subprocess.run(
        ["rst2typst", str(source)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert proc_rst2typst.returncode == 0
    assert not proc_rst2typst.stderr
    proc_typst = subprocess.run(
        ["typst", "c", "-", "-"],
        input=proc_rst2typst.stdout,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert proc_typst.returncode == 0
    assert not proc_typst.stderr
