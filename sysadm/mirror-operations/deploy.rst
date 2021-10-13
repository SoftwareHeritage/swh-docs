.. _mirror_deploy:

How to deploy a mirror
======================

This section describes how to deploy a mirror using the software stack provided
by |swh|.

A mirror deployment will consists in running several components of the |swh|
stack:

- an instance of the storage (swh-storage) with its backend storage (PostgreSQL
  or Cassandra),
- an instance of the object storage (swh-objstorage) with its backend storage
  solution (in-house with the `pathslicer` backend, or cloud based)
- an instance of the front page (swh-web)
- an instance of the search engine (swh-search)
- the vault service and its support tooling,
- the replayer services.

Each service consists in an HTTP-based RPC served by a `gunicorn
<https://gunicorn.org/>`_ `WSGI
<https://fr.wikipedia.org/wiki/Web_Server_Gateway_Interface>`_ server.


Docker-based deployment
-----------------------

This represents a lot of services to configure and orchestrate. In order to
help to start the configuration of a mirror, a `docker-swarm
<https://docs.docker.com/engine/swarm/>`_ based deployment solution is provided
as a working example of the mirror stack:

  https://forge.softwareheritage.org/source/swh-docker

It is strongly recommended to :ref:`start from there <mirror_docker>` in a test
environment before planning a production-like deployment.


Step by step deployment of a mirror
-----------------------------------

When using the |swh| software stack to deploy a mirror, a number of |swh|
software components must be installed and configured to interact woth each other:

#. :ref:`How to deploy the objstorage <mirror_objstorage>`: the objstorage
   consists in an object storage solution (can be cloud-based or on local
   filesystem like ZFS pools) and the :ref:`swh-objstorage` service,

#. :ref:`How to deploy graph replayer services <mirror_graph_replayer>`:
   :mod:`swh-devel:swh.objstorage.replayer.replay` service is responsible for
   consuming the ``content`` topic from the |swh| kafka broker and filling the mirror
   objstorage, retrieving blob objects from a |swh| objstarage,

#. :ref:`How to deploy the storage <mirror_storage>`: the storage consists in a
   database to store the graph of the |swh| archive (PostgreSQL or Cassandra)
   and the :ref:`swh-devel:swh-storage` service,

#. :ref:`How to deploy graph replayer services <mirror_graph_replayer>`:
   :mod:`swh-devel:swh.storage.replay` service is responsible for consuming from
   the |swh| kafka broker and fill the mirror storage,

#. :ref:`How to deploy the frontend <mirror_frontend>`: the :ref:`frontend
   <swh-devel:swh-web>` consists in a `django <https://www.djangoproject.com/>`_
   based application serving both the web API and the main UI for browsing the
   Archive.

#. :ref:`How to deploy the search engine <mirror_search>`: the :ref:`search engine
   <swh-devel:swh-search>` consists in a `ElasticSearch <https://www.elastic.co/>`_
   based application used by the frontend.

#. :ref:`How to deploy the vault service <mirror_vault>`: the :ref:`vault
   service <swh-devel:swh-vault>` consists in a backend asynchronous service
   allowing the user to ask for a zip archive of a given repository or git
   history.



.. toctree::
   :titlesonly:
   :hidden:

   docker
   objstorage
   storage
   content-replayer
   graph-replayer
   frontend
   search
   vault
