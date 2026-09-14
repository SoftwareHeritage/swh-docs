GitLab upgrade procedure
========================

Overview
--------

The GitLab platform is deployed on two Kubernetes clusters:

* ``staging``
* ``production``

Each GitLab deployment is managed by the `GitLab Operator`_.

The GitLab Operator embeds specific versions of the GitLab Helm chart that it
is able to deploy. Therefore, a GitLab upgrade must be performed in two steps:

#. Upgrade the GitLab Operator to a version supporting the target GitLab
   version.
#. Upgrade the GitLab instance itself.

The upgrade must always be tested and validated on the staging environment
before being applied to production.

.. note::

   We generally avoid upgrading directly to an ``x.x.0`` GitLab release.
   A patch release is often published shortly afterwards to fix issues found
   in the initial release.

.. _GitLab Operator: https://gitlab.com/gitlab-org/cloud-native/gitlab-operator
.. _GitLab Operator documentation: https://docs.gitlab.com/operator/
.. _GitLab Operator releases: https://gitlab.com/gitlab-org/cloud-native/gitlab-operator/-/releases
.. _GitLab Operator upgrade documentation: https://docs.gitlab.com/operator/gitlab_upgrades/
.. _GitLab upgrade planning documentation: https://docs.gitlab.com/update/plan_your_upgrade/


Upgrade workflow
----------------

The upgrade procedure follows this order:

#. Review the GitLab upgrade path and release notes.
#. Verify that a recent production backup is available.
#. Upgrade the GitLab Operator in staging.
#. Upgrade GitLab in staging.
#. Validate the staging environment.
#. Notify the team before starting the production upgrade.
#. Upgrade the GitLab Operator in production.
#. Upgrade GitLab in production.
#. Validate the production environment.
#. Notify the team when the upgrade is complete.


Pre-flight checks
-----------------

Review the GitLab upgrade path
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before starting the upgrade, review the
`GitLab upgrade planning documentation`_.

Check especially:

* required intermediate upgrade versions;
* mandatory upgrade stops;
* deprecated features;
* breaking changes;
* database migration requirements;
* known issues affecting the target release.

GitLab sometimes requires specific intermediate versions before upgrading to a
newer release.

These intermediate versions must not be skipped.


Check the target Operator version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Review the `GitLab Operator releases`_ and identify the Operator version that
supports the target GitLab version.

The selected Operator version must support the GitLab Helm chart associated
with the version that will be deployed.


Verify the production backup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before starting the upgrade procedure, verify that production has a recent and
successful backup.

Review the latest execution of the GitLab backup CronJob.

If the last backup is too old or failed, trigger a manual backup before
proceeding.

.. note::

   A GitLab backup currently takes approximately 45 minutes to 1 hour.
   It is therefore recommended to start a backup before beginning the staging
   upgrade.

Do not start the production upgrade until a recent backup has completed
successfully.


Staging upgrade
---------------

Upgrade the GitLab Operator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Select the Operator version
^^^^^^^^^^^^^^^^^^^^^^^^^^^

From the `GitLab Operator releases`_, select the latest Operator release that
supports the next GitLab version in the upgrade path.


Update the Operator version
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Update the Operator version in:

.. code-block:: text

   k8s-clusters-config/argocd-configuration/applications/gitlab-staging/gitlab-operator.yaml

Review the Git changes and create the corresponding merge request.


Synchronize the Argo CD applications
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once the change has been merged, synchronize the following Argo CD
applications in this order:

#. ``admin-rke2-argocd-applications``
#. ``gitlab-staging-gitlab-operator``


Check the GitLab Operator
^^^^^^^^^^^^^^^^^^^^^^^^^

Open the logs of the ``gitlab-controller-manager`` pod.

After the Operator upgrade, the controller may report that the currently
deployed GitLab chart version does not match the version supported or expected
by the new Operator.

This is expected at this stage.

It confirms that the Operator has been upgraded and that the GitLab instance
must now be upgraded.


Upgrade GitLab
~~~~~~~~~~~~~~

Update the GitLab version
^^^^^^^^^^^^^^^^^^^^^^^^^

Update the GitLab version in:

.. code-block:: text

   k8s-clusters-config/gitlab-staging/gitlab-staging.yaml

Make sure that the selected version follows the supported GitLab upgrade path.

Review the changes and create the corresponding merge request.


Synchronize the GitLab configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once the change has been merged, synchronize the following Argo CD
application:

.. code-block:: text

   gitlab-staging-cluster-configuration


