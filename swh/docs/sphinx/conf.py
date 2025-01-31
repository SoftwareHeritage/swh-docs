# Copyright (C) 2017-2024  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU Affero General Public License version 3, or any later version
# See top-level LICENSE file for more information

import logging
import os
from pathlib import Path
import re
import sys
from typing import Dict

from sphinx import addnodes
from sphinx.ext import autodoc
from sphinx.transforms import SphinxTransform

from swh.docs.django_settings import force_django_settings

# General information about the project.
project = "Software Heritage"
copyright = "2015-2024 The Software Heritage developers"
author = "The Software Heritage developers"

# -- General configuration ------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinxcontrib.httpdomain",
    "sphinx.ext.extlinks",
    "sphinxcontrib.images",
    "sphinxcontrib.mermaid",
    "sphinxcontrib.programoutput",
    "sphinx.ext.viewcode",
    "sphinx.ext.graphviz",
    "sphinx_click.ext",
    "myst_parser",
    "sphinx.ext.todo",
    "sphinx_reredirects",
    "swh.docs.sphinx.view_in_gitlab",
    # swh.scheduler inherits some attribute descriptions from celery that use
    # custom crossrefs (eg. :setting:`task_ignore_result`)
    "sphinx_celery.setting_crossref",
    "sphinx_carousel.carousel",
    "sphinx_design",
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
.. |swh| replace:: *Software Heritage*
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
exclude_patterns = [
    "_build",
    "**swh-icinga-plugins/*.rst",
    "**/swh/lister/maven/README.md",
    "**/swh/loader/cvs/cvs2gitdump/README.md",
    "**/swh/web/tests/resources/contents/code/extensions/test.md",
    "**/*.inc",
    "**/swh/scanner/resources/*",
]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "pydata_sphinx_theme"

html_favicon = "_static/favicon.ico"

# Theme options are theme-specific and customize the look and feel of a theme
# further. See: https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/
#
html_theme_options = {
    "show_prev_next": True,
    "use_edit_page_button": True,
    "icon_links": [
        {
            "name": "GitLab",
            "url": "https://gitlab.softwareheritage.org/swh/devel",
            "icon": "fa-brands fa-square-gitlab",
            "type": "fontawesome",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/user/swh/",
            "icon": "fa-solid fa-box",
            "type": "fontawesome",
        },
        {
            "name": "System Status",
            "url": "https://status.softwareheritage.org/",
            "icon": "fa-solid fa-heart-pulse",
            "type": "fontawesome",
        },
        {
            "name": "Software Heritage Homepage",
            "url": "https://www.softwareheritage.org/",
            "icon": "fa-solid fa-house",
            "type": "fontawesome",
        },
    ],
    "navbar_persistent": ["search-button"],
    "navigation_with_keys": False,
}

html_logo = "_static/software-heritage-logo-title.svg"

