:orphan:

.. _glossary:

Glossary
========

.. glossary::

   archive

     An instance of the |swh| data store.

   ark

     `Archival Resource Key`_ (ARK) is a Uniform Resource Locator (URL) that is
     a multi-purpose persistent identifier for information objects of any type.

   artifact
   software artifact

     An artifact is one of many kinds of tangible by-products produced during
     the development of software.

   bulk on-demand archival

     A |swh| service allowing a partner to ask the archival for (possibly
     large) number of origins. It consists in an authenticated API endpoint
     allowing the user to upload a list of origins (as a CSV file) to be
     ingested as soon as possible. The service allows to get feedback from the
     |swh| archive about the ongoing ingestion process.

   compressed graph

     A compact and randomly-accessible representation of the :term:`graph`,
     as implemented by :ref:`swh-graph`.

   content
   blob

     A (specific version of a) file stored in the archive, identified by its
     cryptographic hashes (SHA1, "git-like" SHA1, SHA256) and its size. Also
     known as: :term:`blob`. Note: it is incorrect to refer to Contents as
     "files", because files are usually considered to be named, whereas
     Contents are nameless. It is only in the context of specific
     :term:`directories <directory>` that :term:`contents <content>` acquire
     (local) names.

   deposit

     A :term:`software artifact` that was pushed to the Software Heritage
     archive (unlike :term:`loaders <loader>`, which pull artifacts).
     A deposit is useful when you want to ensure a software release's source
     code is archived in SWH even if it is not published anywhere else.

     See also: the :ref:`swh-deposit` component, which implements a deposit
     client and server.

   derived dataset

     A dataset that is built from public data, such as the :term:`export`, 
     the :term:`compressed graph`, or the Archive itself.

     This includes datasets computed by :ref:`swh-datasets`, :ref:`swh-digestmap`,
     and :ref:`swh-provenance`.

     Many derived datasets are computed by |swh| themselves, but they can
     be designed and/or recomputed externally.

   directory

     A set of named pointers to contents (file entries), directories (directory
     entries) and revisions (revision entries). All entries are associated to
     the local name of the entry (i.e., a relative path without any path
     separator) and permission metadata (e.g., ``chmod`` value or equivalent).

   doi

     A Digital Object Identifier or DOI_ is a persistent identifier or handle
     used to uniquely identify objects, standardized by the International
     Organization for Standardization (ISO).

   export
   graph export

     A dump of (almost) all data in the |swh| :term:`graph` into terabytes of files
     (currently in the ORC format) that are shared publicly.
     Alongside a complete :term:`objstorage`, it allows rebuilding the
     |swh| :term:`archive`; except personal information (author names and emails)
     which is pseudonymized.

   extid
   external identifier

     An identifier used by a system that does not fit the |swh|
     :ref:`data model <data-model>`, such as Mercurial's ``nodeid``,
     or the hash of a tarball from a package manager.
     They may be stored in the |swh| archive independently of the identified object,
     to quickly match an external object (a changeset or tarball) to an object
     in the archive without downloading it.

   extrinsic metadata

     Metadata about software that is not shipped as part of the software source
     code, but is available instead via out-of-band means. For example,
     homepage, maintainer contact information, and popularity information
     ("stars") as listed on GitHub/GitLab repository pages.

     See also: :term:`intrinsic metadata` :ref:`architecture-metadata`.

   graph

     The set of all :term:`content` metadata, :term:`directory`, :term:`revision`,
     :term:`release`, :term:`snapshot`, and :term:`origin` node, and links between them,
     as a :ref:`Merkle DAG <swh-merkle-dag>`.
     Not to be confused with the :term:`compressed graph`.

     It is stored in a relational database, such as PostgreSQL or Cassandra.

     It excludes :term:`content` nodes' data, which is stored in an :term:`objstorage`.

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
     repository) and import or update its content in the :term:`archive` (ie.
     add new file contents int :term:`object storage` and repository structure
     in the :term:`storage database`).

   loading task

     A celery_ task doing the actual ingestion process; its implementation is
     provided by a :term:`loader`, and it is executed by celery_ workers. They
     used to be backed by Scheduler Tasks instances in the :term:`scheduler`
     database, but it's not the case any more (for performance reasons).

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

   intrinsic identifier

     A short character string that uniquely identifies an object,
     that can be generated deterministically, using only the content of the object,
     usually a :term:`cryptographic hash`.
     This excludes network interaction and central authority.

     Examples of intrinsic identifiers are: checksums (for files/strings only),
     git hashes, and :ref:`SWHIDs <persistent-identifiers>`

   intrinsic metadata

     Metadata about software that is shipped as part of the source code of the
     software itself or as part of related artifacts (e.g., revisions,
     releases, etc). For example, metadata that is shipped in `PKG-INFO` files
     for Python packages, :file:`pom.xml` for Maven-based Java projects,
     :file:`debian/control` for Debian packages, :file:`metadata.json` for NPM, etc.

     See also: :term:`extrinsic metadata`, :ref:`architecture-metadata`.

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

   raw extrinsic metadata
   REMD

     A piece of metadata concerning an objects stored in the |swh| archive that
     is not part of the source code from an :term:`origin`. It can come from a
     software forge (information about a project that is not the source code
     repository for this project), a deposited metadata file (for a
     :term:`deposit`), etc. These pieces of information are kept in their
     original raw format -- for archiving purpose -- but are also converted
     into a minimal format (currently a subset of CodeMeta) allowing them to be
     indexed and searchable.

   raw extrinsic metadata storage
   REMD Storage

     The |swh| storage dedicated to store all the gathered extrinsic metadata
     documents verbatim, in their original format. Currently, this service is
     part of the main :term:`storage`.

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

   save code now

     A publicly accessible service allowing users to ask for immediate save of
     a given source code origin. The request can be automatically accepted and
     processed if the origin is from a well known domain, or may require manual
     validation. Note that a save code now request can only concern a supported
     origin type.

   scheduler

     The component of the |swh| architecture dedicated to the management and
     the prioritization of the many tasks.

   Scheduler Task

     :py:class:`The object <swh.scheduler.model.Task>` (stored in the
     :term:`scheduler` database) representing a background (celery_) task to be
     regularly scheduled for execution. Note that not all the background tasks
     are backed by a Scheduler Task instance; one-shot :term:`loading task`
     are most of the time not represented and model as Scheduler Task.

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
.. _celery: https://docs.celeryq.dev
