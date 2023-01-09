.. _swh_statsd_metrics:

Statsd metrics and Grafana dashboards
=====================================

This page lists all statsd metrics reported by Software Heritage's components,
and other metrics commonly used to monitor them

.. _swh_statsd_metrics_archive:

Archive
-------

* ``sql_swh_archive_object_count``
* ``sql_swh_scheduler_delay``
* ``swh_archive_object_total``

.. _swh_statsd_metrics_journal:

Journal
-------

* ``swh_journal_client_handle_message_total``
* ``swh_journal_client_status``

Client progress and status is monitored using the `Kafka estimated time to completion
<https://grafana.softwareheritage.org/d/Jayj4QsGk/kafka-estimated-time-to-completion>`
dashboard for a loader-specific view, and `Kafka consumer lags
<https://grafana.softwareheritage.org/d/KvQqUhsWz/kafka-consumers-lag>` to show all
consumers at once.

.. _swh_statsd_metrics_indexers:

Indexers
--------

See :ref:`swh_statsd_metrics_rpc`.

.. _swh_statsd_metrics_loaders:

Loaders
-------

Filterered objects, ie. objects received by the loader that the archive
already has (currently only reported by the Git loader):

* ``swh_loader_filtered_objects_percent_bucket``
* ``swh_loader_filtered_objects_percent_count``
* ``swh_loader_filtered_objects_percent_sum``
* ``swh_loader_filtered_objects_total_count``
* ``swh_loader_filtered_objects_total_sum``

Git references which are not loaded:

* ``swh_loader_git_ignored_refs_percent_bucket``
* ``swh_loader_git_ignored_refs_percent_count``
* ``swh_loader_git_ignored_refs_percent_sum``
* ``swh_loader_git_known_refs_percent_bucket``
* ``swh_loader_git_known_refs_percent_count``
* ``swh_loader_git_known_refs_percent_sum``
* ``swh_loader_git_total``

Metadata loading:

* ``swh_loader_metadata_fetchers_count`` and ``swh_loader_metadata_fetchers_sum``: the ratio is the average number of fetchers used by visit
* ``swh_loader_metadata_objects_count``: total number of metadata objects loaded
* ``swh_loader_metadata_objects_sum``
* ``swh_loader_metadata_parent_origins_count`` and ``swh_loader_metadata_parent_origins_sum``: the ratio is the average number of origins this origin is a fork of

Performance (all labeled with the name of an operation; and for the git loader,
by whether they are incremental):

* ``swh_loader_operation_duration_seconds_bucket``
* ``swh_loader_operation_duration_seconds_count``
* ``swh_loader_operation_duration_seconds_error_count``
* ``swh_loader_operation_duration_seconds_sum``

Loader status is monitored through the `Ingestion status`_ and `Loader metrics`_
dashboards, which are focused respectively on loaded objects and loaders themselves.

.. _Ingestion status: https://grafana.softwareheritage.org/d/Cgi8dR8Wz/ingestion-status
.. _Loader metrics: https://grafana.softwareheritage.org/d/FqGC4zu7z/vlorentz-loader-metrics

.. _swh_statsd_metrics_objstorage:

Object storage
--------------

In addition to :ref:`swh_statsd_metrics_rpc`,

* ``swh_objstorage_in_bytes_total``
* ``swh_objstorage_out_bytes_total``

.. _swh_statsd_metrics_outgoing:

Outgoing requests
-----------------

All these metrics are labelled with ``api_type`` and ``api_instance``, which
should match values used for ``lister_name`` and ``lister_instance`` used elsewhere.
Currently, it is only ``github`` for both.
They are also labelled with ``username``, which is either ``anonymous`` or the name of
the user owning the token used to make the request.

* ``swh_outbound_api_requests_total``: total number of requests
* ``swh_outbound_api_responses_total``: total number of responses (excluding low-level failures: DNS, TCP, TLS, ...), with ``http_status`` label
* ``swh_outbound_api_remaining_requests``: gauge of the value of ``X-Ratelimit-Remaining``
* ``swh_outbound_api_reset_seconds``: gauge of the value of ``X-Ratelimit-Reset``
* ``swh_outbound_api_rate_limited_responses_total``
* ``swh_outbound_api_sleep_seconds_total``: number of seconds spent waiting for rate limits to reset

.. _swh_statsd_metrics_provenance:

Provenance
----------

