.. _kubernetes_maintenance_procedure:

Kubernetes Maintenance Procedure
================================

.. admonition:: Intended audience
   :class: important

   sysadm staff members

Maintenance operations are carried out by one human operator one node at a
time, usually:

- "Draining" pods: workloads are gracefully moved away from the node to be
  updated to another node to ensure no downtime happens [1]. The node is set
  aside from the cluster, that means no more pods are started on this node
  node until it gets uncordoned (by the operator, us).

.. code-block:: shell

   # kubectl --context $CLUSTER drain $NODE

- performing the maintenance operation: Any kind of maintenance operation,
  e.g. system or application updates, hardware replacement, reboot, ...

.. code-block:: shell

   # ssh $NODE && # do the operation update

- "Uncordon" the node: Make the updated node join back the kubernetes cluster.
  It's now ready to resume its responsibilities, meaning pods can be scheduled
  again on this node. The operator can either start back previously migrated
  workloads or leave it as is.

.. code-block:: shell

   # kubectl --context $CLUSTER uncordon $NODE


[1] Care must be taken to ensure that the affinity/antiAffinity are properly
    distributed amongst all nodes of the cluster so services can be migrated
    from other nodes in the cluster.

