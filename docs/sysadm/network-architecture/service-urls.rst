.. _service-url:

Service urls
============

.. admonition:: Intended audience
   :class: important

   Staff members

This section regroups the urls of the services.

.. toctree::
   :maxdepth: 2
   :titlesonly:

Staging
-------

Try to use the staging environment as far as possible for your tests

Public urls
~~~~~~~~~~~

============================ ============================================
Service                      URL
============================ ============================================
swh-web                      https://webapp.staging.swh.network
swh-deposit                  https://deposit.staging.swh.network
swh-objstorage read-only [4] https://objstorage.staging.swh.network
swh-graphql                  https://webapp.staging.swh.network/graphql/
software stories             https://software-stories.staging.swh.network
Journal TLS                  broker[1-2].journal.staging.swh.network:9093
============================ ============================================

Internal services
~~~~~~~~~~~~~~~~~

+-----------------------+----------------------------------------------------------------+--------+------------+
| Backend               | URL                                                            | VPN[1] | Private[2] |
+=======================+================================================================+========+============+
| swh-web cassandra     | https://webapp-cassandra.internal.staging.swh.network          | X      |            |
+-----------------------+----------------------------------------------------------------+--------+------------+
| swh-graphql cassandra | https://webapp-cassandra.internal.staging.swh.network/graphql/ | X      |            |
+-----------------------+----------------------------------------------------------------+--------+------------+
| swh-web postgresql    | https://webapp-postgresql.internal.staging.swh.network         | X      |            |
+-----------------------+----------------------------------------------------------------+--------+------------+
| swh-storage-ro        | http://storage-ro.internal.staging.swh.network                 | X      |            |
+-----------------------+----------------------------------------------------------------+--------+------------+
| swh-storage cass ro   | http://storage-cassandra.internal.staging.swh.network          | X      |            |
+-----------------------+----------------------------------------------------------------+--------+------------+
| swh-objstorage-ro     | http://objstorage-ro.internal.staging.swh.network              | X      |            |
+-----------------------+----------------------------------------------------------------+--------+------------+
| swh-counters          | http://counters.internal.staging.swh.network                   | X      |            |
+-----------------------+----------------------------------------------------------------+--------+------------+
| swh-search            | http://search.internal.staging.swh.network                     | X      |            |
+-----------------------+----------------------------------------------------------------+--------+------------+
| swh-scheduler         | http://scheduler.internal.staging.swh.network                  |        | X          |
+-----------------------+----------------------------------------------------------------+--------+------------+
| swh-storage           | http://storage-postgresql-read-write-rpc-ingress               |        | X          |
+-----------------------+----------------------------------------------------------------+--------+------------+
| swh-objstorage        | http://objstorage-read-write-rpc-ingress                       |        | X          |
+-----------------------+----------------------------------------------------------------+--------+------------+
| swh-search            | http://search-rpc-ingress                                      |        | X          |
+-----------------------+----------------------------------------------------------------+--------+------------+
| swh-vault             | http://vault-rpc-ingress                                       |        | X          |
+-----------------------+----------------------------------------------------------------+--------+------------+
| Journal plaintext     | journal[1-2].internal.staging.swh.network:9092                 |        | X          |
+-----------------------+----------------------------------------------------------------+--------+------------+
| Journal internal TLS  | journal[1-2].internal.staging.swh.network:9094                 |        | X          |
+-----------------------+----------------------------------------------------------------+--------+------------+

SWH backends
~~~~~~~~~~~~

+--------------------+---------------------------------------------------------+--------+------------+
|      Backend       |                           URL                           | VPN[1] | Private[2] |
+====================+=========================================================+========+============+
| RabbitMq GUI       | http://scheduler0.internal.staging.swh.network:15672    | X      |            |
+--------------------+---------------------------------------------------------+--------+------------+
| archive database   | db1.internal.staging.swh.network:5432/swh               | X      |            |
+--------------------+---------------------------------------------------------+--------+------------+
| webapp database    | db1.internal.staging.swh.network:5432/swh-web           | X      |            |
+--------------------+---------------------------------------------------------+--------+------------+
| deposit database   | db1.internal.staging.swh.network:5432/swh-deposit       | X      |            |
+--------------------+---------------------------------------------------------+--------+------------+
| vault database     | db1.internal.staging.swh.network:5432/swh-vault         | X      |            |
+--------------------+---------------------------------------------------------+--------+------------+
| scheduler database | db1.internal.staging.swh.network:5432/swh-scheduler     | X      |            |
+--------------------+---------------------------------------------------------+--------+------------+
| lister database    | db1.internal.staging.swh.network:5432/swh-lister        | X      |            |
+--------------------+---------------------------------------------------------+--------+------------+
| swh-search ES      | http://search-esnode0.internal.staging.swh.network:9200 |        | X          |
+--------------------+---------------------------------------------------------+--------+------------+
| Counters redis     | counters0.internal.staging.swh.network:6379             |        | X          |
+--------------------+---------------------------------------------------------+--------+------------+
| Cassandra          | cassandra[1-3].internal.staging.swh.network:9042        | X      |            |
+--------------------+---------------------------------------------------------+--------+------------+

