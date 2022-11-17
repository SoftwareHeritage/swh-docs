.. _mirror_onboard:

How to onboard a mirror
=======================

.. admonition:: Intended audience
   :class: important

   sysadm staff members

A mirror needs credentials to access our journal and to retrieve the contents.

They are manually created by a software Heritage System Administrator.
**Different credentials must be provided for staging and production.**

The URLs to communicate to the mirror operator are defined in :ref:`service-url`
in the 'Public URLs' sections, ``Journal TLS`` entries and ``swh-objstorage read-only``.

User naming rules
-----------------

The convention in place for the mirroring credentials are the following:

The names are composed of three parts: ``<short>-<environment>-<id>``

- A short meaningful name relative to the mirror company/owner. For example ``acme``.
  For a Software Heritage internal account, the name must be ``swh-<account name>``. For example: ``swh-jdoe``
- The environment: ``stg`` for staging, ``prod`` for production
- A counter if several accounts are needed for the same environment

Examples of correct names:

- ``acme-stg-01``
- ``acme-stg-02``
- ``acme-prod-01``
- ``swh-jdoe-stg-01``
- ``swh-jdoe-prod-01``

How to create the journal credentials
-------------------------------------

Connect on the journal orchestrator server (getty)

A script per existing kafka cluster is created by puppet in the ``/usr/local/sbin`` directory.
The file name follow this pattern: ``create_kafka_user_<cluster name>.sh``

The different clusters are:

- ``rocquencourt``: production journal
- ``rocquencourt_staging``: staging journal

For example, to add a user ``new-mirror-stg`` in the staging's journal:

.. code-block:: bash

   ssh getty.internal.softwareheritage.org
   sudo /usr/local/sbin/create_kafka_user_rocquencourt_staging.sh new-mirror-stg

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


How to use the credentials
--------------------------

Refer to the :ref:`journal client authentication configuration <swh-devel:journal-client-authentication>`.

How to create the objstorage credentials
----------------------------------------

The read-only public storages are protected by an basic authentication mechanism.
To allow a mirror to retrieve the content files, they need to have valid credentials.

These credentials are managed and deployed by puppet.

To add a credential in the puppet configuration:

- for staging:

  - locate the ``swh::deploy::objstorage::reverse_proxy::basic_auth::users``
    property in the `data/deployment/staging/common.yaml` file
  - add the username in the list

- for production
   - locate the ``swh::deploy::objstorage::reverse_proxy::basic_auth::users``
     property in the `data/common/common.yaml` file
   - add the username in the list

- Add an entry ``swh::deploy::objstorage::reverse_proxy::basic_auth::<<username>>``
  in the ``private/swh-private-data/common.yaml``
- in the ``private`` directory of your puppet sources, execute the following command
  to refresh the censored credentials (used by octocatalog-diff and vagrant):

.. code-block:: bash

   private_data/generate-public-data swh-private-data swh-private-data-censored

- Deploy the changes to the puppet master

