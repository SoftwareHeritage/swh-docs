.. _mirror_docker:

Deploy a Software Heritage stack with docker deploy
===================================================

.. admonition:: Intended audience
   :class: important

   mirror operators

Prerequisites
-------------

We assume that you have a properly set up docker swarm cluster with support for
the `docker stack deploy
<https://docs.docker.com/engine/reference/commandline/stack_deploy/>`_ command,
e.g.:

.. code-block:: console

   swh:~/swh-mirror$ docker node ls
   ID                            HOSTNAME  STATUS   AVAILABILITY  MANAGER STATUS  ENGINE VERSION
   py47518uzdb94y2sb5yjurj22     host2     Ready    Active                        18.09.7
   n9mfw08gys0dmvg5j2bb4j2m7 *   host1     Ready    Active        Leader          18.09.7


Note: on some systems (centos for example), making docker swarm work requires some
permission tuning regarding the firewall and selinux. Please refer to `the upstream
docker-swarm documentation <https://docs.docker.com/engine/swarm/swarm-tutorial/>`_.
Deploying a docker swarm cluster on top of LXC/LXD has also been proven to be difficult.

.. warning:: Check your docker setup with a simple example

             Make sure your docker swarm environment is working properly
             **before** doing any of the following steps. You should check you
             can deploy a simple 2 services properly.

             For example:

             $ docker service create --name web --publish 8080:80 nginx
             $ curl 127.0.0.1:8080
             <!DOCTYPE html>
             <html>
             <head>
             <title>Welcome to nginx!</title>
             <style>
             html { color-scheme: light dark; }
             body { width: 35em; margin: 0 auto;
             font-family: Tahoma, Verdana, Arial, sans-serif; }
             </style>
             </head>
             <body>
             <h1>Welcome to nginx!</h1>
             <p>If you see this page, the nginx web server is successfully installed and
             working. Further configuration is required.</p>

             <p>For online documentation and support please refer to
             <a href="http://nginx.org/">nginx.org</a>.<br/>
             Commercial support is available at
             <a href="http://nginx.com/">nginx.com</a>.</p>

             <p><em>Thank you for using nginx.</em></p>
             </body>
             </html>
             $ docker service rm web

             Note: this will not ensure everything is OK (especially,
             inter-service communication is not tested in this simple
             scenario). You may want to validate that as well.

.. warning:: It is advisable to be able to run the ``docker`` command directly,
             without using ``sudo``; using docker via sudo may have side
             effects, especially regarding usage of environment variables. On a
             debian system, your user account should be in the ``docker``
             group.

In the following how-to, we will assume that the service ``STACK`` name is ``swh``
(this name is the last argument of the :command:`docker stack deploy` command below).

Several preparation steps will depend on this name.

We also use `docker-compose <https://github.com/docker/compose>`_ to merge compose
files, so make sure it is available on your system.

You also need to clone the git repository:

  https://gitlab.softwareheritage.org/swh/infra/swh-mirror.git


Set up volumes
--------------

Before starting the ``swh`` service, you will certainly want to specify where the
data should be stored on your docker hosts.

By default docker will use docker volumes for storing databases and the content of
the objstorage (thus put them in :file:`/var/lib/docker/volumes`).

**Optional:** if you want to specify a different location to put the data in,
you should create the docker volumes before starting the docker service. For
example, the ``objstorage`` service uses a volume named ``<STACK>_objstorage``:

.. code-block:: console

   swh:~/swh-mirror$ docker volume create -d local \
     --opt type=none \
     --opt o=bind \
     --opt device=/data/docker/swh-objstorage \
     swh_objstorage


If you want to deploy services like the ``objstorage`` on several hosts, you will need a
shared storage area in which blob objects will be stored. Typically a NFS storage can be
used for this, or any existing docker volume driver like `REX-Ray
<https://rexray.readthedocs.io/>`_. This is not covered in this documentation.

Please read the documentation of docker volumes to learn how to use such a
device/driver as volume provider for docker.


Node labels
-----------

Note that the provided :file:`base-services.yaml` file has label-based
placement constraints for several services.

The ``elasticsearch``, ``scheduler-db``, ``storage-db``, ``vault-db``,
``web-db``, ``objstorage`` and ``redis`` containers, which depend on the
availability of specific volumes, are pinned to specific nodes using labels
named ``org.softwareheritage.mirror.volumes.<base volume name>`` (e.g.
``org.softwareheritage.mirror.volumes.objstorage``).

When you create a local volume for a given container, you should add the relevant label
to the docker swarm node metadata with:

