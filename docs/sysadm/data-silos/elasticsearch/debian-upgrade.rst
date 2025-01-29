.. _upgrade-debian-elasticsearch-cluster:

Upgrade Procedure for Debian Nodes in an Elasticsearch Cluster
==============================================================

.. admonition:: Intended audience
   :class: important

   sysadm staff members

Purpose
--------

This page documents the steps to upgrade Debian nodes running in an Elasticsearch
cluster. The upgrade process involves various commands and checks before and after
rebooting the node.

Prerequisites
-------------

+ Familiarity with SSH and CLI-based command execution
+ Out-of-band Access to the node (IDRAC/ILO) for reboot
+ Access to the node through SSH (requires the vpn)

Step 0: Initial Steps
---------------------

The elasticsearch nodes are only running on bare metal machines. So, ensuring the out of
band access to the machine is ok. This definitely helps when something goes wrong during
a reboot (disk order or names change, network, ...).

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

Step 5: Stop the elasticsearch service
--------------------------------------

The cluster can support one non-responding node so it's ok to stop the service.

We can check the cluster's status which should stay green after the elasticsearch
service is stopped.

.. code::

   root@node:~# systemctl stop elasticsearch
   root@node:~# curl -s $server/_cluster/health | jq .status
   "green"

Note: ``$server`` if of the form ``hostname:9200`` (with hostname another cluster node
than the one we are currently upgrading)

Step 6: Reboot the node
-----------------------

We are ready to reboot the node:

.. code::

   root@node:~# reboot

You can connect to the serial console of the machine to follow through the reboot.

Step 7: Clean up some more
--------------------------

Once the machine is restarted, some cleanup might be necessary.

.. code::

   root@node:~# apt autopurge

Step 8: Activate puppet agent
-----------------------------

Activate back the puppet agent and make it run. This will start back the elasticsearch
service again.

.. code::

   root@node:~# puppet agent --enable && puppet agent --test

Step 8: Join back the cluster
-----------------------------

After the service restarted, check the node joined back the cluster.

.. code::

   root@node:~# curl -s $server/_cat/allocation?v\&s=node;
   root@node:~# curl -s $server/_cluster/health | jq .number_of_nodes

For example:

.. code::

   root@esnode1:~# server=http://esnode1.internal.softwareheritage.org:9200; date; \
     curl -s $server/_cat/allocation?v\&s=node; echo; \
     curl -s $server/_cluster/health | jq
   Wed Jan 29 09:57:01 UTC 2025
   shards shards.undesired write_load.forecast disk.indices.forecast disk.indices disk.used disk.avail disk.total disk.percent host           ip             node    node.role
      638                0                 0.0                 5.6tb        5.6tb     5.6tb      1.1tb      6.8tb           82 192.168.100.61 192.168.100.61 esnode1 cdfhilmrstw
      634                0                 0.0                 5.7tb        5.7tb     5.7tb        1tb      6.8tb           84 192.168.100.62 192.168.100.62 esnode2 cdfhilmrstw
      639                0                 0.0                 5.6tb        5.6tb     5.6tb      1.1tb      6.8tb           82 192.168.100.63 192.168.100.63 esnode3 cdfhilmrstw
      644                0                 0.0                 5.6tb        5.6tb     5.6tb      8.2tb     13.8tb           40 192.168.100.64 192.168.100.64 esnode7 cdfhilmrstw
      645                0                 0.0                 5.5tb        5.5tb     5.5tb      5.9tb     11.4tb           48 192.168.100.65 192.168.100.65 esnode8 cdfhilmrstw
      666                0                 0.0                 5.1tb        5.1tb     5.1tb      6.3tb     11.4tb           44 192.168.100.66 192.168.100.66 esnode9 cdfhilmrstw

   {
     "cluster_name": "swh-logging-prod",
     "status": "green",
     "timed_out": false,
     "number_of_nodes": 6,
     "number_of_data_nodes": 6,
     "active_primary_shards": 1933,
     "active_shards": 3866,
     "relocating_shards": 0,
     "initializing_shards": 0,
     "unassigned_shards": 0,
     "delayed_unassigned_shards": 0,
     "number_of_pending_tasks": 0,
     "number_of_in_flight_fetch": 0,
     "task_max_waiting_in_queue_millis": 0,
     "active_shards_percent_as_number": 100
   }

Post cluster migration
----------------------

As the cluster should stay green all along the migration, there is nothing more to check
(we just did that after each node).

