.. _storage-database-migration:

How to handle a storage database migration
==========================================

.. admonition:: Intended audience
   :class: important

   sysadm staff members

If a storage database upgrade is needed, a migration script should already exists in the
*swh-storage* git repository.

.. _upgrade_version:

Upgrade version
---------------

Check the current database version (first one in desc order):

.. code:: sql

   select dbversion from dbversion order by version desc limit 1;

Say, for example that the result is 159 here.

Check the migration script folder in swh-storage:/sql/upgrades/ (and find the next one,
for example `160.sql
<https://forge.softwareheritage.org/source/swh-storage/browse/master/sql/upgrades/160.sql>`_).
It's previous version number + 1 from the given db version retrieved (so 160 with the
current example).

Note: That you could need to run more than one migration. It depends on the current
packaged version and the next version we want to deploy. Check the git history to
determine that.

Requisite
---------

Ensure the migration script runs first in the staging database
(db0.internal.staging.swh.network is the node holding the swh staging database). Then
you can go ahead and run it in production database
(belvedere.internal.softwareheritage.org).

Connect to the db with the user with write permission, then run the
script:

.. code::

   $ psql -e ...
   > \i sql/upgrades/160.sql

Note:

-  *-e* so you can see the queries currently running prior to its result

-  For long-running scripts, connect to the remote machine first [5] [6]

Adaptations
-----------

Hopefully, in production, the script runs as is without adaptation…

Otherwise, if the data volume for a given table is large, you may want to adapt. See
`160.sql
<https://forge.softwareheritage.org/source/swh-storage/browse/master/sql/upgrades/160.sql>`_
and `its adaptation <https://forge.softwareheritage.org/P747>`_

For such a case, consider working on ranges on the table id instead. So it uses index
and keep the transaction short. Long-standing migration query (translates to long
running transaction). This could create too many WALs accumulation (for the
replication), thus disk space starvation issue, etc…

Note
----

We use grafana to ensure everything is fine (for example, for the replication, we use
the `postgresql database dashboard, bottom page to the right
<https://grafana.softwareheritage.org/d/PEKz-Ygiz/postgresql-server-overview?orgId=1&refresh=5m&from=1598405876817&to=1598427476817&var-instance=belvedere.internal.softwareheritage.org&var-cluster=:5433&var-datname=All&var-ntop_relations=5&var-interface=All&var-disk=All&var-filesystem=All&var-application_name=All&var-rate_interval=5m>`_).

We also use it to keep a reference of what happened for a given deployment. For this,
Open a grafana dashboard (for example `worker task processing dashboard
<https://grafana.softwareheritage.org/d/b_xh3f9ik/worker-task-processing?orgId=1&from=now-6h&to=now>`_)
and add a tag *deployment* (so it's shared across dashboards) with a description on what
is the current deployment about. It's usually a list of module names that gets deployed
and associated version deployed.
