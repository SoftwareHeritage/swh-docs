#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import django
import os

# General information about the project.
project = 'Software Heritage - Development Documentation'
copyright = '2015-2017, the Software Heritage developers'
author = 'the Software Heritage developers'

# -- General configuration ------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.napoleon',
              'sphinx.ext.intersphinx',
              'sphinxcontrib.httpdomain',
              'sphinx.ext.extlinks']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
source_suffix = ['.rst', '.md']
# source_suffix = '.rst'

source_parsers = {
   '.md': 'recommonmark.parser.CommonMarkParser',
}

# The master toctree document.
master_doc = 'index'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = ''
# The full version, including alpha/beta/rc tags.
release = ''

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    'logo': 'software-heritage-logo-title-motto-vertical.svg',
    'font_family': "'Alegreya Sans', sans-serif",
    'head_font_family': "'Alegreya', serif",
    #                     equivalent of alabaster's:
    'gray_1': '#5b5e6f',  # dark gray
    'gray_2': '#efeff2',  # light gray
    'gray_3': '#b1b5ae',  # medium gray
    'pink_1': '#e5d4cf',  # light pink
    'pink_2': '#bd9f97',  # medium pink

}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# make logo actually appear, avoiding gotcha due to alabaster default conf.
# https://github.com/bitprophet/alabaster/issues/97#issuecomment-303722935
html_sidebars = {
    '**': [
        'about.html',
        'localtoc.html',
        'relations.html',
        'sourcelink.html',
        'searchbox.html',
    ]
}


# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'https://docs.python.org/3/': None}


# -- autodoc configuration ----------------------------------------------
autodoc_default_flags = ['members', 'undoc-members']
autodoc_member_order = 'bysource'

# for the extlinks extension, sub-projects should fill that dict
extlinks = {}


# hack to set the adequate django settings when building global swh doc
# to avoid build errors
def source_read_handler(app, docname, source):
    if 'swh-deposit' in docname:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                              'swh.deposit.settings.development')
        django.setup()
    elif 'swh-web' in docname:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                              'swh.web.settings.development')
        django.setup()


def setup(app):
    app.connect('source-read', source_read_handler)