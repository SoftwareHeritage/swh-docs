.. _postgresql_maintenance_in_kubernetes_with_cloudnativepg:

Postgresql Upgrades and Maintenance with CloudNativePG cluster
==============================================================

.. admonition:: Intended audience
   :class: important

   sysadm staff members

Regarding postgresql, there are 2 kinds of upgrade, either the postgresql
cluster database's version used or the cloudnative-pg operator's version.

Note that it's always necessary to look at the changelog of the new release to
ensure no footgun can occur during the upgrade process.

Upgrade
-------

Whatever the tool to upgrade, the behavior of the postgresql clusters will
remain the same.

When high availability is configured, a rollout update of the postgresql
clusters will occur. That means, upgrade is starting first with standby(s)
then the primary (when everything went fine with standbys). This ensures no
downtime occurs for the database clusters.

When no high availability is configured, as there is no standby to relay the
primary, then downtime can occur. It's ok for testing environment like the
staging-next-version environment.

Postgresql upgrade
------------------

For the postgresql version, we are using an ImageCatalog kind object. This is
a dictionary which references the major version of the postgresql images to
use. Currently, all databases are using the version 17.

Major or minor version, it's up to the cloudnative-pg operator to manage the
`database upgrades
<https://cloudnative-pg.io/documentation/current/postgres_upgrades/>`_
properly.

minor version
^^^^^^^^^^^^^

Minor upgrade can happen when we update the image catalog.

To upgrade such ImageCatalog, retrieve the `latest version
<https://raw.githubusercontent.com/cloudnative-pg/postgres-containers/main/Debian/ClusterImageCatalog-bookworm.yaml>`_
and merge it in `swh-charts's repository file
<https://gitlab.softwareheritage.org/swh/infra/ci-cd/swh-charts/-/blob/production/cluster-components/templates/cloudnative-pg/clusterImageCatalog.yaml?ref_type=heads#L2-20>`_.
Commit and push the commit changes. At the next argocd sync, this will trigger
a rollout update of the postgresql clusters.

See the `official documentation on minor version upgrades
<https://cloudnative-pg.io/documentation/current/postgres_upgrades/#minor-version-upgrades>`_
for more information.

major version
^^^^^^^^^^^^^

The major version is declared in `swh-charts' repository and can be managed
per cluster declaration
<https://gitlab.softwareheritage.org/swh/infra/ci-cd/swh-charts/-/blob/production/cluster-components/values.yaml?ref_type=heads#L255>`_. It's
currently declared globally but can be overridden per instance. Commit and
push the commit changes. At the next argocd sync, this will trigger a rollout
update of the postgresql clusters.

See the `official documentation on major version upgrades
<https://cloudnative-pg.io/documentation/current/postgres_upgrades/#major-version-upgrades>`_
for more information.

Postgresql Operator upgrade
---------------------------

The cloudnative-pg operator is managed through the swh-charts repository, with
the cluster-configuration chart. `Update the version key entry either globally
<https://gitlab.softwareheritage.org/swh/infra/ci-cd/swh-charts/-/blob/production/cluster-configuration/values.yaml?ref_type=heads#L108>`_
or `in the specific cluster version first
<https://gitlab.softwareheritage.org/swh/infra/ci-cd/swh-charts/-/blob/01d129c93f3a252939302e5cc090eabf18fcbea7/cluster-configuration/values/archive-staging-rke2.yaml#L66>`_
(to restrict changes).

In the same way described previously, there will be an update of the
cloudnative-pg operator then a rollout update of the postgresql clusters.

Kubernetes Upgrade
------------------

:ref:`Usual kubernetes upgrade happens automatically when nodes are drained
<kubernetes_maintenance_procedure>`. The behavior will depend on how the
postgresql cluster is configured. Overall, it's the cloudnative-pg operator
which drives the behavior of the clusters when this occurs.

The following chapters will described what's expected per environment.

staging
^^^^^^^

As mentioned in :ref:`the document about postgresql instance
<postgresql-running-in-kubernetes-with-cloudnativepg>`, the staging kubernetes
cluster has postgresql clusters configured with one primary and one
standby.

When a node is drained, any primary from a database cluster, when present on
that node, will be evicted. Ahead of this drain, the postgresql operator will
switchover the standby(s) (present in another kubernetes cluster node) as
primary [1]. This ensures no downtime as the database remains available. Any
standby(s) are also evicted from the node. This will not create any downtime
either since the primary will remain untouched (in that case, the primary runs
elsewhere).

[1] Providing there is no issue in that cluster (inconsistent replication,
...)

staging-next-version
^^^^^^^^^^^^^^^^^^^^

As there is no high availability in this kubernetes environment, there will be
downtime when upgrading to a new version. The pod with the only database
instance will be stopped for the upgrade part.

If we want to absolutely avoid the downtime, the simpler way is to first stop
the next-version environment. And then proceed with the usual upgrade. That
way, no services will be using the impacted databases during the upgrade.

production
^^^^^^^^^^

Nothing yet.
