.. _howto-run-swh-in-local-kube-cluster:

How to run the swh stack in a local kubernetes cluster
======================================================

.. admonition:: Intended audience
   :class: important

   staff/syadmin members who wants to run a production-like swh stack in a local
   kubernetes cluster

.. _howto-requirements:

Requirements
------------

- `helm <https://helm.sh/>`_ the package manager for kubernetes
- a local kubernetes environment, we assume `kind <https://kind.sigs.k8s.io>`_
  in this document (another could be `minikube
  <https://minikube.sigs.k8s.io>`_)
- one up-to-date local checkout of the `swh charts
  <https://gitlab.softwareheritage.org/swh/infra/ci-cd/swh-charts.git>`_

Place yourselves in the root folder of your local checkout of swh-charts.

.. _howto-create-cluster:

Create a local cluster
~~~~~~~~~~~~~~~~~~~~~~

We will first create a local cluster named 'local-cluster' with the necessary
dependencies for the swh stack to run:

.. code::

   make local-cluster-create
   make local-cluster-install-deps

Note:

- The associated cluster configuration is written at `$HOME/.kube/config.d/local-cluster.yaml`

.. code-block::

   $ pwd
   /path/to/swh/sysadm-environment/swh-charts
   $ make local-cluster-create
   ---
   kind: Cluster
   apiVersion: kind.x-k8s.io/v1alpha4
   nodes:
   - role: control-plane
   - role: worker
   - role: worker
   - role: worker
   Creating cluster "local-cluster" ...
    ✓ Ensuring node image (kindest/node:v1.30.0)
    ✓ Preparing nodes
    ✓ Writing configuration
    ✓ Starting control-plane
    ✓ Installing CNI
    ✓ Installing StorageClass
    ✓ Joining worker nodes
   Set kubectl context to "kind-local-cluster"
   You can now use your cluster with:

   kubectl cluster-info --context kind-local-cluster --kubeconfig
     $HOME/.kube/config.d/local-cluster.yaml

   $ make local-cluster-install-deps
   Release "ingress-nginx" does not exist. Installing it now.
   NAME: ingress-nginx
   LAST DEPLOYED: Fri Jul  5 10:45:49 2024
   NAMESPACE: ingress-nginx
   STATUS: deployed
   REVISION: 1
   TEST SUITE: None
   ...
   NAME: rabbitmq-operator
   LAST DEPLOYED: Fri Jul  5 10:46:10 2024
   NAMESPACE: default
   STATUS: deployed
   REVISION: 1
   TEST SUITE: None
   NOTES:
   ...
   CHART NAME: rabbitmq-cluster-operator
   CHART VERSION: 4.3.10
   APP VERSION: 2.9.0
   +info https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
   Release "cloudnative-pg" does not exist. Installing it now.
   NAME: cloudnative-pg
   LAST DEPLOYED: Fri Jul  5 10:46:12 2024
   NAMESPACE: cnpg-system
   STATUS: deployed
   REVISION: 1
   TEST SUITE: None
   NOTES:
   ...
   Release "cert-manager" does not exist. Installing it now.
   NAME: cert-manager
   LAST DEPLOYED: Fri Jul  5 10:46:14 2024
   NAMESPACE: cert-manager
   STATUS: deployed
   REVISION: 1
   TEST SUITE: None
   NOTES:
   ...
   Release "k8ssandra-operator" does not exist. Installing it now.
   NAME: k8ssandra-operator
   LAST DEPLOYED: Fri Jul  5 10:46:59 2024
   NAMESPACE: k8ssandra-operator
   STATUS: deployed
   REVISION: 1
   TEST SUITE: None

Install the cluster-components chart
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We have defined various gitted `local-cluster.yaml` files in our repository
swh-charts. As most functionalities are toggled off by default, we need to
enable those when installing the charts.

We'll do this using locally non-gitted override files at the root of the
repository, namely:

- cluster-components (cc): local-cluster-cc.override.yaml
- swh: local-cluster-swh.override.yaml

.. code-block::

   # Install the cluster-components chart (mostly backends)
   $ make local-cluster-cc

   # Give it some time for the various backends to start properly
   # The first time around, plenty of docker images will get pulled
   # so that can take a while

   # One can add some kubernetes command line to wait for some condition to be
   met
   # kubectl --context kind-local-cluster wait --for=condition=Ready
   #   pod/search-es-node-0 \
     --namespace swh

   # Install the swh chart (swh stack)
   $ make local-cluster-swh


Note: The Makefile detects your (optional) override files, ensure they are
correctly named or nothing will get installed.

.. code-block:: yaml

   $ cat local-cluster-cc.override.yaml

   podPriority:
     enabled: true

   svix:
     enabled: true

   rabbitmq:
     enabled: true

   cloudnativePg:
     enabled: true

   kafka:
     enabled: true

   cassandra:
     enabled: true

   elasticsearch:
     enabled: true

   redis:
     enabled: true

   $ cat local-cluster-swh.override.yaml

   storage:
     enabled: true

   web:
     enabled: true

   webhooks:
     enabled: true

   deposit:
     enabled: true

   toolbox:
     enabled: true

   scheduler:
     enabled: true

   cookers:
     enabled: false

   indexers:
     enabled: true

   scrubber:
     enabled: true

   graphql:
     enabled: false

   listers:
     enabled: true

   loaders:
     enabled: true

   loaderMetadata:
     enabled: true

   checkerDeposit:
     enabled: true

   memcached:
     enabled: false

   podPriority:
     enabled: true

   vault:
     enabled: true

   indexerStorage:
     enabled: true

   search:
     enabled: true

   objstorage:
     enabled: false

   counters:
     enabled: true

   alter:
     enabled: false

   storageReplayer:
     enabled: true


The full local-cluster configuration can be found in their respective values
files (and you can override more than just the enabled flag):

- `cluster-components/values/local-cluster.yaml <https://gitlab.softwareheritage.org/swh/infra/ci-cd/swh-charts/-/blob/production/cluster-components/values/local-cluster.yaml?ref_type=heads>`_
- `swh/values/local-cluster.yaml <https://gitlab.softwareheritage.org/swh/infra/ci-cd/swh-charts/-/blob/production/swh/values/local-cluster.yaml?ref_type=heads>`_
