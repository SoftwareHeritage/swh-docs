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

- Configure the ipxe configuration for the new server (follow :ref:`server_architecture_install_physical`)
  without running puppet to avoid the zfs configuration if declared
- Perform a low level nvme disk format to use a lbf format of 4096b

  - for each nvme disk, execute:

.. code-block:: shell

   # apt update
   # apt install nvme
   # # for each disk
   # # nvme id-ns -H /dev/nvme0n1| grep LBA
  [3:0] : 0x1   Current LBA Format Selected
  [0:0] : 0x1   Metadata as Part of Extended Data LBA Supported
  LBA Format  0 : Metadata Size: 0   bytes - Data Size: 512 bytes - Relative Performance: 0x1 Better (in use)
  LBA Format  1 : Metadata Size: 0   bytes - Data Size: 4096 bytes - Relative Performance: 0 Best  <-- we want to use this one
  LBA Format  2 : Metadata Size: 8   bytes - Data Size: 512 bytes - Relative Performance: 0x3 Degraded
  LBA Format  3 : Metadata Size: 8   bytes - Data Size: 4096 bytes - Relative Performance: 0x2 Good
  LBA Format  4 : Metadata Size: 64  bytes - Data Size: 4096 bytes - Relative Performance: 0x3 Degraded
  # nvme format -f --lbaf=1 /dev/nvme0n1
  Success formatting namespace:1

- Launch puppet

.. code-block:: shell

  # puppet agent --vardir /var/lib/puppet --server pergamon.internal.softwareheritage.org -t

.. warning::

  Do not restart the server without disabling the `cassandra@instance1` service or cassandra
  will start after the reboot without zfs configured

- Disable cassandra to avoid any issue in case of restart

.. code-block:: shell

  # systemctl disable cassandra@instance1

- Create the zfs pool and datasets

.. note::

  Always use the WWN (World Wide Name) of the device to be sure it will never change

.. code-block:: shell

  # # get the wwmn name
  # ls -al /dev/disk/by-id/nvme-*
  #
  # # Load the zfs module (only if the server was not restarted after initial puppet run)
  # modprobe zfs
  #
  # # Create the zfs pool(s)
  # zpool create -o ashift=12 -O atime=off -O relatime=on -O mountpoint=none -O compression=off \
    mixeduse \
    nvme-XX nvme-XY nvme-XZ nvme-YX
  # # Only if the server has a write intensive disk for the commit log
  # zpool create -o ashift=12 -O atime=off -O relatime=on -O mountpoint=none -O compression=off \
    writeintensive \
    nvme-XX
  #
  # Create the zfs datasets
  # zfs create -o mountpoint=/srv/cassandra/instance1/data mixeduse/cassandra-instance1-data
  # # Change the pool to writeintensive if the server has a dedicated disk for the commit logs
  # zfs create -o mountpoint=/srv/cassandra/instance1/commitlog mixeduse/cassandra-instance1-commitlog
  #
  # # Reboot the server to ensure everything is correct
  # reboot
  #
  # # Check the zfs configuration after the reboot
  # zpool status
  # zfs list

- Ensure the zfs dataset permissions are correct

.. code-block:: shell

  # chown cassandra: /srv/cassandra/instance1/{data,commitlog}

- Start cassandra

.. code-block:: shell

  # systemctl enable cassandra@instance1
  # systemctl start cassandra@instance1

.. note::

  During the first start, cassandra will bootstrap the new node with the data it must manage.
  It usually take around 12 hours to finish

- Check everything is Ok

  - On any node of the cluster

.. code-block:: shell

  $ % /opt/cassandra/bin/nodetool  -u cassandra --password [redacted] status -r

  Datacenter: sesi_rocquencourt
  =============================
  Status=Up/Down
  |/ State=Normal/Leaving/Joining/Moving
  --  Address                                    Load       Tokens  Owns (effective)  Host ID                               Rack
  UN  cassandra04.internal.softwareheritage.org  9.91 TiB   16      27.4%             9c618479-7898-4d89-a8e0-dc1a23fce04e  rack1
  UN  cassandra01.internal.softwareheritage.org  10 TiB     16      27.5%             cb0695ee-b7f1-4b31-ba5e-9ed7a068d993  rack1
  UN  cassandra06.internal.softwareheritage.org  10.12 TiB  16      27.4%             557341c9-dc0c-4a37-99b3-bc71fb46b29c  rack1
  UN  cassandra08.internal.softwareheritage.org  10.02 TiB  16      27.2%             247cd9e3-a70c-465c-bca1-ea9d3af9609a  rack1
  UN  cassandra03.internal.softwareheritage.org  10.01 TiB  16      27.0%             4cc44367-67dc-41ea-accf-4ef8335eabad  rack1
  UN  cassandra11.internal.softwareheritage.org  8.94 TiB   16      27.2%             1199974f-9f03-4cc8-8d63-36676d00d53f  rack1
  UN  cassandra10.internal.softwareheritage.org  10.03 TiB  16      27.4%             f39713c4-d78e-4306-91dd-25a8b276b868  rack1
  UN  cassandra05.internal.softwareheritage.org  9.99 TiB   16      26.8%             ac5e4446-9b26-43e4-8203-b05cb34f2c35  rack1
  UN  cassandra09.internal.softwareheritage.org  9.92 TiB   16      27.4%             e635af9a-3707-4084-b310-8cde61647a6e  rack1
  UJ  cassandra12.internal.softwareheritage.org  22.01 GiB  16      ?                 563d9f83-7ab4-41a2-95ff-d6f2bfb3d8ba  rack1
  UN  cassandra02.internal.softwareheritage.org  9.75 TiB   16      27.6%             a3c89490-ee69-449a-acb1-c2aa6b3d6c71  rack1
  UN  cassandra07.internal.softwareheritage.org  9.94 TiB   16      27.3%             0b7b2a1f-1403-48a8-abe1-65734cc02622  rack1

