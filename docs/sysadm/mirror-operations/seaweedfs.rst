.. _mirror_seaweedfs:

Using seaweedfs as object storage backend
=========================================

When deploying a mirror, one of the key technological choice you have to make
is the backend used for the Software Heritage object storage.

The :ref:`swh-objstorage` module support a variety of backends, one of which is
seaweedfs_.

seaweedfs_ is a SeaweedFS is a fast distributed storage system for blobs,
objects, files, and data lake. It's able to handle billions of files. It comes
with many valuable features that are useful a :ref:`swh-objstorage` backend:

- Distributed architecture; allows to easily grow the objstorage cluster when
  needed.
- Pack small files in big (30GB by default) volumes, implementing the concepts
  behind the Haystack storage system developed by Facebook, preventing space
  amplication problems.
- Support for `Erasure Coding`_, allowing to have data replication at a
  fraction of the cost in terms of storage space.
- Supports asynchronous cross-DC replication.

For seaweedfs to be used as an objstorage backend, it needs:

- one seaweedfs master (ideally at least 3 for HA),
- one seaweedfs filer using a fast key-value store as backend (e.g. leveldb or redis)
- a number of seaweedfs volume servers with enough capacity to store the whole
  Software Heritage Archive object storage (including erasure coding
  replication factor, if used).

The key to achieve good replication performances is to have a good
communication backbone behind the seawwwedfs cluster. At least a properly
configured 10G network is mandatory.

For example, a seaweedfs cluster consisting of 4 bare metal machines hosting
all the seaweedfs components (3x master, 1x filer, 4x volumes), the content
replication process can achieve a steady throughput of 2000 objects/s at about
200MB/s (giving a total replication ETA of about 3 months as of march 2023).

.. _`Erasure Coding`: https://en.wikipedia.org/wiki/Erasure_code


Master
------

The master configuration is pretty straightforward. Typically, you will want to
ensure the following options of the ``weed master`` command are set:

- ``volumePreallocate``: Preallocate disk space for volumes
- ``metrics.address``: Prometheus gateway address

You will also want to have a fair number of writable volumes set up (for good
concurrent write performances); this can be done in the :file:`master.toml`
configuration file:

.. code-block:: ini

   [master.volume_growth]
   copy_1 = 32


This ensure there are always at least 32 volumes used for writing.

See `the SeaweedFS optimization page
<https://github.com/seaweedfs/seaweedfs/wiki/Optimization>`_ for more details.

Having multiple masters is a good idea. The number of masters must be an even
number.

Replication and erasure coding
++++++++++++++++++++++++++++++

Seaweedfs support both replication (keeping multiple copies of each content
object) and erasure coding. The erasure coding implementedin seaweedfs is 10.4
Reed-Solomon Erasure Coding (EC). The large volumes are split into chunks of
1GB, and every 10 data chunks are also encoded into 4 parity chunks. So a 30 GB
data volume will be encoded into 14 EC shards, each shard is of size 3 GB and
has 3 EC blocks. This allows loss of 4 shards of data with 1.4x data size.
Compared to replicating data 5 times to achieve the same robustness, it saves
3.6x disk space.

Erasure Coding is only activated for warm storage, i.e. storage volumes that
are sealed (almost full, not part of the active volumes in which new writes are
done, and have not been modified for a while).

As such, performing the EC processing is a asynchronous background process
initiated by the master. It is typically set up using this piece of
:file:`master.toml` configuration:

.. code-block:: ini

   [master.maintenance]
   # periodically run these scripts are the same as running them from 'weed shell'
   scripts = """
     ec.encode -fullPercent=95 -quietFor=1h
     ec.rebuild -force
     ec.balance -force
   """
   sleep_minutes = 17          # sleep minutes between each script execution


For replication, you can choose between different replication strategies:
number of copies, placement constraints for copies (server, rack, datacenter);
see `the documentation
<https://github.com/seaweedfs/seaweedfs/wiki/Replication>`_ for more details.


Filer
-----

The filer is the component used to make the link between the way objects are
identified in software heritage (using the hash of the object as identifier)
and the location of the objects (as well as a few other metadata entries) in a
seaweedfs volume.

This is a rather simple key/value store. Seaweedfs filer actually uses an
existing k/v store as backend. By default, it will use a local leveldb store,
putting all the objects in a flat namespace. This works ok up to a few billions
of objects, but it might be a good idea to organize the filer a bit.

When using leveldb as backend k/v store, the volume needed to index the whole
|swh| archive objstorage is about 2TB (as of March 2023).

Multi-filer deployment
++++++++++++++++++++++

seaweedfs filer does support for multiple filers. When using a
shared/distributed k/v store as backend (redis, postgresql, cassandra, HBase,
etc.), the filer itself is stateless so it's easy to deploy several filer
instances. But Seaweedfs also support parallel filers with embedded filer store
(e.g. leveldb). But in this case, the asynchronous and eventually consistent
nature of the replication process between the different filer instances makes
it not suitable for the |swh| objstorage mirroring workload.

It's however possible to use several filer instances (for HA or load balancing)
when using a shared or distributed k/v store as backend (typically redis).