* ``swh_provenance_archive_direct_duration_seconds_bucket``
* ``swh_provenance_archive_direct_duration_seconds_count``
* ``swh_provenance_archive_direct_duration_seconds_error_count``
* ``swh_provenance_archive_direct_duration_seconds_sum``
* ``swh_provenance_archive_graph_duration_seconds_bucket``
* ``swh_provenance_archive_graph_duration_seconds_count``
* ``swh_provenance_archive_graph_duration_seconds_sum``
* ``swh_provenance_archive_multiplexed_duration_seconds_bucket``
* ``swh_provenance_archive_multiplexed_duration_seconds_count``
* ``swh_provenance_archive_multiplexed_duration_seconds_error_count``
* ``swh_provenance_archive_multiplexed_duration_seconds_sum``
* ``swh_provenance_archive_multiplexed_per_backend_count``
* ``swh_provenance_backend_duration_seconds_bucket``
* ``swh_provenance_backend_duration_seconds_count``
* ``swh_provenance_backend_duration_seconds_error_count``
* ``swh_provenance_backend_duration_seconds_sum``
* ``swh_provenance_backend_operations_total``
* ``swh_provenance_graph_duration_seconds_bucket``
* ``swh_provenance_graph_duration_seconds_count``
* ``swh_provenance_graph_duration_seconds_error_count``
* ``swh_provenance_graph_duration_seconds_sum``
* ``swh_provenance_origin_revision_layer_duration_seconds_bucket``
* ``swh_provenance_origin_revision_layer_duration_seconds_count``
* ``swh_provenance_origin_revision_layer_duration_seconds_error_count``
* ``swh_provenance_origin_revision_layer_duration_seconds_sum``
* ``swh_provenance_storage_postgresql_duration_seconds_bucket``
* ``swh_provenance_storage_postgresql_duration_seconds_count``
* ``swh_provenance_storage_postgresql_duration_seconds_error_count``
* ``swh_provenance_storage_postgresql_duration_seconds_sum``
* ``swh_provenance_storage_rabbitmq_duration_seconds_bucket``
* ``swh_provenance_storage_rabbitmq_duration_seconds_count``
* ``swh_provenance_storage_rabbitmq_duration_seconds_error_count``
* ``swh_provenance_storage_rabbitmq_duration_seconds_sum``

`Index of Provenance dashboards
<https://grafana.softwareheritage.org/dashboards/f/eKOFn6y7k/provenance>`_

.. _swh_statsd_metrics_replayers:

Content and graph replayers
---------------------------

* ``swh_content_replayer_bytes``
* ``swh_content_replayer_duration_seconds_bucket``
* ``swh_content_replayer_duration_seconds_count``
* ``swh_content_replayer_duration_seconds_error_count``
* ``swh_content_replayer_duration_seconds_sum``
* ``swh_content_replayer_operations_total``
* ``swh_content_replayer_retries_total``
* ``swh_graph_replayer_duration_seconds_bucket``
* ``swh_graph_replayer_duration_seconds_count``
* ``swh_graph_replayer_duration_seconds_sum``
* ``swh_graph_replayer_operations_total``

Dashboards:

* `Cassandra <https://grafana.softwareheritage.org/d/HW1-UgO4k/cassandra-replayers>`__
* `S3 <https://grafana.softwareheritage.org/d/d3l2oqXWz/s3-object-copy>`__

.. _swh_statsd_metrics_rpc:

RPC servers
-----------

``indexer_storage``, ``objstorage``, ``storage``, ``search``
each report this set of metrics:

* ``swh_<NAME>_request_duration_seconds_bucket``
* ``swh_<NAME>_request_duration_seconds_count``
* ``swh_<NAME>_request_duration_seconds_error_count``
* ``swh_<NAME>_request_duration_seconds_sum``

``indexer_storage``, and ``search`` also have:

* ``swh_<NAME>_operations_total``

.. _swh_statsd_metrics_scheduler:

Scheduler
---------

* ``swh_scheduler_listener_handled_event_total``
* ``swh_scheduler_origins_enabled``
* ``swh_scheduler_origins_known``
* ``swh_scheduler_origins_last_update``
* ``swh_scheduler_origins_never_visited``
* ``swh_scheduler_origins_with_pending_changes``
* ``swh_scheduler_runner_scheduled_task_total``
* ``swh_task_called_count``
* ``swh_task_duration_seconds_bucket``
* ``swh_task_duration_seconds_count``
* ``swh_task_duration_seconds_error_count``
* ``swh_task_duration_seconds_sum``
* ``swh_task_end_ts``
* ``swh_task_failure_count``
* ``swh_task_start_ts``
* ``swh_task_success_count``

.. _swh_statsd_metrics_search:

Search
------

See :ref:`swh_statsd_metrics_rpc`.

.. _swh_statsd_metrics_scrubber:

Scrubber
--------

Performance:

* ``swh_scrubber_batch_duration_seconds_bucket``
* ``swh_scrubber_batch_duration_seconds_count``
* ``swh_scrubber_batch_duration_seconds_error_count``
* ``swh_scrubber_batch_duration_seconds_sum``
* ``swh_scrubber_objects_hashed_total``

Corruptions found:

* ``swh_scrubber_hash_mismatch_total``
* ``swh_scrubber_missing_object_total``

.. _swh_statsd_metrics_storage:

Storage
-------

In addition to :ref:`swh_statsd_metrics_rpc`,

* ``swh_storage_operations_bytes_total``, which reports the total number of content bytes
  going through the RPC server

.. _swh_statsd_metrics_webapp:

Webapp
------

* ``swh_web_accepted_save_requests``
* ``swh_web_save_requests_delay_seconds``
* ``swh_web_submitted_save_requests``
* ``swh_web_submitted_save_requests_from_webhooks``

Dashboard: `Save Code Now
<https://grafana.softwareheritage.org/d/WXRVVc_Mz/save-code-now>`_

.. _swh_statsd_metrics_misc:

Other metrics
-------------

Performance of end-to-end tests:

* ``swh_e2e_duration_seconds``
* ``swh_e2e_status``
