.. _postgresql_connect:

How to connect to PostgreSQL databases
======================================

.. admonition:: Intended audience
   :class: important

   Members of the Software Heritage staff who need access to do raw queries on
   databases.

.. warning:: There are performance implications for the whole infrastructure
   (ingestion as well as public access) on long running queries on production
   databases; when in doubt, please make sure that you've notified the sysadmin
   team before using raw database queries

To connect to Software Heritage PostgreSQL databases, you need access to the VPN.

To simplify connections we rely on:

- |pg_service|_: DB connection aliases
- |pgpass|_: DB access credentials (not needed for read-only queries)

Sample content for both files follows, referencing actual databases that you might need to access.

.. |pg_service| replace:: ``~/.pg_service.conf``
.. _pg_service: https://www.postgresql.org/docs/current/static/libpq-pgservice.html

.. |pgpass| replace:: ``~/.pgpass``
.. _pgpass: https://www.postgresql.org/docs/current/static/libpq-pgpass.html

Sample |pg_service|
-------------------

::

  [swh]
  dbname=softwareheritage
  host=postgresql-storage-rw.internal.softwareheritage.org
  user=guest

  [swh-replica]
  dbname=softwareheritage
  host=postgresql-storage-replica.internal.softwareheritage.org
  user=guest
  port=5432

  [swh-deposit]
  dbname=softwareheritage-deposit
  host=postgresql-deposit-rw.internal.softwareheritage.org
  user=guest
  port=5432

  [swh-indexer]
  dbname=softwareheritage-indexer
  host=postgresql-indexer-rw.internal.softwareheritage.org
  user=guest
  port=5432

  [swh-scheduler]
  dbname=softwareheritage-scheduler
  host=postgresql-scheduler-rw.internal.softwareheritage.org
  user=guest

  [swh-vault]
  dbname=swh-vault
  host=postgresql-vault-rw.internal.softwareheritage.org
  port=5432
  user=guest

  [swh-scrubber]
  dbname=swh-scrubber
  host=postgresql-scrubber-rw.internal.softwareheritage.org
  port=5432
  user=guest

  [admin-swh-scrubber]
  dbname=swh-scrubber
  host=postgresql-scrubber-rw.internal.softwareheritage.org
  port=5432
  user=swh-scrubber

  [swh-masking]
  dbname=swh-masking
  host=postgresql-masking-rw.internal.softwareheritage.org
  port=5432
  user=guest

  [admin-swh-masking]
  dbname=swh-masking
  host=postgresql-masking-rw.internal.softwareheritage.org
  port=5432
  user=swh-masking

  [staging-swh-coar-notify]
  dbname=swh-coar-notify
  host=db.internal.staging.swh.network
  port=5432
  user=guest

  [staging-swh-deposit]
  dbname=swh-deposit
  host=db.internal.staging.swh.network
  port=5432
  user=guest

  [staging-swh-scheduler]
  dbname=swh-scheduler
  host=db.internal.staging.swh.network
  port=5432
  user=guest

  [staging-swh-scrubber]
  dbname=swh-scrubber
  host=db.internal.staging.swh.network
  port=5432
  user=guest

  [staging-swh-svix]
  dbname=swh-svix
  host=db.internal.staging.swh.network
  port=5432
  user=guest

  [staging-swh-vault]
  dbname=swh-vault
  host=db.internal.staging.swh.network
  port=5432
  user=guest

  [staging-swh-web]
  dbname=swh-web
  host=db.internal.staging.swh.network
  port=5432
  user=guest

  [staging-swh]
  dbname=swh
  host=db1.internal.staging.swh.network
  port=5432
  user=guest

  [staging-swh-indexer]
  dbname=swh-indexer
  host=db.internal.staging.swh.network
  port=5432
  user=guest

With this file, you can connect to any DB like this:

::

  psql service=ALIAS

for ``ALIAS`` in ``swh``, ``swh-replica``, ``swh-indexer``, ...

Sample |pgpass|
---------------

.. note:: The |pgpass| file is needed for read-only (``guest``) and read-write access to
   databases.

::

  # hostname:port:database:username:password
  db.internal.softwareheritage.org:*:*:<login>:<password>
  somerset.internal.softwareheritage.org:*:*:<login>:<password>

.. warning:: |pgpass| should be made readable only by your user (``chmod 600
   ~/.pgpass``)
