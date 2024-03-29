.. _argocd-config:

ArgoCD
======

.. admonition:: Intended audience
   :class: important

   sysadm staff members

The CD is run by `ArgoCD <https://argo-cd.readthedocs.io>`_ on argocd.softwareheritage.org.

The repositories
----------------

To manage the kubernetes clusters and ArgoCD, 2 git repositories are used:

- `k8s-clusters-conf
  <https://gitlab.softwareheritage.org/infra/ci-cd/k8s-clusters-conf>`_: Kubernetes
  yaml files deployed on the clusters, it contains the configurations to apply directly
  on the clusters. The ArgoCD configuration is also committed in this repository.
- `k8s-private data
  <https://gitlab.softwareheritage.org/infra/ci-cd/k8s-swh-private-data/>`_: private
  repository with the yaml files to configure the secrets per cluster

**Except during the bootstrap phase, the configuration files are automatically applied
on the clusters by ArgoCD.**

2 others deployment services related are indirectly related to deployments:

- `swh-apps <https://gitlab.softwareheritage.org/infra/swh-apps>`_:
  Image definitions (version and dependencies, docker images definitions)
- `swh-charts <https://gitlab.softwareheritage.org/infra/ci-cd/swh-charts>`_:
  Application definitions, mostly helm charts defining the way to deploy an application.
  The public configurations per environment are also in this repository due to argocd
  constraints. The deployment of these applications is done by ArgoCD.

Bootstrap ArgoCD
----------------

Prerequisite: A working kubernetes cluster sized to your needs. At SoftwareHeritage, we
chose to deploy a small cluster of 2 nodes which looks enough for our dozen of
applications.

Install ArgoCD
~~~~~~~~~~~~~~

TODO: Detail how it was done in the swh environment

  Some working notes are available in a `Readme.md in the k8s-clusters-conf repository
  <https://gitlab.softwareheritage.org/infra/ci-cd/k8s-clusters-conf/-/blob/master/Readme.md>`_.
  It's based on the official `ArgoCD documentation
  <https://argo-cd.readthedocs.io/en/stable/cli_installation/>`_

Upgrade ArgoCD
~~~~~~~~~~~~~~

Follow the `official ArgoCD document procedure
<https://argo-cd.readthedocs.io/en/stable/operator-manual/upgrading/overview/>`_

Bootstrap the self configuration management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ArgoCD is able to manage its own configuration.

To do so, some manual installation steps are needed:

- Clone the ``k8s-private-data`` and ``k8s-clusters-conf`` repositories locally (or
  directly the `sysadm-environment repository
  <https://gitlab.softwareheritage.org/infra/sysadm-environment>`_)
- Configure the ``k8s-private-data`` repository credentials in ArgoCD:

.. code:: bash

    cd k8s-private-data/argocd/repositories
    kubectl apply -f k8s-swh-private-data.yaml

- Declare the ArgoCD that will import all the ArgoCD configuration

.. code:: bash

    cd k8s-clusters-conf/argocd/applications
    kubectl apply -f argocd-applications.yaml

After that, ArgoCD will populate itself with all the applications in charge of the
clusters configuration and service deployments.

Manage a new kubernetes cluster
-------------------------------

As we saw, ArgoCD can take care of automatically applying and synchronizing the cluster
configurations and secrets based on what is committed in the ``k8s-clusters-conf`` and
``k8s-private-data`` repositories.

A couple of steps are needed to add a new cluster and its associated management
applications:

- Declare the cluster in ``k8s-private-data/argocd/clusters``

  - Copy an existing cluster file and adapt to use the new cluster credentials

- If this cluster has some secrets, create a directory matching the cluster name at the
  root of the ``k8s-private-data`` repository too

    - Put the secret configurations in the directory in kubernetes yaml files.

.. warning::  Only the secrets and private data must be put in this repository

- In the ``k8s-clusters-conf`` repository, create a new application in the
  ``argocd/applications/cluster-secrets`` named ``<cluster-name>.yaml`` to manage the
  new cluster secrets under ``argocd/applications``

  Check other applications in this directory and adapt the following properties:

  - metadata.name: change to <cluster-name>-secrets
  - spec.source.path: change to <cluster-name>, it must match the directory created in
    the ``k8s-private-data`` repository
  - spec.destination.server: change to the server url, it must match the
    ``stringData.server`` value in the cluster configuration created in
    ``k8s-private-data/argocd/clusters/<cluster-name>.yaml``