The new node appears with a status `UJ` Up and  Joining

  - On the new node, the bootstrap progressing can be checked with

.. code-block:: shell

  $ /opt/cassandra/bin/nodetool  -u cassandra --password [REDACTED] netstats -H | grep -v 100%
  Mode: JOINING
  Bootstrap 9af73f50-5f97-11ef-88d7-57efd8d208be
      /192.168.100.191
          Receiving 1206 files, 566.42 GiB total. Already received 37 files (3.07%), 80.61 GiB total (14.23%)
      /192.168.100.189
          Receiving 756 files, 647.48 GiB total. Already received 65 files (8.60%), 90.85 GiB total (14.03%)
      /192.168.100.186
          Receiving 731 files, 811.57 GiB total. Already received 35 files (4.79%), 76.18 GiB total (9.39%)
              swh/directory_entry-7 253477270/8750624313 bytes (2%) received from idx:0/192.168.100.186
      /192.168.100.183
          Receiving 730 files, 658.71 GiB total. Already received 43 files (5.89%), 83.18 GiB total (12.63%)
              swh/directory_entry-7 17988974073/19482031143 bytes (92%) received from idx:0/192.168.100.183
      /192.168.100.185
          Receiving 622 files, 477.56 GiB total. Already received 36 files (5.79%), 81.96 GiB total (17.16%)
              swh/directory_entry-8 2812190730/12861515323 bytes (21%) received from idx:0/192.168.100.185
      /192.168.100.181
          Receiving 640 files, 679.54 GiB total. Already received 38 files (5.94%), 84.17 GiB total (12.39%)
      /192.168.100.184
          Receiving 743 files, 813.96 GiB total. Already received 42 files (5.65%), 93.4 GiB total (11.47%)
              swh/directory_entry-5 13940867674/15691104673 bytes (88%) received from idx:0/192.168.100.184
      /192.168.100.190
          Receiving 804 files, 792.49 GiB total. Already received 69 files (8.58%), 95.88 GiB total (12.10%)
              swh/directory_entry-11 2315131981/3494406702 bytes (66%) received from idx:0/192.168.100.190
      /192.168.100.188
          Receiving 741 files, 706.3 GiB total. Already received 43 files (5.80%), 82.24 GiB total (11.64%)
              swh/directory_entry-6 6478486533/17721982774 bytes (36%) received from idx:0/192.168.100.188
      /192.168.100.182
          Receiving 685 files, 623.98 GiB total. Already received 38 files (5.55%), 77.86 GiB total (12.48%)
              swh/directory_entry-6 9007635102/12045552338 bytes (74%) received from idx:0/192.168.100.182
      /192.168.100.187
          Receiving 638 files, 706.2 GiB total. Already received 41 files (6.43%), 83.17 GiB total (11.78%)
              swh/directory_entry-6 1508815317/6276710418 bytes (24%) received from idx:0/192.168.100.187
  Read Repair Statistics:
  Attempted: 0
  Mismatch (Blocking): 0
  Mismatch (Background): 0
  Pool Name                    Active   Pending      Completed   Dropped
  Large messages                  n/a         0              0         0
  Small messages                  n/a         0        5134236         0

- New node declaration

  - To activate the monitoring, declare the node in the monitoring endpoints in
    `swh-charts/cluster-components/values/archive-production-rke2.yaml` for production.
    In the section `scrapeExternalMetrics.cassandra.ips`, add the ip of the new server.
  - Add the node in the list of seeds in `swh-charts/swh/values/production/default.yaml`
    for a production node. Add it in the `cassandraSeeds` list.

- Cleanup of the old nodes

After the new node is bootstrapped, the old nodes are not automatically cleaned and continue
to host the data migrated to the new host. To free the space, the cleanup operation must but
launched manually on all the pre-existing nodes.

.. note::
  If several new node must be added in the same batch, the cleanup operation can be done after
  all the new nodes were added and bootstrapped. It will avoid to clean each old node after each new
  node bootstrap.

.. note::
  The cleanup operation can be started in several nodes in parallel without any problem. Just check
  carefully in the monitoring if the load of the cluster is not too important.

.. code-block:: shell

  $ # Run this on each node except the last one added
  $ /opt/cassandra/bin/nodetool  -u cassandra --password [REDACTED] cleanup -j 0

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
  CREATE KEYSPACE reaper_db WITH replication = {'class': 'NetworkTopologyStrategy', 'sesi_rocquencourt_staging': '3'}  AND durable_writes = true;


2. Alter the system keyspace replication to prepare the authenticated accesses

(from https://cassandra.apache.org/doc/latest/cassandra/operating/security.html#password-authentication)

::

  export PASS=<your jmx password>
  ALTER KEYSPACE system_auth WITH replication = {'class': 'NetworkTopologyStrategy', 'sesi_rocquencourt_staging': 3};
  seq 1 3 | xargs -t -i{} /opt/cassandra/bin/nodetool -h cassandra{} -u cassandra --password $PASS repair --full -j4 system_auth


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
