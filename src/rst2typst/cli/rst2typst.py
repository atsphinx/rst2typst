"""CLI Entrypoint (rst2typst)."""

from docutils.core import publish_cmdline

from .. import Writer


def main():
    publish_cmdline(writer=Writer())
