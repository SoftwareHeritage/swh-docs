.. _architecture-overview:

Software Architecture Overview
==============================


From an end-user point of view, the |swh| platform consists in the
:term:`archive`, which can be accessed using the web interface or its REST API.
Behind the scene (and the web app) are several components/services that expose
different aspects of the |swh| :term:`archive` as internal RPC APIs.

These internal APIs have a dedicated database, usually PostgreSQL_.

A global (and incomplete) view of this architecture looks like:

.. thumbnail:: ../images/general-architecture.svg

   General view of the |swh| architecture.

.. _architecture-tier-1:

Core components
---------------

The following components are the foundation of the entire |swh| architecture,
as they fetch data, store it, and make it available to every other service.

Data storage
^^^^^^^^^^^^

The :ref:`Storage <swh-storage>` provides an API to store and retrieve
elements of the :ref:`graph <data-model>`, such as directory structure,
revision history, and their respective metadata.
It relies on the :ref:`Object Storage <swh-objstorage>` service to store
the content of source code file themselves.

Both the Storage and Object Storage are designed as abstractions over possible
backends. The former supports both PostgreSQL (the current solution in production)
and Cassandra (a more scalable option we are exploring).
The latter supports a large variety of "cloud" object storage as backends,
as well as a simple local filesystem.

Task management
^^^^^^^^^^^^^^^

The :ref:`Scheduler <swh-scheduler>` manages the entire choreography of jobs/tasks
in |swh|, from detecting and ingesting repositories, to extracting metadata from them,
to repackaging repositories into small downloadable archives.

It does this by managing its own database of tasks that need to run
(either periodically or only once),
and passing them to celery_ for execution on dedicated workers.

Listers
^^^^^^^

:term:`Listers <lister>` are type of task, run by the Scheduler, aiming at scraping a
web site, a forge, etc. to gather all the source code repositories it can
find, also known as :term:`origins <origin>`.
For each found source code repository, a :term:`loader` task is created.

The following sequence diagram shows the interactions between these components
when a new forge needs to be archived. This example depicts the case of a
gitlab_ forge, but any other supported source type would be very similar.

.. thumbnail:: ../images/tasks-lister.svg

As one might observe in this diagram, it does two things:

- it asks the forge (a gitlab_ instance in this case) the list of known
  repositories, and

- it insert one :term:`loader` task for each source code repository that will
  be in charge of importing the content of that repository.

Note that most listers usually work in incremental mode, meaning they store in a
dedicated database the current state of the listing of the forge. Then, on a subsequent
execution of the lister, it will ask only for new repositories.

Also note that if the lister inserts a new loading task for a repository for which a
loading task already exists, the existing task will be updated (if needed) instead of
creating a new task.

Loaders
^^^^^^^

:term:`Loaders <loader>` are also a type of task, but aim at importing or
updating a source code repository. It is the one that inserts :term:`blob`
objects in the :term:`object storage`, and inserts nodes and edges in the
:ref:`graph <swh-merkle-dag>`.


The sequence diagram below describe this second step of importing the content
of a repository. Once again, we take the example of a git repository, but any
other type of repository would be very similar.

.. thumbnail:: ../images/tasks-git-loader.svg


Journal
^^^^^^^

The last core component is the :term:`Journal <journal>`, which is a persistent logger
of every change in the archive, with publish-subscribe_ support, using Kafka.

The Storage writes to it every time a new object is added to the archive;
and many components read from it to be notified of these changes.
For example, it allows the Scheduler to know how often software repositories are
updated by their developers, to decide when next to visit these repositories.

It is also the foundation of the :ref:`mirror` infrastructure, as it allows
mirrors to stay up to date.


.. _architecture-tier-2:

Other major components
----------------------

All the components we saw above are critical to the |swh| archive as they are
in charge of archiving source code.
But are not enough to provide another important features of |swh|: making
this archive accessible and searchable by anyone.


Archive website and API
^^^^^^^^^^^^^^^^^^^^^^^

First of all, the archive website and API, also known as :ref:`swh-web <swh-web>`,
is the main entry point of the archive.

This is the component that serves https://archive.softwareheritage.org/, which is the
window into the entire archive, as it provides access to it through a web browser or the
HTTP API.

It does so by querying most of the internal APIs of |swh|: the Data Storage (to display
source code repositories and their content), the Scheduler (to allow manual scheduling
of loader tasks through the :swh_web:`Save Code Now <save/>` feature), and many of the
other services we will see below.

Internal data mining
^^^^^^^^^^^^^^^^^^^^

:term:`Indexers <indexer>` are a type of task aiming at crawling
the content of the :term:`archive` to extract derived information.

It ranges from detecting the MIME type or license of individual files,
to reading all types of metadata files at the root of repositories
and storing them together in a unified format, CodeMeta_.