- Create a new directory ``k8s-clusters-conf/<cluster-name>`` and add the yaml for the
  static configurations of the cluster (namespace, crd, ...)
- Create a new directory ``argocd/<cluster-name>``
- Create a new ``configuration-application.yaml`` to manage the static configurations

  Copy another configuration application and adapt the following properties:

  - metadata.name: Change to ``<cluster-name>-configuration``
  - spec.source.path: Change to ``<cluster-name>``, it must match the directory name
    created earlier
  - spec.destination.server: Change to the url of the server as declared in the cluster
    configuration created in ``k8s-private-data``

Commit and push, ArgoCD will apply all the configurations and will keep it in sync.

Deploy a new service
--------------------

The deployments of the services with kubernetes are also managed by ArgoCD.

To create a new application:
  - Identify the cluster on which the service will be deployed
  - Declare a new ArgoCD application in
    ``k8s-clusters-conf/argocd/application/<cluster-name>/<application>-application.yaml``

.. warning:: When possible, we try to use helm charts to deploy service.

You can find some other applications used to deploy helm based services in the
repository.

More information about the application configuration can also be found in the `official
ArgoCD documentation
<https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/>`_

Manage users
------------

This documentation is based on the `official user management documentation
<https://archive.softwareheritage.org/swh:1:cnt:c0a70eae47429de31f5eb3eb707ad2a498bee0ab;origin=https://github.com/argoproj/argo-cd;visit=swh:1:snp:2ea44c7c86241d081851907e778a41260304d898;anchor=swh:1:rev:a773b1effb6f59be14176c6402a9a69c4b480275;path=/docs/operator-manual/user-management/index.md>`_
(archived link)

Prerequisite
~~~~~~~~~~~~

The argocd cli will be necessary to perform some action relative to the user management.

Add a user
~~~~~~~~~~

- Add the user on the `argo-cm.yaml
  <https://gitlab.softwareheritage.org/infra/ci-cd/k8s-clusters-conf/-/blob/87aa53624d61601b31697d312254aa3c57a6227d/argocd/configmaps/argocd-cm.yaml>`_
  file
- Add the user role on the `argocd-rbac-cm.yaml
  <https://gitlab.softwareheritage.org/infra/ci-cd/k8s-clusters-conf/-/blob/87aa53624d61601b31697d312254aa3c57a6227d/argocd/configmaps/argocd-rbac-cm.yaml>`_
  file
  If no role is specified, the user will only have a read-only access

.. code:: yaml

  g, <user>, role:admin

- Commit and push your changes, wait a couple of minutes to let ArgoCD apply the changes
- Modify the user password with the cli

.. code:: bash

    $ # Check the user is created
    $ argocd --grpc-web account list
    NAME      ENABLED  CAPABILITIES
    admin     true     login
    newuser   true     apiKey, login
    $ # update its password
    $ argocd --grpc-web account update-password --account newuser
    *** Enter password of currently logged in user (admin):
    *** Enter new password for user newuser: XXX
    *** Confirm new password for user newuser: XXX
    Password updated

Disable a user
~~~~~~~~~~~~~~

- Add the following line in the `argocd-cm.yaml
  <https://gitlab.softwareheritage.org/infra/ci-cd/k8s-clusters-conf/-/blob/87aa53624d61601b31697d312254aa3c57a6227d/argocd/configmaps/argocd-cm.yaml>`_
  file

.. code:: yaml

    accounts.usertodisable.enabled: "false"

- Commit and push your change, wait a couple of minutes to let ArgoCD apply the changes
- Ensure the user is disabled

.. code:: bash

    $ argocd --grpc-web account list
    NAME           ENABLED  CAPABILITIES
    admin          true     login
    usertodisable  false    apiKey, login

Delete a user
~~~~~~~~~~~~~

- Remove the changes committed in the `Add a user` procedure
- Commit and push your changes, wait a couple of minutes to let ArgoCD apply the changes
- Ensure the user is deleted

.. code:: bash

    $ argocd --grpc-web account list
    NAME           ENABLED  CAPABILITIES
    admin          true     login
