.. _mirror_docker:

Deploy a Software Heritage stack with docker deploy
===================================================

.. admonition:: Intended audience
   :class: important

   mirror operators

Prerequisities
--------------

We assume that you have a properly set up docker swarm cluster with support for
the `docker stack deploy
<https://docs.docker.com/engine/reference/commandline/stack_deploy/>`_ command,
e.g.:

.. code-block:: bash

   ~/swh-docker$ docker node ls
   ID                            HOSTNAME  STATUS   AVAILABILITY  MANAGER STATUS  ENGINE VERSION
   py47518uzdb94y2sb5yjurj22     host2     Ready    Active                        18.09.7
   n9mfw08gys0dmvg5j2bb4j2m7 *   host1     Ready    Active        Leader          18.09.7


Note: on some systems (centos for example), making docker swarm work requires some
permission tuning regarding the firewall and selinux. Please refer to `the upstream
docker-swarm documentation <https://docs.docker.com/engine/swarm/swarm-tutorial/>`_.

In the following how-to, we will assume that the service `STACK` name is `swh`
(this name is the last argument of the `docker stack deploy` command below).

Several preparation steps will depend on this name.

We also use `docker-compose <https://github.com/docker/compose>`_ to merge compose
files, so make sure it is available on your system.

You also need to clone the git  repository:

  https://forge.softwareheritage.org/source/swh-docker


Set up volumes
--------------

Before starting the `swh` service, you will certainly want to specify where the
data should be stored on your docker hosts.

By default docker will use docker volumes for storing databases and the content of
the objstorage (thus put them in `/var/lib/docker/volumes`).

**Optional:** if you want to specify a different location to put the data in,
you should create the docker volumes before starting the docker service. For
example, the `objstorage` service uses a volume named `<STACK>_objstorage`:

.. code-block:: bash

   ~/swh-docker$ docker volume create -d local \
     --opt type=none \
     --opt o=bind \
     --opt device=/data/docker/swh-objstorage \
     swh_objstorage


If you want to deploy services like the `objstorage` on several hosts, you will need a
shared storage area in which blob objects will be stored. Typically a NFS storage can be
used for this, or any existing docker volume driver like `REX-Ray
<https://rexray.readthedocs.io/>`_. This is not covered in this documentation.

Please read the documentation of docker volumes to learn how to use such a
device/driver as volume provider for docker.

Note that the provided `base-services.yaml` file has placement constraints for the
`db-storage`, `db-web` and `objstorage` containers, that depend on the availability of
specific volumes (respectively `<STACK>_storage-db`, `<STACK>_web-db` and
`<STACK>_objstorage`). These services are pinned to specific nodes using labels named
`org.softwareheritage.mirror.volumes.<base volume name>` (e.g.
`org.softwareheritage.mirror.volumes.objstorage`).

When you create a local volume for a given container, you should add the relevant label
to the docker swarm node metadata with:

.. code-block:: bash

   docker node update \
       --label-add org.softwareheritage.mirror.volumes.objstorage=true \
       <node_name>

You have to set the node labels, or to adapt the placement constraints to your local
requirements, for the services to start.

Managing secrets
----------------

Shared passwords (between services) are managed via `docker secret`. Before
being able to start services, you need to define these secrets.

Namely, you need to create a `secret` for:

- `swh-mirror-db-postgres-password`
- `swh-mirror-web-postgres-password`

For example:

.. code-block:: bash

   ~/swh-docker$ xkcdpass -d- | docker secret create swh-mirror-db-postgres-password -
   [...]


Spawning the swh base services
------------------------------

If you haven't done it yet, clone this git repository:

.. code-block:: bash

   ~$ git clone https://forge.softwareheritage.org/source/swh-docker.git
   ~$ cd swh-docker

This repository provides the docker compose/stack manifests to deploy all the relevant
services.

.. note::

   These manifests use a set of docker images `published in the docker hub
   <https://hub.docker.com/r/softwareheritage/base/tags>`_. By default, the manifests
   will use the `latest` version of these images, but for production uses, you should
   set the `SWH_IMAGE_TAG` environment variable to pin them to a specific version.

