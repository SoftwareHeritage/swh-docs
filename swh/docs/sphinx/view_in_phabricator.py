# Copyright (C) 2021  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

"""
Shows a link 'View this page in Phabricator' on top of each page.
"""


def html_page_context(app, pagename, templatename, context, doctree):
    if pagename.startswith("apidoc/"):
        # Auto-generated documentation.
        # TODO: link to the .py
        context["show_source"] = False
        return
    elif pagename.startswith("swh-"):
        # .rst from a package's docs/ directory
        repository = pagename.split("/", 1)[0]
        path = "docs/"
    else:
        # .rst from swh-docs/docs/
        repository = "swh-docs"
        path = "docs/"
    context[
        "source_url_prefix"
    ] = f"https://forge.softwareheritage.org/source/{repository}/browse/master/{path}"


def setup(app):
    app.connect("html-page-context", html_page_context)
