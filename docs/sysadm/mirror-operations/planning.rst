.. _planning-a-mirror:

Hosting a mirror
================

This section present and discuss the technical requirements needed to host a
|SWH| mirror.

There are many different options to host a mirror, but there are common overall
requirements that needs to be fulfilled.

Namely, hosting a mirror requires:

- a dedicated infrastructure with enough compute (s/computing) power and storage
- enough network bandwidth (both ingress and egress)
- good IT tooling (supervision, alerting)
- a legal and operational structure to :ref:`handle takedown requests
  <mirror_takedown_requests>`

The mirror operator is not required to run the Software Heritage `full software
stack <https://docs.softwareheritage.org/devel>`_, however it is possible to
use it.

.. Warning::

   Volumes given in this section are estimations and numbers from **May 2024**.

The global raw hardware requirements are:

- a database system for the main storage of the archive (the graph structure);
  the current volume of the Postgresql database is about 42TB, with an increase rate of about
  16To/year, the cassandra database it about 30TB with an increase of 7TB/year (multiply
  this per 3 to use a standard x3 replication factor)
- an object storage system for the objects (archived software source code
  files); the current volume is about 3PB with an increase rate of
  about 750TB/year,
- an elasticsearch engine; the current main index is about 390M entries
  (origins) for an index size of 380GB; the increase rate is about 2M
  entries/month,
- a web/application server for the main web application and public API,
- a few compute nodes for the application services.

Using a zfs-like filesystem supporting compression for the objstorage and the Postgresql database
can reduce the on disk volume by a factor of 1.5 or 2.5 respectively.

A mirror should provision machines or cloud-based resources with these numbers
in mind. This should include the usual robustness margins (RAID-like storage,
replication, backup etc.).

General hardware requirements
-----------------------------

When deploying a mirror based on the Software Heritage software stack, one will
need:


Core services
^^^^^^^^^^^^^

- a database for the storage; this can be either a
  `Postgresql <https://postgresql.org>`_ database (single machine)
  or a `Cassandra <https://cassandra.apache.org>`_ cluster (at least 3 nodes),
- an object storage system; this can be any
  :py:mod:`supported backend <swh.objstorage.backends>`
  -- a public cloud-based obstorage (e.g. s3), any private supported object storage,
  an ad-hoc filesystem storage system, etc.
- an `Elasticsearch <https://www.elastic.co>`_ instance,
- a few nodes for backend applications
  (:py:mod:`swh-storage <swh.storage>`, :py:mod:`swh-objstorage <swh.objstorage>`)
- the web frontend (:py:mod:`swh-web <swh.web>`)
  serving the main web app and the `public
  API <https://docs.softwareheritage.org/devel/swh-web/uri-scheme-api.html>`_)


Replaying services
^^^^^^^^^^^^^^^^^^

- `graph
  replayers <https://docs.softwareheritage.org/devel/swh-storage/cli.html#swh-storage-replay>`_
  as mirroring workers (increase parallelism to increase speed)
- `content
  replayers <https://docs.softwareheritage.org/devel/swh-objstorage-replayer/cli.html>`_
  as mirroring workers (id.)


Vault service
^^^^^^^^^^^^^

- a node for the :ref:`swh-vault <swh-vault>` backend service,
- a node for the :ref:`swh-vault <swh-vault>` worker service


Sizing a mirror infrastructure
------------------------------

.. Note:: solutions with a star (*) in the tables below are still under test or
          validation.

Common components
^^^^^^^^^^^^^^^^^

================ ====================== ========= ===== ============== ==============
SWH Service      Tool                   Instances RAM   Storage Type   Storage Volume
================ ====================== ========= ===== ============== ==============
storage          swh-storage            16        16GB  regular        10GB
search           elasticsearch          3         24GB  fast / zfs     1TB
web              swh-web                2         8GB   regular        100GB
---------------- ---------------------- --------- ----- -------------- --------------
graph replayer   swh-storage            32        32GB  regular        10GB
content replayer swh-obstorage-replayer 32        64GB  regular        10GB
replayer         redis                  1         8GB   regular        100GB
---------------- ---------------------- --------- ----- -------------- --------------
vault            swh-vault              1         4GB   regular        10GB
vault worker     swh-vault              1         16GB  fast           1TB
vault            rabbitmq               1         8GB   regular        10GB
================ ====================== ========= ===== ============== ==============


Storage backend
^^^^^^^^^^^^^^^

