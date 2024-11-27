.. _cassandra_upgrade_cluster:

How to upgrade a cassandra cluster
==================================

.. admonition:: Intended audience
   :class: important

   sysadm staff members


This page document the actions to upgrade a cassandra cluster.  The overall
plan is to upgrade each node of the cluster one at a time.

Our (static) cassandra clusters are managed through puppet.

As we need to upgrade the nodes in a rolling upgrade fashion, we will want to
stop the puppet agent from running.

So first, connect to pergamon and trigger a puppet agent test (just in case
some pending actions need to be applied) then stop the puppet agent.


.. code-block:: shell

   $ clush @staging-nodes 'puppet agent --test && \
     puppet agent --disable "Upgrade to cassandra"'

Then identify the desired new version and retrieve its sha512 hash.

https://archive.apache.org/dist/cassandra/4.0.15/apache-cassandra-4.0.15-bin.tar.gz
https://archive.apache.org/dist/cassandra/4.0.15/apache-cassandra-4.0.15-bin.tar.gz.sha512

In the swh-site repository, adapt the environment's common.yaml file with
those values:

.. code-block:: yaml

    $ echo $environment
    staging
    $ grep "cassandra::" .../swh-site/data/deployments/$environment/common.yaml
    cassandra::version: 4.0.15
    cassandra::version_checksum: 9368639fe07613995fec2d50de13ba5b4a2d02e3da628daa1a3165aa009e356295d7f7aefde0dedaab385e9752755af8385679dd5f919902454df29114a3fcc0

Commit and push the changes.

Connect to pergamon and deploy those changes.

Then connect on each machine of the cluster in any order (lexicographic order
is fine though).

We'll need the nodetool access, so here is a simple alias to simplify the
commands (used for the remaining part of the doc).

.. code-block:: shell

   $ USER=$(awk '{print $1}' /etc/cassandra/jmxremote.password)
   $ PASS=$(awk '{print $2}' /etc/cassandra/jmxremote.password)
   $ alias nodetool="/opt/cassandra/bin/nodetool --username $USER --password $PASS"


From another node in the cluster, connect and check the status of the cluster
is fine during the migration.

.. code-block:: shell

   $ period=10; while true; do \
       date; nodetool status -r; echo; nodetool netstats; sleep $period; \
     done


Now, we can remove the node from the cluster (in terms of writing). It will
stop the writing in that node so we can stop it without losing data.

.. code-block:: shell

   $ nodetool drain


Lookup for the '- DRAINED' pattern in the service log to know it's done.

.. code-block:: log

   $ journalctl -e cassandra@instance1 | grep DRAINED
   Nov 27 14:09:06 cassandra01 cassandra[769383]: INFO  [RMI TCP Connection(20949)-192.168.100.181] 2024-11-27 14:09:06,084 StorageService.java:1635 - DRAINED


We stop the cassandra service.

.. code-block:: shell

    $ systemctl stop cassandra@instance1


In the output of the `nodetool status`, the node whose service is stopped
should be marked as DN (Down and Normal):

   $ nodetool -h cassandra02 status -r | grep DN
   DN  cassandra01.internal.softwareheritage.org  8.63 TiB  16      22.7%             cb0695ee-b7f1-4b31-ba5e-9ed7a068d993  rack1


Finally we upgrade cassandra version in the node (through puppet):

.. code-block:: shell

    $ puppet agent --enable && puppet agent --test

Let's check the correct version is installed in /opt

.. code-block:: shell

   $ ls -lah /opt/ | grep cassandra-$version
   lrwxrwxrwx  1 root root   21 Nov 27 14:13 cassandra -> /opt/cassandra-$version
   drwxr-xr-x  8 root root 4.0K Nov 27 14:13 cassandra-$version


Now start back the cassandra service.

.. code-block:: shell

    $ systemctl start cassandra@instance1

Once the service is started again, the `nodetool status` should display an
`UN` (Up and Normal) status again for the node upgraded.

   $ nodetool status -r
   ...
   UN  cassandra01.internal.softwareheritage.org  8.63 TiB  16      22.7%             cb0695ee-b7f1-4b31-ba5e-9ed7a068d993  rack1

Finally, check the version is the expected one.

.. code-block:: shell

   $ nodetool version
   ReleaseVersion: $version
