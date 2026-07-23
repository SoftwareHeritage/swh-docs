.. _openbao-secrets-engines-and-secrets-structure:

Openbao Secrets engines and secrets structure
=============================================

.. admonition:: Intended audience
   :class: important

   staff members

Secrets in openbao are stored in secrets engines.
In softwareheritage, we chose the k/v v2 engine.

In our infrastructure, we have one per kubernetes cluster named
'secrets-${cluster-name}' plus one for our puppet manifests secrets named
'secrets-puppet':

   - secrets-admin-rk2
   - secrets-archive-production-rke2
   - secrets-gitlab-production
   - secrets-archive-staging-rke2
   - secrets-test-staging-rke2
   - secrets-gitlab-staging
   - secrets-rancher
   - secrets-puppet

Kubernetes
^^^^^^^^^^

In kubernetes, secrets are of the same structure as kubernetes secrets. The name of the
secret ``${secret-name}`` is the name mentioned in the kubernetes manifest.

.. code-block:: bash

   ${secret-engine}/${secret-name}:
     secret-key: secret-value
     secret-key2: secret-value2


Puppet
^^^^^^

In Puppet, due to the `hiera_vault` plugin used to read secrets, we had to slightly
diverge from the existing structure we used to have when directly inlined secrets (in
private repository).

There is the existing file ``common`` or the ``${hostname}`` name which is inside the
secret path.

Each secret name ${secret-name} is a file with only one hard-coded "secret" key. The
associated value is the actual secret puppet will use to complete the manifest.

.. code-block:: bash

  secrets-puppet/{common|$hostname}/${secret-name}:
    "secret": secret-value
