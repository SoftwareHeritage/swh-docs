.. _firewall_settings:

How to access firewall settings
===============================

.. admonition:: Intended audience
   :class: important

   sysadm staff members

The firewalls are 2 `OPNsense <https://opnsense.org>`_ VMs deployed on the PROXMOX
cluster with an `High Availability
<https://docs.opnsense.org/manual/hacarp.html?highlight=high%20availability>`_
configuration.

They are sharing a virtual IP on each VLAN to act as the gateway. Only one of the 2
firewalls is owning all the GW ips at the same time. The owner is called the ``PRIMARY``

.. list-table::
  :header-rows: 1

  * - Nominal Role
    - name (link to the inventory)
    - login page
  * - PRIMARY
    - `pushkin <https://inventory.internal.softwareheritage.org/virtualization/virtual-machines/75/>`_
    - `https://pushkin.internal.softwareheritage.org <https://pushkin.internal.softwareheritage.org>`_
  * - BACKUP
    - `glyptotek <https://inventory.internal.softwareheritage.org/virtualization/virtual-machines/86/>`_
    - `https://glyptotek.internal.softwareheritage.org <https://glyptotek.internal.softwareheritage.org>`_

Access to the gui of the secondary firewall
-------------------------------------------

The secondary firewall is not directly reachable for VPN user. As the OpenVPN service is
also running when the firewall is a backup, the packets coming from the VPN are routed
to the local VPN on the secondary and lost.

To access to GUI, a tunnel can be used:

    ssh -L 8443:pushkin.internal.softwareheritage.org:443 pergamon.internal.softwareheritage.org

Once the tunnel is created, the gui is accessible at https://localhost:8443 in any
browser

Configuration backup
--------------------

The configuration is automatically committed on a `git repository
<https://forge.softwareheritage.org/source/iFWCFG/branches/master/>`_. Each firewall
regularly pushes its configuration on a dedicated branch of the repository.

The configuration is visible on the `System / Configuration / Backups
<https://pushkin.internal.softwareheritage.org/diag_backup.php>`_ page of each one.
