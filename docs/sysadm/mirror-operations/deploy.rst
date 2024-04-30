.. _mirror_deploy:

How to deploy a mirror
======================

This section describes how to deploy a mirror using the software stack provided
by |swh|.

A mirror deployment will consists in running several components of the |swh|
stack:

- An instance of the storage (:ref:`swh-storage`);
- A backend database (PostgreSQL or Cassandra) for the storage;
- An instance of the object storage (:ref:`swh-objstorage`);
- A large storage system (zfs or cloud storage) as the objstorage backend;
- An instance of the frontend (:ref:`swh-web`);
- An instance of the search engine backend (:ref:`swh-search`);
- An elasticsearch instance as swh-search backend;
- The vault service and its support tooling (RabbitMQ,
  :ref:`swh-scheduler`, :ref:`swh-vault`, ...);
- The replayer services:

  - :mod:`swh.storage.replay` service (part of the :ref:`swh-storage`
    package)
  - :mod:`swh.objstorage.replayer.replay` service (from the
    :ref:`swh-objstorage-replayer` package)

Each service consists in an HTTP-based RPC served by a `gunicorn
<https://gunicorn.org/>`_ `WSGI
<https://fr.wikipedia.org/wiki/Web_Server_Gateway_Interface>`_ server.

Docker-based deployment
-----------------------

This represents a lot of services to configure and orchestrate. In order to
help to start the configuration of a mirror, a `docker-swarm
<https://docs.docker.com/engine/swarm/>`_ based deployment solution is provided
as a working example of the mirror stack:

  https://gitlab.softwareheritage.org/swh/infra/swh-mirror

It is strongly recommended to :ref:`start from there <mirror_docker>` in a test
environment before planning a production-like deployment.

.. toctree::
   :titlesonly:
   :hidden:

   docker
