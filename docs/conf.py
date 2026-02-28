import os
from importlib.metadata import version

# -- Project information
project = "rst2typst"
copyright = "2026, Kazuya Takei"
author = "Kazuya Takei"
release = version("rst2typst")

# -- General configuration
extensions = [
    # Built-in extensions
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    # atsphinx extensions
    "atsphinx.footnotes",
    # Third-party extensions
    "sphinx_design",
    "sphinxext.opengraph",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output
html_theme = "shibuya"
html_static_path = ["_static"]
html_theme_options = {
    "github_url": "https://github.com/atsphinx/rst2typst",
    "nav_links": [
        {
            "title": '"atsphinx" project',
            "url": "https://atsphinx.github.io/",
            "external": True,
        },
    ],
    "nav_links_align": "right",
}
_announcement = os.environ.get("SHIBUYA_ANNOUNCEMENT", None)
if _announcement:
    html_theme_options["announcement"] = _announcement

# -- Options for extensions
# sphinx.ext.intersphinx
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "sphinx": ("https://sphinx-doc.org/en/master", None),
}
# sphinxext.opengraph
ogp_site_url = "https://rst2typst.attakei.dev/"
