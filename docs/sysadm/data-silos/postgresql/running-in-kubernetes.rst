.. _postgresql-running-in-kubernetes-with-cloudnativepg:

Postgresql running in Kubernetes with CloudNativePG operator
============================================================

.. admonition:: Intended audience
   :class: important

   sysadm staff members

staging
-------

In the staging environment, dedicated postgresql clusters are now running in
kubernetes. They are managed by the `CloudNativePG
operator <https://cloudnative-pg.io/documentation/current/>`_.

Each postgresql cluster are running a version 17 of postgresql.

Each postgresql cluster manages its own database with `one primary and one
stand-by for high
availability <https://cloudnative-pg.io/documentation/current/replication/>`_.

The primary is running in one node of the kubernetes cluster and the stand-by
in another node. Should one node go down (for maintenance or a plain crash),
the operator will ensure the switch between the primary and the stand-by
occurs between the primary and the replica.

Backups are configured to happen daily (over night). The wals and the backups
are stored in our `minio instance
<https://minio-console.internal.admin.swh.network/>`_ in a dedicated bucket
*s3://backup-cnpg/archive-staging-rke2/cnpg/<db-name>*.

They are configured with a retention policy of 7 days for most of them.

Those databases, when relevant, can be accessed through a dedicated pgbouncer
instance with the guest user (follow :ref:`howto connect to postgresql
instance <postgresql_connect>`).

staging-next-version
--------------------

It's a similar setup as the staging one except there is no high availability
nor backups. As it's a scratch environment, there is no guarantee about the
data there.

So when an upgrade occurs, there will be some downtime (if services are using
the databases to upgrade).

production
----------

All ancillary databases are still running in bare metal machines for now so
nothing in kubernetes yet.
