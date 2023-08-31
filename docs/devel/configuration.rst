.. _cli-config:

Configuration reference
=======================

.. highlight:: yaml

|swh| components are all configured with a YAML file, made of multiple blocks,
most of which describe how to connect to other components/services.

Most services are composable, so they can be either instantiated locally or
accessed through |swh|'s HTTP-based RPC protocol (``cls: remote``).

For example, a possible configuration for swh-vault is::

    graph:
      url: http://graph.internal.softwareheritage.org:5009/

    storage:
      cls: pipeline
      steps:
      - cls: retry
      - cls: remote
        url: http://webapp.internal.staging.swh.network:5002/

    objstorage:
      cls: s3
      compression: gzip
      container_name: softwareheritage
      path_prefix: content


All URLs in this document are examples, see :ref:`service-url` for actual values.


.. _cli-config-celery:

celery
------

The :ref:`scheduler <swh-scheduler>` uses Celery for running some tasks. This
configuration key is used for parameters passed directly to Celery, e.g. the URI
of the RabbitMQ broker used for distribution of tasks, for both scheduler
commands as well as Celery workers.

The contents of this configuration key follow the `"lowercase settings" schema from
Celery upstream
<https://docs.celeryq.dev/en/stable/userguide/configuration.html#new-lowercase-settings>`_.

Some default values can be found in :mod:`swh.scheduler.celery_backend.config`.


.. _cli-config-graph:

graph
-----

The :ref:`graph <swh-graph>` can only be accessed as a remote service, and
its configuration block is a single key: ``url``, which is the URL to its
HTTP endpoint; usually on port 5009 or at the path ``/graph/``.

.. _cli-config-journal:

journal
-------

The :ref:`journal <swh-journal>` can only be locally instantiated to consume
directly from Kafka::

    journal:
      brokers:
        - broker1.journal.softwareheritage.org:9093
        - broker2.journal.softwareheritage.org:9093
        - broker3.journal.softwareheritage.org:9093
        - broker4.journal.softwareheritage.org:9093
      prefix: swh.journal.objects
      sasl.mechanism: "SCRAM-SHA-512"
      security.protocol: "sasl_ssl"
      sasl.username: "..."
      sasl.password: "..."
      privileged: false
      group_id: "..."


.. _cli-config-scheduler:

scheduler
---------

The :ref:`scheduler <swh-scheduler>` can only be accessed as a remote service, and
its configuration block is a single key: ``url``, which is the URL to its
HTTP endpoint; usually on port 5008 or at the path ``/scheduler/``.::

    scheduler:
      cls: remote
      url: http://saatchi.internal.softwareheritage.org:5008

.. _cli-config-storage:

storage
-------

Backends
^^^^^^^^

The :ref:`storage <swh-storage>` has four possible classes:

* ``cassandra``, see :class:`swh.storage.cassandra.storage.CassandraStorage`::

    storage:
      cls: cassandra
      hosts: [...]
      keyspace: swh
      port: 9042
      journal_writer:
        # ...
      # ...

* ``postgresql``, which takes a `libpq connection string <https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING>`_::

    storage:
      cls: postgresql
      db: service=swh
      journal_writer:
        # ...

  For optional arguments, see :class:`swh.storage.postgresql.storage.Storage`

* ``memory``, which stores data in-memory instead of persisting it somewhere;
  this should only be used for debugging::

    storage:
      cls: memory
      journal_writer:
        # ...

* ``remote``, which takes a URL to a remote service's HTTP endpoint;
  usually on port 5002 or at the path ``/storage/``::

    storage:
      cls: remote
      url: http://webapp.internal.staging.swh.network:5002/


The ``journal_writer`` key is optional. If provided, it will be used to write all
additions to some sort of log (usually Kafka) before any write to the main database.

:mod:`swh.journal.writer.kafka`::

    cls: kafka
    brokers:
      - broker1.journal.softwareheritage.org:9093
      - broker2.journal.softwareheritage.org:9093
      - broker3.journal.softwareheritage.org:9093
      - broker4.journal.softwareheritage.org:9093
    prefix: swh.journal.objects
    anonymize: true
    client_id: ...
    producer_config: ...

:mod:`swh.journal.writer.stream`, which writes directly to a file
(or stdout if set to ``-``)::

    cls: stream
    output_stream: /tmp/messages.msgpack

:mod:`swh.journal.writer.inmemory`, which does not actually persist anywhere,
and should only be used for tests::

    cls: memory
    anonymize: false


Proxies
^^^^^^^

In addition to these three backends, "storage proxies" can be used and chained in order
to change the behavior of accesses to it. They usually do not change the semantics,
but perform optimizations such as batching calls, stripping redundant operations,
and retrying on error.
They are invoked through the special ``pipeline`` class, which takes as parameter
a list of proxy configurations, ending with a backend configuration as seen above::

    storage:
      cls: pipeline
      steps:
        - cls: buffer
          min_batch_size:
            content: 10000
            directory: 5000
        - cls: filter
        - cls: retry
        - cls: remote
          url: http://webapp1.internal.softwareheritage.org:5002/

which is equivalent to this nested configuration::

    storage:
      cls: buffer
      min_batch_size:
        content: 10000
        directory: 5000
      storage:
        cls: filter
        storage:
          cls: retry
          storage:
            cls: remote
            url: http://webapp1.internal.softwareheritage.org:5002/

See :mod:`swh.storage.proxies` for the list of proxies.
