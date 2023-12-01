.. _objstorage-overview:

Object Storage Overview
=======================

The Object Storage: Contents
----------------------------

All the history and context of the archive is represented by
a graph (Merkle DAG) with the following nodes types:

- releases,
- revisions (commits)
- directories
- directory entries (file names)

This graph is stored in a database, commonly called "Graph" or
"Storage".

This database is currently based on PostgreSQL, and is going
to be migrated to Cassandra, which is more efficient in terms of
concurrent writing.

The source code itself (the content of the files) represents a huge
volume of data, and one can find exactly the same content in different
files. In order to avoid storing several times the same content,
contents are deduplicated: a single content is stored only once,
and all the files entries having this exact content will refer to the
same content.

Ceph
----

These contents are stored in a customized file system, called
"Object Storage", each content being considered as an object.
Until now, the actual object storage is based on an open source
File System technology called ZFS.

The growth of the archive requires a more adapted technology,
and an few years ago, we chose Ceph, a distributed Storage
technology created by RedHat.

A specificity of Software Heritage is that each content has a
small size (half of our contents are less than 3KB), which is
much smaller than the minimum space used by Ceph to store a
single file (16KB).
Using Ceph directly would hence result in a massive waste of space.

Winery
------

So we needed to create a custom layer on top of Ceph to group
the data we store, using sharding techniques: a shard is a Ceph
object that contains many contents. In order to be able to retrieve
the single contents, we need to handle a mechanism that enables to
know where the content is located in the shard.

This layer is called Winery, and was developed especially for
Software Heritage by Easter Eggs.

.. thumbnail:: ../images/object-storage.svg
