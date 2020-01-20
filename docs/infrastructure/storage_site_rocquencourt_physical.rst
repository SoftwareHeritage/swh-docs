Physical machines at Rocquencourt
=================================

hypervisors
-----------

The :doc:`hypervisors <hypervisors>` mostly use local storage on the form of internal
SSDS but also have access to a :ref:`ceph_cluster`.

NFS server
----------

There is only one NFS server managed by Software Heritage, *uffizi.internal.softwareheritage.org*.
That machine is located at Rocquencourt and is directly attached to two SAS storage bays.

NFS-exported data is present under these local filesystem paths::

/srv/storage/space
/srv/softwareheritage/objects

belvedere
---------

This server is used for at least two separate PostgreSQL instances:

- *softwareheritage* database (port 5433)
- *swh-lister* and *softwareheritage-scheduler* databases (port 5434)

Data is stored on local SSDs. The operating system lies on a LSI hardware RAID 1 volume and
each PostgreSQL instance uses a dedicated set of drives in mdadm RAID10 volume(s).

It also uses a single NFS volume::

  uffizi:/srv/storage/space/postgres-backups/prado

banco
-----

This machine is located in its own building in Rocquencourt, along
with a SAS storage bay.
It is intended to serve as a backup for the main site on building 30.

Elasticsearch cluster
---------------------

The :doc:`Elasticsearch cluster <elasticsearch>` only uses local storage on
its nodes.

Test / staging server
---------------------

There is also *orsay*, a refurbished machine only used for testing / staging
new software versions.

.. _ceph_cluster:

Ceph cluster
------------

The Software Heritage Ceph cluster contains three nodes:

- ceph-mon1
- ceph-osd1
- ceph-osd2
