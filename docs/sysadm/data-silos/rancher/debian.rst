.. _upgrade-debian-rancher-cluster:

Upgrade Procedure for Debian Nodes in a Rancher Cluster
=======================================================

.. admonition:: Intended audience
   :class: important

   sysadm staff members

Purpose
--------

This page documents the steps to upgrade Debian nodes running in a Rancher cluster. The
upgrade process involves various commands and checks before and after rebooting the
node.

Prerequisites
-------------

+ Familiarity with SSH and CLI-based command execution
+ Out-of-band Access to the node (IDRAC/ILO) for reboot
+ Access to the node through SSH (requires the vpn)

Step 0: Initial Steps
---------------------

For vm nodes
~~~~~~~~~~~~

For VM nodes, we can take a vm snapshot in case something goes wrong during the
migration. Connect to the proxmox ui and select the node, click on the snapshot menu and
hit ``Take snapshot``.

We can then switch to the console view to have access to the serial console (in case
something bad happened during the reboot).

For bare metal nodes
~~~~~~~~~~~~~~~~~~~~

Ensure the out of band access to the machine is ok. This definitely helps when something
goes wrong during a reboot (disk order or names change, network, ...).

Rancher snapshot
~~~~~~~~~~~~~~~~

To disable Rancher etcd snapshots go to ``Cluster Management`` from
`Rancher UI <https://rancher.euwest.azure.internal.softwareheritage.org/dashboard/>`_,
choose a cluster then there are two methods:

1. edit the YAML configuration:

   From a cluster dashboard choose ``Edit YAML``.

   .. code:: yaml

      etcd:
        disableSnapshots: false
        s3: null
        snapshotRetention: 5
        snapshotScheduleCron: <min> */5 * * *

   .. code:: yaml

      etcd:
        s3:
          bucket: backup-rke2-etcd
          cloudCredentialName: cattle-global-data::<xxx>
          endpoint: minio.admin.swh.network
          folder: <folder>
        snapshotRetention: 5
        snapshotScheduleCron: <min> */5 * * *

   ======================= ===
   folder                  min
   ======================= ===
   archive-production-rke2 00
   cluster-admin-rke2      15
   archive-staging-rke2    30
   test-staging-rke2       45
   ======================= ===

2. edit the configuration:

   - from a cluster dashboard ``Edit Config``;
   - in ``etcd`` section tab choose disable in ``Backup Snapshots to S3`` section;
   - if there is a custom configuration, CoreDNS for example, plan/apply the ``terraform`` cluster deployment.


.. admonition:: Edit configuration graphically
   :class: warning

   With `Edit Config` all the custom configurations (CoreDNS) will be overwrite.