Production
----------

.. _public-urls-1:

Public urls
~~~~~~~~~~~

+----------------------------------------+---------------------------------------------------+
|             Service                    |                      URL                          |
+========================================+===================================================+
| swh-web                                | https://archive.softwareheritage.org              |
+----------------------------------------+---------------------------------------------------+
| swh-deposit                            | https://deposit.softwareheritage.org              |
+----------------------------------------+---------------------------------------------------+
| swh-objstorage read-only [3][4]        | https://objstorage.softwareheritage.org           |
+----------------------------------------+---------------------------------------------------+
| swh-storage cassandra read-only [4][5] | https://storage-cassandra-ro.softwareheritage.org |
+----------------------------------------+---------------------------------------------------+
| software stories                       | https://stories.softwareheritage.org              |
+----------------------------------------+---------------------------------------------------+
| Journal TLS                            | broker[1-4].journal.softwareheritage.org:9093     |
+----------------------------------------+---------------------------------------------------+

.. _internal-services-1:

Internal services
~~~~~~~~~~~~~~~~~

+-----------------------------+-----------------------------------------------------------------+--------+------------+
|           Service           |                              URL                                | VPN[1] | Private[2] |
+=============================+=================================================================+========+============+
| swh-web test/validation     | https://webapp1.internal.softwareheritage.org                   | X      |            |
+-----------------------------+-----------------------------------------------------------------+--------+------------+
| swh-web cassandra           | https://webapp-cassandra.internal.softwareheritage.org          |   X    |            |
+-----------------------------+-----------------------------------------------------------------+--------+------------+
| swh-graphql cassandra       | https://webapp-cassandra.internal.softwareheritage.org/graphql/ |   X    |            |
+-----------------------------+-----------------------------------------------------------------+--------+------------+
| swh-storage                 | http://saam.internal.softwareheritage.org:5002                  |        | X          |
+-----------------------------+-----------------------------------------------------------------+--------+------------+
| swh-storage read-only       | http://moma.internal.softwareheritage.org:5002                  | X      |            |
+-----------------------------+-----------------------------------------------------------------+--------+------------+
| swh-objstorage              | http://saam.internal.softwareheritage.org:5003                  |        | X          |
+-----------------------------+-----------------------------------------------------------------+--------+------------+
| swh-objstorage read-only[3] | http://objstorage.internal.softwareheritage.org:5003            | X      |            |
+-----------------------------+-----------------------------------------------------------------+--------+------------+
| swh-scheduler               | http://saatchi.internal.softwareheritage.org:5008               | X      |            |
+-----------------------------+-----------------------------------------------------------------+--------+------------+
| swh-counters                | http://counters1.internal.softwareheritage.org:5011             | X      |            |
+-----------------------------+-----------------------------------------------------------------+--------+------------+
| swh-search                  | http://moma.internal.softwareheritage.org:5010                  | X      |            |
+-----------------------------+-----------------------------------------------------------------+--------+------------+
| swh-search                  | http://search1.internal.softwareheritage.org:5010               |        | X          |
+-----------------------------+-----------------------------------------------------------------+--------+------------+
| swh-graph rpc               | http://granet.internal.softwareheritage.org:5009                | X      |            |
+-----------------------------+-----------------------------------------------------------------+--------+------------+
| swh-graph grpc              | http://granet.internal.softwareheritage.org:50091               | X      |            |
+-----------------------------+-----------------------------------------------------------------+--------+------------+
| swh-vault                   | http://vangogh.euwest.azure.internal.softwareheritage.org:5005  |        | X          |
+-----------------------------+-----------------------------------------------------------------+--------+------------+
| Journal plaintext           | kafka[1-4].internal.softwareheritage.org:9092                   |        | X          |
+-----------------------------+-----------------------------------------------------------------+--------+------------+
| Journal internal TLS        | kafka[1-4].internal.softwareheritage.org:9094                   | X      |            |
+-----------------------------+-----------------------------------------------------------------+--------+------------+

