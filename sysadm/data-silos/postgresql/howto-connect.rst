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

.. |pg_service| replace:: ``~/pg_service.conf``
.. _pg_service: https://www.postgresql.org/docs/current/static/libpq-pgservice.html

.. |pgpass| replace:: ``~/.pgpass``
.. _pgpass: https://www.postgresql.org/docs/current/static/libpq-pgpass.html

Sample |pg_service|
-------------------

::

  [swh]
  dbname=softwareheritage
  host=db.internal.softwareheritage.org
  user=guest

  [swh-replica]
  dbname=softwareheritage
  host=somerset.internal.softwareheritage.org
  user=guest
  port=5432

  [swh-archiver]
  dbname=softwareheritage-archiver
  host=db.internal.softwareheritage.org
  user=guest

  [swh-indexer]
  dbname=softwareheritage-indexer
  host=belvedere.internal.softwareheritage.org
  user=guest
  port=5432

  [swh-scheduler]
  dbname=softwareheritage-scheduler
  host=db.internal.softwareheritage.org
  user=guest

  [staging-swh]
  dbname=swh
  host=db1.internal.staging.swh.network
  port=5432
  user=guest

  [admin-staging-swh]
  dbname=swh
  host=db1.internal.staging.swh.network
  port=5432
  user=swh

  [staging-swh-indexer]
  dbname=swh-indexer
  host=db1.internal.staging.swh.network
  port=5432
  user=guest

  [admin-staging-swh-indexer]
  dbname=swh-indexer
  host=db1.internal.staging.swh.network
  port=5432
  user=swh-indexer

  [staging-swh-scheduler]
  dbname=swh-scheduler
  host=db1.internal.staging.swh.network
  port=5432
  user=guest

  [admin-staging-swh-scheduler]
  dbname=swh-scheduler
  host=db1.internal.staging.swh.network
  port=5432
  user=swh-scheduler

  [staging-swh-deposit]
  dbname=swh-deposit
  host=db1.internal.staging.swh.network
  port=5432
  user=guest

  [admin-staging-swh-deposit]
  dbname=swh-deposit
  host=db1.internal.staging.swh.network
  port=5432
  user=swh-deposit

  [staging-swh-vault]
  dbname=swh-vault
  host=db1.internal.staging.swh.network
  port=5432
  user=guest

  [admin-staging-swh-vault]
  dbname=swh-vault
  host=db1.internal.staging.swh.network
  port=5432
  user=swh-vault

  [staging-swh-lister]
  dbname=swh-lister
  host=db1.internal.staging.swh.network
  port=5432
  user=guest

  [admin-staging-swh-lister]
  dbname=swh-lister
  host=db1.internal.staging.swh.network
  port=5432
  user=swh-lister

With this file, you can connect to any DB like this:

::

  psql service=ALIAS

for ``ALIAS`` in ``swh``, ``swh-replica``, ``swh-indexer``, ...

Sample |pgpass|
---------------

.. note:: The |pgpass| file is not needed for guest (read-only) access to
   databases. You will only need it for read-write access.

::

  # hostname:port:database:username:password
  db.internal.softwareheritage.org:*:*:<login>:<password>
  somerset.internal.softwareheritage.org:*:*:<login>:<password>

.. warning:: |pgpass| should be made readable only by your user (``chmod 600
   ~/.pgpass``)
