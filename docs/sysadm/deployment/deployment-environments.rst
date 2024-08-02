.. _deployment-environments:

Reference: Deployment Environments
==================================

.. admonition:: Intended audience
   :class: important

   sysadm staff members

We have 3 deployment environments:

- staging-next-version
- staging
- production

.. _staging-next-version-environment:

Staging Next-version Environment
--------------------------------

This is a sandboxed environment dedicated to run the next versions of swh (a
subset of our swh modules newly released). It's currently running in the same
cluster as the staging environment (same cluster but in a dedicated namespace
swh-cassandra-next-version). The backends of this environment is also
kubernetes managed.

.. _staging-environment:

Staging Environment
-------------------

Staging nodes are currently running in the `hypervisor pompidou
<https://pompidou.internal.softwareheritage.org:8006/#v1:0:18:4:::::::>`__.

It is now a mix of static (renewed) bare-metal machines (backends) & vms. They
are running the debian operating system. Most of which run a rancher agent and
form a kubernetes cluster (archive-staging-rke2). This allows to deploy the
swh stack in kubernetes.

The environment components are listed in `the inventory
<https://inventory.internal.admin.swh.network/tenancy/tenants/1/>`__

|staging_environment|

.. _provisioning_source:

Provisioning source
^^^^^^^^^^^^^^^^^^^

The source for the provisioning of those nodes is declared in the
`swh-sysadmin-provisioning
<https://gitlab.softwareheritage.org/infra/swh-sysadmin-provisioning/-/tree/master/proxmox/terraform/staging/>`__
repository. Its source code is a mix of `terraform <https://www.terraform.io/>`__ with
`terraform-proxmox <https://github.com/Telmate/terraform-provider-proxmox>`__ plugin
DSL.

.. _configuration_source:

Configuration source
^^^^^^^^^^^^^^^^^^^^

The source for the configuration of those nodes is our `puppet manifest swh-site
repository <https://gitlab.softwareheritage.org/infra/puppet/puppet-swh-site/>`__ on the
*staging* branch (for the production nodes, it's the *production* branch).

Access
^^^^^^

`Those machines
<https://intranet.softwareheritage.org/wiki/Network_configuration#192.168.128.1.2F24>`__
are ssh accessible like the production ones as long as you have `vpn access
<https://wiki.softwareheritage.org/wiki/VPN>`__ to the infrastructure.

.. |staging_environment| image:: ../images/staging-environment.svg
                         :target: ../_images/staging-environment.svg

.. _production-environment:

Production Environment
----------------------

Production nodes are a mix of static bare-metal machines (backends) &
vms. They are running the debian operating system (managed through
puppet). Most of which run a rancher agent and form a kubernetes cluster
(archive-production-rke2). This allows to deploy the swh stack in kubernetes.

The environment components are listed in `the inventory
<https://inventory.internal.admin.swh.network/tenancy/tenants/2/>`__

.. todo::
   This section is a work in progress.
