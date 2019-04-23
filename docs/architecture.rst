.. _architecture:

Software Architecture
=====================

From an end-user point of view, the |swh| platform consists in the
:term:`archive`, which can be accessed using the web interface or its REST API.
Behind the scene (and the web app) are several components that expose
different aspects of the |swh| :term:`archive` as internal REST APIs.

Each of these internal APIs have a dedicated (Postgresql) database.

A global view of this architecture looks like:

.. thumbnail:: images/general-architecture.svg

   General view of the |swh| architecture.

The front API components are:

- :ref:`Storage API <swh-storage>`
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


Tasks
-----

The following sequence diagram shows the interactions between these components
when a new forge needs to be archived. This example depicts the case of a
gitlab_ forge, but any other supported source type would be very similar.

.. thumbnail:: images/tasks-lister.svg

As one might observe in this diagram, it does create two things:

- it adds one :term:`origin` objects in the :term:`storage` database for each
  source code repository, and

- it insert one :term:`loader` task for each source code repository that will
  be in charge of importing the content of that repository.


The sequence diagram below describe this second step of importing the content
of a repository. Once again, we take the example of a git repository, but any
other type of repository would be very similar.

.. thumbnail:: images/tasks-git-loader.svg


.. _celery: https://www.celeryproject.org
.. _gitlab: https://gitlab.com
