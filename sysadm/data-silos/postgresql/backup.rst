.. _postgresql_backups:

How to manage the PostgreSQL backups
====================================

.. admonition:: Intended audience
   :class: important

   sysadm staff members

The archive's postgresql is backed up every week by barman.

The service is running on ``banco``

List the servers with backups
-----------------------------

.. code:: bash

    root@banco:~# sudo -u barman barman list-server
    swh-10 - Software Heritage Database (inactive)
    swh-11 - Software Heritage Database (inactive)
    swh-12 - Software Heritage Database

List the backups of a server
----------------------------

.. code:: bash

    root@banco:~# sudo -u barman barman list-backup swh-12
    swh-12 20220207T153405 - STARTED
    swh-12 20220129T003102 - Mon Jan 31 11:09:42 2022 - Size: 17.3 TiB - WAL Size: 425.5 GiB
    swh-12 20220122T003103 - Mon Jan 24 19:41:52 2022 - Size: 17.0 TiB - WAL Size: 608.4 GiB

Manually delete a backup
------------------------

.. code:: bash

    root@banco:~# sudo -u barman barman delete swh-12 20220115T003103
    Deleting backup 20220115T003103 for server swh-12
    Delete associated WAL segments:
        00000001000266820000004E
        00000001000266820000004F
        000000010002668200000050
    ...
    Deleted backup 20220115T003103 (start time: Mon Feb  7 15:24:00 2022, elapsed time: 6 minutes, 56 seconds)

Manually start a backup
-----------------------

A backup can take several days to complete, so don't forget to launch it in a tmux or equivalent.

.. code:: bash

    root@banco:~# sudo -u barman barman backup swh-12
    Starting backup using rsync-concurrent method for server swh-12 in /srv/barman/swh-12/base/20220207T153405
    Backup start at LSN: 26F60/E5916DD0 (0000000100026F60000000E5, 00916DD0)
    Starting backup copy via rsync/SSH for 20220207T153405
    ...

Check the progress:

.. code:: bash

    root@banco:~# sudo -u barman barman list-backup swh-12
    swh-12 20220207T153405 - STARTED
    swh-12 20220129T003102 - Mon Jan 31 11:09:42 2022 - Size: 17.3 TiB - WAL Size: 426.1 GiB
    swh-12 20220122T003103 - Mon Jan 24 19:41:52 2022 - Size: 17.0 TiB - WAL Size: 608.4 GiB

