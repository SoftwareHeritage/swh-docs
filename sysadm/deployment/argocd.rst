.. _argocd:

ArgoCD
=======

.. admonition:: Intended audience
   :class: important

   sysadm staff members

The CD is run by `ArgoCD <https://argo-cd.readthedocs.io>`_ on argocd.softwareheritage.org.

The repositories
----------------

To manage the kubernetes clusters and ArgoCD, 2 git repositories are used:

- `k8s-clusters-conf <https://forge.softwareheritage.org/source/k8s-clusters-conf/>`__ :
  Kubernetes yaml files deployed on the clusters, it contains the configurations to apply
  directly on the clusters. The ArgoCD configuration is also committed in this repository.
- `k8s-private data <https://forge.softwareheritage.org/source/k8s-swh-private-data/>`__ :
  private repository with the yaml files to configure the secrets per cluster

**Except during the bootstrap phase, the configuration files are automatically applied on the clusters
by ArgoCD.**

2 others deployment services related are indirectly related to deployments:

- `swh-apps <https://forge.softwareheritage.org/source/swh-apps/>`__ :
  Image definitions (version and dependencies, docker images definitions)
- `swh-charts <https://forge.softwareheritage.org/source/swh-charts/>`__
  Application definitions, mostly helm charts defining the way to deploy an application.
  The public configurations per environment are also in this repository due to an argocd constraints.
  The deployment of these applications is done by ArgoCD.

Bootstrap ArgoCD
----------------

Prerequisite: A working kubernetes cluster sized to your needs. At SoftwareHeritage, we chose to
deploy a small cluster of 2 nodes which looks enough for our dozen of applications.

Install ArgoCD
~~~~~~~~~~~~~~

TODO: Detail how it was done in the swh environment
  Some working notes are available in a `Readme.md in the k8s-clusters-conf repository <https://archive.softwareheritage.org/swh:1:cnt:f3594c8ccfe1f00abf09d49ffa640ea8f22a1440;origin=https://forge.softwareheritage.org/source/k8s-clusters-conf.git;visit=swh:1:snp:66a35583e901a1a5a62b4097fcd64e822316e80e;anchor=swh:1:rev:f0c609c40c463d39bd12f912570c34eebe0f217d;path=/README.md>`__.
  It's based on the official `ArgoCD documentation <https://argo-cd.readthedocs.io/en/stable/cli_installation/>`__

Upgrade ArgoCD
~~~~~~~~~~~~~~

Follow the `official ArgoCD document procedure <https://argo-cd.readthedocs.io/en/stable/operator-manual/upgrading/overview/>`__

Bootstrap the self configuration management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ArgoCD is able to manage its own configuration.

To do so some manual installation steps are needed:

- Clone the `k8s-private-data` and `k8s-clusters-conf` repositories locally (or directly the `sysadm-environment repository <https://forge.softwareheritage.org/source/sysadm-environment/>`__)
- Configure the `k8s-private-data` repository credentials in ArgoCD:

.. code:: bash

    cd k8s-private-data/argocd/repositories
    kubectl apply -f k8s-swh-private-data.yaml

- Declare the ArgoCD that will import all the ArgoCD configuration

.. code:: bash

    cd k8s-clusters-conf/argocd/applications
    kubectl apply -f argocd-applications.yaml

After that, ArgoCD will populate itself with all the applications in charge of the clusters configuration
and service deployments.

Manage a new kubernetes cluster
-------------------------------

As we saw, ArgoCD can take care of automatically applying and synchronizing the cluster configurations
and secrets based on what is committed in the `k8s-clusters-conf` and `k8s-private-data` repositories.

A couple of steps are needed to add a new cluster and its associated management applications:

- Declare the cluster in `k8s-private-data/argocd/clusters`

  - Copy an existing cluster file and adapt to use the new cluster credentials

- If this cluster has some secrets, create a directory matching the cluster name at the root of the `k8s-private-data` repository too

    - Put the secret configurations in the directory in kubernetes yaml files.

.. warning::  Only the secrets and private data must be put in this repository

- In the `k8s-clusters-conf` repository, create a new application in the `argocd/applications/cluster-secrets`
  named `<cluster-name>.yaml` to manage the new cluster secrets
  under `argocd/applications`
    Check other applications in this directory and adapt the following properties:
  - metadata.name: change to <cluster-name>-secrets
  - spec.source.path: change to <cluster-name>, it must match the directory created in the `k8s-private-data` repository
  - spec.destination.server: change to the server url, it must match the `stringData.server` value in the
    cluster configuration created in `k8s-private-data/argocd/clusters/<cluster-name>.yaml`

- Create a new directory `k8s-clusters-conf/<cluster-name>` and add the yaml for the static
  configurations of the cluster (namespace, crd, ...)
- Create a new directory `argocd/<cluster-name>`
- Create a new `configuration-application.yaml` to manage the static
  configurations
    Copy another configuration application and adapt the following properties:
  - metadata.name: Change to `<cluster-name>-configuration`
  - spec.source.path: Change to `<cluster-name>`, it must match the directory name created earlier
  - spec.destination.server: Change to the url of the server as declared in the cluster configuration
    created in `k8s-private-data`

Commit and push, ArgoCD will apply all the configurations and will keep it in sync

Deploy a new service
--------------------

The deployments of the services with kubernetes are also managed by ArgoCD.

To create a new application:
  - Identify the cluster on which the service will be deployed
  - Declare a new ArgoCD application in `k8s-clusters-conf/argocd/application/<cluster-name>/<application>-application.yaml`

.. warning:: We are trying when it's possible to always use helm charts to deploy a service.

You can find some other applications used to deploy helm based services in the repository.

More information about the application configuration can also be found in the `official ArgoCD documentation <https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/>`__

