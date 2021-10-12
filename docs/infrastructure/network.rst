

Network documentation
#####################

.. keep this in sync with the 'infrastructure' section in swh-docs/docs/index.rst

This section regroups the knowledge base for our network components.


.. toctree::
   :maxdepth: 2
   :titlesonly:


Network architecture
********************

The network is split in several VLANs provided by the INRIA network team:

.. thumbnail:: ../images/network.png


Firewalls
=========

The firewalls are 2 `OPNsense <https://opnsense.org>`_ VMs deployed on the PROXMOX cluster with an `High Availability <https://docs.opnsense.org/manual/hacarp.html?highlight=high%20availability>`_ configuration.

They are sharing a virtual IP on each VLAN to act as the gateway. Only one of the 2 firewalls is owning all the GW ips at the same time. The owner is called the ``PRIMARY``

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
----------------------------------------------

The secondary firewall is not directly reachable for VPN user.
As the OpenVPN service is also running when the firewall is a backup, the packets
coming from tne VPN are routed to the local VPN on the secondary and lost.

To access to GUI, a tunnel can be used:

    ssh -L 8443:pushkin.internal.softwareheritage.org:443 pergamon.internal.softwareheritage.org

Once the tunnel is created, the gui is accessible at https://localhost:8443 in any browser

Configuration backup
--------------------

The configuration is automatically committed on a `git repository <https://forge.softwareheritage.org/source/iFWCFG/branches/master/>`_.
Each firewall regularly pushes its configuration on a dedicated branch of the repository.

The configuration is visible on the `System / Configuration / Backups <https://pushkin.internal.softwareheritage.org/diag_backup.php>`_ page
of each one.

Upgrade procedure
-----------------

Initial status
^^^^^^^^^^^^^^

This is the nominal status of the firewalls:

.. list-table::
  :header-rows: 1

  * - Firewall
    - Status
  * - pushkin
    - PRIMARY
  * - glyptotek
    - BACKUP

Preparation
^^^^^^^^^^^

* Connect to the `principal <https://pushkin.internal.softwareheritage.org>`_ (pushkin here)
* Check the `CARP status <https://pushkin.internal.softwareheritage.org/carp_status.php>`_ to ensure the firewall is the principal (must have the status MASTER for all the IPS)
* Connect to the `backup <https://glyptotek.internal.softwareheritage.org>`_ (glytotek here)
* Check the `CARP status <https://glyptotek.internal.softwareheritage.org/carp_status.php>`__ to ensure the firewall is the backup (must have the status BACKUP for all the IPS)
* Ensure the 2 firewalls are in sync:

  * On the principal, go to the `High availability status <https://pushkin.internal.softwareheritage.org/status_habackup.php>`_ and force a synchronization
  * click on the button on the right of ``Synchronize config to backup``

.. image:: ../images/infrastructure/network/sync.png

* Switch the principal/backup to prepare the upgrade of the master
  (The switch is transparent from the user perspective and can be done without service interruption)

  * [1] On the principal, go to the `Virtual IPS status <https://pushkin.internal.softwareheritage.org/carp_status.php>`_ page
  * Activate the CARP maintenance mode

  .. image:: ../images/infrastructure/network/carp_maintenance.png

  * check the status of the VIPs, they must be ``BACKUP`` on pushkin and ``PRIMARY`` on glyptotek


* wait a few minutes to let the monitoring detect if there are connection issues, check ssh connection on several servers on different VLANs (staging, admin, ...)

If everything is ok, proceed to the next section.

Upgrade the first firewall
^^^^^^^^^^^^^^^^^^^^^^^^^^

Before starting this section, the firewall statuses should be:

.. list-table::
  :header-rows: 1

  * - Firewall
    - Status
  * - pushkin
    - BACKUP
  * - glyptotek
    - PRIMARY

If not, be sure of what you are doing and adapt the links accordingly

* [2] go to the `System Firmware: status <https://pushkin.internal.softwareheritage.org/ui/core/firmware#status>`_ page (pushkin here)
* Click on the ``Check for upgrades`` button

.. image:: ../images/infrastructure/network/check_for_upgrade.png

* follow the interface indication, one or several reboots can be necessary depending to the number of upgrade to apply

.. image:: ../images/infrastructure/network/proceed_update.png

* repeat from the ``Check for upgrades`` operation until there is no upgrades to apply
* Switch the principal/backup to restore ``pushkin`` as the principal:

  * on the current backup (pushkin here) go to `Virtual IPS status <https://pushkin.internal.softwareheritage.org/carp_status.php>`_
  * [3] click on `Leave Persistent CARP Maintenance Mode`

  .. image:: ../images/infrastructure/network/reactivate_carp.png

  * refresh the page, the role should have changed from ``BACKUP`` to ``MASTER``
  * check on the other firewall, if the roles is indeed ``BACKUP`` for all the IPs

* Wait few moment to ensure everything is ok with the new version

Upgrade the second firewall
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Before starting this section, the firewall statuses should be:

.. list-table::
  :header-rows: 1

  * - Firewall
    - Status
  * - pushkin
    - PRIMARY
  * - glyptotek
    - BACKUP

If not, be sure of what you are doing and adapt the links accordingly

* Proceed to the second firewall upgrade

  * perform [1] on the backup (should be ``glyptotek`` here)
  * perform [2] on the backup (should be ``glyptotek`` here)
  * perform [3] on the backup (should be ``glyptotek`` here)
