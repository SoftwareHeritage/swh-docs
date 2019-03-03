.. highlight:: bash

.. _getting-started:

Run your own Software Heritage
==============================

This tutorial will guide from the basic step of obtaining the source code of
the Software Heritage stack to running a local copy of it with which you can
archive source code and browse it on the web. To that end, just follow the
steps detailed below.


Using Docker
++++++++++++

The easiest way to run a Software Heritage instance is to use Docker and
docker-compose. Please refer to the `docker-compose documentation
<https://docs.docker.com/compose/>`_ if you do not have a working docker setup.

Then::

  git clone https://forge.softwareheritage.org/source/swh-docker-dev.git
  cd swh-docker-dev
  docker-compose up -d

When all the containers are up and running, you have a running Software
Heritage platform. You should open:

- http://localhost:5080/ to navigate your (empty for now) SWH archive,
- http://localhost:5080/rabbitmq to access the rabbitmq dashboard (guest/guest),
- http://localhost:5080/prometheus to explore the platform's metrics,

All the internal APIs are also exposed:

- http://localhost:5080/scheduler
- http://localhost:5080/storage
- http://localhost:5080/indexer-storage
- http://localhost:5080/deposit
- http://localhost:5080/objstorage

At this point, the simplest way to start indexing software is to use the 'Save
Code Now' feature of the archive web interface:

  http://localhost:5080/browse/origin/save/

Enjoy filling your hard drives!


Hacking the archive
+++++++++++++++++++

If you want to hack the code of the Software Heritage Archive, a bit more work
will be required.

The best way to have a development-friendly environment is to build a mixed
docker/virtual env setup.

Such a setup is described in the :ref:`Perfect Developer Setup guide
<developer-setup>`.


Installing from sources (without Docker)
++++++++++++++++++++++++++++++++++++++++

If you prefer to run everything straight, you should refer to the :ref:`Manual
Setup Guide <manual-setup>`
