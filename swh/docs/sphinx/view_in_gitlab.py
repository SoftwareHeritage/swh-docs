# Copyright (C) 2021-2023  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

"""
Shows a link 'View page source' on top of each page.
"""


def html_page_context(app, pagename, templatename, context, doctree):
    if pagename.startswith("apidoc/"):
        # Auto-generated documentation.
        # TODO: link to the .py
        context["show_source"] = False
        return
    elif pagename.startswith("swh-"):
        # .rst from a package's docs/ directory
        (repository, _, path) = pagename.partition("/")
    else:
        # .rst from swh-docs/docs/
        repository = "swh-docs"
        path = pagename
    source_url = (
        f"https://gitlab.softwareheritage.org/swh/devel/{repository}"
        f"/-/blob/master/docs/{path}"
    )

    # Set a variable that can be used by swh-docs/docs/_templates/breadcrumbs.html:
    context["swh_source_url"] = source_url


def setup(app):
    app.connect("html-page-context", html_page_context)
    return {"parallel_read_safe": True}
