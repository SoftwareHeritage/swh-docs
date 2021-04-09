.. _architecture-overview:

Software Architecture Overview
==============================


From an end-user point of view, the |swh| platform consists in the
:term:`archive`, which can be accessed using the web interface or its REST API.
Behind the scene (and the web app) are several components that expose
different aspects of the |swh| :term:`archive` as internal RPC APIs.

Each of these internal APIs have a dedicated (Postgresql) database.

A global (and incomplete) view of this architecture looks like:

.. thumbnail:: ../images/general-architecture.svg

   General view of the |swh| architecture.

The front API components are:

- :ref:`Storage API <swh-storage>` (including the Metadata Storage)
- :ref:`Deposit API <swh-deposit>`
- :ref:`Vault API <swh-vault>`
- :ref:`Indexer API <swh-indexer>`
- :ref:`Scheduler API <swh-scheduler>`

On the back stage of this show, a celery_ based game of tasks and workers
occurs to perform all the required work to fill, maintain and update the |swh|
:term:`archive`.

The main components involved in this choreography are:

- :term:`Listers <lister>`: a lister is a type of task aiming at scraping a
  web site, a forge, etc. to gather all the source code repositories it can
  find. For each found source code repository, a :term:`loader` task is
  created.

- :term:`Loaders <loader>`: a loader is a type of task aiming at importing or
  updating a source code repository. It is the one that inserts :term:`blob`
  objects in the :term:`object storage`, and inserts nodes and edges in the
  :ref:`graph <swh-merkle-dag>`.

- :term:`Indexers <indexer>`: an indexer is a type of task aiming at crawling
  the content of the :term:`archive` to extract derived information (mimetype,
  etc.)

- :term:`Vault <vault>`: this type of celery task is responsible for cooking a
  compressed archive (zip or tgz) of an archived object (typically a directory
  or a repository). Since this can be a rather long process, it is delegated to
  an asynchronous (celery) task.


Tasks
-----

Listers
+++++++

The following sequence diagram shows the interactions between these components
when a new forge needs to be archived. This example depicts the case of a
gitlab_ forge, but any other supported source type would be very similar.

.. thumbnail:: images/tasks-lister.svg

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
+++++++

The sequence diagram below describe this second step of importing the content
of a repository. Once again, we take the example of a git repository, but any
other type of repository would be very similar.

.. thumbnail:: images/tasks-git-loader.svg


.. _celery: https://www.celeryproject.org
.. _gitlab: https://gitlab.com

