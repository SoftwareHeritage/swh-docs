.. _swh-docs:


Software Heritage - Development Documentation
=============================================


Getting started
---------------

* :ref:`getting-started` ← start here to get your own Software Heritage
  platform running in less than 5 minutes, or
* :ref:`developer-setup` ← here to hack on the Software Heritage software
  stack


Architecture
------------

* :ref:`architecture` ← go there to have a glimpse on the Software Heritage software
  architecture
* :ref:`mirror` ← go there to have learn what a Software Heritage mirror is and
  how set up one



Components
----------

Here is brief overview of the most relevant software components in the Software
Heritage stack. Each component name is linked to the development documentation
of the corresponding Python module.

:ref:`swh.core <swh-core>`
    low-level utilities and helpers used by almost all other modules in the
    stack

:ref:`swh.dataset <swh-dataset>`
    public datasets and periodic data dumps of the archive released by Software
    Heritage

:ref:`swh.deposit <swh-deposit>`
    push-based deposit of software artifacts to the archive

swh.docs
    developer documentation (used to generate this doc you are reading)

:ref:`swh.fuse <swh-fuse>`
    Virtual file system to browse the Software Heritage archive, based on
    `FUSE <https://github.com/libfuse/libfuse>`_

:ref:`swh.graph <swh-graph>`
    Fast, compressed, in-memory representation of the archive, with tooling to
    generate and query it.

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

:ref:`swh.loader-git <swh-loader-git>`
    loader for `Git <https://git-scm.com/>`_ repositories

:ref:`swh.loader-mercurial <swh-loader-mercurial>`
    loader for `Mercurial <https://www.mercurial-scm.org/>`_ repositories

:ref:`swh.loader-svn <swh-loader-svn>`
    loader for `Subversion <https://subversion.apache.org/>`_ repositories

:ref:`swh.model <swh-model>`
    implementation of the :ref:`data-model` to archive source code artifacts

:ref:`swh.objstorage <swh-objstorage>`
    content-addressable object storage

:ref:`swh.objstorage.replayer <swh-objstorage-replayer>`
    Object storage replication tool

:ref:`swh.scanner <swh-scanner>`
    source code scanner to analyze code bases and compare them with source code
    artifacts archived by Software Heritage

:ref:`swh.scheduler <swh-scheduler>`
    task manager for asynchronous/delayed tasks, used for recurrent (e.g.,
    listing a forge, loading new stuff from a Git repository) and one-off
    activities (e.g., loading a specific version of a source package)

:ref:`swh.search <swh-search>`
    search engine for the archive

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

:ref:`swh.web.client <swh-web-client>`
    Python client for :ref:`swh.web <swh-web>`


Dependencies
------------

The dependency relationships among the various modules are depicted below.

.. _py-deps-swh:
.. figure:: images/py-deps-swh.svg
   :width: 1024px
   :align: center

   Dependencies among top-level Python modules (click to zoom).


Archive
-------

* :ref:`Archive ChangeLog <archive-changelog>`: notable changes to the archive
  over time


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* `URLs index <http-routingtable.html>`_
* :ref:`search`
* :ref:`glossary`


.. ensure sphinx does not complain about index files not being included

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   :titlesonly:
   :hidden:

   architecture
   getting-started
   developer-setup
   journal
   mirror
   API documentation <apidoc/modules>
   swh.core <swh-core/index>
   swh.dataset <swh-dataset/index>
   swh.deposit <swh-deposit/index>
   swh.fuse <swh-fuse/index>
   swh.graph <swh-graph/index>
   swh.indexer <swh-indexer/index>
   swh.journal <swh-journal/index>
   swh.lister <swh-lister/index>
   swh.loader <swh-loader>
   swh.model <swh-model/index>
   swh.objstorage <swh-objstorage/index>
   swh.scanner <swh-scanner/index>
   swh.scheduler <swh-scheduler/index>
   swh.search <swh-search/index>
   swh.storage <swh-storage/index>
   swh.vault <swh-vault/index>
   swh.web <swh-web/index>
   swh.web.client <swh-web-client/index>
