"""CLI Entrypoint (rst2typstpdf)."""

from docutils.core import publish_cmdline

from ..package import install_package
from ..pdf import Writer


def main():
    install_package()
    publish_cmdline(writer=Writer())
