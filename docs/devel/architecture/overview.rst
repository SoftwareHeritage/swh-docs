.. _architecture-overview:

Software Architecture Overview
==============================


From an end-user point of view, the |swh| platform consists in the
:term:`archive`, which can be accessed using the web interface or its public
APIs (REST or GraphQL). Behind the scene (and the web app) are several
components/services that expose different aspects of the |swh| :term:`archive`
as internal RPC APIs.

These internal APIs have a dedicated database, typically PostgreSQL_ or
Cassandra_.

Big Pictures
------------


The Read-Only View
^^^^^^^^^^^^^^^^^^

A global (and incomplete) view of this architecture, limited to components
involved when reading from the archive, looks like:

.. thumbnail:: ../images/general-architecture-read.svg

   General view of the |swh| architecture when reading.

As you can see, there are quite a few parts in this infrastructure. We will come
back on each of them in more details later, but here is a quick description:

- **Ingress**: HTTP requests from the end user are received by a frontend ingress service (a
  reverse proxy), responsible for routing and load balancing them to the proper
  backend service.

- **WebApp**: this is the main |swh| frontend tier; it is a Django based HTTP server
  responsible for handling most the frontend and public API requests (browsing
  the archive or using the public REST API). Being a central component for any
  user interaction, it needs to have access to most other |swh| services.

- **Authentication**: this is a Keycloak server used to handle authentication for
  users that want to have authenticated access to the archive (using lifted
  rate limiting, have access to administration boards, etc.)

- **Deposit**: this is a Django-based HTTP server with a very minimal UI (a single
  static documentation page), but providing SWORD API allowing deposit partners
  to upload software source code (with metadata) directly in the archive. It
  also allows to check and have feedback on the status of previous deposits.
  Since it is an authenticated only service, it has access toand uses the Keycloak
  authentication service.

- **Counters**: a simple service maintaining general archive statistics. It is used
  by the frontend to generate the per-forge counters and overall evolution
  curves. It uses a Redis backend (for Hyperloglog counters).

- **Scheduler**: the scheduler service. This is needed by the webapp frontend to
  get feedback for services like Save Code Now and like, or schedule new
  loading and listing tasks for these services. This service uses a database
  storage.

- **Vault**: the service responsible for managing and executing retrieval queries
  (when a user wants to retrieve a whole directory or a whole git history).
  This service uses a database storage.

- **Indexer Storage**: a data store that keeps track of all the indexed metadata
  objects in the archive. It is used directly by the webapp frontend to get
  information like the mimetype or the possible license of a content. This
  service is using a database storage.

- **RO Storage**: the main storage service, hosting the whole |swh| archive
  structure (but the file content themselves). In the context of the read
  access to the archive, the Storage used is a Read-Only storage with a Masking
  Proxy. This proxy allows to mask or modify on the fly objects that need
  to be either hidden completely (typically when a takedown request is being
  processed that impact the browsed object) or altered (typically when a person
  asked for their former name not to be visible any more). The main storage can
  be hosted either on a Postgresql database or a Cassandra one. The main
  archive now uses Cassandra as main backend storage.

- **Search**: the |swh| search service. This service is using an Elasticsearch
  backend.

- **Objstorage**: this data storage is used to store all the content blobs (the
  actual source code files). It is a content-addressable object storage. The
  |swh| objstorage provides an abstract frontend/API for many possible
  backends. Currently the main archive is using a Ceph cluster for this, with a
  custom layer (named Winery) in front to account for the specificities of the
  |swh| workload (handle 10th of billions of small objects).


The Ingestion View
^^^^^^^^^^^^^^^^^^

When looking at how software source code are harvested and ingested in the
archive, the global picture looks like:

.. thumbnail:: ../images/general-architecture-ingestion.svg

   General view of the |swh| ingestion architecture.

.. Note:: :term:`REMD` in this pictures stands for :term:`raw extrinsic metadata`.

The central part of this setup is the scheduler service, responsible for
keeping track of loading, listing and a few other types of tasks. The task
execution framework uses Celery_ as backend. There are actually 2 completely
different tasks systems provided by both the scheduler and the side services:

- one is dedicated to managing the loading of source code from origins (aka spawning
  :ref:`Loader <swh-loader-core>` tasks); these are one-shot celery tasks not
  reified in the scheduler database,

- the other is a generic task scheduling service mostly responsible for
  recurring tasks; especially :ref:`forge listing <swh-lister>` ones, but not
  only. Some one-shot loading tasks are still handled by this scheduler
  (especially loading origins from :term:`save code now` requests). There are
  also :ref:`vault <swh-vault>` cooking tasks and deposit checker tasks that
  are using this generic scheduler.

