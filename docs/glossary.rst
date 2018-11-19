:orphan:

.. _glossary:

Glossary
========

.. glossary::

   archive

     An instance of the |swh| data store.

   archiver

     A component dedicated at replicating an :term:`archive` and ensure there
     are enough copies of each element to ensure resiliency.

   ark

     `Archival Resource Key`_ (ARK) is a Uniform Resource Locator (URL) that is
     a multi-purpose persistent identifier for information objects of any type.

   artifact
   software artifact

     An artifact is one of many kinds of tangible by-products produced during
     the development of software.

   content
   blob

     A (specific version of a) file stored in the archive, identified by its
     cryptographic hashes (SHA1, "git-like" SHA1, SHA256) and its size. Also
     known as: :term:`blob`. Note: it is incorrect to refer to Contents as
     "files", because files are usually considered to be named, whereas
     Contents are nameless. It is only in the context of specific
     :term:`directories <directory>` that :term:`contents <content>` acquire
     (local) names.

   directory

     A set of named pointers to contents (file entries), directories (directory
     entries) and revisions (revision entries). All entries are associated to
     the local name of the entry (i.e., a relative path without any path
     separator) and permission metadata (e.g., ``chmod`` value or equivalent).

   doi

     A Digital Object Identifier or DOI_ is a persistent identifier or handle
     used to uniquely identify objects, standardized by the International
     Organization for Standardization (ISO).

   journal

     The :ref:`journal <swh-journal>` is the persistent logger of the |swh| architecture in charge
     of logging changes of the archive, with publish-subscribe_ support.

   lister

     A :ref:`lister <swh-lister>` is a component of the |swh| architecture that is in charge of
     enumerating the :term:`software origin` (e.g., VCS, packages, etc.)
     available at a source code distribution place.

   loader

     A :ref:`loader <swh-loader-core>` is a component of the |swh| architecture
     responsible for reading a source code :term:`origin` (typically a git
     reposiitory) and import or update its content in the :term:`archive` (ie.
     add new file contents int :term:`object storage` and repository structure
     in the :term:`storage database`).

   hash
   cryptographic hash
   checksum
   digest

     A fixed-size "summary" of a stream of bytes that is easy to compute, and
     hard to reverse. (Cryptographic hash function Wikipedia article) also
     known as: :term:`checksum`, :term:`digest`.

   indexer

     A component of the |swh| architecture dedicated to producing metadata
     linked to the known :term:`blobs <blob>` in the :term:`archive`.

   objstore
   objstorage
   object store
   object storage

     Content-addressable object storage. It is the place where actual object
     :term:`blobs <blob>` objects are stored.

   origin
   software origin
   data source

     A location from which a coherent set of sources has been obtained, like a
     git repository, a directory containing tarballs, etc.

   person

     An entity referenced by a revision as either the author or the committer
     of the corresponding change. A person is associated to a full name and/or
     an email address.

   release
   tag
   milestone

     a revision that has been marked as noteworthy with a specific name (e.g.,
     a version number), together with associated development metadata (e.g.,
     author, timestamp, etc).

   revision
   commit
   changeset

     A point in time snapshot of the content of a directory, together with
     associated development metadata (e.g., author, timestamp, log message,
     etc).

   scheduler

     The component of the |swh| architecture dedicated to the management and
     the prioritization of the many tasks.

   snapshot

     the state of all visible branches during a specific visit of an origin

   storage
   storage database

     The main database of the |swh| platform in which the all the elements of
     the :ref:`data-model` but the :term:`content` are stored as a :ref:`Merkle
     DAG <swh-merkle-dag>`.

   type of origin

     Information about the kind of hosting, e.g., whether it is a forge, a
     collection of repositories, an homepage publishing tarball, or a one shot
     source code repository. For all kind of repositories please specify which
     VCS system is in use (Git, SVN, CVS, etc.) object.

   vault
   vault service

     User-facing service that allows to retrieve parts of the :term:`archive`
     as self-contained bundles (e.g., individual releases, entire repository
     snapshots, etc.)

   visit

     The passage of |swh| on a given :term:`origin`, to retrieve all source
     code and metadata available there at the time. A visit object stores the
     state of all visible branches (if any) available at the origin at visit
     time; each of them points to a revision object in the archive. Future
     visits of the same origin will create new visit objects, without removing
     previous ones.



.. _blob: https://en.wikipedia.org/wiki/Binary_large_object
.. _DOI: https://www.doi.org
.. _`persistent identifier`: https://docs.softwareheritage.org/devel/swh-model/persistent-identifiers.html#persistent-identifiers
.. _`Archival Resource Key`: http://n2t.net/e/ark_ids.html
.. _publish-subscribe: https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern