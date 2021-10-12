.. _mirror_docker:

Deploy a Software Heritage stack with docker deploy
===================================================

Prerequisities
--------------

According you have a properly set up docker swarm cluster with support for the
`docker stack deploy
<https://docs.docker.com/engine/reference/commandline/stack_deploy/>`_ command,
e.g.:

.. code-block:: bash

   ~/swh-docker$ docker node ls
   ID                            HOSTNAME  STATUS   AVAILABILITY  MANAGER STATUS  ENGINE VERSION
   py47518uzdb94y2sb5yjurj22     host2     Ready    Active                        18.09.7
   n9mfw08gys0dmvg5j2bb4j2m7 *   host1     Ready    Active        Leader          18.09.7


Note: on some systems (centos for example), making docker swarm works require
some permission tuning regarding the firewall and selinux.

In the following how-to, we will assume that the service `STACK` name is `swh`
(this name is the last argument of the `docker stack deploy` command below).

Several preparation steps will depend on this name.

We also use [docker-compose](https://github.com/docker/compose) to merge
compose files, so make sure it iavailable on your system.

You also need to clone the git  repository:

  https://forge.softwareheritage.org/source/swh-docker


Set up volumes
--------------

Before starting the `swh` service, you may want to specify where the data
should be stored on your docker hosts.

By default docker will use docker volumes for storing databases and the content of
the objstorage (thus put them in `/var/lib/docker/volumes`).

**Optional:** if you want to specify a different location to put a storage in,
create the storage before starting the docker service. For example for the
`objstorage` service you will need a storage named `<STACK>_objstorage`:

.. code-block:: bash

   ~/swh-docker$ docker volume create -d local \
     --opt type=none \
     --opt o=bind \
     --opt device=/data/docker/swh-objstorage \
     swh_objstorage


If you want to deploy services like the `swh-objstorage` on several hosts, you
will need a shared storage area in which blob objects will be stored. Typically
a NFS storage can be used for this, or any existing docker volume driver like
[REX_Rey](https://rexray.readthedocs.io/). This is not covered in this doc.

Please read the documentation of docker volumes to learn how to use such a
device/driver as volume provider for docker.

Note that the provided `base-services.yaml` file have a few placement
constraints: containers that depends on a volume (db-storage and objstorage)
are stick to the manager node of the cluster, under the assumption persistent
volumes have been created on this node. Make sure this fits your needs, or
amend these placement constraints.


Managing secrets
----------------

Shared passwords (between services) are managed via `docker secret`. Before
being able to start services, you need to define these secrets.

Namely, you need to create a `secret` for:

- `postgres-password`

For example:

.. code-block:: bash

   ~/swh-docker$ echo 'strong password' | docker secret create postgres-password -
   [...]


Creating the swh base services
------------------------------

If you haven't done it yet, clone this git repository:

.. code-block:: bash

   ~$ git clone https://forge.softwareheritage.org/source/swh-docker.git
   ~$ cd swh-docker


then from within this repository, just type:

.. code-block:: bash

   ~/swh-docker$ docker stack deploy -c base-services.yml swh
   Creating network swh-mirror_default
   Creating config swh-mirror_storage
   Creating config swh-mirror_objstorage
   Creating config swh-mirror_nginx
   Creating config swh-mirror_web
   Creating service swh-mirror_grafana
   Creating service swh-mirror_prometheus-statsd-exporter
   Creating service swh-mirror_web
   Creating service swh-mirror_objstorage
   Creating service swh-mirror_db-storage
   Creating service swh-mirror_memcache
   Creating service swh-mirror_storage
   Creating service swh-mirror_nginx
   Creating service swh-mirror_prometheus
   ~/swh-docker$ docker service ls
   ID            NAME                                    MODE        REPLICAS  IMAGE                                   PORTS
   sz98tofpeb3j  swh-mirror_db-storage                   global      1/1       postgres:11
   sp36lbgfd4qi  swh-mirror_grafana                      replicated  1/1       grafana/grafana:latest
   7oja81jngiwo  swh-mirror_memcache                     replicated  1/1       memcached:latest
   y5te0gqs93li  swh-mirror_nginx                        replicated  1/1       nginx:latest                            *:5081->5081/tcp
   79t3r3mv3qn6  swh-mirror_objstorage                   replicated  1/1       softwareheritage/base:20200918-133743
   l7q2zocoyvq6  swh-mirror_prometheus                   global      1/1       prom/prometheus:latest
   p6hnd90qnr79  swh-mirror_prometheus-statsd-exporter   replicated  1/1       prom/statsd-exporter:latest
   jjry62tz3k76  swh-mirror_storage                      replicated  1/1       softwareheritage/base:20200918-133743
   jkkm7qm3awfh  swh-mirror_web                          replicated  1/1       softwareheritage/web:20200918-133743


This will start a series of containers with:

- an objstorage service,
- a storage service using a postgresql database as backend,
- a web app front end,
- a memcache for the web app,
- a prometheus monitoring app,
- a prometeus-statsd exporter,
- a grafana server,
- an nginx server serving as reverse proxy for grafana and swh-web.

using the latest published version of the docker images by default.


The nginx frontend will listen on the 5081 port, so you can use:

- http://localhost:5081/ to navigate your local copy of the archive,
- http://localhost:5081/grafana/ to explore the monitoring probes
  (log in with admin/admin).


>[!WARNING]
>the 'latest' docker images work, it is highly recommended to
>explicitly specify the version of the image you want to use.

Docker images for the Software Heritage stack are tagged with their build date:

.. code-block:: bash

   ~$ docker images -f reference='softwareheritage/*:20*'
   REPOSITORY              TAG                     IMAGE ID            CREATED             SIZE
   softwareheritage        web-20200819-112604     32ab8340e368        About an hour ago   339MB
   softwareheritage        base-20200819-112604    19fe3d7326c5        About an hour ago   242MB
   softwareheritage        web-20200630-115021     65b1869175ab        7 weeks ago         342MB
   softwareheritage        base-20200630-115021    3694e3fcf530        7 weeks ago         245MB

To specify the tag to be used, simply set the SWH_IMAGE_TAG environment variable, like:

.. code-block:: bash

   export SWH_IMAGE_TAG=20200819-112604
   docker deploy -c base-services.yml swh

>[!WARNING]
>make sure to have this variable properly set for any later `docker deploy`
>command you type, otherwise you running containers will be recreated using the
>':latest' image (which might **not** be the latest available version, nor
>consistent amond the docker nodes on you swarm cluster).

Updating a configuration
------------------------

When you modify a configuration file exposed to docker services via the `docker
config` system. Unfortunately, docker does not support updating these config
objects, so you need to either:

- destroy the old config before being able to recreate them. That also means
  you need to recreate every docker container using this config, or
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
can safely destoy and recreate any container you want, you will not loose any
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
          softwareheritage/replayer:${SWH_IMAGE_TAG} ) \
          swh_graph-replayer


Set up a mirror
===============

>[!WARNING] you cannot "upgrade" an existing docker stack built from the
>base-services.yml file to a mirror one; you need to recreate it; more
>precisely, you need to drop the storage database before. This is due to the
>fact the storage database for a mirror is not initialized the same way as
>the default storage database.

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
is up to date.) Parameters to check/update are:

