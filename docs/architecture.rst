.. _architecture:

Architecture
============


Python modules
--------------

.. _py-deps-swh:
.. figure:: images/py-deps-swh.svg
   :width: 1024px
   :align: center

   Dependencies among top-level Python modules (click to zoom).

Here is brief overview of the most relevant Python modules in the Software
Heritage Python stack (each module name is linked to its API documentation).

:mod:`swh.archiver`
    orchestrator in charge of guaranteeing that object storage content is
    pristine and available in a sufficient amount of copies

:mod:`swh.core`
     low-level utilities and helpers used by almost all other modules in the
     stack

:mod:`swh.docs`
     developer documentation (used to generate the docs you are reading)

:mod:`swh.indexer`
     tools and workers used to crawl the content of the archive and extract
     derived information from any artifact stored in it

:mod:`swh.journal`
     persistent logger of changes to the archive, with publish-subscribe
     support

:mod:`swh.lister`
     collection of listers for all sorts of source code hosting and
     distribution places (forges, distributions, package managers, etc.)

:mod:`swh.loader.core`
     low-level loading utilities and helpers used by all other loaders

:mod:`swh.loader.debian`
     loader for `Debian <https://www.debian.org/>`_ source packages

:mod:`swh.loader.dir`
     loader for source directories (e.g., expanded tarballs)

:mod:`swh.loader.git`
     loader for `Git <https://git-scm.com/>`_ repositories

:mod:`swh.loader.mercurial`
     loader for `Mercurial <https://www.mercurial-scm.org/>`_ repositories

:mod:`swh.loader.svn`
     loader for `Subversion <https://subversion.apache.org/>`_ repositories

:mod:`swh.loader.tar`
     loader for source tarballs

:mod:`swh.model`
     implementation of the :ref:`data-model` to archive source code artifacts

:mod:`swh.objstorage`
     content-addressable object storage

:mod:`swh.scheduler`
     task manager for asynchronous/delayed tasks, used for recurrent (e.g.,
     listing a forge, loading new stuff from a Git repository) and one-off
     activities (e.g., loading a specific version of a source package)

:mod:`swh.storage`
     abstraction layer over the archive, allowing to access all stored source
     code artifacts as well as their metadata

:mod:`swh.vault`
     implementation of the vault service, allowing to retrieve parts of the
     archive as self-contained bundles (e.g., individual releases, entire
     repository snapshots, etc.)

:mod:`swh.web`
     Web client to browse the archive, for both interactive (HTML UI) and
     mechanized (REST API) use