All results computed by Indexers are stored in a PostgreSQL database,
the Indexer Storage.


Vault
^^^^^

The :term:`Vault <vault>` is an internal API, in charge of cooking
compressed archive (zip or tgz) of archived objects on request (via swh-web).
These compressed objects are typically directories or repositories.

Since this can be a rather long process, it is delegated to
an asynchronous (celery) task, through the Scheduler.

.. _architecture-tier-3:

Extra services
--------------

Finally, |swh| provides additional tools that, although not necessary to operate
the archive, provide convenient interfaces or performance benefits.

It is therefore possible to have a fully-functioning archive without any of these
services (our :ref:`development Docker environment <getting-started>` disables
most of these by default).

Search
^^^^^^

The :ref:`swh-search <swh-search>` service complements both the Storage
and the Indexer Storage, to provide efficient advanced reverse-index search queries,
such as full-text search on origin URLs and metadata.

This service is a recent addition to the |swh| architecture based on ElasticSearch,
and is currently in use only for URL search.

Graph
^^^^^

:ref:`swh-graph <swh-graph>` is also a recent addition to the architecture
designed to complement the Storage using a specialized backend.
It leverages WebGraph_ to store a compressed in-memory representation of the
entire graph, and provides fast implementations of graph traversal algorithms.

Counters
^^^^^^^^

The :swh_web:`archive's landing page </>` features counts of the total number of
files/directories/revisions/... in the archive. Perhaps surprisingly, counting unique
objects at |swh|'s scale is hard, and a performance bottleneck when implemented purely
in the Storage's SQL database.

:ref:`swh-counters <swh-counters>` provides an alternative design to solve this issue,
by reading new objects from the Journal and counting them using Redis_' HyperLogLog_
feature; and keeps the history of these counters over time using Prometheus_.

Deposit
^^^^^^^

The :ref:`Deposit <swh-deposit>` is an alternative way to add content to the archive.
While listers and loaders, as we saw above, **discover** repositories
and **pull** artifacts into the archive, the Deposit allows trusted partners to
**push** the content of their repository directly to the archive,
and is internally loaded by the
:mod:`Deposit Loader <swh.loader.package.deposit.loader>`

The Deposit is centered on the SWORDv2_ protocol, which allows depositing archives
(usually TAR or ZIP) along with metadata in XML.

The Deposit has its own HTTP interface, independent of swh-web.
It also has its own SWORD client, which is specialized to interact with the Deposit
server.

Authentication
^^^^^^^^^^^^^^

While the archive itself is public, |swh| reserves some features
to authenticated clients, such as higher rate limits, access to experimental APIs
(currently: the Graph service), or the Deposit.

This is managed centrally by :ref:`swh-auth <swh-auth>` using KeyCloak.

Web Client, Fuse, Scanner
^^^^^^^^^^^^^^^^^^^^^^^^^

SWH provides a few tools to access the archive via the API:

* :ref:`swh-web-client`, a command-line interface to authenticate with SWH
  and a library to access the API from Python programs
* :ref:`swh-fuse`, a Filesystem in USErspace implementation,
  that exposes the entire archive as a regular directory on your computer
* :ref:`swh-scanner`, a work-in-progress to check which of the files in
  a project are already in the archive, without submitting them

Replayers and backfillers
^^^^^^^^^^^^^^^^^^^^^^^^^

As the Journal and various databases may be out of sync for various reasons
(scrub of either of them, migration, database addition, ...),
and because some databases need to follow the content of the Journal (mirrors),
some places of the |swh| codebase contains tools known as "replayers" and "backfillers",
designed to keep them in sync:

* the :mod:`Object Storage Replayer <swh.objstorage.replayer>` copies the content
  of an objects storage to another one. It first performs a full copy, then streams
  new objects using the Journal to stay up to date
* the Storage Replayer loads the entire content of the Journal into a Storage database,
  and also keeps them in sync.
  This is used for mirrors, and when creating a new database.
* the Storage Backfiller, which does the opposite. This was initially used to populate
  the Journal from the database; and is occasionally when one needs to clear a topic
  in the Journal and recreate it.


.. _celery: https://www.celeryproject.org
.. _CodeMeta: https://codemeta.github.io/
.. _gitlab: https://gitlab.com
.. _PostgreSQL: https://www.postgresql.org/
.. _Prometheus: https://prometheus.io/
.. _publish-subscribe: https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern
.. _Redis: https://redis.io/
.. _SWORDv2: http://swordapp.github.io/SWORDv2-Profile/SWORDProfile.html
.. _HyperLogLog: https://redislabs.com/redis-best-practices/counting/hyperloglog/
.. _WebGraph: https://webgraph.di.unimi.it/
