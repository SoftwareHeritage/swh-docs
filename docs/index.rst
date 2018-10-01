.. _swh-docs:

Software Heritage - Development Documentation
=============================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Getting started
---------------

* :ref:`getting-started` ← start here to hack on the Software Heritage software
  stack


Components
----------

Here is brief overview of the most relevant software components in the Software
Heritage stack. Each component name is linked to the development documentation
of the corresponding Python module.

:ref:`swh.archiver <swh-archiver>`
    orchestrator in charge of guaranteeing that object storage content is
    pristine and available in a sufficient amount of copies

:ref:`swh.core <swh-core>`
    low-level utilities and helpers used by almost all other modules in the
    stack

:ref:`swh.deposit <swh-deposit>`
    push-based deposit of software artifacts to the archive

swh.docs
    developer documentation (used to generate this doc you are reading)

:ref:`swh.indexer <swh-indexer>`
    tools and workers used to crawl the content of the archive and extract
    derived information from any artifact stored in it

:ref:`swh.journal <swh-journal>`
    persistent logger of changes to the archive, with publish-subscribe support

:ref:`swh.lister <swh-lister>`
    collection of listers for all sorts of source code hosting and distribution
    places (forges, distributions, package managers, etc.)

:ref:`swh.loader-core <swh-loader-core>`
    low-level loading utilities and helpers used by all other loaders

:ref:`swh.loader-debian <swh-loader-debian>`
    loader for `Debian <https://www.debian.org/>`_ source packages

:ref:`swh.loader-dir <swh-loader-dir>`
    loader for source directories (e.g., expanded tarballs)

:ref:`swh.loader-git <swh-loader-git>`
    loader for `Git <https://git-scm.com/>`_ repositories

:ref:`swh.loader-mercurial <swh-loader-mercurial>`
    loader for `Mercurial <https://www.mercurial-scm.org/>`_ repositories

:ref:`swh.loader-pypi <swh-loader-pypi>`
    loader for `PyPI <https://pypi.org/>`_ source code releases

:ref:`swh.loader-svn <swh-loader-svn>`
    loader for `Subversion <https://subversion.apache.org/>`_ repositories

:ref:`swh.loader-tar <swh-loader-tar>`
    loader for source tarballs (including Tar, ZIP and other archive formats)

:ref:`swh.model <swh-model>`
    implementation of the :ref:`data-model` to archive source code artifacts

:ref:`swh.objstorage <swh-objstorage>`
    content-addressable object storage

:ref:`swh.scheduler <swh-scheduler>`
    task manager for asynchronous/delayed tasks, used for recurrent (e.g.,
    listing a forge, loading new stuff from a Git repository) and one-off
    activities (e.g., loading a specific version of a source package)

:ref:`swh.storage <swh-storage>`
    abstraction layer over the archive, allowing to access all stored source
    code artifacts as well as their metadata

:ref:`swh.vault <swh-vault>`
    implementation of the vault service, allowing to retrieve parts of the
    archive as self-contained bundles (e.g., individual releases, entire
    repository snapshots, etc.)

:ref:`swh.web <swh-web>`
    Web application(s) to browse the archive, for both interactive (HTML UI)
    and mechanized (REST API) use


Dependencies
------------

The dependency relationships among the various modules are depicted below.

.. _py-deps-swh:
.. figure:: images/py-deps-swh.svg
   :width: 1024px
   :align: center

   Dependencies among top-level Python modules (click to zoom).


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* `URLs index <http-routingtable.html>`_
* :ref:`search`
