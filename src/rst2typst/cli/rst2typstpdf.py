"""CLI Entrypoint (rst2typstpdf)."""

from docutils.core import publish_cmdline

from ..pdf import Writer


def main():
    publish_cmdline(writer=Writer())