To specify the tag to be used, simply set the SWH_IMAGE_TAG environment variable, like
so:

.. code-block:: bash

   ~/swh-docker$ export SWH_IMAGE_TAG=20211022-121751

You can then spawn the base services using the following command:

.. code-block:: bash

   ~/swh-docker$ docker stack deploy -c base-services.yml swh

   Creating network swh_default
   Creating config swh_storage
   Creating config swh_objstorage
   Creating config swh_nginx
   Creating config swh_web
   Creating service swh_grafana
   Creating service swh_prometheus-statsd-exporter
   Creating service swh_web
   Creating service swh_objstorage
   Creating service swh_db-storage
   Creating service swh_memcache
   Creating service swh_storage
   Creating service swh_nginx
   Creating service swh_prometheus

   ~/swh-docker$ docker service ls

   ID             NAME                             MODE         REPLICAS   IMAGE                                       PORTS
   tc93talbe2tg   swh_db-storage                   global       1/1        postgres:13
   42q5jtxsh029   swh_db-web                       global       1/1        postgres:13
   rtlz62ok6s96   swh_grafana                      replicated   1/1        grafana/grafana:latest
   jao3rt0et17n   swh_memcache                     replicated   1/1        memcached:latest
   rulxakqgu2ko   swh_nginx                        replicated   1/1        nginx:latest                                *:5081->5081/tcp
   q560pvw3q3ls   swh_objstorage                   replicated   2/2        softwareheritage/base:20211022-121751
   a2h3ltaqdt56   swh_prometheus                   global       1/1        prom/prometheus:latest
   lm24et9gjn2k   swh_prometheus-statsd-exporter   replicated   1/1        prom/statsd-exporter:latest
   gwqinrao5win   swh_storage                      replicated   2/2        softwareheritage/base:20211022-121751
   7g46blmphfb4   swh_web                          replicated   1/1        softwareheritage/web:20211022-121751


This will start a series of containers with:

- an objstorage service,
- a storage service using a postgresql database as backend,
- a web app front end using a postgresql database as backend,
- a memcache for the web app,
- a prometheus monitoring app,
- a prometeus-statsd exporter,
- a grafana server,
- an nginx server serving as reverse proxy for grafana and swh-web.

using the pinned version of the docker images.

The nginx frontend will listen on the 5081 port, so you can use:

- http://localhost:5081/ to navigate your local copy of the archive,
- http://localhost:5081/grafana/ to explore the monitoring probes
  (log in with admin/admin).

.. warning::

   Please make sure that the `SWH_IMAGE_TAG` variable is properly set for any later
   `docker stack deploy` command you type, otherwise all the running containers will be
   recreated using the ':latest' image (which might **not** be the latest available
   version, nor consistent among the docker nodes on your swarm cluster).

Updating a configuration
------------------------

Configuration files are exposed to docker services via the `docker
config` system. Unfortunately, docker does not support updating these config
objects, so you will need to either:

- destroy the old config before being able to recreate them. That also means
  you need to recreate every docker service using this config, or
- adapt the `name:` field in the compose file.


For example, if you edit the file `conf/storage.yml`:

.. code-block:: bash

   ~/swh-docker$ docker service rm swh_storage
   swh_storage
   ~/swh-docker$ docker config rm swh_storage
   swh_storage
   ~/swh-docker$ docker stack deploy -c base-services.yml swh
   Creating config swh_storage
   Creating service swh_storage
   Updating service swh_nginx (id: l52hxxl61ijjxnj9wg6ddpaef)
   Updating service swh_memcache (id: 2ujcw3dg8f9dm4r6qmgy0sb1e)
   Updating service swh_db-storage (id: bkn2bmnapx7wgvwxepume71k1)
   Updating service swh_web (id: 7sm6g5ecff1979t0jd3dmsvwz)
   Updating service swh_objstorage (id: 3okk2njpbopxso3n3w44ydyf9)
   [...]


Note: since persistent data (databases and objects) are stored in volumes, you
can safely destoy and recreate any container you want, you will not lose any
data.

Or you can change the compose file like:

