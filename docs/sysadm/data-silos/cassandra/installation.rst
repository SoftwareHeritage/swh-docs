.. _cassandra_installation:

How to install a cassandra node
===============================

.. admonition:: Intended audience
   :class: important

   sysadm staff members


This page document the actions to configure a cassandra node and the associated instances

.. - Prepare the puppet configuration

Puppet configuration
--------------------

Implicit configuration
^^^^^^^^^^^^^^^^^^^^^^

By default, each cassandra instance is isolated in its own repositories:

- `/etc/cassandra/<instance>`: the instance configuration
- `cassandra@<instance>`: the systemd service (configured with a template and a drop-in
  directory `/etc/systemd/system/cassandra@<instance>.d`)
- `/var/log/cassandra/<instance>`: the log directory (the logs are also sent to the journal)
- `/srv/cassandra/<instance>/commitlog`: the commitlog directory. It should be configured on a
  different zfs pool than the data directory
- `/srv/cassandra/<instance>/data`: the base data dir. The data, hints, system tables are stored
  in this directory.

Declare the node
^^^^^^^^^^^^^^^^

In the `common/cassandra.yaml` file, declare the node configuration:

- Declare the node fqdn in the `cassandra::nodes` hash
- List all the instances that need to be installed on the node and their eventual overrides
- If the node is for a new cluster, also declare the cluster in the `cassandra::clusters` property

System installation
-------------------

- Install the node with a debian bullseye distribution
- Install zfs and configure the pools according to the instances that will run on the node.
  Based on the usual cassandra server swh uses:

  - one pool for the commitlogs using a fast write intensive disk
  - one or several pools with the mixeduse disks

- If the server name starts with `cassandra[0-9]+`, puppet will install all the necessary
  packages and the configured instances.

.. warning:: The services are just enabled, aka puppet doesn't force the service start. It's done
  on purpose to let the system administrator control the restarts of the instances

- Check the configuration looks correct and start the instance(s) with `systemctl start cassandra@<instance>`

Monitoring
^^^^^^^^^^

TODO

Metric
^^^^^^

TODO
