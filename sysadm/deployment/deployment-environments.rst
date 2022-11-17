.. _deployment-environments:

Reference: Deployment Environments
==================================

We have 2 main environments for deployment:

- staging
- production

Staging Environment
-------------------

Staging nodes are currently running in the `hypervisor pompidou
<https://pompidou.internal.softwareheritage.org:8006/#v1:0:18:4:::::::>`__.

The environment components are listed in `the inventory
<https://inventory.internal.softwareheritage.org/tenancy/tenants/swh-staging/>`__

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

Production Environment
----------------------

.. todo::
   This section is a work in progress.