.. _swh-backends-1:

SWH backends
~~~~~~~~~~~~

+--------------------------+-----------------------------------------------------------------------+--------+------------+
|         Backend          |                                  URL                                  | VPN[1] | Private[2] |
+==========================+=======================================================================+========+============+
| RabbitMq GUI             | http://saatchi.internal.softwareheritage.org:15672                    | X      |            |
+--------------------------+-----------------------------------------------------------------------+--------+------------+
| archive database replica | somerset.internal.softwareheritage.org:5432/softwareheritage          | X      |            |
+--------------------------+-----------------------------------------------------------------------+--------+------------+
| archive database main    | belvedere.internal.softwareheritage.org:5432/softwareheritage         | X      |            |
+--------------------------+-----------------------------------------------------------------------+--------+------------+
| webapp database main     | belvedere.internal.softwareheritage.org:5432/swh-web                  | X      |            |
+--------------------------+-----------------------------------------------------------------------+--------+------------+
| scheduler database       | belvedere.internal.softwareheritage.org:5432/swh-scheduler            | X      |            |
+--------------------------+-----------------------------------------------------------------------+--------+------------+
| lister database          | belvedere.internal.softwareheritage.org:5432/swh-lister               | X      |            |
+--------------------------+-----------------------------------------------------------------------+--------+------------+
| deposit database         | belvedere.internal.softwareheritage.org:5432/softwareheritage-deposit | X      |            |
+--------------------------+-----------------------------------------------------------------------+--------+------------+
| vault database           | belvedere.internal.softwareheritage.org:5432/swh-vault                | X      |            |
+--------------------------+-----------------------------------------------------------------------+--------+------------+
| swh-search ES            | search-esnode[1-3].internal.softwareheritage.org:9200                 |        | X          |
+--------------------------+-----------------------------------------------------------------------+--------+------------+
| Counters redis           | counters1.internal.softwareheritage.org:6379                          |        | X          |
+--------------------------+-----------------------------------------------------------------------+--------+------------+
| cassandra                | cassandra[1-8].internal.softwareheritage.org:9042                     |        | X          |
+--------------------------+-----------------------------------------------------------------------+--------+------------+

Other tools
-----------

+-------------------+------------------------------------------------------------+--------------------+--------+------------+
| Tool              | URL                                                        | Public             | VPN[1] | Private[2] |
+===================+============================================================+====================+========+============+
| grafana           | https://grafana.softwareheritage.org                       | X                  |        |            |
+-------------------+------------------------------------------------------------+--------------------+--------+------------+
| Kibana            | http://kibana0.internal.softwareheritage.org:5601          |                    | X      |            |
+-------------------+------------------------------------------------------------+--------------------+--------+------------+
| Log Elasticsearch | search[1-4,7].internal.softwareheritage.org:9200           |                    | X      |            |
+-------------------+------------------------------------------------------------+--------------------+--------+------------+
| C.M.A.K.          | http://getty.internal.softwareheritage.org:9000            |                    | X      |            |
+-------------------+------------------------------------------------------------+--------------------+--------+------------+
| Sentry            | https://sentry.softwareheritage.org                        | X (authentication) |        |            |
+-------------------+------------------------------------------------------------+--------------------+--------+------------+
| Reaper Staging    | https://reaper.internal.staging.swh.network                |                    | X      |            |
+-------------------+------------------------------------------------------------+--------------------+--------+------------+
| Reaper Production | https://reaper.internal.softwareheritage.org               |                    | X      |            |
+-------------------+------------------------------------------------------------+--------------------+--------+------------+
| ArgoCD            | https://argocd.internal.admin.swh.network                  |                    | X      |            |
+-------------------+------------------------------------------------------------+--------------------+--------+------------+

[1] VPN: URL only accessible when connected to the SoftwareHeritage VPN

[2] Private: URL only accessible from the internal network, i.e nor public neither accessible through the VPN.

[3] Use banco and saam as underlying objstorage

[4] Protected by a basic authentication. Credentials are available in the credential store.

[5] Use AWS/banco and saam/Azure in this order as underlying objstorage
