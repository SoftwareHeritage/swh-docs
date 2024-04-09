.. _howto-bulk-ingest:

How to bulk ingest a list of origins
====================================

.. admonition:: Intended audience
   :class: important

   sysadm staff members


The scheduler provides a cli to send a list of origins directly in a rabbitmq queue. If a loading stack
is configured to listen to this queue, these origins will be loaded by the loaders the classical way.

.. warning:: Only a one-shot loading will be performed, a recurring task is not created.

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

