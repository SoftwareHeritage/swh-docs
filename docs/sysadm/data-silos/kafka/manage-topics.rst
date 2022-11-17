.. _manage-topics:

Reference: Manage topics
========================

.. admonition:: Intended audience
   :class: important

   sysadm members


In the following documentation, we'll describe the common actions we have to
periodically execute during deployments.

The demonstrated commands are triggered from one of the kafka cluster nodes (be it
staging or production).

Common configuration
--------------------

Once connected to the nodes, we have a bunch of environment variables to setup:

::

   KAFKA_TOPICS=/opt/kafka/bin/kafka-topics.sh
   KAFKA_CONSUMER_GROUPS=/opt/kafka/bin/kafka-consumer-groups.sh


staging
-------

The following setup is expected for staging:

::

   export KAFKA_SERVER=storage1.internal.staging.swh.network:9092
   export NB_PARTITIONS=64
   export REPLICATION_FACTOR=1

production
----------

The following setup is expected for production:

::

   export KAFKA_SERVER=kafka1.internal.softwareheritage.org:9092
   export NB_PARTITIONS=256
   export REPLICATION_FACTOR=2


Note: Report to the :ref:`service-url` page to determine what kafka server to use.


Topic naming
------------


Existing topics are prefixed with the following names:

- swh.journal.objects: Objects written (by loaders) in the archive are pushed in those
  topics
- swh.journal.indexed: Objects written by the indexers (derived out of the objects in
  the archive)

.. warning:: FIXME: Update topics with test topics and eventually the new provenance
             ones

Examples:

- `swh.journal.objects.directory`
- `swh.journal.indexed.origin_extrinsic_metadata`
- ...


Topic (re)creation
------------------

.. warning:: Topics must be created before any services consume or write to them.
             Otherwise, they will be created with the wrong configuration.


If a topic got created without the proper configuration, we can delete it:

.. code::

   $KAFKA_TOPICS --bootstrap-server $KAFKA_SERVER \
    --topic $TOPIC \
    --delete

And then create it back with the proper setup:

.. code::

   $KAFKA_TOPICS  --bootstrap-server $KAFKA_SERVER \
     --create --topic $TOPIC \
     --partitions $NB_PARTITIONS \
     --replication-factor $REPLICATION_FACTOR

Note:
Provided the `TOPIC` variable is set appropriately.


Consumer group reset
--------------------

Once in a while, due to a change in data format, or migration, we need to reset the
topics so the consumer can restart from scratch.

Example of consumer groups:

- `swh.indexer.journal_client.extrinsic_metadata`: anonymous consumer group
- `swh-indexer-prod-01-swh.indexer.journal_client.extrinsic_metadata`: authenticated
  production consumer group is prefixed by the user name

.. code::

   $KAFKA_CONSUMER_GROUPS \
     --bootstrap-server $KAFKA_SERVER \
     --group $CONSUMER_GROUP \
     --reset-offsets --to-earliest \
     --all-topics

Note:

- Provided the `CONSUMER_GROUP` variable is set appropriately
- The reset can be more restrictive on specific topics, replace `--all-topics` by
  as many calls to `--topic $TOPIC` as topics are involved.