.. code-block:: yaml

   [...]
   configs:
     storage:
       file: conf/storage.yml
       name: storage-updated  # change this as desired


then it's just a matter of redeploying the stack:

.. code-block:: bash

   ~/swh-docker$ docker stack deploy -c base-services.yml swh
   [...]


See https://docs.docker.com/engine/swarm/configs/ for more details on
how to use the config system in a docker swarm cluster.

See https://blog.sunekeller.dk/2019/01/docker-stack-deploy-update-configs/ for
an example of scripting this second solution.


Updating a service
------------------

When a new version of the softwareheritage image is published, running
services must updated to use it.

In order to prevent inconsistency caveats due to dependency in deployed
versions, we recommend that you deploy the new image on all running
services at once.

This can be done as follow:

.. code-block:: bash

   ~/swh-docker$ export SWH_IMAGE_TAG=<new version>
   ~/swh-docker$ docker stack deploy -c base-services.yml swh


Note that this will reset the replicas config to their default values.


If you want to update only a specific service, you can also use (here for a
replayer service):

.. code-block:: bash

   ~/swh-docker$ docker service update --image \
          softwareheritage/replayer:${SWH_IMAGE_TAG} \
          swh_graph-replayer


Set up the mirroring components
===============================

A Software Heritage mirror consists in base Software Heritage services, as
described above, without any worker related to web scraping nor source code
repository loading. Instead, filling local storage and objstorage is the
responsibility of kafka based `replayer` services:

- the `graph replayer` which is in charge of filling the storage (aka the
  graph), and

- the `content replayer` which is in charge of filling the object storage.

Examples of docker deploy files and configuration files are provided in
the `graph-replayer.yml` deploy file for replayer services
using configuration from yaml files in `conf/graph-replayer.yml`.

Copy these example files as plain yaml ones then modify them to replace
the XXX markers with proper values (also make sure the kafka server list
is up to date). The parameters to check/update are:

- `journal_client.brokers`: list of kafka brokers.
- `journal_client.group_id`: unique identifier for this mirroring session;
  you can choose whatever you want, but changing this value will make kafka
  start consuming messages from the beginning; kafka messages are dispatched
  among consumers with the same `group_id`, so in order to distribute the
  load among workers, they must share the same `group_id`.
- `journal_client."sasl.username"`: kafka authentication username.
- `journal_client."sasl.password"`: kafka authentication password.

Then you need to merge the compose files "by hand" (due to this still
`unresolved <https://github.com/docker/cli/issues/1651>`_
`bugs <https://github.com/docker/cli/issues/1582>`_). For this we will use
`docker compose <https://github.com/docker/compose>`_ as helper tool to merge the
compose files.

To merge 2 (or more) compose files together, typically `base-services.yml` with
a mirror-related file:

.. code-block:: bash

   ~/swh-docker$ docker-compose \
       -f base-services.yml \
       -f graph-replayer-override.yml \
       config > mirror.yml


Then use this generated file as argument of the `docker stack deploy` command, e.g.:

.. code-block:: bash

   ~/swh-docker$ docker stack deploy -c mirror.yml swh


Graph replayer
--------------

To run the graph replayer component of a mirror:

.. code-block:: bash

   ~/swh-docker$ cd conf
   ~/swh-docker/conf$ cp graph-replayer.yml.example graph-replayer.yml
   ~/swh-docker/conf$ $EDITOR graph-replayer.yml
   ~/swh-docker/conf$ cd ..


Once you have properly edited the `conf/graph-replayer.yml` config file, you can
start these services with:

.. code-block:: bash

   ~/swh-docker$ docker-compose \
       -f base-services.yml \
       -f graph-replayer-override.yml \
       config > stack-with-graph-replayer.yml
   ~/swh-docker$ docker stack deploy \
       -c stack-with-graph-replayer.yml \
       swh
   [...]

You can check everything is running with:

