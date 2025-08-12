.. _postgresql_maintenance_in_kubernetes_with_cloudnativepg:

Postgresql Upgrades and Maintenance with CloudNativePG cluster
==============================================================

.. admonition:: Intended audience
   :class: important

   sysadm staff members

Regarding postgresql, there are 2 kinds of upgrade, either the postgresql
cluster version (the raw postgresql version) or the operator itself.

Whatever the upgrade, it's always necessary to look at the changelog to ensure
no footgun can occur.

Postgresql upgrade
------------------

For the postgresql version, we are using an ImageCatalog kind object. This is
a dictionary which references the major version of the postgresql images to
use. Currently, all databases are using the version 17.

Major or minor version, it's up to the cloudnative-pg operator to manage the
`database upgrades
<https://cloudnative-pg.io/documentation/current/postgres_upgrades/>`_
properly. We still have to check that everything is ok prior to upgrade it.

minor version
^^^^^^^^^^^^^

Minor upgrade can happen when we update ghe image catalog.

To upgrade such ImageCatalog, retrieve the `latest version
<https://raw.githubusercontent.com/cloudnative-pg/postgres-containers/main/Debian/ClusterImageCatalog-bookworm.yaml>`_
and merge it in `swh-charts's repository file
<https://gitlab.softwareheritage.org/swh/infra/ci-cd/swh-charts/-/blob/production/cluster-components/templates/cloudnative-pg/clusterImageCatalog.yaml?ref_type=heads#L2-20>`_.
Commit and push the commit in staging branch. At the next argocd sync, this
will trigger a rollout updates of the postgresql clusters.

See the `official documentation
<https://cloudnative-pg.io/documentation/current/postgres_upgrades/#minor-version-upgrades>`_
for more information.

major version
^^^^^^^^^^^^^

The major version is declared in `swh-charts' repository and can be managed
per cluster declaration
<https://gitlab.softwareheritage.org/swh/infra/ci-cd/swh-charts/-/blob/production/cluster-components/values.yaml?ref_type=heads#L255>`_. It's
currently declared globally but can be overridden per declaration instance. As
already mentioned, if changed, the operator will proceed with the upgrade.

See the `official documentation
<https://cloudnative-pg.io/documentation/current/postgres_upgrades/#major-version-upgrades>`_
for more information.

Postgresql Operator upgrade
---------------------------

The cloudnative-pg operator is managed through the swh-charts repository, with
the cluster-configuration chart. `Update the version key entry either globally
<https://gitlab.softwareheritage.org/swh/infra/ci-cd/swh-charts/-/blob/production/cluster-configuration/values.yaml?ref_type=heads#L108>`_
or `in the specific cluster version first
<https://gitlab.softwareheritage.org/swh/infra/ci-cd/swh-charts/-/blob/01d129c93f3a252939302e5cc090eabf18fcbea7/cluster-configuration/values/archive-staging-rke2.yaml#L66>`_
(to restrict changes). In the same manner as previously described, there will
be a rollout update of first the operator and then possibly the postgresql
clusters.

Kubernetes Upgrade
------------------

:ref:`Usual kubernetes upgrade happens automatically when nodes are drained
<kubernetes_maintenance_procedure>`. The behavior will depend on how the
postgresql cluster is configured. Overall, it's still the cloudnative-pg's
operator that will drive the behavior of the clusters.



Upgrade
=======

Whatever the upgrade kind chosen from before, the behavior of the postgresql
clusters will remain the same regarding primary and standby behavior.

staging
-------

As mentioned in :ref:`the document about postgresql instance
<postgresql-running-in-kubernetes-with-cloudnativepg>`, staging has cluster
with one primary and one standby. When a node is drained, a primary database
pod, when present on that node, will be evicted. But, as the replica is in
another node, it will become the primary [1]. If, on the other hand, a replica
is present, it will be evicted [2] for the upgrade time. This will not create
any downtime since the primary will remain untouched.

[1] Providing there is no issue in that cluster (inconsistent replication,
...)

[2] It will be stopped because we are currently using volume mount on node to
store the data.

staging-next-version
--------------------

As there is no high availability in this kubernetes environment, there will be
downtime when upgrading to a new version. The pod with the only database
instance will be stopped for the upgrade part.

If we want to absolutely avoid the downtime, the simpler way is to first stop
the next-version environment. That way, no services will be using the impacted
databases. And then proceed with the usual upgrade.

production
----------

Nothing yet.
