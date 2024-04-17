.. _how-to-add-forge-now-process-requests:

How to process add-forge-now requests
=====================================

.. admonition:: Intended audience
   :class: important

   sysadm staff members

The processing is semi-automatic for the moment. Referencing the steps is a kickstarter
for automation.


Introduction
------------

A forge ticket (`see for example the git.afpy.org ticket
<https://gitlab.softwareheritage.org/infra/sysadm-environment/-/issues/4674>`_) should
have been opened by a moderator.

Meaning the `moderation process is ongoing
<https://archive.softwareheritage.org/admin/add-forge/request/18/>`_ and the upstream
forge (to be ingested) has been notified we will start the ingestion soon.

Note that there exists roughly 2 kinds of forges, either the technology used by the
forge exists is mono-instance (e.g. github, bitbucket, ...), either the technology is
the same across multiple forges (e.g. gitlab, cgit, gitea, gogs).


.. _add-forge-now-testing-on-staging:

Testing on staging
------------------

To ensure we can ingest that forge, we start by testing out a subset of that forge
listing on staging. It's a pre-check flight to determine we have the right amount of
information.

Mono-instance forge listing
^^^^^^^^^^^^^^^^^^^^^^^^^^^

For mono-instance forge or for multi-instance forge whose url cannot be computed easily,
(e.g. some cgit instance with a subdomain), we provide the ``<url>`` of the forge to
ingest.

.. code::

   swh scheduler --url http://scheduler0.internal.staging.swh.network:5008/ \
     add-forge-now --preset staging \
       register-lister gitea \
         url=<url>

For example, forge `git.replicant.us <https://git.replicant.us/infrastructure>`_ which
is a cgit instance, we'd run:

.. code::

   swh scheduler --url http://scheduler0.internal.staging.swh.network:5008/ \
     add-forge-now --preset staging \
       register-lister cgit \
         url=https://git.replicant.us/infrastructure


Multi-instance forge listing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We currently support the technology gitea, gogs and gitlab which are multi-instance. The
corresponding listers are able to compute their api url directly (to avoid manual
mistakes) so we just need to provide the <instance> parameter for those.

.. code::

   swh scheduler --url http://scheduler0.internal.staging.swh.network:5008/ \
     add-forge-now --preset staging \
       register-lister gitea \
         instance=<instance>


For example, the forge `git.afpy.org <https://git.afpy.org>`_ is a `gitea
<https://gitea.io/en-us/>`_ instance, so we'd run:

.. code::

   swh scheduler --url http://scheduler0.internal.staging.swh.network:5008/ \
     add-forge-now --preset staging \
       register-lister gitea \
         instance=git.afpy.org

   INFO:swh.lister.pattern:Max origins per page set, truncated 36 page results down to 30
   INFO:swh.lister.pattern:Disabling origins before sending them to the scheduler
   INFO:swh.lister.pattern:Reached page limit of 3, terminating


Ensure the :ref:`lister got registered<check-lister-is-registered>` in the staging
scheduler db.

Forge's listed origin ingestion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After the previous lister registration, we now need to trigger the first ingestion for
those origins:

.. code::

   swh scheduler --url http://scheduler0.internal.staging.swh.network:5008/ \
     add-forge-now --preset staging \
     schedule-first-visits \
       --type-name <visit-type> \
       --type-name <another-visit-type> \
       --lister-name <lister> \
       --lister-instance-name <lister-instance-name>

For example, for one of the instance listed above:

.. code::

   swh scheduler --url http://scheduler0.internal.staging.swh.network:5008/ \
     add-forge-now --preset staging \
     schedule-first-visits \
       --type-name git \
       --lister-name gitea \
       --lister-instance-name git.afpy.org

   100 slots available in celery queue
   15 visits to send to celery

After some time, :ref:`check those origins got ingested at least in part
<check-origins-got-ingested>`.

If everything is fine, let's :ref:`schedule that forge in production
<add-forge-now-deploying-on-production>`.


.. _add-forge-now-deploying-on-production:

Deploying on production
-----------------------

After :ref:`testing with success the forge ingestion in staging
<add-forge-now-testing-on-staging>`, it's time to deploy the full and recurrent listing
for that forge.

Let's start by registering the lister for that forge as usual (use the same method as
above):

.. code::

   swh scheduler --url http://saatchi.internal.softwareheritage.org:5008/ \
     add-forge-now ( --preset production ) \
     register-lister <lister-name> \
       url=<url>

.. code::

   swh scheduler --url http://saatchi.internal.softwareheritage.org:5008/ \
     add-forge-now ( --preset production ) \
     register-lister <lister-name> \
       instance=<instance>

For example:

.. code::

   swh scheduler --url http://saatchi.internal.softwareheritage.org:5008/ \
     add-forge-now ( --preset production ) \
     register-lister gitea \
       instance=git.afpy.org

Ensure the :ref:`lister got registered<check-lister-is-registered>` in the production
scheduler db.

After a bit of time, you can :ref:`check origins from that forge got listed
<check-origins-got-listed>` in the scheduler db:

Once the listing is through, we trigger the add-forge-now scheduling to make a first
pass on that forge.

.. code::

   swh scheduler --url http://saatchi.internal.softwareheritage.org:5008/ \
     add-forge-now ( --preset production ) \
       schedule-first-visits \
         --type-name <visit-type> \
         --lister-name <lister-name> \
         --lister-instance-name <lister-instance-name>

For example:

.. code::

   swh scheduler --url http://saatchi.internal.softwareheritage.org:5008/ \
     add-forge-now ( --preset production ) \
       schedule-first-visits \
         --type-name git \
         --lister-name gitea \
         --lister-instance-name git.afpy.org

   10000 slots available in celery queue
   37 visits to send to celery

After a while, :ref:`you can check those origins should have been ingested in part
<check-origins-got-ingested>`. You can now notify the moderator in the ticket that the
first ingestion got done.

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
