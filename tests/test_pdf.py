import os
from unittest.mock import patch, MagicMock

import pytest
from docutils.core import publish_string

from rst2typst import pdf


@pytest.fixture(autouse=True)
def _clear_font_paths_env(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("TYPST_FONT_PATHS", raising=False)


def _publish(**settings_overrides) -> MagicMock:
    with patch.object(pdf.typst, "compile") as mock:
        publish_string(
            "",
            writer=pdf.Writer(),
            settings_overrides=settings_overrides,
        )
    return mock


def test_font_paths_is_not_set():
    mock = _publish()
    assert mock.call_args.kwargs["font_paths"] == []


def test_font_paths_from_args():
    mock = _publish(font_paths=["/tmp/fonts"])
    assert mock.call_args.kwargs["font_paths"] == ["/tmp/fonts"]


def test_font_paths_from_env(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv(
        "TYPST_FONT_PATHS", os.pathsep.join(["/opt/fonts", "/tmp/fonts"])
    )
    mock = _publish()
    assert mock.call_args.kwargs["font_paths"] == [
        "/opt/fonts",
        "/tmp/fonts",
    ]


def test_font_paths_from_args_and_env(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("TYPST_FONT_PATHS", "/opt/fonts")
    mock = _publish(font_paths=["/tmp/fonts"])
    assert mock.call_args.kwargs["font_paths"] == [
        "/tmp/fonts",
        "/opt/fonts",
    ]