Check the clusters leases and configmaps used by Rancher snapshots:

   .. code:: bash

      ᐅ for context in $(kubectx | awk '/-rke2/');do
      echo -e "---\nEtcd leader in cluster $context"
      kubectl --context "$context" exec $(kubectl --context "$context" get po -n kube-system -l component=etcd --no-headers -o jsonpath='{range .items[0]}{.metadata.name}{end}') -n kube-system \
      -- etcdctl --cacert='/var/lib/rancher/rke2/server/tls/etcd/server-ca.crt' \
      --cert='/var/lib/rancher/rke2/server/tls/etcd/server-client.crt' \
      --key='/var/lib/rancher/rke2/server/tls/etcd/server-client.key' \
      endpoint status --cluster | awk '/true/{split($1,a,":");print substr(a[2],3)}' | \
      xargs -I{} dig -x {} +short | awk -F '.' '{printf "\t%s\n",$1}'
      echo "Leases and configmaps in cluster $context"
      for name in rke2 rke2-etcd;do
      kubectl --context "$context" get cm -n kube-system "$name" -o jsonpath='{.kind} {.metadata.name} {.metadata.annotations.control-plane\.alpha\.kubernetes\.io/leader}' | \
      awk '{split($3,a,",");printf "\t%-10s %-10s %s\n",$1,$2,substr(a[1],2)}'
      kubectl --context "$context" get leases -n kube-system "$name" -o jsonpath='{.kind} {.metadata.name} {.spec.holderIdentity}' | \
      awk '{printf "\t%-10s %-10s %s\n",$1,$2,$3}'
      done
      done
      ---
      Etcd leader in cluster archive-production-rke2
              rancher-node-production-rke2-mgmt1
      Leases and configmaps in cluster archive-production-rke2
              ConfigMap  rke2       "holderIdentity":"rancher-node-production-rke2-mgmt1"
              Lease      rke2       rancher-node-production-rke2-mgmt1
              ConfigMap  rke2-etcd  "holderIdentity":"rancher-node-production-rke2-mgmt1"
              Lease      rke2-etcd  rancher-node-production-rke2-mgmt1
      ---
      Etcd leader in cluster archive-staging-rke2
              rancher-node-staging-rke2-mgmt1
      Leases and configmaps in cluster archive-staging-rke2
              ConfigMap  rke2       "holderIdentity":"rancher-node-staging-rke2-mgmt1"
              Lease      rke2       rancher-node-staging-rke2-mgmt1
              ConfigMap  rke2-etcd  "holderIdentity":"rancher-node-staging-rke2-mgmt1"
              Lease      rke2-etcd  rancher-node-staging-rke2-mgmt1
      ---
      Etcd leader in cluster cluster-admin-rke2
              rancher-node-admin-rke2-mgmt3
      Leases and configmaps in cluster cluster-admin-rke2
              ConfigMap  rke2       "holderIdentity":"rancher-node-admin-rke2-mgmt2"
              Lease      rke2       rancher-node-admin-rke2-mgmt2
              ConfigMap  rke2-etcd  "holderIdentity":"rancher-node-admin-rke2-mgmt2"
              Lease      rke2-etcd  rancher-node-admin-rke2-mgmt2
      ---
      Etcd leader in cluster test-staging-rke2
              rancher-node-test-rke2-mgmt1
      Leases and configmaps in cluster test-staging-rke2
              ConfigMap  rke2       "holderIdentity":"rancher-node-test-rke2-mgmt1"
              Lease      rke2       rancher-node-test-rke2-mgmt1
              ConfigMap  rke2-etcd  "holderIdentity":"rancher-node-test-rke2-mgmt1"
              Lease      rke2-etcd  rancher-node-test-rke2-mgmt1

`https://www.suse.com/support/kb/doc/?id=000021447 <https://www.suse.com/support/kb/doc/?id=000021447>`_

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

Step 3: Autoremove and Purge
-----------------------------

Perform autoremove to remove unnecessary packages left-over from the migration:

.. code::

   root@node:~# apt autoremove

Step 4: Put an argocd sync window
---------------------------------

Our deployments are managed by argocd which keeps in sync all the deployments. We want
to temporarily disable this sync.

Go to the argocd ui and put the sync window from allow to deny.

We want this so we can adapt the deployments scalability to a minimum. That decreases
the overall number of pods running, hence less churn around moving pods from one node to
another (which will eventually have to also migrate).

Note that either the deployment scale is to be adapted or the keda scaled objects (e.g.
loader*, replayer, ...). It depends on the deployments.

Step 5: Drain the node
----------------------

Now that we scale down the deployments, we still have some pods running and we want to
keep running but not on the currently upgrading node.

For this, we must drain the node so pods are redistributed back to the other cluster
nodes.

.. code::

   user@admin-node:~# kubectl --cluster-context archive-production-rke2 \
     drain \
       --delete-emptydir-data=true \
       --ignore-daemonsets=true \
      $NODE_UPGRADING

Wait for the cli to return and for the pods stopped to be running on the other nodes of
the cluster.

Step 6: Reboot the Node
------------------------

We are finally ready to reboot the node, so just do it:

.. code::

   root@node:~# reboot

You can connect to the serial console of the machine to follow through the reboot.

Step 7: Clean up some more
--------------------------

Once the machine is restarted, some cleanup might be necessary.

.. code::

   root@node:~# apt autopurge

In the case of the bullseye-bookworm migration, on some vms, we needed to uninstall some
package and disable some new failing services.

.. code::

   root@node:~# apt purge -y openipmi
   root@node:~# systemctl reset-failed   # so icinga stops complaining


Step 8: Join back the rancher cluster
-------------------------------------

After the node reboots, check the node joined back the Rancher cluster.

And then must ``uncordon`` the node so the kube scheduler can schedule pods on this node
again (the node will be mared as ``ready``.

Post cluster migration
----------------------

Once all the nodes of the cluster have been migrated:

- Remove the argocd sync window so the cluster is back to nominal state.
- Enable back the Rancher etcd snapshots.
- Check the `holderIdentity` value in `rke2` and `rke2-lease` leases and configmaps.
