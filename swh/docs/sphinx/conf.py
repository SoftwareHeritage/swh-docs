#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import os
from typing import Dict

import django

# General information about the project.
project = "Software Heritage - Development Documentation"
copyright = "2015-2019  The Software Heritage developers"
author = "The Software Heritage developers"

# -- General configuration ------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinxcontrib.httpdomain",
    "sphinx.ext.extlinks",
    "sphinxcontrib.images",
    "sphinxcontrib.programoutput",
    "sphinx.ext.viewcode",
    "sphinx_tabs.tabs",
    "sphinx_rtd_theme",
    "sphinx.ext.graphviz",
    "sphinx_click.ext",
    "myst_parser",
    "sphinx.ext.todo",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# A string of reStructuredText that will be included at the beginning of every
# source file that is read.
# A bit hackish but should work both for each swh package and the whole swh-doc
rst_prolog = """
.. include:: /../../swh-docs/docs/swh_substitutions
"""

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = ""
# The full version, including alpha/beta/rc tags.
release = ""

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ["_build", "swh-icinga-plugins/index.rst", "swh-search/index.rst"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

html_favicon = "_static/favicon.ico"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    "collapse_navigation": True,
    "sticky_navigation": True,
}

html_logo = "_static/software-heritage-logo-title-motto-vertical-white.png"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# make logo actually appear, avoiding gotcha due to alabaster default conf.
# https://github.com/bitprophet/alabaster/issues/97#issuecomment-303722935
html_sidebars = {
    "**": [
        "about.html",
        "globaltoc.html",
        "relations.html",
        "sourcelink.html",
        "searchbox.html",
    ]
}

# If not None, a 'Last updated on:' timestamp is inserted at every page
# bottom, using the given strftime format.
# The empty string is equivalent to '%b %d, %Y'.
html_last_updated_fmt = "%Y-%m-%d %H:%M:%S %Z"

# refer to the Python standard library.
intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}


# -- autodoc configuration ----------------------------------------------
autodoc_default_flags = [
    "members",
    "undoc-members",
    "private-members",
    "special-members",
]
autodoc_member_order = "bysource"
autodoc_mock_imports = ["rados"]

modindex_common_prefix = ["swh."]

# For the todo extension. Todo and todolist produce output only if this is True
todo_include_todos = True

# for the extlinks extension, sub-projects should fill that dict
extlinks: Dict = {}


# XXX Kill this ASA this PR is accepted and released
# https://github.com/sphinx-contrib/httpdomain/pull/19
def register_routingtable_as_label(app, document):
    from sphinx.locale import _  # noqa

    labels = app.env.domaindata["std"]["labels"]
    labels["routingtable"] = "http-routingtable", "", _("HTTP Routing Table")
    anonlabels = app.env.domaindata["std"]["anonlabels"]
    anonlabels["routingtable"] = "http-routingtable", ""


# hack to set the adequate django settings when building global swh doc
# to avoid autodoc build errors
def setup(app):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "swh.docs.django_settings")
    django.setup()
    from distutils.version import StrictVersion  # noqa

    import pkg_resources  # noqa

    httpdomain = pkg_resources.get_distribution("sphinxcontrib-httpdomain")
    if StrictVersion(httpdomain.version) <= StrictVersion("1.7.0"):
        app.connect("doctree-read", register_routingtable_as_label)
