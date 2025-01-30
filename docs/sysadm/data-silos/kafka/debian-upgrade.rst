.. _upgrade-debian-kafka-cluster:

Upgrade Procedure for Debian Nodes in Kafka Cluster
===================================================

.. admonition:: Intended audience
   :class: important

   sysadm staff members

Purpose
--------

This page documents the steps to upgrade Debian nodes running in a Kafka cluster. The
upgrade process involves various commands and checks before and after rebooting the
node.

Prerequisites
-------------

+ Familiarity with SSH and CLI-based command execution
+ Out-of-band Access to the node (IDRAC/ILO) for reboot
+ Access to the node through SSH (requires the vpn)

Step 0: Initial Steps
---------------------

The kafka nodes are mostly running on bare metal machines. So, ensuring the out of band
access to the machine is ok. This definitely helps when something goes wrong during a
reboot (disk order or names change, network, ...).

Note: For (kubernetes) pods running kafka, this kind is dealt with automatically for
kafka operator so this documentation does not cover this part.

Step 1: Migrate to the next debian suite
----------------------------------------

Update the Debian version of the node (e.g. bullseye to bookworm) using the following
command:

.. code::

   root@node:~# /usr/local/bin/migrate-to-${NEXT_CODENAME}.sh

Note: The script should be present on the machine (installed through puppet).

Step 2: Run Puppet Agent
-------------------------

Once the upgrade procedure happened, run the puppet agent to apply any necessary
configuration changes (e.g. /etc/apt/sources.list change, etc...)

.. code::

   root@node:~# puppet agent -t

Step 2: Stop Puppet Agent
-------------------------

As we will stop the service, we don't want the agent to start it back again.

.. code::

   root@node:~# puppet agent --disable "Ongoing debian upgrade"

Step 4: Autoremove and Purge
-----------------------------

Perform autoremove to remove unnecessary packages left-over from the migration.

.. code::

   root@node:~# apt autoremove

Step 5: Stop the kafka service
-------------------------------

The cluster can support one non-responding node so it's ok to stop the service (and let
the node leave the cluster for maintenance operation).

We can check the cluster's status which should stay green after the elasticsearch
service is stopped.

.. code::

   root@node:~# systemctl stop kafka
   root@node:~# kcat -b $server

Note: ``$server`` if of the form ``hostname:9092`` (with the hostname another cluster
node than the one we are currently upgrading). ``kcat`` is a program from the kafkacat
debian package.

Step 6: Reboot the node
-----------------------

We are ready to reboot the node:

.. code::

   root@node:~# reboot

You can connect to the serial console of the machine to follow through the reboot (and
unstuck it if any problem arises).

Step 7: Clean up some more
--------------------------

Once the machine is restarted, some cleanup might be necessary.

.. code::

   root@node:~# apt autopurge

Step 8: Activate puppet agent
-----------------------------

Activate back the puppet agent and make it run. This will start back the disabled
service again.

.. code::

   root@node:~# puppet agent --enable && puppet agent --test

Step 8: Join back the cluster
-----------------------------

After the service restarted, check the node joined back the cluster.

.. code::

   root@node:~# kcat -b $server

Example:

.. code::

   root@kafka1:~# kcat -L -b $server | head
   Metadata for all topics (from broker -1: kafka1:9092/bootstrap):
   2 brokers:
    broker 3 at kafka3.internal.staging.swh.network:9092
    broker 1 at journal2.internal.staging.swh.network:9092 (controller)

