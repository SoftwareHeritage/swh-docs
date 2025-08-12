.. _postgresql_running_in_kubernetes_with_cloudnativepg:

Postgresql running in Kubernetes with CloudNativePG operator
============================================================

.. admonition:: Intended audience
   :class: important

   sysadm staff members

In the staging environment, dedicated postgresql clusters are now running in
kubernetes. They are managed by the `CloudNativePG
operator<https://cloudnative-pg.io/documentation/current/>`__.

Each cluster manages its own database with `one primary and one stand-by for
high
availability<https://cloudnative-pg.io/documentation/current/replication/>`__.

The primary is running in one node of the kubernetes cluster and the stand-by
in another node. Should one node go down (for maintenance or a plain crash),
the operator will ensure the switch between the primary and the stand-by
occurs between the primary and the replica.

Backups are configured to happen daily (over night). The wals and the backups
are stored in our `minio
instance<https://minio-console.internal.admin.swh.network/>__` in a dedicated
bucket *s3://backup-cnpg/archive-staging-rke2/cnpg/<db-name>*.

They are configured with a retention policy of 7 days for most of them.

Those databases, when relevant, can be accessed through a dedicated pgbouncer
instance with the guest user (follow :ref:`postgresql_connect` documentation).