.. code-block:: console

   swh:~/swh-mirror$ docker node update \
       --label-add org.softwareheritage.mirror.volumes.objstorage=true \
       <node_name>

You have to set the node labels, or to adapt the placement constraints to your local
requirements, for the services to start.

The monitoring services, ``prometheus``, ``prometheus-statsd-exporter`` and
``grafana`` also have placement constraints based on the label
``org.softwareheritage.mirror.monitoring`` (and they also use volumes). So make
sure to add this label to one (and only one) node of the cluster:

.. code-block:: console

   swh:~/swh-mirror$ docker node update \
       --label-add org.softwareheritage.mirror.monitoring=true \
       <node_name>

To check labels defined on a specific node, one can use the ``docker node
inspect`` command:

.. code-block:: console

   swh:~/swh-mirror$ docker node inspect \
       -f '{{ .ID }} [{{ .Description.Hostname}}]: '\
          '{{ range $k, $v := .Spec.Labels }}{{ $k }}={{ $v }} {{end}}' \
       <node_name>

Labels that need to be defined are:

- ``org.softwareheritage.mirror.monitoring=true``: node that will host
  the monitoring services.

- ``org.softwareheritage.mirror.volumes.objstorage=true``: node that will host
  the objstorage service.

- ``org.softwareheritage.mirror.volumes.elasticsearch=true``: node that will
  host the elasticsearch service.

- ``org.softwareheritage.mirror.volumes.redis=true``: node that will host the
  redis service.

- ``org.softwareheritage.mirror.volumes.storage-db=true``: node that will host
  the swh-storage Postgresql database.

- ``org.softwareheritage.mirror.volumes.scheduler-db=true``: node that will
  host the swh-scheduler Postgresql database.

- ``org.softwareheritage.mirror.volumes.vault-db=true``: node that will host
  the swh-vault Postgresql database.

- ``org.softwareheritage.mirror.volumes.web-db=true``: node that will host the
  swh-web Postgresql database.


Managing secrets
----------------

Shared passwords (between services) are managed via :command:`docker secret`. Before
being able to start services, you need to define these secrets.

Namely, you need to create a ``secret`` for:

- ``swh-mirror-db-postgres-password``
- ``swh-mirror-web-postgres-password``

For example:

.. code-block:: console

   swh:~/swh-mirror$ xkcdpass -d- | docker secret create swh-mirror-db-postgres-password -
   [...]


Spawning the swh base services
------------------------------

If you haven't done it yet, clone this git repository:

.. code-block:: console

   swh:~$ git clone https://gitlab.softwareheritage.org/swh/infra/swh-mirror.git
   swh:~$ cd swh-mirror

This repository provides the docker compose/stack manifests to deploy all the relevant
services.

.. note::

   These manifests use a set of docker images `published in the docker hub
   <https://hub.docker.com/r/softwareheritage/base/tags>`_. By default, the manifests
   will use the ``latest`` version of these images, but for production uses, you should
   set the ``SWH_IMAGE_TAG`` environment variable to pin them to a specific version.

To specify the tag to be used, simply set the :envvar:`SWH_IMAGE_TAG`
environment variable:

.. code-block:: console

   swh:~/swh-mirror$ export SWH_IMAGE_TAG=20240417-190717

Make sure you have node labels attributed properly. Then you can spawn the
base services using the following command:

.. code-block:: console

   swh:~/swh-mirror$ docker stack deploy -c mirror.yml swh

   Creating network swh_default
   Creating config swh_content-replayer
   Creating config swh_grafana-provisioning-datasources-prometheus
   Creating config swh_graph-replayer
   Creating config swh_grafana-provisioning-dashboards-all
   Creating config swh_grafana-dashboards-content-replayer
   Creating config swh_grafana-dashboards-backend-stats
   Creating config swh_prometheus
   Creating config swh_prometheus-statsd-exporter
   Creating config swh_storage
   Creating config swh_nginx
   Creating config swh_web
   Creating config swh_grafana-dashboards-graph-replayer
   Creating config swh_objstorage
   Creating service swh_storage
   Creating service swh_redis
   Creating service swh_content-replayer
   Creating service swh_nginx
   Creating service swh_prometheus
   Creating service swh_web
   Creating service swh_prometheus-statsd-exporter
   Creating service swh_db-web
   Creating service swh_objstorage
   Creating service swh_db-storage
   Creating service swh_graph-replayer
   Creating service swh_memcache
   Creating service swh_grafana

   swh:~/swh-mirror$ docker service ls

   ID             NAME                             MODE         REPLICAS               IMAGE                                       PORTS
   ptlhzue025zm   swh_content-replayer             replicated   0/0                    softwareheritage/replayer:20240417-190717
   ycyanvhh0jnt   swh_db-storage                   replicated   1/1 (max 1 per node)   postgres:13
   qlaf9tcyimz7   swh_db-web                       replicated   1/1 (max 1 per node)   postgres:13
   aouw9j8uovr2   swh_grafana                      replicated   1/1 (max 1 per node)   grafana/grafana:latest
   uwqe13udgyqt   swh_graph-replayer               replicated   0/0                    softwareheritage/replayer:20240417-190717
   mepbxllcxctu   swh_memcache                     replicated   1/1                    memcached:latest
   kfzirv0h298h   swh_nginx                        global       3/3                    nginx:latest                                *:5081->5081/tcp
   t7med8frg9pr   swh_objstorage                   replicated   2/2                    softwareheritage/base:20240417-190717
   5s34wzo29ukl   swh_prometheus                   replicated   1/1 (max 1 per node)   prom/prometheus:latest
   rwom7r3yv5ql   swh_prometheus-statsd-exporter   replicated   1/1 (max 1 per node)   prom/statsd-exporter:latest
   wuwydthechea   swh_redis                        replicated   1/1 (max 1 per node)   redis:6.2.6
   jztolbmjp1vi   swh_storage                      replicated   2/2                    softwareheritage/base:20240417-190717
   xxc4c66x0uj1   swh_web                          replicated   1/1                    softwareheritage/web:20240417-190717


This will start a series of containers with:

- an objstorage service,
- a storage service using a postgresql database as backend,
- a web app front end using a postgresql database as backend,
- a memcache for the web app,
- a prometheus monitoring app,
- a prometeus-statsd exporter,
- a grafana server,
- an nginx server serving as reverse proxy for grafana and swh-web.
- a swh_content-replayer service (initially set to 0 replica, see below)
- a swh_graph-replayer service (initially set to 0 replica, see below)
- a redis for the replication error logs,
- a set of services for the vault,
- a set of services for the search (including a single node elasticsearch)

using the pinned version of the docker images.

The nginx frontend will listen on the 5081 port, so you can use:

- http://localhost:5081/ to navigate your local copy of the archive,
- http://localhost:5081/grafana/ to explore the monitoring probes
  (log in with admin/admin).

.. warning::

   Please make sure that the :envvar:`SWH_IMAGE_TAG` variable is properly set for any later
   :command:`docker stack deploy` command you type, otherwise all the running containers will be
   recreated using the ``:latest`` image (which might **not** be the latest available
   version, nor consistent among the docker nodes on your swarm cluster).


Set up the mirroring components
===============================

A Software Heritage mirror consists in base Software Heritage services, as
described above, without any worker related to web scraping nor source code
repository loading. Instead, filling local storage and objstorage is the
responsibility of kafka based ``replayer`` services:

- the ``graph replayer`` which is in charge of filling the storage (aka the
  graph), and

- the ``content replayer`` which is in charge of filling the object storage.

The examples docker deploy file ``mirror.yml`` already define these 2
services, but they are not deployed by default (their ``replicas`` is set to
0). This allows to first deploy core components and check they are properly
started and running.

To start the replayers, first their configuration files need to be adjusted to
your setup.

Edit the provided example files ``conf/graph-replayer.yml`` and
``conf/content-replayer.yml`` to modify fields with an XXX markers with proper
values (also make sure the kafka server list is up to date). The parameters to
check/update are:

- ``journal_client.brokers``: list of kafka brokers.
- ``journal_client.group_id``: unique identifier for this mirroring session;
  you can choose whatever you want, but changing this value will make kafka
  start consuming messages from the beginning; kafka messages are dispatched
  among consumers with the same ``group_id``, so in order to distribute the
  load among workers, they must share the same ``group_id``.
- ``journal_client.sasl.username``: kafka authentication username.
- ``journal_client.sasl.password``: kafka authentication password.

Then you need to update the configuration, as described above:

.. code-block:: console

   swh:~/swh-mirror$ docker config create swh_graph-replayer-2 conf/graph-replayer.yml
   swh:~/swh-mirror$ docker service update \
                   --config-rm swh_graph-replayer \
                   --config-add source=swh_graph-replayer-2,target=/etc/softwareheritage/config.yml \
                   swh_graph-replayer

and

.. code-block:: console

   swh:~/swh-mirror$ docker config create swh_content-replayer-2 conf/content-replayer.yml
   swh:~/swh-mirror$ docker service update \
                   --config-rm swh_content-replayer \
                   --config-add source=swh_content-replayer-2,target=/etc/softwareheritage/config.yml \
                   swh_content-replayer