.. code-block:: bash

   ~/swh-docker$ docker stack ls

   NAME         SERVICES            ORCHESTRATOR
   swh          11                  Swarm

   ~/swh-docker$ docker service ls

   ID             NAME                             MODE         REPLICAS   IMAGE                                       PORTS
   tc93talbe2tg   swh_db-storage                   global       1/1        postgres:13
   42q5jtxsh029   swh_db-web                       global       1/1        postgres:13
   rtlz62ok6s96   swh_grafana                      replicated   1/1        grafana/grafana:latest
   7hvn66um77wr   swh_graph-replayer               replicated   4/4        softwareheritage/replayer:20211022-121751
   jao3rt0et17n   swh_memcache                     replicated   1/1        memcached:latest
   rulxakqgu2ko   swh_nginx                        replicated   1/1        nginx:latest                                *:5081->5081/tcp
   q560pvw3q3ls   swh_objstorage                   replicated   2/2        softwareheritage/base:20211022-121751
   a2h3ltaqdt56   swh_prometheus                   global       1/1        prom/prometheus:latest
   lm24et9gjn2k   swh_prometheus-statsd-exporter   replicated   1/1        prom/statsd-exporter:latest
   gwqinrao5win   swh_storage                      replicated   2/2        softwareheritage/base:20211022-121751
   7g46blmphfb4   swh_web                          replicated   1/1        softwareheritage/web:20211022-121751


If everything is OK, you should have your mirror filling. Check docker logs:

.. code-block:: bash

   ~/swh-docker$ docker service logs swh_graph-replayer
   [...]

or:

.. code-block:: bash

   ~/swh-docker$ docker service logs --tail 100 --follow swh_graph-replayer
   [...]


Content replayer
----------------

Similarly, to run the content replayer:

.. code-block:: bash

   ~/swh-docker$ cd conf
   ~/swh-docker/conf$ cp content-replayer.yml.example content-replayer.yml
   ~/swh-docker/conf$ # edit content-replayer.yml files
   ~/swh-docker/conf$ cd ..


Once you have properly edited the `conf/content-replayer.yml` config file, you can
start these services with:

.. code-block:: bash

   ~/swh-docker$ docker-compose \
       -f base-services.yml \
       -f content-replayer-override.yml \
       config > content-replayer.yml
   ~/swh-docker$ docker stack deploy \
       -c content-replayer.yml \
       swh
   [...]


Full mirror
-----------

Putting all together is just a matter of merging the 3 compose files:

.. code-block:: bash

   ~/swh-docker$ docker-compose \
       -f base-services.yml \
       -f graph-replayer-override.yml \
       -f content-replayer-override.yml \
       config > mirror.yml
   ~/swh-docker$ docker stack deploy \
       -c mirror.yml \
       swh
   [...]


Getting your deployment production-ready
========================================

docker-stack scaling
--------------------

In order to scale up a replayer service, you can use the `docker scale` command. For example:

.. code-block:: bash

   ~/swh-docker$ docker service scale swh_graph-replayer=4
   [...]


will start 4 copies of the graph replayer service.

Notes on the throughput of the mirroring process
------------------------------------------------

- One graph replayer service requires a steady 500MB to 1GB of RAM to run, so
  make sure you have properly sized machines for running these replayer
  containers, and to monitor these.

- The graph replayer containers will require sufficient network bandwidth for the kafka
  traffic (this can easily peak to several hundreds of megabits per second, and the
  total volume of data fetched will be multiple tens of terabytes).

- The biggest kafka topics are directory, revision and content, and will take the
  longest to initially replay.

Operational concerns for the Storage database
---------------------------------------------

The overall throughput of the mirroring process will depend heavily on the `swh_storage`
service, and on the performance of the underlying `swh_db-storage` database. You will
need to make sure that your database is `properly tuned
<https://wiki.postgresql.org/wiki/Tuning_Your_PostgreSQL_Server>`_.

You may also want to deploy your database directly to a bare-metal server rather than
have it managed within the docker stack. To do so, you will have to:

- modify the (merged) configuration of the docker stack to drop references to the
  `db-storage` service (itself, and as dependency for the `storage` service)
- ensure that docker containers deployed in your swarm are able to connect to your
  external database server
- override the environment variables of the `storage` service to reference the external
  database server and dbname