A more detailed view of this later is :ref:`available below
<source_code_scrapping>`.

One noticeable point in this schematic is the presence of the :py:class:`Blocking
Proxy <swh.storage.proxies.blocking.BlockingProxyStorage>` in the :ref:`storage
<swh-storage>` configuration. This proxy is a helper to prevent from ingesting
from origins that have been disabled as a result of a takedown notice.

.. Note:: Even if not represented in this diagram, there are actually several
   :term:`Scheduler Task` runner service instances running: one is scheduling
   high priority :term:`Scheduler Task` (using a dedicated set of `celery
   queues`_), typically for :term:`save code now` requests; one is special case
   for scheduling first visits of a newly added forge or a :term:`bulk
   on-demand archival` request (also using dedicated celery queues); the last
   is responsible for scheduling all other standard (non priority)
   :term:`Scheduler Task`.

.. Note:: Loading tasks are not represented by one-shot :term:`Scheduler Task`
   instances (in the scheduler database) anymore, but the corresponding celery
   tasks are directly spawned by the "loader scheduler" (it was not possible to
   handle that many entries in the database efficiently). There is however
   still an exception for deposit loading tasks that are still managed via this
   generic scheduling scaffolding (mostly for historical reasons).


The Indexation View
^^^^^^^^^^^^^^^^^^^

The |swh| archive platform also comes with a complex indexation system. A view
from this indexation side would look like:

.. thumbnail:: ../images/general-architecture-indexation.svg

   General view of the |swh| indexation architecture.

See the :ref:`swh-indexer` documentation for more details.

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
backends. The former supports both PostgreSQL (the former solution in production)
and Cassandra (a more scalable option, now used as main backend in production).
The latter supports a large variety of "cloud" object storage as backends,
as well as a simple local filesystem.

Alterations
~~~~~~~~~~~

The main objective of an archive is to store facts forever. As such, it can be
viewed as an append-only infrastructure. However, it may be necessary to alter
the content of the archive to account for removal or alteration requests that
may happen `for several reasons`_.

We currently consider 2 types of alterations that may have to be done to the
archive:

- content removal: some objects stored in the archive should not be visible any
  more; these can be either removed entirely or masked, depending on the
  situation.
- personal identity modification: some personal information (namely the name
  and email of a person) needs not to be visible any more.

These requirements have impact on the overall architecture of the archive.
Details are documented in a :ref:`dedicated section<alterations>`.


Journal
^^^^^^^

The :term:`Journal <journal>`, which is a persistent logger of every change in
the archive, with publish-subscribe_ support, using Kafka.

The Storage publishes a kafka message in the journal each time a new object is
added to the archive; and many components consumes them to be notified of these
changes. For example, it allows the Scheduler to know when an origin has been
visited and what was the resulting status of that visit, which helps to decide
when to visit again these repositories.

It is also the foundation of the :ref:`mirror` infrastructure, as it allows
mirrors to stay up to date.

.. _source_code_scrapping:

Source code scraping
^^^^^^^^^^^^^^^^^^^^

The infrastructure aiming at finding new source code origins (git, mercurial
and other type of VCS, source packages, etc.) and regularly visiting them is
build around a few components based on a task scheduling scaffolding and using
a Celery-based asynchronous task execution framework. The scheduler itself
consists in 2 parts: a generic asynchronous task management system and a
specific management database aiming at gathering and keeping up to date
liveness information of listed origins that can be used to choose which of
them should be visited in priority.

To summarize, the parts involved in this carousel are:

:term:`Listers <lister>`:
     tasks aiming at scraping a web site like a forge, etc. to gather all the
     source code repositories it can find, also known as :term:`origins
     <origin>`. Lister tasks are triggered by the scheduler, via Celery, and
     will fill the listed origins table of the listing and visit statistics
     database (see below).

:term:`Loaders <loader>`:
     tasks dedicated to importing source code from a source code repository (an
     origin). It is the component that will insert :term:`blob` objects in the
     :term:`object storage`, and insert nodes and edges in the :ref:`graph
     <swh-merkle-dag>`.

:ref:`Scheduler <swh-scheduler>`'s generic task management:
     manages the choreography of listing tasks in |swh|, as well as a few other
     utility tasks (save code now, deposit, vault, indexers). Note that this
     component will not handle the scheduling of loading tasks any more. It
     consists in a database and API allowing to define task types and to create
     tasks to be scheduled (recurring or one shot), as well as a tool (the
     ``scheduler-runner``) dedicated to spawn these tasks via the Celery
     asynchronous execution framework, as well as another tool (the
     ``scheduler-listener``) dedicated to keeping the scheduler database in
     sync with executed tasks (task execution status, execution timestamps,
     etc.).