html_context = {
    "gitlab_url": "https://gitlab.softwareheritage.org",
    "gitlab_user": "swh/devel",
    "gitlab_repo": "swh-docs",
    "gitlab_version": "master",
    "doc_path": "docs",
    # The swh-docs building process symlinks the documentation for
    # individual modules into the swh-docs tree to generate a single Sphinx
    # project. The “Edit this page” link therefore needs to point to the right
    # repository on GitLab in these case.
    # We implement this using the `edit_page_url_template` option, see:
    # https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/source-buttons.html#custom-edit-url
    # We can take advantage that it’s a Jinja2 template to recognize
    # that API documentation file path starts with `devel/swh-` and adjust
    # accordingly. This is a bit of a hack, but we can hope it’ll be enough as
    # long as we stay consistent for module paths.
    # Please note the usage of `{%-` and `-%}` used to trim spaces from the
    # generated string. See:
    # https://jinja.palletsprojects.com/en/3.1.x/templates/#whitespace-control
    "edit_page_url_template": """
        {%- if file_name.startswith('devel/swh-') -%}
          {% set path = file_name.split('/') -%}
          {% set gitlab_repo = path[1] -%}
          {% set doc_path -%}
            docs/{{ path[2:-1] | join('/') }}
          {%- endset -%}
          {% set file_name = path[-1] -%}
        {% endif -%}
        {{ gitlab_url }}/{{ gitlab_user }}/{{ gitlab_repo -}}
        /-/edit/{{ gitlab_version }}/{{ doc_path }}{{ file_name -}}
    """,
    # Use light mode by default until the landing page better supports dark mode
    "default_mode": "light",
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_js_files = ["custom.js"]
html_css_files = ["custom.css"]

# Possible sidebar configuration is explained at:
# https://pydata-sphinx-theme.readthedocs.io/en/latest/user_guide/layout.html
# html_sidebars = {}

# If not None, a 'Last updated on:' timestamp is inserted at every page
# bottom, using the given strftime format.
# The empty string is equivalent to '%b %d, %Y'.
html_last_updated_fmt = "%Y-%m-%d %H:%M:%S %Z"

# refer to the Python standard library.
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# Redirects for pages that were moved, so we don't break external links.
# Uses sphinx-reredirects
redirects = {
    "devel/swh-deposit/spec-api": "api/api-documentation.html",
    "devel/swh-deposit/metadata": "api/metadata.html",
    "devel/swh-deposit/specs/blueprint": "../api/use-cases.html",
    "devel/swh-deposit/user-manual": "api/user-manual.html",
    "devel/swh-dataset/index": "../swh-export/index.html",
    "devel/swh-dataset/graph/dataset": "../../swh-export/graph/dataset.html",
    "devel/swh-dataset/graph/schema": "../../swh-export/graph/schema.html",
    "devel/swh-dataset/graph/athena": "../../swh-export/graph/athena.html",
    "devel/swh-dataset/graph/databricks": "../../swh-export/graph/databricks.html",
    "devel/swh-dataset/export": "../swh-export/export.html",
    "devel/swh-dataset/generate_subdataset": "../swh-export/generate_subdataset.html",
    "devel/apidoc/swh.dataset": "swh.export.html",
    "infrastructure/index": "../sysadm/network-architecture/index.html",
    "infrastructure/network": "../sysadm/network-architecture/index.html",
    "infrastructure/service-urls": "../sysadm/network-architecture/service-urls.html",  # noqa
    "architecture": "devel/architecture/overview.html",
    "architecture/mirror": "../../sysadm/mirror-operations/index.html",
    "keycloak": "../../sysadm/user-management/keycloak/index.html",
    "mirror": "architecture/mirror.html",
    "users": "user",
    "devel/swh-web/uri-scheme-identifiers": "uri-scheme-swhids.html",
}


# -- autodoc configuration ----------------------------------------------
autodoc_default_flags = [
    "members",
    "undoc-members",
    "private-members",
    "special-members",
]
autodoc_member_order = "bysource"
autodoc_mock_imports = [
    "rados",
]
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


# sphinx event handler to set adequate django settings prior reading
# apidoc generated rst files when building doc to avoid autodoc errors
def set_django_settings(app, env, docname):
    if any(
        [
            pattern in str(app.srcdir)
            for pattern in ("swh-web-client", "DWCLI", "swh-webhooks")
        ]
    ):
        # swh-web-client and swh-webhooks are detected as swh-web by the code below
        # but django is not installed when building standalone doc for these packages
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
        lookup = (
            Path(sys.prefix) / "share/swh-docs/docs/devel/glossary.rst",
            Path(sys.prefix) / "local/share/swh-docs/docs/devel/glossary.rst",
            Path(__file__).parents[3] / "docs/devel/glossary.rst",
            Path(__file__).parents[4] / "docs/devel/glossary.rst",
            Path(__file__).parents[5] / "docs/devel/glossary.rst",
        )
        for glossary in lookup:
            if glossary.is_file():
                print(f"Injecting glossary from {glossary} in index")
                with glossary.open("r") as f:
                    source[0] += "\n" + f.read()
                    break
        else:
            raise EnvironmentError("glossary file not found")


def get_sphinx_warning_handler():
    from sphinx.util.logging import WarningStreamHandler

    logger = logging.getLogger("sphinx")
    for handler in logger.handlers:
        if isinstance(handler, WarningStreamHandler):
            return handler


# before starting building the doc, we want to ensure all the
# swh-xxx/docs/README.{rst,md} exists, or create a symlink if not. This is only
# useful when building the documentation of a sw package in isolation; when
# building the whole swh-docs, then the docs/devel/bin/ln-sphinx-subprojects
# will take care of these symlinks
def ensure_readme(app, config):
    srcpath = app.srcdir
    if srcpath.name.endswith("swh.docs"):
        # ln-sphinx-subprojects script should already have done the job
        return
    for extension in ("rst", "md"):
        fname = f"README.{extension}"
        readme_file = srcpath / ".." / fname
        symlink = srcpath / fname
        if readme_file.exists() and not symlink.exists():
            symlink.symlink_to(readme_file)
            break


def setup(app):
    app.connect("config-inited", ensure_readme)
    # env-purge-doc event is fired before source-read
    app.connect("env-purge-doc", set_django_settings)
    # add autosimple directive (used in swh-web)
    app.add_autodocumenter(SimpleDocumenter)
    # set an environment variable indicating we are currently building
    # the documentation
    os.environ["SWH_DOC_BUILD"] = "1"

    # filter out parallel read/write in sphinx extension warnings
    # to not consider them as errors when using -W option of sphinx-build
    class ParallelReadWarningFilter(logging.Filter):
        def filter(self, record: logging.LogRecord) -> bool:
            message = record.getMessage()
            return all(
                text not in message
                for text in (
                    "extension does not declare if it is safe for parallel",
                    "extension is not safe for parallel",
                    "doing serial",
                )
            )

    # insert a custom filter in the warning log handler of sphinx
    get_sphinx_warning_handler().filters.insert(0, ParallelReadWarningFilter())

    if swh_package_doc_tox_build:
        # ensure glossary will be available in package doc scope
        app.connect("source-read", add_glossary_to_index)

        # suppress some httpdomain warnings in non web packages
        if not any([pattern in str(app.srcdir) for pattern in ("swh-web", "DWAPPS")]):
            # filter out httpdomain unresolved reference warnings
            # to not consider them as errors when using -W option of sphinx-build
            class HttpDomainRefWarningFilter(logging.Filter):
                def filter(self, record: logging.LogRecord) -> bool:
                    return not record.msg.startswith("Cannot resolve reference to")

            # insert a custom filter in the warning log handler of sphinx
            get_sphinx_warning_handler().filters.insert(0, HttpDomainRefWarningFilter())

    else:

        class SwhPackageTocTreeAddApidoc(SphinxTransform):
            # Post processing. Deadline to modify text and referencing.
            default_priority = 700

            def apply(self, **kwargs):
                # Act only on indexes of swh packages
                match = re.match(r"^devel/(swh-[^/]+)/index$", self.env.docname)
                if not match:
                    return

                # Compute path to the module index generated by apidoc
                swh_package = match.group(1).replace("-", ".")
                swh_package_apidoc = f"devel/apidoc/{swh_package}"
                swh_package_apidoc_file = (
                    os.path.join(self.env.srcdir, swh_package_apidoc) + ".rst"
                )

                # If the path exists, add it to the toc
                if not os.path.exists(swh_package_apidoc_file):
                    return
                nodes = list(self.document.findall(addnodes.toctree))
                if nodes:
                    main_toc = nodes[0]
                    main_toc["entries"].append((None, swh_package_apidoc))
                    main_toc["includefiles"].append(swh_package_apidoc)

        app.add_transform(SwhPackageTocTreeAddApidoc)
