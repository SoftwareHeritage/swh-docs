.. _network_configuration:

Reference: Network configuration
================================

.. admonition:: Intended audience
   :class: important

   sysadm staff members.

The network is split in several VLANs provided by the INRIA network team:

.. thumbnail:: ../images/network.svg

VLANs
-----

All inter vlan communications are filtered by our firewalls `pushkin` and `glyptotek`.

.. todo::
   Check the :ref:`firewall settings <firewall_settings>` page for more information.

VLAN1300 - Public network
~~~~~~~~~~~~~~~~~~~~~~~~~

The detail of this range is available in this `VLAN1300 inventory page
<https://inventory.internal.softwareheritage.org/ipam/prefixes/6/>`_

All the inbound traffic is firewalled by the INRIA gateway. The detail of the opened
ports is visible on the private archive in the file
:file:`sysadm/Software_Heritage_VLAN1300_plan.ods`

Some nodes are directly exposed on this network for special needs:

* moma: the main archive entry point
* production workers: to have different visible ips during forge crawling
* pergamon: act as a reverse proxy for some public sites (debian repository, annex,
  sentry, ...)
* forge: needs some special rules

VLAN440 - Production network
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All the nodes dedicated to the main archive are deployed in this network.

The detail of this range is available in this `VLAN440 inventory page
<https://inventory.internal.softwareheritage.org/ipam/prefixes/2/>`_

For historical reasons, some admin nodes are deployed in this range (monitoring, ci,
...) and will be progressively moved into the admin network.

The internal domain associted to this vlan is ``.internal.staging.swh.network``

VLAN443 - Staging network
~~~~~~~~~~~~~~~~~~~~~~~~~

All the nodes dedicated to the staging version of the archive are deployed on this
network. POCs and temporary nodes can also take place in the range.

The detail of this range is visible in this `VLAN443 inventory page
<https://inventory.internal.softwareheritage.org/ipam/prefixes/8/>`_

The internal domain associted to this vlan is ``.internal.staging.swh.network``

VLAN442 - Admin network
~~~~~~~~~~~~~~~~~~~~~~~

This network is dedicated for admin and support nodes.

The detail of this range is visible in this `VLAN442 inventory page
<https://inventory.internal.softwareheritage.org/ipam/prefixes/10/>`_.

The internal domain associated to this vlan is ``.internal.admin.swh.network``

