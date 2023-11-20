.. _user-software-origins-conda:

Conda
=====

.. include:: dynamic/conda_status.inc

`Conda <https://conda.io/>`_ is an alternative package manager for Python, used
in particular by the `Anaconda <https://www.anaconda.com/>`_ and
`conda-forge <https://anaconda.org/conda-forge/>`_ distributions,
with support for other language ecosystems.

|swh| currently has a lister and a loader for Archlinux packages, but they load
binary packages (``.tar.gz``); and need to be modified to load source packages instead
(``.conda``).

For every configured channel (``main``, ``conda-forge``, ...) and every architecture
(``linux-64``, ``win-64``, ...), the Conda lister downloads
:file:`https://repo.anaconda.com/pkgs/{channel}/{arch}/repodata.json.bz2`,
from which it extracts a list of package names. Then, from each of these package names,
it triggers a load for the origin :file:`https://anaconda.org/{channel}/{package_name}`
with the list of tarballs of that package.

.. note::

    There is a ``_anaconda_depends`` package; what do we and should we do with it?

Source code from Conda is currently only archived on |swh|'s staging infrastructure.
Metadata from Conda is currently not collected or indexed at all.
