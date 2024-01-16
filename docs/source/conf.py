# -- Path setup --------------------------------------------------------------
# https://github.com/evansd/whitenoise/blob/main/docs/conf.py

import datetime
import sys
import tomllib
from pathlib import Path

here = Path(__file__).parent.resolve()
sys.path.insert(0, str(here / ".." / ".." / "src"))


# -- Project information -----------------------------------------------------

project = "django-turbo-helper"
copyright = f"{datetime.datetime.now().year}, Michael Yin"
author = "Michael Yin"

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.


def _get_version() -> str:
    with (here / ".." / ".." / "pyproject.toml").open("rb") as fp:
        data = tomllib.load(fp)
    version: str = data["tool"]["poetry"]["version"]
    return version


version = _get_version()
# The full version, including alpha/beta/rc tags.
release = version


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.

extensions = ["sphinx.ext.autodoc", "autoapi.extension", "myst_parser"]

source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}

# Document Python Code
autoapi_type = "python"
autoapi_dirs = ["../../src"]
autoapi_ignore = ["*/tests/*.py"]
autodoc_typehints = "description"

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []  # type: ignore

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "furo"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".

html_theme_options = {
    "announcement": 'If you are new to Hotwire, you may be interested in this free eBook <a href="https://tutorial.saashammer.com/" rel="nofollow" target="_blank">Hotwire Django Tutorial</a>',
}
