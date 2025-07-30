# Configuration file for the Sphinx documentation builder.

import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath("../../"))

# Project information
project = "prs-commons"
copyright = "2025, Your Name"  # Update the year as needed
author = "isha-prs"

# The full version, including alpha/beta/rc tags
release = "0.1.0"

# Extensions
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "myst_parser",
]

# Templates
html_theme = "sphinx_rtd_theme"

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# HTML theme options
html_theme_options = {
    "navigation_depth": 3,
    "collapse_navigation": False,
}

# Enable Markdown support
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
