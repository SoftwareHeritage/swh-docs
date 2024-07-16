.. _howto-bulk-ingest:

How to bulk ingest a list of origins
====================================

.. admonition:: Intended audience
   :class: important

   sysadm staff members


The scheduler provides a cli to send a list of origins directly in a rabbitmq queue. If a loading stack
is configured to listen to this queue, these origins will be loaded by the loaders the classical way.

.. warning:: Only a one-shot loading will be performed, a recurring task is not created.


The automated way
=================

`swh-charts` includes a script to automate the bulk ingestion of a list of repository based on a
file downloaded from the internet (usually, a paste on our GitLab instance).

The actions performed are exactly the same as in the `manually_bulk_ingest`_ section but embedded
in a kubernetes job.

The bulk ingest job is based on the toolbox configuration, to avoid duplicating the scheduler
configuration. The job config is added as a new subsection of the main config file.

Declare a job
-------------

In the proper environment, edit the helm values file, locate the `toolbox:` section and add the new
`bulkLoad` job:

.. code-block:: yaml

  toolbox:
    enabled: true
    configs:
      ...
      scheduler:
        schedulerDbConfigurationRef: postgresqlSchedulerConfiguration
        celeryConfigurationRef: producerCeleryConfiguration
      ...
    bulkLoad:
      schedulerConfigurationRef: scheduler
      jobs:
        jobName:
          originListUrl: https://gitlab.softwareheritage.org/...
          taskType: load-git
          maxTasks: 10000
          queuePrefix: oneshot


The `toolbox.configs` section must already exist.

`schedulerConfigurationRef` is referencing the `scheduler` configuration declaration in the `toolbox.configs` part.

`forgeName` is an informational name to identify the job.

The job will be named by concatenating several info: `toolbox-bulk-load--<queuePrefix>-<jobName>`

Once the job is completed, the configuration can be removed from the value file. Helm will automatically
cleaned the job when applied by ArgoCD.

In case of an error during the scheduling, the job will be flagged as failing by kubernetes and
is raised by the monitoring system. The resources (pods, etc.) of a failing job are not automatically removed
to allow easier diagnostics. An operator must manually remove the job to cleanup the resources.

An example of issue for a bulk ingestion: `MBed forge ingestion <https://gitlab.softwareheritage.org/swh/infra/sysadm-environment/-/issues/5363>`__

.. _manually_bulk_ingest:

How to do it manually
=====================


The following example explains how to launch an ingestion from a raw list of origins.

The toolbox deployed in kubernetes contains all the configuration pre-installed to simplify the
interaction with the scheduler. The example is based on this. You must have the `kubectl`
command installed on your local environment and the configuration to access the staging and production
clusters.

- Deploy the loader stack with a queue configuration <prefix>:<usual queue names>

  - for example `Activate oneshot loaders <https://gitlab.softwareheritage.org/swh/infra/ci-cd/swh-charts/-/commit/f478419e4f350f3710ad4d32b3c8875bcf0db812>`_

- If not provided, sort the origins per loader type (git/svn/hg/cvs/...)

  - A quick and dirty helper script could help: `snippets bulk import directory <https://gitlab.softwareheritage.org/swh/devel/snippets/-/tree/master/sysadmin/bulk_import>`_

- Prepare your local environment, the next commands are for staging, adapt according to your needs

.. code::

  CONTEXT=archive-staging-rke2
  NAMESPACE=swh-cassandra
  TOOLBOX=toolbox-oneshot-loading
  ORIGINS=git_origins.lst

- Create a dedicated toolbox pod:

.. code::

  kubectl debug --context $CONTEXT -n $NAMESPACE \
  $(kubectl --context $CONTEXT -n $NAMESPACE get pods -l app=swh-toolbox -o name | head -1) \
     --container=swh-toolbox --copy-to=$TOOLBOX -- sleep infinity

Cloning the pod allows to not stop the loading if an deployment happens before the end of the
loading

- Copy the file containing the list of origins in the pod

.. code::

  kubectl --context $CONTEXT cp $ORIGINS $NAMESPACE/$TOOLBOX:$ORIGINS -c swh-toolbox

- Connect to the pod via kubectl or k9s

.. code::

  kubectl --context $CONTEXT exec --namespace $NAMESPACE -ti $TOOLBOX -c swh-toolbox -- bash

- Populate the celery queue

.. code::

  export SWH_CONFIG_FILENAME=/etc/swh/config-scheduler.yml
  ORIGINS=git_origins.lst
  TASK_TYPE=load-git
  MAX_TASKS=10000

  nohup bash -c "cat $ORIGINS | swh scheduler -C $SWH_CONFIG_FILENAME origin \
    send-origins-from-file-to-celery $TASK_TYPE --threshold=$MAX_TASKS \
    --queue-name-prefix oneshot " | tee -a $ORIGINS.output &

The process is detached from the terminal so you can exit the pod without stopping the process.
It will run until the end unless the pod is restarted by a maintenance or crash.

- Check the output in the log file and the queue in rabbitmq

  - rabbitmq urls are available in the :ref:`services page <service-url>`

- When the loading is done, remove the temporary toolbox pod

.. code::

  kubectl --context $CONTEXT --namespace $NAMESPACE delete pods $TOOLBOX

