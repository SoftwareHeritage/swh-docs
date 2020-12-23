.. highlight:: bash

.. _mirror:

Software Heritage Mirror
========================

Description
-----------

A mirror is a full copy of the |swh| Archive. A minimal copy consists in 2
parts:

- the graph storage (typically an instance of :ref:`swh.storage <swh-storage>`),
- the object storage (typically an instance of :ref:`swh.objstorage <swh-objstorage>`).

However, a usable mirror needs also to be accessible. As such, a proper mirror
should also allow to:

- navigate the copy of the archive using a web browser (typically using the
  :ref:`the web application <swh-web>`),
- retrieve data from the copy of the archive (typically using the :ref:`the
  vault service <swh-vault>`)

A mirror is filled consuming data from the |swh| Kafka-based :ref:`journal
<journal-specs>` and retrieving the blob objects (file content) from the |swh|
:ref:`object storage <swh-objstorage>`.

.. note:: A mirror of the |swh| Archive is not necessarly implemented using the
   |swh| software stack. In this documentation however we will describe the
   case of a mirror using the |swh| software stack.


.. thumbnail:: images/mirror-architecture.svg

   General view of the |swh| mirroring architecture.

In this documentation, we will focus only on replication mechanisms using the
software stack provided by |swh|. Setting up web services or other storage
methods will not be covered here.


Replicating the Graph Storage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The replication of the graph is based on a journal using Kafka as event
streaming platform.

On the main Software Heritage side, every addition made to the graph consist in
the insertion of a :ref:`data-model` object. This added object is also
serialized as a msgpack_ bytestring which is used as value of a Kafka message
in a topic dedicated to the object type.

Topics for the main part of the |swh| :ref:`data-model` are:

- `swh.journal.objects.content`
- `swh.journal.objects.skipped_content`
- `swh.journal.objects.directory`
- `swh.journal.objects.revision`
- `swh.journal.objects.release`
- `swh.journal.objects.snapshot`
- `swh.journal.objects.origin`
- `swh.journal.objects.origin_visit`
- `swh.journal.objects.origin_visit_status`

In addition to these are a few topics for :ref:`extrinsic metadata
<extrinsic-metadata-specification>`:

- `swh.journal.objects.metadata_authority`
- `swh.journal.objects.metadata_fetcher`
- `swh.journal.objects.raw_extrinsic_metadata`


In order to set up a mirror of the graph, one need to deploy a stack capable of
retrieving all these topics and store their content relialably. For example a
kafka cluster configured as a replica of the main kafka broker hoste by |swh|
would do the job (albeit not in a very useful manner by itself).

A more usable mirror can be set up using the :ref:`Storage <swh-storage>`
component with the help of the special service named `replayer` provided by the
:doc:`apidoc/swh.storage.replay` module.
.. TODO: replace this previous link by a link to the 'swh storage replay'
   command once available, and ideally once
   https://github.com/sphinx-doc/sphinx/issues/880 is fixed, but humm...

Replicating the Object Storage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

File content (blobs) are **not** embedded in messages of the
`swh.journal.objects.content` Kafka topic. As these messages do not include the
file content, another component must be in charge of replicating blob objects
from the original Software Heritage Archive and inserted in the local object
storage instance.

The idea for this component is to have another `swh-journal` client that
subscribe to the `swh.journal.objects.content` topic to get the stream of blob
objects identifiers, then retrieve the blob object from Software Heritage's
object storage and insert it in the local object storage.

The proposed implementation for this component is called the :ref:`content
replayer <swh-objstorage-replayer>`.


Installation
------------

If using the |swh| software stack to deploy a mirror, a number of
|swh| software components must be installed.

As shown in the architecture diagram above, one needs to have:

- a database to store the graph of the |swh| Archive,
- the :ref:`swh-storage` component,
- an object storage solution (can be cloud based or on local filesystem like
  ZFS pools),
- the :ref:`swh-objstorage` component,
- the :ref:`swh.storage.replay` service (part of the :ref:`swh-storage`
  package)
- the :ref:`swh.objstorage.replayer.replay` service (from the
  :ref:`swh-objstorage-replayer` package).

As this can be quite complex to set up properly, we provide a `docker-swarm
<https://docs.docker.com/engine/swarm/>`_ based deployment which is provided as
a working example of the mirror stack:

  https://forge.softwareheritage.org/source/swh-docker

It is strongly recommended to start from there before planning a
production-like deployment.

See the `README
<https://forge.softwareheritage.org/source/swh-docker/browse/master/README.md>`_
file of the `swh-docker
<https://forge.softwareheritage.org/source/swh-docker>`_ repository for more
detailed explanations.


.. _msgpack: https://msgpack.org
