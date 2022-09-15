.. highlight:: bash

.. _getting-started:

Run your own Software Heritage
==============================

This tutorial will guide from the basic step of obtaining the source code of
the Software Heritage stack to running a local copy of it with which you can
archive source code and browse it on the web. To that end, just follow the
steps detailed below.

.. warning::
   Running a Software Heritage instance on your machine can
   consume quite a bit of resources: if you play a bit too hard (e.g., if
   you try to list all GitHub repositories with the corresponding lister),
   you may fill your hard drive, and consume a lot of CPU, memory and
   network bandwidth.

Dependencies
------------

The easiest way to run a Software Heritage instance is to use Docker.
Please `ensure that you have a working recent installation first
<https://docs.docker.com/engine/install/>`_ (including the
`Compose <https://docs.docker.com/compose/>`_ plugin.

Quick start
-----------

First, retrieve Software Heritage development environment to get the
Docker configuration::

   ~$ git clone https://forge.softwareheritage.org/source/swh-environment.git
   ~$ cd swh-environment/docker

Then, start containers::

   ~/swh-environment/docker$ docker compose up -d
   [...]
   Creating docker_amqp_1               ... done
   Creating docker_zookeeper_1          ... done
   Creating docker_kafka_1              ... done
   Creating docker_flower_1             ... done
   Creating docker_swh-scheduler-db_1   ... done
   [...]

This will build Docker images and run them. Check everything is running
fine with::

   ~/swh-environment/docker$ docker compose ps
                            Name                                       Command               State                                      Ports
   -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
   docker_amqp_1                                    docker-entrypoint.sh rabbi ...   Up      15671/tcp, 0.0.0.0:5018->15672/tcp, 25672/tcp, 4369/tcp, 5671/tcp, 5672/tcp
   docker_flower_1                                  flower --broker=amqp://gue ...   Up      0.0.0.0:5555->5555/tcp
   docker_kafka_1                                   start-kafka.sh                   Up      0.0.0.0:5092->5092/tcp
   docker_swh-deposit-db_1                          docker-entrypoint.sh postgres    Up      5432/tcp
   docker_swh-deposit_1                             /entrypoint.sh                   Up      0.0.0.0:5006->5006/tcp
   [...]

The startup of some containers may fail the first time for
dependency-related problems. If some containers failed to start, just
run the ``docker compose up -d`` command again.

If a container really refuses to start properly, you can check why using
the ``docker compose logs`` command. For example::

   ~/swh-environment/docker$ docker compose logs swh-lister
   Attaching to docker_swh-lister_1
   [...]
   swh-lister_1                      | Processing /src/swh-scheduler
   swh-lister_1                      | Could not install packages due to an EnvironmentError: [('/src/swh-scheduler/.hypothesis/unicodedata/8.0.0/charmap.json.gz', '/tmp/pip-req-build-pm7nsax3/.hypothesis/unicodedata/8.0.0/charmap.json.gz', "[Errno 13] Permission denied: '/src/swh-scheduler/.hypothesis/unicodedata/8.0.0/charmap.json.gz'")]
   swh-lister_1                      |

.. note::

  For details on the various Docker images and how to work with them,
  see the full :ref:`docker-environment` documentation.

Once all containers are running, you can use the web interface by
opening http://localhost:5080/ in your web browser.

At this point, the archive is empty and needs to be filled with some
content. The simplest way to start loading software is to use the
*Save Code Now* feature of the archive web interface:

  http://localhost:5080/browse/origin/save/

You can also use the command line interface to inject code. For
example to retrieve projects hossted on the https://0xacab.org GitLab forge::

   ~/swh-environment/docker$ docker compose exec swh-scheduler \
       swh scheduler task add list-gitlab-full \
         -p oneshot url=https://0xacab.org/api/v4

   Created 1 tasks

   Task 1
     Next run: just now (2018-12-19 14:58:49+00:00)
     Interval: 90 days, 0:00:00
     Type: list-gitlab-full
     Policy: oneshot
     Args:
     Keyword args:
       url=https://0xacab.org/api/v4

This task will scrape the forge’s project list and register origins to the scheduler.
This takes at most a couple of minutes.

Then, you must tell the scheduler to create loading tasks for these origins.
For example, to create tasks for 100 of these origins::

   ~/swh-environment/docker$ docker compose exec swh-scheduler \
       swh scheduler origin schedule-next git 100

This will take a bit of time to complete.

To increase the speed at which git repositories are imported, you can
spawn more ``swh-loader-git`` workers::

   ~/swh-environment/docker$ docker compose exec swh-scheduler \
       celery status
   listers@50ac2185c6c9: OK
   loader@b164f9055637: OK
   indexer@33bc6067a5b8: OK
   vault@c9fef1bbfdc1: OK

   4 nodes online.
   ~/swh-environment/docker$ docker compose exec swh-scheduler \
       celery control pool_grow 3 -d loader@b164f9055637
   -> loader@b164f9055637: OK
           pool will grow
   ~/swh-environment/docker$ docker compose exec swh-scheduler \
       celery inspect -d loader@b164f9055637 stats | grep prefetch_count
          "prefetch_count": 4

Now there are 4 workers ingesting git repositories. You can also
increase the number of ``swh-loader-git`` containers::

   ~/swh-environment/docker$ docker compose up -d --scale swh-loader=4
   [...]
   Creating docker_swh-loader_2        ... done
   Creating docker_swh-loader_3        ... done
   Creating docker_swh-loader_4        ... done


Updating the docker image
-------------------------

All containers started by ``docker compose`` are bound to a docker image
named ``swh/stack`` including all the software components of Software
Heritage. When new versions of these components are released, the docker
image will not be automatically updated. In order to update all Software
Heritage components to their latest version, the docker image needs to
be explicitly rebuilt by issuing the following command from within the
``docker`` directory::

   ~/swh-environment/docker$ docker build --no-cache -t swh/stack .

Monitor your local installation
-------------------------------

You can monitor your local installation by looking at:

- http://localhost:5080/rabbitmq to access the rabbitmq dashboard (guest/guest),
- http://localhost:5080/grafana to explore the platform's metrics (admin/admin),

Shut down your local installation
---------------------------------

To shut down your SoftWare Heritage, just run::

   ~/swh-environment/docker$ docker compose down

Hacking the archive
-------------------

If you want to hack the code of the Software Heritage Archive, a more involved
setup is required described in the :ref:`developer setup
guide <developer-setup>`.