:ref:`Scheduler <swh-scheduler>`'s listing and visit statistics:
     database and API allowing to store information about liveness of a listed
     origin as well as statistics about the loading of said origin. The visit
     statistics are updated from the main :ref:`storage <swh-storage>` kafka
     journal.

:ref:`Scheduler <swh-scheduler>`'s origin visit scheduling:
     tool that will use the statistics about listed origins and previous visits
     stored in the database to apply scheduling policies to select the next
     pool origins to visit. This does not use the generic task management
     system, but instead directly spawn loading Celery tasks.


.. thumbnail:: ../images/lister-loader-scheduling-architecture.svg


The Scheduler
~~~~~~~~~~~~~

The :ref:`Scheduler <swh-scheduler>` manages the generic choreography of
jobs/tasks in |swh|, namely listing origins of software source code, loading
them, extracting metadata from loaded origins and repackaging repositories into
small downloadable archives for the :term:`Vault <vault>`.

It consists in a database where all the scheduling information is stored, an
API allowing unified access to this database, and a set of services and tools
to orchestrate the actual scheduling of tasks. Their execution being delegated
to a Celery-based set of asynchronous workers.

While initially a single generic scheduling utility for all asynchronous task
types, the scheduling of origin visits has now been extracted in a new,
dedicated part of the Scheduler. These loading tasks used to be managed by this
generic task scheduler as recurrent tasks, but the number of these loading
tasks baceame a problem to handle then efficiently, as well as some of their
specificities could not be accounted for to help better and more efficient
scheduling of origin visits.

There are now 2 parts in the scheduler: the original SWH Task management
system, and the new Origin Visit scheduling utility.

Both have a similar architecture at first sight: a database, an API, a celery
based execution system. The main difference of the new visit-centric system it
is dedicated to origin visits, and thus can use specific information and
metadata on origins to optimise the scheduling policy; statstics about known
origins resulting from the listing of a forge can be used as entry point for
the scheduling of origin visits according to scheduling policies that can take
several metrics into considerations, like:

- have the origin already been visited,

- if not, how "old" is the origin (what is the timestamp of its first sign of
  activity, e.g. creation date, timestamp of the first revision, etc.),

- how long since the origin has last been visited,

- how active is the origin (and thus how often it should be visited),

- etc.

For each new source code repository, a ``listed origin`` entry is added in the
scheduler database, as well as the timestamp of last known activity for this
origin as reported by the forge. For already known origins, only this last
activity timestamp is updated, if need be.

It is then the responsibility of the ``schedule-recurrent`` scheduler service
to check listed origins, as well as visit statistics (see below), in order to
regularly select the next origins to visit. This service also uses live data
from Celery to choose an appropriate number of visits to schedule (keeping the
Celery queues filled at a constant and controlled level).

The following sequence diagram shows the interactions between these components
when a new forge needs to be archived. This example depicts the case of a
gitlab_ forge, but any other supported source type would be very similar.

.. thumbnail:: ../images/tasks-lister.svg

As one might observe in this diagram, it does two things:

- it asks the forge (a gitlab_ instance in this case) the list of known
  repositories as well as some metadata (especially last update timestamp), and

- it inserts one ``listed origin`` for each new source code repository found or
  update the ``last update`` timestamp for the origin.

The sequence diagram below describe this second step of importing the content
of a repository. Once again, we take the example of a git repository, but any
other type of repository would be very similar.

.. thumbnail:: ../images/tasks-git-loader.svg


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

Compressed Graph
^^^^^^^^^^^^^^^^

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


.. _Cassandra: https://cassandra.apache.org
.. _celery: https://www.celeryproject.org
.. _CodeMeta: https://codemeta.github.io
.. _gitlab: https://gitlab.com
.. _PostgreSQL: https://www.postgresql.org
.. _Prometheus: https://prometheus.io
.. _publish-subscribe: https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern
.. _Redis: https://redis.io
.. _SWORDv2: http://swordapp.github.io/SWORDv2-Profile/SWORDProfile.html
.. _HyperLogLog: https://redislabs.com/redis-best-practices/counting/hyperloglog
.. _WebGraph: https://webgraph.di.unimi.it
.. _`for several reasons`: https://www.softwareheritage.org/legal/content-policy
.. _`celery queues`: https://docs.celeryq.dev/en/stable/getting-started/introduction.html#what-s-a-task-queue