.. tab-set::

  .. tab-item:: Postgresql

    ================ ====================== ========= ===== ============== ==============
    SWH Service      Tool                   Instances RAM   Storage Type   Storage Volume
    ================ ====================== ========= ===== ============== ==============
    storage          postgresql             1         512GB fast+zfs (lz4) 20TB
    ================ ====================== ========= ===== ============== ==============

  .. tab-item:: Cassandra (min.)*

    ================ ====================== ========= ===== ============== ==============
    SWH Service      Tool                   Instances RAM   Storage Type   Storage Volume
    ================ ====================== ========= ===== ============== ==============
    storage          cassandra              3         32GB  fast           30TB
    ================ ====================== ========= ===== ============== ==============

  .. tab-item:: Cassandra (typ.)*

    ================ ====================== ========= ===== ============== ==============
    SWH Service      Tool                   Instances RAM   Storage Type   Storage Volume
    ================ ====================== ========= ===== ============== ==============
    storage          cassandra              6+        32GB  fast           90TB
    ================ ====================== ========= ===== ============== ==============


Objstorage backend
^^^^^^^^^^^^^^^^^^

.. tab-set::

  .. tab-item:: FS

    ================ ====================== ========= ===== ============== ==============
    SWH Service      Tool                   Instances RAM   Storage Type   Storage Volume
    ================ ====================== ========= ===== ============== ==============
    objstorage       swh-objstorage         1 [#f1]_  512GB zfs (with lz4) 2PB
    ================ ====================== ========= ===== ============== ==============

  .. tab-item:: Winery - Ceph*

    ================ ====================== ========= ===== ============== ==============
    SWH Service      Tool                   Instances RAM   Storage Type   Storage Volume
    ================ ====================== ========= ===== ============== ==============
    objstorage       swh-objstorage         2 [#f2]_  32GB  standard       100GB
    winery-db        postgresql             2 [#f2]_  512GB fast           10TB
    ceph-mon         ceph                   3         4GB   fast           60GB
    ceph-osd         ceph                   12+       64GB  mix fast+HDD   2PB (total)
    ================ ====================== ========= ===== ============== ==============

  .. tab-item:: Seaweedfs*

    ================ ====================== ========= ===== ============== ==============
    SWH Service      Tool                   Instances RAM   Storage Type   Storage Volume
    ================ ====================== ========= ===== ============== ==============
    objstorage       swh-objstorage         3         32GB  standard       100GB
    seaweed LB       nginx                  1         32GB  fast           100GB
    seaweed-master   seaweedfs              3         8GB   standard       10GB
    seaweed-filer    seaweedfs              3         32GB  fast           1TB
    seaweed-volume   seaweedfs              3+        32GB  standard       1PB (total)
    ================ ====================== ========= ===== ============== ==============

.. rubric:: Notes

.. [#f1] An swh-objstorage using :py:mod:`simple filesystem
         <swh.objstorage.backends.pathslicing>` as backend can actually be
         split on several machines using the
         :py:mod:`swh.objstorage.multiplexer` backend.
.. [#f2] The swh-objstorage RPC service and the index database can be hosted on
         the same machine.

Example of hardware used by Software Heritage
---------------------------------------------

These configurations are only documented as example. Feel free to adapt the architecture
to suit your own use of the mirror or use any other architecture type (cloud/vms/...).

Database
^^^^^^^^

.. tab-set::

  .. tab-item:: Postgresql

    ========== =========== ===== ====== ====================
    Type       Instance(s) Cores Memory Disk
    ========== =========== ===== ====== ====================
    Postgresql 2           >= 32 768GB  30TB Write Intensive
    ========== =========== ===== ====== ====================

  .. tab-item:: Cassandra

    ========= =========== ===== ====== =================================
    Type      Instance(s) Cores Memory Disk
    ========= =========== ===== ====== =================================
    Cassandra 12          >= 16 256GB  12TB fast + 600Go Write intensive
    ========= =========== ===== ====== =================================

Objstorage
^^^^^^^^^^

.. tab-set::

  .. tab-item:: FS

    ==== =========== ===== ====== ============================
    Type Instance(s) Cores Memory Disk
    ==== =========== ===== ====== ============================
    FS   1           >= 16 384GB  1.5PB (attached disk arrays)
    ==== =========== ===== ====== ============================

  .. tab-item:: Ceph

    ======== =========== ===== ====== ======================
    Type     Instance(s) Cores Memory Disk
    ======== =========== ===== ====== ======================
    api/pg   2           >= 32 768GB  10TB fast
    Ceph mon 3           >= 16 192GB  500GB
    Ceph osd 26          >= 16 192GB  144TB SAS + 360GB fast
    ======== =========== ===== ====== ======================

Compute nodes
^^^^^^^^^^^^^

=============== =========== ===== ====== ========
Type            Instance(s) Cores Memory Disk
=============== =========== ===== ====== ========
Kubernetes node 3           >= 32 256GB  2TB fast
=============== =========== ===== ====== ========

Elasticsearch
^^^^^^^^^^^^^

============= =========== ===== ====== ========
Type          Instance(s) Cores Memory Disk
============= =========== ===== ====== ========
Elasticsearch 3           >= 8  64GB   6TB fast
============= =========== ===== ====== ========
