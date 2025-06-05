.. _howto-deploy-swh-graph:

How to deploy swh.graph?
========================

.. admonition:: Intended audience
   :class: important

   sysadm staff members

This page describes how to declaratively deploy the graph in production in the
kubernetes environment.

For production, as the dataset is multiple terabytes of files, some manual
intervention can occur to manipulate the zfs datasets.

The compression pipeline (which actually extracts the full dataset) is not yet
documented.

.. _swh-graph-services:

What are the graph services?
----------------------------

It's composed of 2 (kubernetes) deployments, the:

- grpc service which holds the dataset files
- rpc service which relays queries to the grpc backend (they don't have access
  to the dataset files)

.. _swh-graph-where-does-it-run:

Where does the graph services run?
----------------------------------

The graph services runs on kubernetes nodes with label `swh/graph=true`.

How to connect to the graph services?
-------------------------------------

To access it, you need access to the kubernetes cluster targeted
(e.g. next-version, staging, production).

Either use k9s and select the pod `graph-grpc-$version` and then hit `s` to
`shell` into it.

Or use kubectl to connect to the pod.

.. _swh-graph-how-to-install-next-graph-dataset:

How to install the graph dataset?
---------------------------------

Currently, the graph dataset are built on the maxxi machine in dedicated zfs
dataset. That helps in zfs snapshot manipulation.

When the dataset is ready, we need to copy it over on the machine chosen for
running the new graph.

.. code::

   VERSION=2025-04-19
   # On the source machine (maxxi), create a snapshot of the ready dataset
   zfs snapshot ssd/datasets/$VERSION/compressed@snapshot-graph-$VERSION

   # On the target machine, create the dataset that will receive the newly
   # created zfs snapshot
   zfs create data/datasets/$VERSION
   # Then copy the dataset from the source machine (maxxi)
   time ssh root@maxxi zfs send ssd/datasets/$VERSION/compressed@graph-$VERSION | zfs receive data/datasets/$VERSION/compressed

.. code::

   # On the target machine that will run the grpc service
   # Once the copy has been done, we need to mount the zfs dataset
   # And then reference it in the chart value
   MOUNT_DIR="/srv/softwareheritage/ssd/graph/${VERSION}/compressed"
   mkdir -p $MOUNT_DIR
   zfs set mountpoint=$MOUNT_DIR data/datasets/${VERSION}/compressed
   # This will show the graph files
   ls $MOUNT_DIR


Example::

   root@rancher-node-highmem02:~# zfs set mountpoint=$MOUNT_DIR data/datasets/${VERSION}/compressed
   root@rancher-node-highmem02:~# ls $MOUNT_DIR
   graph-labelled.ef                       graph-transposed.graph       graph.labels.fcl.bytearray   graph.offsets                               graph.property.committer_timestamp.bin         graph.pthash.order
   graph-labelled.labeloffsets             graph-transposed.offsets     graph.labels.fcl.pointers    graph.persons.count.txt                     graph.property.committer_timestamp_offset.bin  graph.stats
   graph-labelled.labels                   graph-transposed.properties  graph.labels.fcl.properties  graph.persons.csv.zst                       graph.property.content.is_skipped.bits         logs
   graph-labelled.properties               graph.edges.count.txt        graph.labels.pthash          graph.persons.pthash                        graph.property.content.length.bin              meta
   graph-transposed-labelled.ef            graph.edges.stats.txt        graph.labels.pthash.order    graph.properties                            graph.property.message.bin
   graph-transposed-labelled.labeloffsets  graph.ef                     graph.node2swhid.bin         graph.property.author_id.bin                graph.property.message.offset.bin
   graph-transposed-labelled.labels        graph.graph                  graph.node2type.bin          graph.property.author_timestamp.bin         graph.property.tag_name.bin
   graph-transposed-labelled.properties    graph.labels.count.txt       graph.nodes.count.txt        graph.property.author_timestamp_offset.bin  graph.property.tag_name.offset.bin
   graph-transposed.ef                     graph.labels.csv.zst         graph.nodes.stats.txt        graph.property.committer_id.bin             graph.pthash


.. _swh-graph-deploy-next-graph-version:

How to deploy the next graph version?
-------------------------------------

The graph are running on ``highmemXY`` machines.

Multiple graph versions can run concurrently as long as there are enough disk
space and memory.

The m.o. is:

- Install the new dataset on one of the highmem machines
- Deploy a new gprc and rpc instance running concurrently to the previous
  ones. The grpc service shall be using the newly installed zfs dataset using
  the newly installed dataset. And the new new rpc hitting the new grpc
  service as backend.
- Check everything is fine for those new instances.
- Once the new instances are running ok, switch the "public" ingresses fqdn
  [1] [2] so they target the new instances (grpc & rpc)

The `following merge request
<https://gitlab.softwareheritage.org/swh/infra/ci-cd/swh-charts/-/merge_requests/596>_`
can be used as a reference on how to adapt the swh-charts repository for a new
graph version. Each commit describes what needs to happen in order according
to the previous m.o.

It declares:

- 1 persistent volume (pv) which target where the zfs dataset is mounted
  on the node that will run the grpc service.
- 2 persistent volume claims (pvc):

  - 1 persistent pvc which uses the previous pv to detect where the compresses
    graph files are
  - another in-memory pvc which is in memory for the graph files which will be
    mounted in the node's memory

- 1 grpc service which uses as volumes the 2 previous pvcs to serve the grpc
  queries
- 1 rpc service which uses as backend the grpc service

[1] graph-grpc.internal.softwareheritage.org & graph-grpc-default-ingress

[2] graph-rpc.internal.softwareheritage.org & graph-rpc-default-ingress

.. _swh-graph-post-actions:

Post graph deployment actions
-----------------------------

Decommission previous instance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As mentioned, when the new graph is deployed, we can:

- first decommission the previous graph instance (to avoid unnecessary
  resources consumption, be it disk or memory).
- free the associated zfs dataset which is no longer used (if freeing disk
  space is required)

Clean up record references table in storage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The compressed graph is a snapshot view in time of the main archive. Its
export takes some time to compute.

To avoid heavy computations to compute the differences a-la-demande between
the main archive and the compressed graph (which would be wasteful in time and
resources), we have some references tables stored in cassandra. They keep such
difference between the last graph version running and now (at the expanse of
resources).

When the new graph is deployed, we can clean up those references tables to
reclaim resources.

Connect to the swh-cassandra namespace in a writing workload
(e.g. storage-cassandra-winery or a toolbox) pod and call the cli to cleanup
reference tables. The script to use will prompt your for a response so you can
always abort.

.. code::

   # Ask for removal of the record reference from the most recent graph version
   swh storage remove-old-object-reference-partitions YYYY-MM-DD

Example::

   swh@pod:~$ swh storage remove-old-object-reference-partitions 2025-04-19
   We will remove the following partitions before 2025-04-19:
   - 2024 week 48
   - 2024 week 49
   - 2024 week 50
   - 2024 week 51
   - 2024 week 52
   - 2025 week 01
   - 2025 week 02
   - 2025 week 03
   - 2025 week 04
   - 2025 week 05
   - 2025 week 06
   - 2025 week 07
   - 2025 week 08
   - 2025 week 09
   - 2025 week 10
   - 2025 week 11
   - 2025 week 12
   - 2025 week 13
   - 2025 week 14
   - 2025 week 15
   Do you want to proceed? [y/N]: N
   Aborted!
