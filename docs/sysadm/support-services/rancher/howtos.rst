.. _rancher_howtos:

.. admonition:: Intended audience
   :class: important

   sysadm staff members


Rancher howtos
==============

How to connect to the underlying kubernetes
-------------------------------------------

- Add the following line in your `/etc/hosts`

.. code::

    192.168.200.18 euwest-rancher-3a905e13.1bef1012-0a93-4a25-8419-ac60363bf3d2.privatelink.westeurope.azmk8s.io


- Get the cluster credentials

.. code:: bash

    az aks get-credentials --resource-group euwest-rancher --name euwest-rancher  -f rancher-admin.yaml


- Test the connectivity

.. code:: bash

    kubectl --kubeconfig rancher-admin.yaml get nodes