Note that using a multiple filers with embedded filer store (leveldb) remains
possible as a HA or backupping solution; as long as all the content replayers
do target the same filer instance for writing objects, it should be fine. Doing
so, the filer is (eventually) replicated and the behavior of the replication
process remains consistent.

Note that a single leveldb filer can support up to 2000 object insertions / sec
(with fast SSD storage).

Using Redis as filer store
++++++++++++++++++++++++++

For a |swh| mirror deployment, it is probably a good idea to go with a solution
based on a shared filer store (redis should be the best choice to ensure good
performances during the replication process).

However there is a small catch: a redis filer (``redis2``) store won't be able to
handle having all the |swh| content entries in a single (flat) directory.

Seaweedfs provides an alternate redis backend implementation, ``redis3``, that
can circumvent this issue. This comes at the cost of slightly slower
insertions.

Another approach is to configure the |swh| ``seaweedfs`` objstorage to use a
slicer: this will organize the objects in a directory structure built from the
object hash. For example, using this |swh| objstorage configuration:

.. code-block:: yaml

   objstorage_dst:
   cls: seaweedfs
   compression: none
   url: http://localhost:8088/swh/
   slicing: "0:2/2:4"

will organize the placement of objects in a tree structure with 2 levels of
directory. For instance a file with SHA1
`34973274ccef6ab4dfaaf86599792fa9c3fe4689` will be located at
`http://localhost:8088/swh/34/97/34973274ccef6ab4dfaaf86599792fa9c3fe4689`.

Note that using the slicer also comes with a slight performance hit.

See `this page
<https://github.com/seaweedfs/seaweedfs/wiki/Filer-Redis-Setup#super-large-directories>`_
for more details on the ``redis3`` filer backend, and `this one
<https://github.com/seaweedfs/seaweedfs/wiki/Super-Large-Directories>`_ for a
more general discussion about handling super large directories in seaweedfs
filer.

Filer backup
++++++++++++

The filer db is a key component of the seaweedfs backend; it's content can be
rebuilt from the volumes, but the time it take to do so will probably be in the
range of 1 to 2 months, so better not to loose it!

One can use the integrated filer backup tool to perform continuous backups of
the filer metadata using the command: ``weed filer.meta.backup``. This command
needs a :file:`backup_filer.toml` file specifying a filer store that will be used as
backup. For example, backupping an existing filer in a local leveldb the
:file:`backup_filer.toml` file would be like:

.. code-block:: ini

   [leveldb2]
   enabled = true
   dir = "/tmp/filerrdb"  # directory to store leveldb files


then:

.. code-block:: bash

   weed filer.meta.backup -config ./backup_filer.toml -filer localhost:8581
   I0315 11:18:44 95975 leveldb2_store.go:42] filer store leveldb2 dir: /tmp/filerrdb
   I0315 11:18:44 95975 file_util.go:23] Folder /tmp/filerrdb Permission: -rwxr-xr-x
   I0315 11:18:45 95975 filer_meta_backup.go:112] configured filer store to leveldb2
   I0315 11:18:45 95975 filer_meta_backup.go:80] traversing metadata tree...
   I0315 11:18:45 95975 filer_meta_backup.go:86] metadata copied up to 2023-03-15 11:18:45.559363829 +0000 UTC m=+0.915180010
   I0315 11:18:45 95975 filer_meta_backup.go:154] streaming from 2023-03-15 11:18:45.559363829 +0000 UTC


It can be interrupted and restarted. Using the ``-restart`` argument force a full
backup (rather than resuming incremental backup).

This is however very similar to having multiple filers configured in the
seawwedf cluster. As a backup component, it can however be a good idea not to
have this backup filer store not part of the cluster at all.


Volume
------

seaweedfs volume servers are the backbone of a seaweedfs cluster; where objects
are stored. Each volume server will manage a number of volumes, each os which is
by default about 30GB.

Content objects are packed in small (compressed) chunks in one or more volumes
(so one content object can be spread in several volumes).

When using several disks on one volume server, you may use hardware or software
RAID or similar redundancy techniques, but you may also prefer to run one
volume server per disk. When using safety features like erasure coding or
volume replication, seaweedfs has support for ensuring safe distribution among
servers (depending on the number if servers and the number of disks, make sure
losing one (or more) server does not lead to data loss.)

By default, each volume server will use memory to store indexes for volume
content (keep track of the position of each chunk in local volumes). This can
lead to a few problems when the number of volumes increases:

- extended startup time of the volume server (it needs to load all volume file
  indexes at startup), and
- consumed memory can grow pretty large.

In the context of a |swh| mirror, it's a good idea to have `volume servers
using a leveldb index
<https://github.com/seaweedfs/seaweedfs/wiki/Optimization#use-leveldb>`_. This
can be done using ``weed volume -index=leveldb`` command line argument (note
there are 3 possible index arguments: ``leveldb``, ``leveldbMedium`` and
``leveldbLarge``; see the seaweedfs documentation for more details).


.. _seaweedfs: https://github.com/seaweedfs/seaweedfs/
