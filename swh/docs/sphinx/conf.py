#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import logging
import os
from typing import Dict

from sphinx.ext import autodoc

from swh.docs.django_settings import force_django_settings

# General information about the project.
project = "Software Heritage - Development Documentation"
copyright = "2015-2021  The Software Heritage developers"
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
    "sphinx_reredirects",
    "swh.docs.sphinx.view_in_phabricator",
    # swh.scheduler inherits some attribute descriptions from celery that use
    # custom crossrefs (eg. :setting:`task_ignore_result`)
    "sphinx_celery.setting_crossref",
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
exclude_patterns = ["_build", "swh-icinga-plugins/index.rst"]

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

# Redirects for pages that were moved, so we don't break external links.
# Uses sphinx-reredirects
redirects = {
    "swh-deposit/spec-api": "api/api-documentation.html",
    "swh-deposit/metadata": "api/metadata.html",
    "swh-deposit/specs/blueprint": "../api/use-cases.html",
    "swh-deposit/user-manual": "api/user-manual.html",
    "architecture": "architecture/overview.html",
    "mirror": "architecture/mirror.html",
}


# -- autodoc configuration ----------------------------------------------
autodoc_default_flags = [
    "members",
    "undoc-members",
    "private-members",
    "special-members",
]
autodoc_member_order = "bysource"
autodoc_mock_imports = ["rados"]
autoclass_content = "both"

modindex_common_prefix = ["swh."]

# For the todo extension. Todo and todolist produce output only if this is True
todo_include_todos = True

_swh_web_base_url = "https://archive.softwareheritage.org"

# for the extlinks extension, sub-projects should fill that dict
extlinks: Dict = {
    "swh_web": (f"{_swh_web_base_url}/%s", None),
    "swh_web_api": (f"{_swh_web_base_url}/api/1/%s", None),
    "swh_web_browse": (f"{_swh_web_base_url}/browse/%s", None),
}

# SWH_PACKAGE_DOC_TOX_BUILD environment variable is set in a tox environment
# named sphinx for each swh package (except the swh-docs package itself).
swh_package_doc_tox_build = os.environ.get("SWH_PACKAGE_DOC_TOX_BUILD", False)

# override some configuration when building a swh package
# documentation with tox to remove warnings and suppress
# those related to unresolved references
if swh_package_doc_tox_build:
    swh_substitutions = os.path.join(
        os.path.dirname(__file__), "../../../docs/swh_substitutions"
    )
    rst_prolog = f".. include:: /{swh_substitutions}"
    suppress_warnings = ["ref.ref"]
    html_favicon = ""
    html_logo = ""


class SimpleDocumenter(autodoc.FunctionDocumenter):
    """
    Custom autodoc directive to inline the docstring of a function
    in a document without the signature header and with no indentation.

    Example of use::

        .. autosimple:: swh.web.api.views.directory.api_directory
    """

    objtype = "simple"
    # ensure the priority is lesser than the base FunctionDocumenter
    # to avoid side effects with autodoc processing
    priority = -1

    # do not indent the content
    content_indent = ""

    # do not add a header to the docstring
    def add_directive_header(self, sig):
        pass


# XXX Kill this ASA this PR is accepted and released
# https://github.com/sphinx-contrib/httpdomain/pull/19
def register_routingtable_as_label(app, document):
    from sphinx.locale import _  # noqa

    labels = app.env.domaindata["std"]["labels"]
    labels["routingtable"] = "http-routingtable", "", _("HTTP Routing Table")
    anonlabels = app.env.domaindata["std"]["anonlabels"]
    anonlabels["routingtable"] = "http-routingtable", ""


# sphinx event handler to set adequate django settings prior reading
# apidoc generated rst files when building doc to avoid autodoc errors
def set_django_settings(app, env, docname):
    if any([pattern in app.srcdir for pattern in ("swh-web-client", "DWCLI")]):
        # swh-web-client is detected as swh-web by the code below but
        # django is not installed when building standalone swh-web-client doc
        return
    package_settings = {
        "auth": "swh.auth.tests.django.app.apptest.settings",
        "deposit": "swh.deposit.settings.development",
        "web": "swh.web.settings.development",
    }
    for package, settings in package_settings.items():
        if any(
            [pattern in docname for pattern in (f"swh.{package}", f"swh-{package}")]
        ):
            force_django_settings(settings)


# when building local package documentation with tox, insert glossary
# content at the end of the index file in order to resolve references
# to the terms it contains
def add_glossary_to_index(app, docname, source):
    if docname == "index":
        glossary_path = os.path.join(
            os.path.dirname(__file__), "../../../docs/glossary.rst"
        )
        with open(glossary_path, "r") as glossary:
            source[0] += "\n" + glossary.read()


def setup(app):
    # env-purge-doc event is fired before source-read
    app.connect("env-purge-doc", set_django_settings)
    # add autosimple directive (used in swh-web)
    app.add_autodocumenter(SimpleDocumenter)
    # set an environment variable indicating we are currently building
    # the documentation
    os.environ["SWH_DOC_BUILD"] = "1"

    # register routingtable label for sphinxcontrib-httpdomain <= 1.7.0
    from distutils.version import StrictVersion  # noqa

    import pkg_resources  # noqa

    httpdomain = pkg_resources.get_distribution("sphinxcontrib-httpdomain")
    if StrictVersion(httpdomain.version) <= StrictVersion("1.7.0"):
        app.connect("doctree-read", register_routingtable_as_label)

    if swh_package_doc_tox_build:
        # ensure glossary will be available in package doc scope
        app.connect("source-read", add_glossary_to_index)

        # suppress httpdomain warnings in non web packages
        if "swh-web" not in app.srcdir:

            # filter out httpdomain unresolved reference warnings
            # to not consider them as errors when using -W option of sphinx-build
            class HttpDomainWarningFilter(logging.Filter):
                def filter(self, record: logging.LogRecord) -> bool:
                    return not record.msg.startswith("Cannot resolve reference to")

            logger = logging.getLogger("sphinx")
            # insert a custom filter in the warning log handler of sphinx
            logger.handlers[1].filters.insert(0, HttpDomainWarningFilter())