Graph replayer
--------------

To run the graph replayer component of a mirror is just a matter of scaling its service:

.. code-block:: console

   swh:~/swh-mirror$ docker service scale swh_graph-replayer=1

You can check everything is running with:

.. code-block:: console

   swh:~/swh-mirror$ docker service ps swh_graph-replayer

   ID             NAME                   IMAGE                                       NODE   DESIRED STATE   CURRENT STATE            ERROR     PORTS
   ioyt34ok118a   swh_graph-replayer.1   softwareheritage/replayer:20240417-190717   node1  Running         Running 17 minutes ago


If everything is OK, you should have your mirror filling. Check docker logs:

.. code-block:: console

   swh:~/swh-mirror$ docker service logs swh_graph-replayer
   [...]

or:

.. code-block:: console

   swh:~/swh-mirror$ docker service logs --tail 100 --follow swh_graph-replayer
   [...]


Content replayer
----------------

Similarly, to run the content replayer:

.. code-block:: console

   swh:~/swh-mirror$ docker service scale swh_content-replayer=1


Updating a running stack
========================

Updating a configuration
------------------------

Configuration files are exposed to docker services via the :command:`docker config`
system. Unfortunately, docker does not support updating these config
objects. The usual method to update a config in a service is:

- create a new config entry with updated config content,
- update targeted running services to replace the original config entry by the new one,
- destroy old (now unused) docker config objects.

For example, if you edit the file :file:`conf/storage.yml`:

.. code-block:: console

   swh:~/swh-mirror$ docker config create storage-2 conf/storage.yml
   h0m8jvsacvpl71zdcq3wnud6c
   swh:~/swh-mirror$ docker service update \
                   --config-rm storage \
                   --config-add source=storage-2,target=/etc/softwareheritage/config.yml \
                   swh_storage
   swh_storage
   overall progress: 2 out of 2 tasks
   verify: Service converged
   swh:~/swh-mirror$ docker config rm storage

.. Warning:: this procedure will update the live configuration of the service
             stack, which will then be out of sync with the stack described in
             the compose file used to create the stack. This needs to be kept
             in mind if you try to apply the stack configuration using
             :command:`docker stack deploy` later on. However if you destroy
             the unused config entry as suggested above, an execution of the
             :command:`docker stack deploy` will not break anything (just recreate
             containers) since it will recreate original config object with the
             proper content.

See https://docs.docker.com/engine/swarm/configs/ for more details on
how to use the config system in a docker swarm cluster.


Note that the :command:`docker service update` command can be used for many other
things, for example it can be used to change the debug level of a service:

.. code-block:: console

   swh:~/swh-mirror$ docker service update --env-add LOG_LEVEL=DEBUG swh_storage

Then you can revert to the previous setup using:

.. code-block:: console

   swh:~/swh-mirror$ docker service update --rollback swh_storage

See the documentation of the `swh service update
<https://docs.docker.com/engine/reference/commandline/service_update/>`_
command for more details.

Updating an image
-----------------

When a new version of the softwareheritage image is published, running
services must updated to use it.

In order to prevent inconsistency caveats due to dependency in deployed
versions, we recommend that you deploy the new image on all running
services at once.

This can be done as follow:

.. code-block:: console

   swh:~/swh-mirror$ export SWH_IMAGE_TAG=<new version>
   swh:~/swh-mirror$ docker stack deploy -c base-services.yml swh


Note that this will reset the replicas config to their default values.

If you want to update only a specific service, you can also use (here for a
replayer service):

.. code-block:: console

   swh:~/swh-mirror$ docker service update --image \
          softwareheritage/replayer:${SWH_IMAGE_TAG} \
          swh_graph-replayer

.. warning::

   Updating the image of a storage service may come with a database migration
   script. So we strongly recommend you scale the service back to one before
   updating the image:

   .. code-block:: console

          swh:~/swh-mirror$ docker service scale swh_storage=1
          swh:~/swh-mirror$ docker service update --image \
          softwareheritage/base:${SWH_IMAGE_TAG} \
          swh_storage
          swh:~/swh-mirror$ docker service scale swh_storage=16


Deploy a mirror using a Cassandra backend for the storage
=========================================================

The section above describe the default test deployment of the mirror stack in
which the `swh-storage` service is using Postgresql as backend storage. This is
the simplest and easiest solution to try a full mirror deployment. However
mirror operators may chose to use a Cassandra cluster instead of Postgresql as
storage backend.

The example deployment stack comes with an example of such de configuration
set. It consists in a dedicated `mirror_cassandra.yml` stack file and is mostly
identical to the process described above. Differences are:

