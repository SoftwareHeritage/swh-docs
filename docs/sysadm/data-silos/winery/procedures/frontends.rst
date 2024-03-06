.. _winery-proc-frontends:

Frontends procedures
====================

.. admonition:: Intended audience
   :class: important

   sysadm staff members

Pacemaker maintenance mode
--------------------------

In maintenance mode, pacemaker will not attempt to manage the service or switch the ips from one
node to another.

.. _winery-pacemaker-maintenance:

- Force the maintenance mode

.. code-block:: shell

   crm_attribute --name maintenance-mode --update true

- Go back to the nominal mode

.. code-block:: shell

   crm_attribute --name maintenance-mode --delete

- check the status

Nominal mode:

.. code-block:: shell

   root@gloin001:~# crm status
   Status of pacemakerd: 'Pacemaker is running' (last updated 2024-03-06 18:45:31 +01:00)
   Cluster Summary:
      * Stack: corosync
      * Current DC: gloin001 (version 2.1.5-a3f44794f94) - MIXED-VERSION partition with quorum
      * Last updated: Wed Mar  6 18:45:31 2024
      * Last change:  Wed Mar  6 18:45:27 2024 by root via crm_attribute on gloin001
      * 2 nodes configured
      * 4 resource instances configured

   Node List:
      * Online: [ gloin001 gloin002 ]

   Full List of Resources:
      * r_vip_pub   (ocf:heartbeat:IPaddr2):         Started gloin001
      * r_vip_ha    (ocf:heartbeat:IPaddr2):         Started gloin001
      * Clone Set: ha_postgresql [r_postgresql] (promotable):
         * Promoted: [ gloin001 ]
         * Unpromoted: [ gloin002 ]
..

In maintenance:

.. code-block:: shell

   root@gloin001:~# crm status
   Status of pacemakerd: 'Pacemaker is running' (last updated 2024-03-06 18:43:58 +01:00)
   Cluster Summary:
      * Stack: corosync
      * Current DC: gloin001 (version 2.1.5-a3f44794f94) - MIXED-VERSION partition with quorum
      * Last updated: Wed Mar  6 18:43:58 2024
      * Last change:  Wed Mar  6 18:41:47 2024 by root via crm_attribute on gloin001
      * 2 nodes configured
      * 4 resource instances configured

               *** Resource management is DISABLED ***
   The cluster will not attempt to start, stop or recover services

   Node List:
      * Online: [ gloin001 gloin002 ]

   Full List of Resources:
      * r_vip_pub   (ocf:heartbeat:IPaddr2):         Started gloin001 (unmanaged)
      * r_vip_ha    (ocf:heartbeat:IPaddr2):         Started gloin001 (unmanaged)
      * Clone Set: ha_postgresql [r_postgresql] (promotable, unmanaged):
         * r_postgresql      (ocf:heartbeat:pgsqlms):         Unpromoted gloin002 (unmanaged)
         * r_postgresql      (ocf:heartbeat:pgsqlms):         Promoted gloin001 (unmanaged)


Clear the pacemaker error status of a resource
----------------------------------------------

For example:

.. code-block:: shell

    crm_resource -r r_postgresql -H gloin002 -C


Restore a postgresql secondary from the primary
-----------------------------------------------

- Activate the :ref:`pacemaker maintenance mode <winery-pacemaker-maintenance>`

- Stop postgresql via pacemaker (here the postgresql on gloin002)

.. code-block:: shell

   crm --wait resource ban r_postgresql gloin002

Check the postgresql logs to check the status

If the postgresql doesn't stop, it can be force with:

.. code-block:: shell

   export VERSION=<version>
   sudo -u postgres /usr/lib/postgresql/$VERSION/bin/pg_ctl -D /var/lib/postgresql/$VERSION/main stop


- Delete or move the content of the postgresql data directory in ``/var/lib/postgresql/<version>/main``
- Launch the restoration from the master

.. code-block:: shell

   sudo -u postgres pg_basebackup -h 10.25.1.1 -D /var/lib/postgresql/16/main/ -P -U replicator --wal-method=fetch

- Restore the :ref:`nominal pacemaker mode <winery-pacemaker-maintenance>`

Postgresql should restart and recover its lag.

- Check the pacemaker after the secondary is up to date
