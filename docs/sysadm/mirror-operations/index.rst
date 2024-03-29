.. _mirror_operations:


Mirror Operations
=================

.. _mirror:

Description
-----------

A mirror is a full copy of the |swh| archive, operated independently from the
Software Heritage initiative. A minimal mirror consists of two parts:

- the graph storage (typically an instance of :ref:`swh.storage <swh-storage>`),
  which contains the Merkle DAG structure of the archive, *except* the
  actual content of source code files (AKA blobs),

- the object storage (typically an instance of :ref:`swh.objstorage <swh-objstorage>`),
  which contains all the blobs corresponding to archived source code files.

However, a usable mirror needs also to be accessible by others. As such, a
proper mirror should also allow to:

- navigate the archive copy using a Web browser and/or the Web API (typically
  using the :ref:`the web application <swh-web>`),
- have minimal search capabilities (typically using :ref:`the swh-search
  service <swh-search>` with an Elasticsearch backend),
- retrieve data from the copy of the archive (typically using the :ref:`the
  vault service <swh-vault>`)

A mirror is initially populated and maintained up-to-date by consuming data
from the |swh| Kafka-based :ref:`journal <journal-specs>` and retrieving the
blob objects (file content) from the |swh| :ref:`object storage <swh-objstorage>`.

.. note:: It is not required that a mirror be deployed using the |swh| software
   stack. Other technologies, including different storage methods, can be
   used. But we will focus in this documentation to the case of mirror
   deployment using the |swh| software stack.


.. thumbnail:: ../images/mirror-architecture.svg

   General view of the |swh| mirroring architecture.

.. Note:: This general view is very simplified and does not show all the
          services involved in hosting and operating a mirror.

See the :ref:`planning-a-mirror` for a complete description of the requirements
to host a mirror.

.. Note:: Hosting a complete mirror is a complex task, involving the deployment
          of dozens of inter related (micro-)services. It should be planned and
          operated carefully, using state-of-art ops practices (cloud-based, or
          using container orchestration tools on an elastic execution platform
          like kubernetes_, `docker swarm`_, or using tools like Ansible_ or
          `Salt Stack`_).

.. Important:: It is **strongly** recommended to start with a simple `docker
          swarm`_ based deployment (this can be done on a single machine) as
          described in :ref:`mirror_deploy`.


Mirroring the Graph Storage
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The replication of the graph is based on a journal using Kafka_ as event
streaming platform.

On the Software Heritage side, every addition made to the archive consist of
the addition of a :ref:`data-model` object. The new object is also serialized
as a msgpack_ bytestring which is used as the value of a message added to a
Kafka topic dedicated to the object type.

The main Kafka topics for the |swh| :ref:`data-model` are:

- `swh.journal.objects.content`
- `swh.journal.objects.directory`
- `swh.journal.objects.extid`
- `swh.journal.objects.metadata_authority`
- `swh.journal.objects.metadata_fetcher`
- `swh.journal.objects.origin_visit_status`
- `swh.journal.objects.origin_visit`
- `swh.journal.objects.origin`
- `swh.journal.objects.raw_extrinsic_metadata`
- `swh.journal.objects.release`
- `swh.journal.objects.revision`
- `swh.journal.objects.skipped_content`
- `swh.journal.objects.snapshot`

In order to set up a mirror of the graph, one needs to deploy a stack capable
of retrieving all these topics and store their content reliably. For example a
Kafka cluster configured as a replica of the main Kafka broker hosted by |swh|
would do the job (albeit not in a very useful manner by itself).

A more useful mirror can be set up using the :ref:`storage <swh-storage>`
component with the help of the special service named `replayer` provided by the
:mod:`swh.storage.replay` module.

.. TODO: replace this previous link by a link to the 'swh storage replay'
  command once available, and ideally once
  https://github.com/sphinx-doc/sphinx/issues/880 is fixed


Mirroring the Object Storage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

File content (blobs) are *not* directly stored in messages of the
`swh.journal.objects.content` Kafka topic, which only contains metadata about
them, such as various kinds of cryptographic hashes. A separate component is in
charge of replicating blob objects from the archive and stored them in the
local object storage instance.

A separate `swh-journal` client should subscribe to the
`swh.journal.objects.content` topic to get the stream of blob objects
identifiers, then retrieve corresponding blobs from the main Software Heritage
object storage, and store them in the local object storage.

A reference implementation for this component is available in
:ref:`content replayer <swh-objstorage-replayer>`.


Installation
------------

When using the |swh| software stack to deploy a mirror, a number of |swh|
software components must be installed (cf. architecture diagram above).

.. Note:: It is **not** recommended to try to deploy each |swh| service
          individually. You should rather start from the example docker-based
          deployment project :ref:`described here <mirror_docker>`.

A `docker swarm`_ based deployment
solution is provided as a working example of the mirror stack,
see :ref:`mirror_deploy`.

It is strongly recommended to start from there before planning a
production-like deployment.

.. _Kafka: https://kafka.apache.org/
.. _msgpack: https://msgpack.org
.. _`docker swarm`: https://docs.docker.com/engine/swarm/
.. _Ansible: https://docs.ansible.com/ansible/latest/index.html
.. _kubernetes: https://kubernetes.io/fr/
.. _`Salt Stack`: https://saltproject.io/


You may want to read:

- :ref:`mirror_monitor` to learn how to monitor your mirror and how to report
  its health back the |swh|.
- :ref:`mirror_seaweedfs` to have some tips and explanations on how to use
  SeaweedFS_ as objstorage backend for a mirror.
- :ref:`mirror_onboard` for the |swh| side view of adding a new mirror.

.. _SeaweedFS: https://github.com/seaweedfs/seaweedfs/

.. toctree::
   :hidden:

   planning
   deploy
   seaweedfs
   takedown-notices
   onboard
   monitor
