# -- Project information
project = "rst2typst"
copyright = "2026, Kazuya Takei"
author = "Kazuya Takei"
release = "0.0.0"

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
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output
html_theme = "shibuya"
html_static_path = ["_static"]
html_theme_options = {
    "announcement": "This is not yet published on PyPI.",
}

# -- Options for extensions
# sphinx.ext.intersphinx
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "sphinx": ("https://sphinx-doc.org/en/master", None),
}
