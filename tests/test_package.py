from importlib import metadata

from rst2typst import package as t

version = metadata.version("rst2typst")


def test_build_install_path():
    fullpath = t.build_install_path()
    assert str(fullpath).endswith(f"typst/packages/local/rst2typst/{version}")
