.. _azure_kubernetes_service_howtos:

.. admonition:: Intended audience
   :class: important

   sysadm staff members

Azure Kubernetes Service howtos
===============================

Kubernetes clusters
-------------------

.. code-block:: bash

   ᐅ az aks list | jq -r '.[]|
   "\(.name) \(.kubernetesVersion) \(.location) \(.resourceGroup)"' | \
   awk 'BEGIN{format="%-25s %-20s %-15s %-15s\n";
   printf format,"Cluster Name", "Kubernetes Version", "Location", "Resource Group";
   printf format,"---","---","---","---"}
   {printf format,$1,$2,$3,$4}'
   Cluster Name              Kubernetes Version   Location        Resource Group
   ---                       ---                  ---             ---
   euwest-gitlab-staging     1.29.4               westeurope      euwest-gitlab-staging
   euwest-rancher            1.28.9               westeurope      euwest-rancher
   euwest-gitlab-production  1.29.4               westeurope      euwest-gitlab-production

Upgrading Kubernetes
--------------------

| The Kubernetes supported version in AKS can be checked on this `release calendar <https://learn.microsoft.com/en-us/azure/aks/supported-kubernetes-versions?tabs=azure-cli#aks-kubernetes-release-calendar>`_.
| For the Rancher cluster, check the `supported versions <https://www.suse.com/suse-rancher/support-matrix/all-supported-versions/>`_.
| For the GitLab clusters, check which versions are supported by the `operator <https://docs.gitlab.com/operator/installation.html#cluster>`_.

.. admonition:: Get the current GitLab operator version
   :class: tip

   .. code-block:: bash

      ᐅ for app in $(kubectl --context cluster-admin-rke2 get applications -n argocd -o name | \
      awk '/gitlab-operator/');do
      awk '{split($1,a,"/");print a[2]}' <<< "$app"
      kubectl --context cluster-admin-rke2 describe "$app" -n argocd | \
      awk '/registry.gitlab.com/{split($1,a,":");printf "\t version: %s\n", a[2]}'
      done
      gitlab-production-gitlab-operator
         version: 1.1.1
      gitlab-staging-gitlab-operator
         version: 1.1.1

.. admonition:: Get the current Rancher version
   :class: tip

   .. code-block:: bash

      ᐅ for pod in $(kubectl --context local get pods -n cattle-system -l app=rancher -o name)
      do kubectl --context local describe -n cattle-system "$pod" | \
      awk '/^([[:space:]]*Image|Name):/'
      done
      Name:                 rancher-58994f549-5phdn
          Image:         rancher/rancher:v2.8.4
      Name:                 rancher-58994f549-dq86k
          Image:         rancher/rancher:v2.8.4

Check the current node pool image.

.. code-block:: bash

   ᐅ az aks nodepool show \
       --resource-group euwest-gitlab-staging \
       --cluster-name euwest-gitlab-staging \
       --name default \
       --query nodeImageVersion
   "AKSUbuntu-2204gen2containerd-202312.06.0"

Check the current kubernetes version and the future node pool image.

.. code-block:: bash

   ᐅ az aks nodepool get-upgrades --resource-group euwest-gitlab-staging \
       --nodepool-name default \
       --cluster-name euwest-gitlab-staging --output table
   KubernetesVersion    LatestNodeImageVersion                    Name     OsType    ResourceGroup
   -------------------  ----------------------------------------  -------  --------  ---------------------
   1.26.10              AKSUbuntu-2204gen2containerd-202406.07.0  default  Linux     euwest-gitlab-staging

.. admonition:: Node Pool Image
   :class: note

   The node image is automatically updated when upgrading the node pool to a new Kubernetes version,
   but the node pool can be manually updated to the latest image outside of a Kubernetes version upgrade.

Get the available upgrades in the next minor version.

.. code-block:: bash

   ᐅ az aks get-upgrades --resource-group euwest-gitlab-staging \
       --name euwest-gitlab-staging --output table
   Name     ResourceGroup          MasterVersion    Upgrades
   -------  ---------------------  ---------------  ---------------
   default  euwest-gitlab-staging  1.26.10          1.27.9, 1.27.13

Launch the upgrade.

.. code-block:: bash

   ᐅ az aks upgrade  \
       --resource-group euwest-gitlab-staging \
       --name euwest-gitlab-staging \
       --kubernetes-version 1.27.13

Repeat the same operations for each minor version.


.. admonition:: GitLab Terraform Code
   :class: warning

   Don't forget to update the ``kubernetes_version`` variable in the ``azure/terraform/gitlab.tf`` file
   in the `sysadm-provisioning <https://gitlab.softwareheritage.org/swh/infra/swh-sysadmin-provisioning>`_
   repository.