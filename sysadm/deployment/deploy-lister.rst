.. _deploy-new-lister:

How to deploy a new lister
==========================

This page describes step by step how to deploy and initialize a new lister on the
staging infractucture.

.. _upgrade-the-packages:

Upgrade the packages
--------------------

The actions can be launched on all the workers at the same time with ``clush``.

There is more information about clush on the `Upgrades
<https://intranet.softwareheritage.org/wiki/Upgrades>`__ page.

With ``clush`` on ``pergamon``:

::

   # check current version
   clush -b -w @staging-loader-workers dpkg -l python3-swh.lister
   # Upgrade
   clush -b -w @staging-loader-workers 'apt-get update; apt-get install -y python3-swh.lister'
   # check the new version is well deployed
   clush -b -w @staging-loader-workers dpkg -l python3-swh.lister

Example of execution:

::

   # check current version
   root@pergamon:~# clush -b -w @staging-loader-workers 'dpkg -l python3-swh.lister | grep ii'
   ii  python3-swh.lister 0.1.4-0~swh1~bpo10+1 all          Software Heritage Listers (bitbucket, git(lab|hub), pypi, etc...)# Upgrade

   # Upgrade
   root@pergamon:~# clush -b -w @staging-loader-workers 'apt-get update; apt-get install -y python3-swh.lister'
   ...

   # check the new version is well deployed
   root@pergamon:~# clush -b -w @staging-loader-workers "dpkg -l python3-swh.lister | grep ii"
   ii  python3-swh.lister 0.1.4-1~swh1~bpo10+1 all          Software Heritage Listers (bitbucket, git(lab|hub), pypi, etc...)# Upgrade

.. _upgrade_the_puppet_configuration:

Upgrade the puppet configuration
--------------------------------

Each type of task is associated to a rabbitmq queue. To have the listers watching to the
new(s) queue(s), `the configuration deployed by puppet
<https://archive.softwareheritage.org/browse/content/sha1_git:9f18b57eaa4f2300ef0a9a0fb7eebdf214f28e8b/#L1891>`__
must be updated to reference them.

The exact name of the task to add is the package name and `the name declared on the
tasks
<https://archive.softwareheritage.org/swh:1:cnt:9e57081f70bf0b73370738a80aaa13be5bcc1c9c;origin=https://github.com/SoftwareHeritage/swh-lister;visit=swh:1:snp:33f02eb3570f02bc94027e606f835d13f48f3d3a;anchor=swh:1:rev:4b27f9d9c4076d3b2aa4e6e6903a41ec7967d724;path=/swh/lister/gitlab/tasks.py;lines=24/>`__
themselves.

The puppet master must be refreshed and the configuration deployed.

.. _upgrade-the-puppet-master:

Upgrade the puppet master
-------------------------

On pergamon:

::

   root@pergamon:~# /usr/local/bin/deploy.sh -v

.. _apply-the-configuration-on-workers:

Apply the configuration on workers
----------------------------------

::

   root@pergamon:~# clush -b -w @staging-loader-workers puppet agent -t

.. _restart-listers:

Restart the listers
-------------------

On ``pergamon``, with ``clush``

::

   clush -b -w @staging-loader-workers 'systemctl restart swh-worker@lister'

.. _create-model-and-update--scheduler:

Create the model and update the scheduler
-----------------------------------------

At this stage, the listers are up to date but not yet ready to accept
new tasks. The scheduler must be updated with the new lister task type.

.. _upgrade-scheduler-packages:

Upgrade the scheduler server packages
-------------------------------------

On the scheduler server (``scheduler0.internal.staging.swh.network`` on
staging) with the \*\ ``root``\ \* user:

::

   # Update the lister package to refresh the cli tool
   apt-get update
   apt-get install -y python3-swh.lister
   # check the version is the same as the workers
   dpkg -l python3-swh.lister

.. _configure-scheduler:

Configure the scheduler
-----------------------

- The lister task type must be registered in the scheduler, trigger the `swh scheduler
  task-type register` command, on the scheduler server with ``swhscheduler`` user:

::

   swh scheduler --config-file /etc/softwareheritage/scheduler.yml \
     task-type register

Example:

::

   swhscheduler@scheduler0:~$ swh scheduler \
     --config-file /etc/softwareheritage/scheduler.yml \
     task-type register
   ...
   INFO:swh.core.config:Loading config file /etc/softwareheritage/scheduler.yml
   INFO:swh.scheduler.cli.task_type:Loading entrypoint for plugin lister.launchpad
   INFO:swh.scheduler.cli.task_type:Create task type list-launchpad-incremental in scheduler
   INFO:swh.scheduler.cli.task_type:Create task type list-launchpad-full in scheduler
   INFO:swh.scheduler.cli.task_type:Create task type list-launchpad-new in scheduler

.. _register-new-task:

Register a new task
-------------------

The listers and the scheduler are now ready to work together. Use the `swh scheduler
task add` command. Check ref:`swh-devel:register-task-type` for more details.

.. _check-logs:

Check the logs
--------------

On ``pergamon`` with ``root`` (or as a sudo user):

::

   clush -b -w @staging-loader-workers 'systemctl status swh-worker@lister'

It will output the status of the listers and the last lines of the
lister's logs on each worker server.

