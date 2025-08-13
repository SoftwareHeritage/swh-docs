.. _kubernetes_maintenance_procedure:

Kubernetes Maintenance Procedure
================================

.. admonition:: Intended audience
   :class: important

   sysadm staff members

Maintenance operations are carried out by one human operator one node at a
time, usually:

- "Draining" the node: workloads (pods) are gracefully moved away from the
  node to another node [1]. The node is marked 'SchedulingDisabled', no more
  pods are started on this node until it gets "uncordoned" by the operator.

.. code-block:: shell

   # kubectl --context $CLUSTER drain $NODE

- "Upgrading": The actual maintenance operation to perform, e.g. system or
  application updates, hardware replacement, reboot, ...

.. code-block:: shell

   # Shutdown the machine per ipmi/idrac access or...
   # ssh $NODE && # do the operation update

- "Uncordon" the node: This marks the updated node as "Ready", so the node
  joins back the kubernetes cluster. The kubernetes scheduler can now schedule
  back pods on this node. The operator can either start back previously
  migrated workloads or leave it as is.

.. code-block:: shell

   # kubectl --context $CLUSTER uncordon $NODE


[1] Care must be taken to ensure that the affinity/antiAffinity are properly
    distributed amongst all nodes of the cluster so services can be migrated
    from other nodes in the cluster.

