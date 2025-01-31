.. _upgrade-debian-cassandra-cluster:

Upgrade Procedure for Debian Nodes in a Cassandra Cluster
=========================================================

.. admonition:: Intended audience
   :class: important

   sysadm staff members

Purpose
--------

This page documents the steps to upgrade Debian nodes running in a Cassandra
cluster. The upgrade process involves various commands and checks before and
after rebooting the node.

Prerequisites
-------------

+ Familiarity with SSH and CLI-based command execution
+ Out-of-band Access to the node (IDRAC/ILO) for reboot
+ Access to the node through SSH (requires the vpn)

Step 0: Initial Steps
---------------------

Ensure the out of band access to the machine is ok. This definitely helps when
something goes wrong during a reboot (disk order or names change, network,
...).

Step 1: Migrate to the next debian suite
----------------------------------------

Update the Debian version of the node (e.g. bullseye to bookworm) using the
following command:

.. code::

   root@node:~# /usr/local/bin/migrate-to-${NEXT_CODENAME}.sh

Note: The script should be present on the machine (installed through puppet).

Step 2: Run Puppet Agent
-------------------------

Once the upgrade procedure happened, run the puppet agent to apply any necessary
configuration changes (e.g. /etc/apt/sources.list change, etc...)

.. code::

   root@node:~# puppet agent -t

Step 3: Stop Puppet Agent
-------------------------

As we will stop the service, we don't want the agent to start it back again.

.. code::

   root@node:~# puppet agent --disable "Ongoing debian upgrade"

Step 4: Autoremove and Purge
-----------------------------

Perform autoremove to remove unnecessary packages left-over from the migration:

.. code::

   root@node:~# apt autoremove

Step 5: Stop the cassandra service
----------------------------------

The cluster can support one non-responding node so it's ok to stop the
service.

.. code-block:: shell

   $ nodetool drain


Lookup for the '- DRAINED' pattern in the service log to know it's done.

.. code-block:: shell

   $ journalctl -e cassandra@instance1 | grep DRAINED
   Nov 27 14:09:06 cassandra01 cassandra[769383]: INFO  [RMI TCP Connection(20949)-192.168.100.181] 2024-11-27 14:09:06,084 StorageService.java:1635 - DRAINED


Then stop the cassandra service.

.. code-block:: shell

    $ systemctl stop cassandra@instance1


In the output of the ``nodetool status``, the node whose service is stopped
should be marked as DN (``Down and Normal``):

   $ nodetool -h cassandra02 status -r | grep DN
   DN  cassandra01.internal.softwareheritage.org  8.63 TiB  16      22.7%             cb0695ee-b7f1-4b31-ba5e-9ed7a068d993  rack1

Step 6: Reboot the Node
------------------------

We are finally ready to reboot the node, so just do it:

.. code::

   root@node:~# reboot

You can connect to the serial console of the machine to follow through the
reboot.

Step 7: Clean up some more
--------------------------

Once the machine is restarted, some cleanup might be necessary.

.. code::

   root@node:~# apt autopurge

Step 8: Activate puppet agent
-----------------------------

Activate back the puppet agent and make it run. This will start back the
cassandra service again.

.. code::

   root@node:~# puppet agent --enable && puppet agent --test

Post cluster migration
----------------------

Once all the nodes of the cluster have been migrated:

- Remove the argocd sync window so the cluster is back to nominal state.
- Enable back the Rancher etcd snapshots.
- Check the `holderIdentity` value in `rke2` and `rke2-lease` leases and configmaps.
