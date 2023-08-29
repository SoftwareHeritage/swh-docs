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

Cassandra configuration
-----------------------

This section explains how to configure the keyspaces and roles for the specific swh usage.

Cassandra need to be configured with authentication and authorization activated. The following options
need to be present on the `cassandra.yaml` file:

::

  authenticator: PasswordAuthenticator
  authorizer: CassandraAuthorizer

Several users are used:

- `swh-rw`: The main user used by swh-storage to manage the content in the database
- `swh-ro`: A read-only user used for read-only storages (webapp, ...) or humans
- `reaper`: A read-write user on the `reaper` keyspace. `Reaper <http://cassandra-reaper.io/>`_ is the tool in charge of managing the repairs

The command line will use the staging environment as examples. The configuration is for a medium
data volume, with a Replication factor (RF) of 3. Adapt according to your own needs.


1. Create the keyspaces to be able to configure the accesses


::

  CREATE KEYSPACE swh WITH replication = {'class': 'NetworkTopologyStrategy', 'sesi_rocquencourt_staging': '3'}  AND durable_writes = true;
  # If needed
  CREATE KEYSPACE swh WITH reaper_db = {'class': 'NetworkTopologyStrategy', 'sesi_rocquencourt_staging': '3'}  AND durable_writes = true;


2. Alter the system keyspace replication to prepare the authenticated accesses

(from https://cassandra.apache.org/doc/latest/cassandra/operating/security.html#password-authentication)

::

  export PASS=<your jmx password>
  ALTER KEYSPACE system_auth WITH replication = {'class': 'NetworkTopologyStrategy', 'sesi_rocquencourt_staging': 3};
  seq 1 3 | xargs -t -i{} /opt/cassandra/bin/nodetool -h cassandra{} -u cassandra --password $PASS repair -j4 system_auth


3. Create a new `admin` superuser

In cqlsh (the default admin user is `cassandra`/`cassandra`):

::

  CREATE ROLE admin WITH SUPERUSER = true AND LOGIN = true AND PASSWORD = 'changeme';

4. Disable the default superuser

Connect to cqlsh with the new `admin` user:

::

  ALTER ROLE cassandra WITH SUPERUSER = false AND LOGIN = false;


5. Create the `swh-rw` user

::

  CREATE ROLE 'swh-rw' WITH LOGIN = true AND PASSWORD = 'changeme';
  GRANT CREATE ON ALL KEYSPACES to 'swh-rw';
  GRANT CREATE ON ALL FUNCTIONS to 'swh-rw';
  GRANT ALTER ON ALL FUNCTIONS to 'swh-rw';
  GRANT SELECT ON KEYSPACE swh to 'swh-rw';
  GRANT MODIFY ON KEYSPACE swh to 'swh-rw';
  GRANT EXECUTE ON ALL FUNCTIONS to 'swh-rw';

6. Create the `swh-ro` user

::

  CREATE ROLE 'swh-ro' WITH LOGIN = true AND PASSWORD = 'changeme';
  GRANT SELECT ON KEYSPACE swh to 'swh-ro';
  GRANT EXECUTE ON ALL FUNCTIONS to 'swh-ro';

7. Create the `reaper` user

::

  CREATE ROLE 'reaper' WITH LOGIN = true AND PASSWORD = 'changeme';
  GRANT CREATE ON ALL KEYSPACES to 'reaper';
  GRANT SELECT ON KEYSPACE reaper_db to 'reaper';
  GRANT MODIFY ON KEYSPACE reaper_db to 'reaper';
  GRANT ALTER ON KEYSPACE reaper_db to 'reaper';

8. Specific table configurations

The table compaction and compression strategies depend on the hardware topology cassandra is deployed on.
For the high density servers used by swh, these specific configurations are used:
- LCS compaction on big tables to reduce the free disk space needed by compactions
- ZSTD compression on big tables to optimize the disk space

.. warning:: These configurations can be applied only once the swh-storage schema was created by the storage


- In staging

::

  ALTER TABLE content WITH
	  compaction = {'class' : 'LeveledCompactionStrategy', 'sstable_size_in_mb':'160'}
	  AND compression = {'class': 'ZstdCompressor', 'compression_level':'1'};
  ALTER TABLE directory_entry WITH
	compaction = {'class' : 'LeveledCompactionStrategy', 'sstable_size_in_mb':'4096'}
	AND compression = {'class': 'ZstdCompressor', 'compression_level':'1'};

- In production

::

  ALTER TABLE content WITH
	  compaction = {'class' : 'LeveledCompactionStrategy', 'sstable_size_in_mb':'2000'}
	  AND compression = {'class': 'ZstdCompressor', 'compression_level':'1'};
  ALTER TABLE directory_entry WITH
	  compaction = {'class' : 'LeveledCompactionStrategy', 'sstable_size_in_mb':'20480'}
	  AND compression = {'class': 'ZstdCompressor', 'compression_level':'1'};


Monitoring
----------

TODO

Metric
------

TODO
