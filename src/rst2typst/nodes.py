from __future__ import annotations

from docutils import nodes


class content(nodes.Element):
    """Marker for contents of content."""

    pass


class outline(nodes.Element):
    """A table of contents."""

    pass
