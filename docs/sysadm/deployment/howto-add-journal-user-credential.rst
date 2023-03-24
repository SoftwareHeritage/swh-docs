.. _deployment-howto-add-journal-user-credential:

How to add journal user credential
==================================

.. admonition:: Intended audience
   :class: important

   sysadm members

.. _deployment-journal-user-naming-rules:

User naming rules
-----------------

The convention in place for the mirroring credentials are the following:

The names are composed of three parts: ``<short>-<environment>-<id>``

- A short meaningful name relative to the mirror company/owner. For example ``acme``.
  For a Software Heritage internal account, the name must be ``swh-<account name>``. For
  example: ``swh-jdoe``
- The environment: ``stg`` for staging, ``prod`` for production
- A counter if several accounts are needed for the same environment

Examples of correct names:

- ``acme-stg-01``
- ``acme-stg-02``
- ``acme-prod-01``
- ``swh-jdoe-stg-01``
- ``swh-jdoe-prod-01``

.. _deployment-journal-user-create-journal-credentials:

How to create the journal credentials
-------------------------------------

Connect on the journal orchestrator server (production: getty, staging: journal0).

A script per existing kafka cluster is created by puppet in the ``/usr/local/sbin`` directory.
The file name follow this pattern: ``create_kafka_users_<cluster name>.sh``

The different clusters are:

- ``rocquencourt``: production journal
- ``rocquencourt_staging``: staging journal

For example, to add a user ``new-mirror-stg`` in the staging's journal:

.. code-block:: bash

   ORCHESTRATOR=getty.internal.softwareheritage.org
   USER=new-mirror-stg
   ssh $ORCHESTRATOR
   sudo /usr/local/sbin/create_kafka_users_rocquencourt_staging.sh $USER

   root@getty:/usr/local/sbin# ./create_kafka_users_rocquencourt_staging.sh mirror-test
   Creating user mirror-test-stg, with unprivileged access to consumer group prefix mirror-test-stg-
   Password for user mirror-test-stg: <---- Enter the user password here
   Setting user credentials
   Warning: --zookeeper is deprecated and will be removed in a future version of Kafka.
   Use --bootstrap-server instead to specify a broker to connect to.
   Completed updating config for entity: user-principal 'mirror-test-stg'.
   Granting access to topics swh.journal.objects. to mirror-test-stg
   Adding ACLs for resource `ResourcePattern(resourceType=TOPIC, name=swh.journal.objects., patternType=PREFIXED)`:
       (principal=User:mirror-test-stg, host=*, operation=READ, permissionType=ALLOW)

   Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=swh.journal.objects., patternType=PREFIXED)`:
       (principal=User:mirror-test, host=*, operation=READ, permissionType=ALLOW)
      (principal=User:mirror-test, host=*, operation=DESCRIBE, permissionType=ALLOW)
      (principal=User:mirror-test-stg, host=*, operation=READ, permissionType=ALLOW)

   Adding ACLs for resource `ResourcePattern(resourceType=TOPIC, name=swh.journal.objects., patternType=PREFIXED)`:
       (principal=User:mirror-test-stg, host=*, operation=DESCRIBE, permissionType=ALLOW)

   Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=swh.journal.objects., patternType=PREFIXED)`:
       (principal=User:mirror-test, host=*, operation=READ, permissionType=ALLOW)
      (principal=User:mirror-test, host=*, operation=DESCRIBE, permissionType=ALLOW)
      (principal=User:mirror-test-stg, host=*, operation=READ, permissionType=ALLOW)
      (principal=User:mirror-test-stg, host=*, operation=DESCRIBE, permissionType=ALLOW)

   Granting access to topics swh.journal.indexed. to mirror-test-stg
   Adding ACLs for resource `ResourcePattern(resourceType=TOPIC, name=swh.journal.indexed., patternType=PREFIXED)`:
       (principal=User:mirror-test-stg, host=*, operation=READ, permissionType=ALLOW)

   Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=swh.journal.indexed., patternType=PREFIXED)`:
       (principal=User:mirror-test, host=*, operation=DESCRIBE, permissionType=ALLOW)
      (principal=User:mirror-test, host=*, operation=READ, permissionType=ALLOW)
      (principal=User:mirror-test-stg, host=*, operation=READ, permissionType=ALLOW)

   Adding ACLs for resource `ResourcePattern(resourceType=TOPIC, name=swh.journal.indexed., patternType=PREFIXED)`:
       (principal=User:mirror-test-stg, host=*, operation=DESCRIBE, permissionType=ALLOW)

   Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=swh.journal.indexed., patternType=PREFIXED)`:
       (principal=User:mirror-test, host=*, operation=DESCRIBE, permissionType=ALLOW)
      (principal=User:mirror-test, host=*, operation=READ, permissionType=ALLOW)
      (principal=User:mirror-test-stg, host=*, operation=READ, permissionType=ALLOW)
      (principal=User:mirror-test-stg, host=*, operation=DESCRIBE, permissionType=ALLOW)

   Granting access to consumer group prefix mirror-test-stg- to mirror-test-stg
   Adding ACLs for resource `ResourcePattern(resourceType=GROUP, name=mirror-test-stg-, patternType=PREFIXED)`:
       (principal=User:mirror-test-stg, host=*, operation=READ, permissionType=ALLOW)

   Current ACLs for resource `ResourcePattern(resourceType=GROUP, name=mirror-test-stg-, patternType=PREFIXED)`:
       (principal=User:mirror-test-stg, host=*, operation=READ, permissionType=ALLOW)

