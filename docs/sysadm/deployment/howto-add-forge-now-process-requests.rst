.. _how-to-add-forge-now-process-requests:

How to process add-forge-now requests
=====================================

.. admonition:: Intended audience
   :class: important

   sysadm staff members

The processing is automatic but may encounter errors.
In this case, the operations must be performed manually (see, :ref:`how-to-add-forge-now-pipeline`).

Introduction
------------

A forge ticket (`see for example the forge.inrae.fr ticket
<https://gitlab.softwareheritage.org/swh/infra/add-forge-now-requests/-/issues/1431>`_) should
have been created.

Meaning the `moderation process is ongoing
<https://archive.softwareheritage.org/admin/add-forge/request/1904/>`_ and the upstream
forge (to be ingested) has been notified we will start the ingestion soon.

Note that there exists roughly 2 kinds of forges, either the technology used by the
forge exists is mono-instance (e.g. github, bitbucket, ...), either the technology is
the same across multiple forges (e.g. gitlab, cgit, gitea, gogs).

All processing operations are performed from the Kubernetes toolbox pod.

.. code::

   kubectl --context archive-staging-rke2 exec -ti -n swh-cassandra -c swh-toolbox deployment/swh-toolbox -- bash

Use the same command with ``archive-production-rke2`` context to access production toolbox.

.. admonition:: ``SWH_CONFIG_FILENAME`` variable
   :class: warning

   Once connected to the toolbox, you must export ``SWH_CONFIG_FILENAME`` with the scheduler configuration.
   The output of the toolbox mentions the right export command.

   .. code::

      ᐅ kubectl --context archive-staging-rke2 exec -ti -n swh-cassandra -c swh-toolbox deployment/swh-toolbox -- bash
      SWH_CONFIG_FILENAME variable is not set!

       This variable must be defined according to your use case (e.g. .
       scheduler, storage, vault, ...). You must define it by yourself.

       For example, use one of the following:

      export SWH_CONFIG_FILENAME=/etc/swh/config-web.yml
      export SWH_CONFIG_FILENAME=/etc/swh/config-masking.yml
      export SWH_CONFIG_FILENAME=/etc/swh/config-scrubber-objstorage-storage1.yml
      export SWH_CONFIG_FILENAME=/etc/swh/config-webhooks.yml
      export SWH_CONFIG_FILENAME=/etc/swh/config-cassandra-storage-rw.yml
      export SWH_CONFIG_FILENAME=/etc/swh/config-indexer-storage.yml
      export SWH_CONFIG_FILENAME=/etc/swh/config-vault.yml
      export SWH_CONFIG_FILENAME=/etc/swh/config-scrubber-objstorage-db1.yml
      export SWH_CONFIG_FILENAME=/etc/swh/config-scheduler.yml
      export SWH_CONFIG_FILENAME=/etc/swh/config-deposit.yml
      export SWH_CONFIG_FILENAME=/etc/swh/config-scrubber-storage.yml
      export SWH_CONFIG_FILENAME=/etc/swh/config-blocking.yml
      swh@swh-toolbox-57d6b657d-tqn4m:~$ export SWH_CONFIG_FILENAME=/etc/swh/config-scheduler.yml

.. _add-forge-now-testing-on-staging:

Testing on staging
------------------

To ensure we can ingest that forge, we start by testing out a subset of that forge
listing on staging. It's a pre-check flight to determine we have the right amount of
information.

Registering the new lister task
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code::

   swh scheduler \
     add-forge-now --preset staging \
       register-lister <lister-type> \
         instance=<instance>

For example, forge `forge.inrae.fr <https://forge.inrae.fr/>`_ which
is a gitlab instance, we'd run:

.. code::

   swh@swh-toolbox-57d6b657d-tqn4m:~$ swh scheduler \
     add-forge-now --preset staging \
       register-lister gitlab \
         instance=forge.inrae.fr

   WARNING:swh.core.sentry:Sentry DSN not provided, events will not be sent.
   Created 1 tasks
   Task 33438839
     Next run: today (2025-07-23T15:44:45.811986+00:00)
     Interval: 90 days, 0:00:00
     Type: list-gitlab-full
     Policy: oneshot
     Args:
     Keyword args:
       enable_origins: False
       instance: 'forge.inrae.fr'
       max_origins_per_page: 5
       max_pages: 2

``instance`` is the parameter used in the `pipeline <https://gitlab.softwareheritage.org/swh/infra/add-forge-now-requests/-/blob/main/.gitlab-ci/bash-functions.sh?ref_type=heads#L121>`_.
It may be necessary to use ``url`` parameter instead of the ``instance`` one:

- for forges which support only http protocol;

   .. code::

      swh@swh-toolbox-798fd68874-zx4wp:~$ swh scheduler \
        add-forge-now --preset production \
          register-lister gitea \
            url=http://vcc-gnd.cn/api/v1/

- for forges reachable by a subpath.

   .. code::

      swh@swh-toolbox-76f4dcdb79-ncrvt:~$ swh scheduler \
        add-forge-now --preset staging \
          register-lister gitlab \
            url=https://microfluidics.utoronto.ca/gitlab/api/v4/

Use ``base_git_url`` to specify the origins url:

.. code::

   swh@swh-toolbox-648b4bd4dd-tjh4c:~$ swh scheduler \
     add-forge-now --preset staging \
       register-lister cgit \
         instance=git.koszko.org \
         base_git_url=https://git.koszko.org

Or use ``url`` and ``base_git_url``:

.. code::

   swh@swh-toolbox-76b76c5565-spw77:~$ swh scheduler \
     add-forge-now --preset staging \
       register-lister gitweb \
       url=http://git.1wt.eu/web \
       base_git_url=http://git.1wt.eu/git

Ensure the :ref:`lister got registered<check-lister-is-registered>` in the staging
scheduler db.

Checking the listed origins
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code::

   swh scheduler origin check-listed-origins <lister-type> <instance-name> -l

For our example, `forge.inrae.fr <https://forge.inrae.fr/>`_:

.. code::

   swh@swh-toolbox-57d6b657d-tqn4m:~$ swh scheduler origin check-listed-origins gitlab forge.inrae.fr -l
   url                                                           last_seen                         last_update
   ------------------------------------------------------------  --------------------------------  --------------------------------
   https://forge.inrae.fr/QTL/spell-qtl.git                      2025-07-23 15:45:48.892705+00:00  2020-02-27 20:56:28.539000+00:00
   https://forge.inrae.fr/adminforgemia/doc-public.git           2025-07-23 15:45:48.892705+00:00  2024-09-09 12:53:34.058000+00:00
   https://forge.inrae.fr/bioger/django-custom-user.git          2025-07-23 15:45:49.655780+00:00  2023-11-08 14:53:09.962000+00:00
   https://forge.inrae.fr/gauthier.quesnel/red-slides.git        2025-07-23 15:45:49.655780+00:00  2019-07-03 06:53:00.720000+00:00
   https://forge.inrae.fr/genotoul-bioinfo/d-genies/dgenies.git  2025-07-23 15:45:48.892705+00:00  2025-02-06 14:49:33.746000+00:00
   https://forge.inrae.fr/genotoul-bioinfo/jflow.git             2025-07-23 15:45:48.892705+00:00  2020-02-14 16:08:06.932000+00:00
   https://forge.inrae.fr/katharina-birgit.budde/testgit.git     2025-07-23 15:45:49.655780+00:00  2019-07-05 09:21:53.092000+00:00
   https://forge.inrae.fr/olivier.bonnefon/selommes.git          2025-07-23 15:45:49.655780+00:00  2019-07-25 12:48:39.151000+00:00
   https://forge.inrae.fr/svdetection/popsim.git                 2025-07-23 15:45:48.892705+00:00  2020-02-28 07:17:22.123000+00:00
   https://forge.inrae.fr/umr-gdec/magatt.git                    2025-07-23 15:45:49.655780+00:00  2025-07-18 12:15:54.773000+00:00

   Forge forge.inrae.fr (gitlab) has 10 listed origins in the scheduler database.

Scheduling the first visit
^^^^^^^^^^^^^^^^^^^^^^^^^^

After the previous lister registration, we now need to trigger the first ingestion for
those origins:

.. code::

   swh scheduler \
     add-forge-now --preset staging \
     schedule-first-visits \
       --type-name <visit-type> \
       --lister-name <lister> \
       --lister-instance-name <lister-instance-name>

For our example, `forge.inrae.fr <https://forge.inrae.fr/>`_:

.. code::

   swh scheduler \
     add-forge-now --preset staging \
     schedule-first-visits \
       --type-name git \
       --lister-name gitlab \
       --lister-instance-name forge.inrae.fr

   WARNING:swh.core.sentry:Sentry DSN not provided, events will not be sent.
   INFO:swh.scheduler.celery_backend.utils:1000 slots available in celery queue add_forge_now:swh.loader.git.tasks.UpdateGitRepository
   INFO:swh.scheduler.celery_backend.utils:10 visits of type git to send to celery

.. admonition:: AFN loaders logs
   :class: tip

   Get the add-forge-now loaders logs:

   .. code::

      kubectl --context archive-staging-rke2 logs -n swh-cassandra -l app=loader-add-forge-now -f

   .. code::

      stern --context archive-staging-rke2 -n swh-cassandra -l app=loader-add-forge-now --only-log-lines

   Use the same commands with ``archive-production-rke2`` context for production environment.

Checking the ingested origins
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code::

   swh scheduler origin check-ingested-origins <lister-type> <instance-name>

For our example, `forge.inrae.fr <https://forge.inrae.fr/>`_:

.. code::

   swh@swh-toolbox-57d6b657d-tqn4m:~$ swh scheduler origin check-ingested-origins gitlab forge.inrae.fr

   Forge forge.inrae.fr (gitlab) has 10 scheduled ingests in the scheduler.
   failed      : 0
   None        : 0
   not_found   : 1
   successful  : 9
   total       : 10
   success rate: 90.00%

After some time, :ref:`check those origins were ingested at least partially
<check-origins-got-ingested>`.

If everything is fine, update the add-forge-now request status to ``Scheduled``
with a comment containing a link to the GitLab Issue. Then, let's :ref:`schedule that forge in production
<add-forge-now-deploying-on-production>`.

.. _add-forge-now-deploying-on-production:

Deploying on production
-----------------------

After :ref:`testing with success the forge ingestion in staging
<add-forge-now-testing-on-staging>`, it's time to deploy the full and recurrent listing
for that forge.

.. admonition:: Production environment

   Use the same commands as for staging, replacing the value of the ``--preset`` option with ``production``.

After some time, :ref:`you can check those origins have been ingested
<check-origins-got-ingested>`.
If everything is fine, update the add-forge-now request status to ``First origin loaded``
with a comment containing a link to the GitLab Issue.

.. _add-forge-now-checks:

Usual checks
------------

In the following, we will demonstrate the usual checks happening in the scheduler db.
The format will be the generic query to execute followed by an actual execution (with a
sampled output).

.. _check-lister-is-registered:

Check the lister is registered
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code::

   select * from listers
   where name='<lister-name>' and
   instance_name='<lister-instance>';

Example:

.. code::

   2022-12-06 11:50:17 swh-scheduler@db1:5432 λ \
       select * from listers
       where name='gitea' and
       instance_name='git.afpy.org';

   +--------------------------------------+-------+---------------+-------------------------------+
   |                  id                  | name  | instance_name |            created            | ...
   +--------------------------------------+-------+---------------+-------------------------------+
   | d07d1c90-5016-4ab6-91ac-3300f8eb4fc6 | gitea | git.afpy.org  | 2022-12-06 10:47:46.975571+00 |
   +--------------------------------------+-------+---------------+-------------------------------+
   (1 row)

   Time: 4.109 ms

.. _check-origins-got-listed:

Check origins got listed
^^^^^^^^^^^^^^^^^^^^^^^^

.. code::

   select lister_id, url, visit_type from listed_origins
   where lister_id = (select id from listers
                      where name='<lister-name>'
                      and instance_name='<lister-instance-name>');

Example:

.. code::

   2022-12-06 11:50:24 swh-scheduler@db1:5432 λ \
       select lister_id, url, visit_type from listed_origins
       where lister_id = (select id from listers
                          where name='gitea' and
                          instance_name='git.afpy.org');

   +--------------------------------------+-----------------------------------------------------------+------------+
   |              lister_id               |                            url                            | visit_type |
   +--------------------------------------+-----------------------------------------------------------+------------+
   | d07d1c90-5016-4ab6-91ac-3300f8eb4fc6 | https://git.afpy.org/AFPy/afpy.org.git                    | git        |
   | d07d1c90-5016-4ab6-91ac-3300f8eb4fc6 | https://git.afpy.org/foxmask/baeuda.git                   | git        |
   | d07d1c90-5016-4ab6-91ac-3300f8eb4fc6 | https://git.afpy.org/fcode/boilerplate-python.git         | git        |
   ...
   +--------------------------------------+-----------------------------------------------------------+------------+
   (15 rows)

   Time: 1225.399 ms (00:01.225)


.. _check-origins-got-ingested:

Check origins got ingested
^^^^^^^^^^^^^^^^^^^^^^^^^^

Either one of the query is fine:

.. code::

   select visit_type, url, last_visit_status from origin_visit_stats
   where visit_type='<visit-type>'
     and url like 'https://<lister-instance-name>%';

Example:

.. code::

   2022-12-12 12:08:58 softwareheritage-scheduler@belvedere:5432 λ \
       select visit_type, url, last_visit_status from origin_visit_stats
       where visit_type='git' and
       url like 'https://git.afpy.org%';

   +------------+-----------------------------------------------------------+-------------------+
   | visit_type |                            url                            | last_visit_status |
   +------------+-----------------------------------------------------------+-------------------+
   | git        | https://git.afpy.org/mdk/infra.git                        | successful        |
   | git        | https://git.afpy.org/ChristopheNan/python-docs-fr.git     | successful        |
   | git        | https://git.afpy.org/fcode/delarte.git                    | successful        |
   ...
   +------------+-----------------------------------------------------------+-------------------+
   (37 rows)

   Time: 95171.399 ms (01:35.171)

or this one, though this will take longer to execute:

.. code::

   select last_visit_status, count(ovs.url)
   from origin_visit_stats ovs
   join listed_origins lo USING(url, visit_type)
   where lister_id = (select id from listers where name='<lister-name>'
                      and instance_name='<lister-instance-name>')

Example:

.. code::

   2022-12-12 11:56:57 softwareheritage-scheduler@belvedere:5432 λ \
       select last_visit_status, count(ovs.url)
       from origin_visit_stats ovs
       join listed_origins lo USING(url, visit_type)
       where lister_id = (select id from listers
                          where name='gitea' and
                          instance_name='git.afpy.org')
       and visit_type='git'
       group by last_visit_status;

   +-------------------+-------+
   | last_visit_status | count |
   +-------------------+-------+
   | successful        |    37 |
   +-------------------+-------+
   (1 row)

   Time: 149774.756 ms (02:29.775)

Check duplicated tasks
^^^^^^^^^^^^^^^^^^^^^^

.. code::

   select id, arguments, status from task
     where arguments -> 'kwargs' ->> 'instance' like '%<domain_name>%'
     or arguments -> 'kwargs' ->> 'url' like '%<domain_name>%'
     and policy = 'recurring';

Example:

.. code::

   softwareheritage-scheduler=> select id, arguments, status from task
     where arguments -> 'kwargs' ->> 'instance' like '%codeberg.org%'
     or arguments -> 'kwargs' ->> 'url' like '%codeberg.org%'
     and policy = 'recurring';
       id     |                            arguments                            |         status
   -----------+-----------------------------------------------------------------+------------------------
    415431745 | {"args": [], "kwargs": {"instance": "codeberg.org"}}            | next_run_not_scheduled
    337306005 | {"args": [], "kwargs": {"url": "https://codeberg.org/api/v1/"}} | next_run_not_scheduled
   (2 rows)