Monitor the upgrade
^^^^^^^^^^^^^^^^^^^

Monitor the ``gitlab-controller-manager`` logs while the Operator reconciles
the GitLab deployment.

The upgrade usually proceeds through several stages:

#. Upgrade of Gitaly.
#. Upgrade of KAS.
#. Upgrade of GitLab Shell.
#. Execution of the pre-upgrade database migrations.
#. Upgrade of the Webservice deployment.
#. Upgrade of the Sidekiq deployment.
#. Execution of the post-upgrade database migrations.
#. Restart or reconciliation of Webservice and Sidekiq.

The exact sequence can vary depending on the GitLab release.

Compare the observed upgrade process with the official GitLab upgrade
documentation when necessary.


Check the Argo CD resources
^^^^^^^^^^^^^^^^^^^^^^^^^^^

During the upgrade, monitor the GitLab resources from Argo CD.

* Pods that remain unhealthy;
* failed migration Jobs;
* resources stuck in ``Progressing``;
* applications remaining ``OutOfSync``;
* repeated reconciliation errors;
* Webservice or Sidekiq deployments failing to become healthy.

Do not proceed to production while the staging environment is unstable.


Validate the staging upgrade
----------------------------

The staging upgrade must be fully validated before starting production.


Check Argo CD
~~~~~~~~~~~~~

Verify that:

* ``gitlab-staging-gitlab-operator`` is ``Healthy`` and ``Synced``;
* ``gitlab-staging-cluster-configuration`` is ``Healthy`` and ``Synced``;
* all expected GitLab resources are healthy;
* migration Jobs completed successfully.


Validate the GitLab interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Log in to the staging GitLab instance and verify:

#. The GitLab web interface is reachable.
#. Authentication works correctly.
#. The Admin Area is accessible.
#. The displayed GitLab version matches the expected target version.
#. No major application errors are visible.
#. Repository browsing works correctly.


Production upgrade
------------------

Once the staging upgrade has been fully validated, apply the same upgrade
procedure to production using the exact Operator and GitLab versions validated
in staging.

.. warning::

   Never deploy a GitLab version directly to production if it has not first
   been validated in staging.

   Do not proceed to production while the staging environment is unstable.


Communication before the upgrade
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A short service interruption can occur during the upgrade.

Before starting the production upgrade, send a short message to:

* the team Matrix channel;
* the devel Matrix channel.


Production-specific configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Follow the same procedure described in `Staging upgrade`_, replacing the
staging-specific files and Argo CD applications with their production
equivalents.


GitLab Operator
^^^^^^^^^^^^^^^

Use the same Operator version validated in staging.

Update the Operator version in:

.. code-block:: text

   k8s-clusters-config/argocd-configuration/applications/gitlab-production/gitlab-operator.yaml

Synchronize the following Argo CD applications in this order:

#. ``admin-rke2-argocd-applications``
#. ``gitlab-production-gitlab-operator``


GitLab
^^^^^^

Use the exact GitLab version validated in staging.

Update the GitLab version in:

.. code-block:: text

   k8s-clusters-config/gitlab-production/gitlab-production.yaml

Then synchronize:

.. code-block:: text

   gitlab-production-cluster-configuration


Validate production
~~~~~~~~~~~~~~~~~~~

Perform the same monitoring and validation checks described for staging.

In particular, verify that:

* ``gitlab-production-gitlab-operator`` is ``Healthy`` and ``Synced``;
* ``gitlab-production-cluster-configuration`` is ``Healthy`` and ``Synced``;
* all expected GitLab resources are healthy;
* migration Jobs completed successfully;
* the GitLab web interface is reachable;
* authentication works correctly;
* the displayed GitLab version matches the version validated in staging;
* repository operations work correctly;
* merge requests remain accessible;
* background migrations are progressing normally.


Post-upgrade monitoring
-----------------------

After the upgrade, continue monitoring the GitLab instance for unexpected
errors.

Pay particular attention to:

* database migrations;
* background migrations;
* Sidekiq;
* Webservice;
* Gitaly;
* Operator reconciliation;
* failed Jobs;
* Argo CD resources becoming degraded.


Communication after the upgrade
-------------------------------

Once production has been validated, send a message to the team and devel
Matrix channels.

The message should confirm that:

* the GitLab upgrade is complete;
* the service is available again;
* the expected GitLab version is running.

References
----------

* `GitLab Operator`_
* `GitLab Operator documentation`_
* `GitLab Operator releases`_
* `GitLab Operator upgrade documentation`_
* `GitLab upgrade planning documentation`_