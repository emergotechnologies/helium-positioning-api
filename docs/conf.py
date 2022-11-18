"""Sphinx configuration."""
project = "Helium Positioning API"
author = "emergo technologies GmbH"
copyright = "2022, emergo technologies GmbH"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
