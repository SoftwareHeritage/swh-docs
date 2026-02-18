.. _howto-process-takedown-requests:

How to process takedown requests
================================

.. admonition:: Intended audience
   :class: important

   Operation/Sysadm staff members

.. _takedown-requests-general-information:

Information
------------

The cli used in the following page is documented in the `project documentation
<https://docs.softwareheritage.org/devel/swh-alter/usage.html>`.

.. _takedown-requests-pod-deployment:

Deployment
----------

This occurs in the main infrastructure, so deployed in kubernetes.

The pods named `alter-$UUID` are toolbox pod like.

We need an operator/sysadm to connect to it to trigger the `swh alter remove` cli call.

Those pods use a ceph persistent volume. That makes their output artifacts stored in
`/srv/recovery-bundles` persistent across restarts.

The configuration of swh-alter in the different environments is managed in the
repository `swh-charts
<https://gitlab.softwareheritage.org/swh/infra/ci-cd/swh-charts/-/blob/a8c6ea7db39be02c78d2eeed24e993ec1025deb2/swh/values/production/swh-cassandra.yaml#L3010>`_.

A pod `alter` is deployed and ready to be used in each environment.

The `alter` configuration uses dedicated deletion allowed ingress endpoints.

.. _howto-perform-a-takedown-request:

How to perform a takedown request
---------------------------------

In the following, we will see how to process a takedown request from the reception up to
the response after having processed the requests.

Prerequisite
~~~~~~~~~~~~

- Received an email in tdn tech mailbox from management asking for the removal of:
  - one or several origins
  - a SWHID to a specific object

- A running `swh-graph` instance

- A storage database (postgresql) with the reference tables populated since the last
  swh-graph update

Procedure for the SWH environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Prior to the actual removal, it's preferable to clone the pod. The removal process can
be long, so this will avoid the pod being redeployed if some new version is deploying in
the infra during the removal process. In the same way, that process is interactive. It
checks what needs to be removed and asks for your validation to trigger the removal.

- Clone the current `alter` pod

.. code::

   CONTEXT=archive-production-rke2
   NAMESPACE=swh-cassandra
   CLONE_NAME=$(id -un)-alter

   kubectl debug --context $CONTEXT -n $NAMESPACE \
       $(kubectl --context $CONTEXT -n $NAMESPACE get pods -l app=alter -o name | head -1) \
       --container=alter --copy-to=$CLONE_NAME -- sleep infinity

   kubectl wait --timeout=3600s --context $CONTEXT -n $NAMESPACE --for=condition=Ready pod/$CLONE_NAME

   kubectl --context $CONTEXT -n $NAMESPACE exec pod/$CLONE_NAME -it -- /bin/bash

- Then connect to that pod with `kubectl` or `k9s`

- Once connected, open a `tmux` session so can connect/disconnect from the pod without
  losing context

- Activate the venv

.. code::

   source venv/bin/activate

Remove the content
~~~~~~~~~~~~~~~~~~

Commands will be launched from the (cloned) `alter` pod:

- Define the request identifier, use `requester-uniq-id` which is the uuid from the
  alteration requests UI. The pattern matches the following
  https://archive.softwareheritage.org/admin/alteration/`requester-uniq-id`/

.. code::

   IDENTIFIER="YYYYDDMM-<requester-uniq-id>"

- With just a few origin/swhid, call:

.. code::

   swh --log-level swh:INFO --log-level azure.core.pipeline.policies.http_logging_policy:WARNING \
     alter remove \
     --identifier $IDENTIFIER \
     --recovery-bundle /srv/recovery-bundles/$IDENTIFIER.zip \
     --reason 'Request from copyright owner' \
     <origin|swhid> <origin|swhid> ... | tee /srv/recovery-bundles/$IDENTIFIER.log
   ...
   Proceed with removing of XXXX SWHIDs [y/N] ?


- With lots of origin/swhid, use an intermediary file, so the call becomes:

.. code::

   # With multiple origins, write origins/swhids to a file first to simplify the call
   echo '<origin|swhid>\norigin|swhid>\n' > $IDENTIFIER.origins
   # Then reuse that file when executing the alter command
   swh --log-level swh:INFO --log-level azure.core.pipeline.policies.http_logging_policy:WARNING \
     alter remove \
     --identifier $IDENTIFIER \
     --recovery-bundle /srv/recovery-bundles/$IDENTIFIER.zip \
     --reason 'Request from copyright owner' \
     $(cat $IDENTIFIER.origins) | tee /srv/recovery-bundles/$IDENTIFIER.log
   Proceed with removing of XXXX SWHIDs [y/N] ?


- The process will output a age key, copy it alongside the output bundle:

.. code::

   # Temporary during the test period
   # Copy the key (logged in the output of the previous call) and save it close to the
   # recovery-bundle
   echo AGE-SECRET-KEY-XXXX > /srv/recovery-bundles/$IDENTIFIER.key

Note:

- The number of SWHIDs is only informational. If no errors are logged during the object
  search, just proceed to the removal.

- At the end of the process, a search of potential new references to the removed objects
  is done. If a new reference is detected (that is, an object has been added to the
  archive that points to one of the removed objects), the bundle is restored and the
  removal must be restarted

Response
--------

We use the alteration requests UI, open the existing request uuid page
https://archive.softwareheritage.org/admin/alteration/<request-uuid>/

Then click on `send a message`, select `Support` and then write the content of what has
been done:

.. quote:

   The request has been processed:
   - The *NUMBER_OF_REMOVED_ORIGINS* provided origins have been removed from the archive.
   - The *NUMBER_OF_BLOCKED_ORIGINS* provided origins have been blocked from any further archival.

Keep the summary of what has been processed relevant and minimal. You can drop the
irrevant mentions (i.e. if no blocked origins, no need for that entry).

.. _takedown-requests-other-commands:


Other commands
--------------

We focused on the take down process. Some other tools under `swh alter` cli can be used.
They are shown for documentation purposes.

Unless specified otherwise, like the previous command, they should be executed in the
`alter` pod.

Test a recovery bundle
~~~~~~~~~~~~~~~~~~~~~~

.. code::

   swh alter recovery-bundle info /srv/recovery-bundle/$IDENTIFIER.zip

Restore a recovery bundle
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code::

   swh alter recovery-bundle restore \
     --decryption-key $(cat /srv/recovery-bundles/$IDENTIFIER.key) \
     /srv/recovery-bundles/$IDENTIFIER.zip

Blocking any future ingestion of an origin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A couple of options are available to interact with blocking requests:

The blocking commands are available in the `swh-toolbox` pod.

We can block origins while waiting for the takedown request to be validated by data
officer:

.. code::

   export SWH_CONFIG_FILENAME=/etc/swh/config-blocking.yml
   swh storage blocking new-request $IDENTIFIER


If the blocking request is related to a takedown request, the same identifier can be
used. A text editor is opened to ask for a reason (usually provided in the alteration
requests ui). For example, 'outdated personal information', 'copyright violation'.

Updating a blocked origin
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code::

   swh storage blocking update-objects $IDENTIFIER blocked


Enter the list of origins to block on stdin and `CTRL+d` to end. A "commit" message is
asked to explain the operation for example "added origins".

Unblocking an origin
~~~~~~~~~~~~~~~~~~~~~

A request can be completely disabled with:

.. code::

   swh storage blocking clear-requests $IDENTIFIER


If a specific origin must be removed in a request:

.. code::

   swh storage blocking list-requests
   swh storage blocking update-objects $IDENTIFIER non-blocked
