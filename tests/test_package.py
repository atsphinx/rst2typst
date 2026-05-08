import pytest

from rst2typst import package as t


def test_build_install_path():
    fullpath = t.build_install_path("rst2typst", "0.0.0")
    assert str(fullpath.as_posix()).endswith("typst/packages/local/rst2typst/0.0.0")


class Test_PackageRegistry:
    @pytest.mark.parametrize(
        "arg,name,alias",
        [
            (None, "*", None),
            ("x", "x", None),
            (("x", "y"), "x", "y"),
        ],
    )
    def test_add(self, arg, name, alias):
        reg = t.PackageRegistry()
        reg.add("test", arg)
        assert len(reg) == 1
        assert len(reg["test"]) == 1
        assert isinstance(list(reg["test"])[0], t.Entrypoint)
        entrypoint = list(reg["test"])[0]
        assert entrypoint.name == name
        assert entrypoint.alias == alias