- there is no ``storage-db`` service (postgresql instance used as backend for
  the ``swh-storage`` service)
- there 3 instances of a ``cassandra-seed`` service making a 3-nodes Cassandra
  cluster,
- the configuration file for the ``swh-storage``
  (``conf/storage-cassandra.yml``) is modified accordingly.


As a consequence, trying a Cassandra based mirror deployment is a matter of:

.. code-block:: console

   swh:~/swh-mirror$ docker stack deploy -c mirror-cassandra.yml swh


.. warning::

   In this configuration:

   - the Cassandra cluster is deployed within the docker stack,

   - it is a very basic Cassandra deploymet which is by no mean intended for
     production-like deployment, merely a simple way to have a working setup
     for testing purpose,

   - there is no authentication to access the Cassandra cluster.


A more realistic deployment would probably depend on an existing IT operated
Cassandra cluster.


Getting your deployment production-ready
========================================

docker-stack scaling
--------------------

Once the replayer services have been checked, started and are working
properly, you can increase the replication to speed up the replication process.

.. code-block:: console

   swh:~/swh-mirror$ docker service scale swh_graph-replayer=64
   swh:~/swh-mirror$ docker service scale swh_content-replayer=64

A proper replication factor value will depend on your infrastructure
capabilities and needs to be adjusted watching the load of the core services
(mainly the swh_storage-db and swh_objstorage services).

Acceptable range should be between 32 to 64 (for staging) or 256 (for production).

Note that when you increase the replication of the replayers, you also need to
increase the replication factor for the core services ``swh_storage`` and
``swh_objstorage`` otherwise they will become the limiting factor of the replaying
process. A factor of 4 between the number of replayer of a type (graph,
content) and the backend service (swh_storage, swh_objstorage) is probably a
good starting point (i.e. have at least one core service for 4 replayer
services). You may have to play a bit with these values to find the right balance.

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

When using The overall throughput of the mirroring process will depend heavily
on the ``swh_storage`` service, and on the performance of the underlying
``storage-db`` database or ``cassandra`` cluster. You will need to make sure
that your database is `properly tuned
<https://wiki.postgresql.org/wiki/Tuning_Your_PostgreSQL_Server>`_ (if relevant).

You may also want to deploy your database or cassandra cluster directly to
bare-metal servers rather than have it managed within the docker stack. To do
so, you will have to:

.. tab-set::

  .. tab-item:: Postgresql

     - modify the configuration of the docker stack to drop references to the
       ``db-storage`` service (itself, and as dependency for the ``storage`` service)
     - ensure that docker containers deployed in your swarm are able to connect to your
       external database server
     - override the environment variables of the ``storage`` service to
       reference the external database server and db name (namely ``PGHOST_0``,
       ``PGUSER_0`` and ``POSTGRESQL_DB_0``) in the
       ``mirror.yml:services/storage/environment`` section,
     - ensure the db password for the user ``PGUSER_0`` is defined using
       ``docker secret`` for ``swh-mirror-db-postgres-password`` (as described
       above).

  .. tab-item:: Cassandra

     - modify the configuration of the docker stack to drop references to the
       ``cassandra-seed`` services in the ``mirror-cassandra.yml``
     - ensure that docker containers deployed in your swarm are able to connect to your
       external cassandra cluster
     - override the environment variables of the ``storage`` service to
       reference the external cassandra cluster (namely the ``CASSANDRA_SEEDS``
       environment variable in the
       ``mirror-cassandra.yml:services/storage/environment`` section; this is a
       comma-separated list of the Cassandra seed nodes).
     - modify the configuration file ``conf/storage-cassandra.yml`` to properly
       configure the ``hosts`` section with the same list of cassndra seed
       nodes as above.
     - this deployment stack does not yet support specifying the Casssandra
       access password using ``docker secret`` so you need to put the proper
       credentials in the ``conf/storage-cassandra.yml`` file. An example
       configuration file ``conf/storage-cassandra.yml.example`` is given as a
       starting point for this.



Operational concerns for the monitoring
---------------------------------------

You may want to use a prometheus server running directly on one of the docker
swarm nodes so that it can easily also monitor the swarm cluster itself and the
running docker services.

See the `prometheus guide <https://prometheus.io/docs/guides/dockerswarm>`_ on
how to configure a Prometheus server to monitor a docker swarm cluster.

In this case, the ``prometheus`` service should be removed from the docker
deploy compose file, and the configuration files should be updated accordingly.
You would probably want to move ``grafana`` from the docker swarm, and rework
the ``prometheus-statsd-exporter`` node setup accordingly.
