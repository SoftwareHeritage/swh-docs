# Copyright (C) 2017-2023  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information


from setuptools import setup

# TODO: usage of `data_files` is now deprecated; we should find another way of
# distributing these files.
#
# These files are distributed because they are required to build the sphinx
# documentation of a swh package isolated from the whole swh-development
# project (esp. as tox target in each swh package; which is e.g. used by the
# CI).
setup(
    data_files=[
        ("share/swh-docs/docs/devel", ["docs/devel/glossary.rst"]),
        ("share/swh-docs/docs/", ["docs/Makefile"]),
        ("share/swh-docs/", ["Makefile.sphinx"]),
    ],
)