- `journal_client/brokers`: list of kafka brokers.
- `journal_client/group_id`: unique identifier for this mirroring session;
  you can choose whatever you want, but changing this value will make kafka
  start consuming messages from the beginning; kafka messages are dispatched
  among consumers with the same `group_id`, so in order to distribute the
  load among workers, they must share the same `group_id`.
- `journal_client/sasl.username`: kafka authentication username.
- `journal_client/sasl.password`: kafka authentication password.

Then you need to merge the compose files "by hand" (due to this still
[unresolved](https://github.com/docker/cli/issues/1651)
[bugs](https://github.com/docker/cli/issues/1582)). For this we will use
[docker-compose](https://github.com/docker/compose) as helper tool to merge the
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

   ~/swh-docker$ docker stack deploy -c mirror.yml swh-mirror


Graph replayer
--------------

To run the graph replayer compoenent of a mirror:

.. code-block:: bash

   ~/swh-docker$ cd conf
   ~/swh-docker/conf$ cp graph-replayer.yml.example graph-replayer.yml
   ~/swh-docker/conf$ # edit graph-replayer.yml files
   ~/swh-docker/conf$ cd ..


Once you have properly edited the `conf/graph-replayer.yml` config file, you can
start these services with:

.. code-block:: bash

   ~/swh-docker$ docker-composer \
       -f base-services.yml \
       -f graph-replayer-override.yml \
       config > graph-replayer.yml
   ~/swh-docker$ docker stack deploy \
       -c graph-replayer.yml \
       swh-mirror
   [...]

You can check everything is running with:

.. code-block:: bash

   ~/swh-docker$ docker stack ls
   NAME                SERVICES            ORCHESTRATOR
   swh-mirror          11                  Swarm
   ~/swh-docker$ docker service ls
   ID             NAME                                    MODE        REPLICAS  IMAGE                          PORTS
   88djaq3jezjm   swh-mirror_db-storage                   replicated  1/1       postgres:11
   m66q36jb00xm   swh-mirror_grafana                      replicated  1/1       grafana/grafana:latest
   qfsxngh4s2sv   swh-mirror_content-replayer             replicated  1/1       softwareheritage/replayer:latest
   qcl0n3ngr2uv   swh-mirror_graph-replayer               replicated  1/1       softwareheritage/replayer:latest
   zn8dzsron3y7   swh-mirror_memcache                     replicated  1/1       memcached:latest
   wfbvf3yk6t41   swh-mirror_nginx                        replicated  1/1       nginx:latest                   *:5081->5081/tcp
   thtev7o0n6th   swh-mirror_objstorage                   replicated  1/1       softwareheritage/base:latest
   ysgdoqshgd2k   swh-mirror_prometheus                   replicated  1/1       prom/prometheus:latest
   u2mjjl91aebz   swh-mirror_prometheus-statsd-exporter   replicated  1/1       prom/statsd-exporter:latest
   xyf2xgt465ob   swh-mirror_storage                      replicated  1/1       softwareheritage/base:latest
   su8eka2b5cbf   swh-mirror_web                          replicated  1/1       softwareheritage/web:latest


If everything is OK, you should have your mirror filling. Check docker logs:

.. code-block:: bash

   ~/swh-docker$ docker service logs swh-mirror_graph-replayer
   [...]

or:

.. code-block:: bash

   ~/swh-docker$ docker service logs --tail 100 --follow swh-mirror_graph-replayer
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

   ~/swh-docker$ docker-composer \
       -f base-services.yml \
       -f content-replayer-override.yml \
       config > content-replayer.yml
   ~/swh-docker$ docker stack deploy \
       -c content-replayer.yml \
       swh-mirror
   [...]


Full mirror
-----------

Putting all together is just a matter of merging the 3 compose files:

.. code-block:: bash

   ~/swh-docker$ docker-composer \
       -f base-services.yml \
       -f graph-replayer-override.yml \
       -f content-replayer-override.yml \
       config > mirror.yml
   ~/swh-docker$ docker stack deploy \
       -c mirror.yml \
       swh-mirror
   [...]


Scaling up services
-------------------

In order to scale up a replayer service, you can use the `docker scale` command. For example:

.. code-block:: bash

   ~/swh-docker$ docker service scale swh_graph-replayer=4
   [...]


will start 4 copies of the graph replayer service.

Notes:

- One graph replayer service requires a steady 500MB to 1GB of RAM to run, so
  make sure you have properly sized machines for running these replayer
  containers, and to monitor these.

- The overall bandwidth of the replayer will depend heavily on the
  `swh_storage` service, thus on the `swh_db-storage`. It will require some
  network bandwidth for the ingress kafka payload (this can easily peak to
  several hundreds of Mb/s). So make sure you have a correctly tuned database
  and enough network bw.

- Biggest topics are the directory, revision and content.
