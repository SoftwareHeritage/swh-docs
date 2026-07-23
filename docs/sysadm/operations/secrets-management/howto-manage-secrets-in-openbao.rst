.. _howto-manage-secrets-in-openbao:

How to manage secrets in openbao
================================

.. admonition:: Intended audience
   :class: important

   staff members

Providing :ref:`openbao has been
configured<howto-configure-openbao-with-keycloak-authentication>` and your
user has the proper `admin-openbao` keycloak client role.

You can either manage secrets from the `openbao ui
<https://openbao.internal.admin.swh.network>`__ (behind :ref:`swh
vpn<howto_configure_openvpn>`).

Or you can create secrets from your own machine with the bao cli installed.

Secret engines
^^^^^^^^^^^^^^

In openbao secrets are stored in k/v secret engines.

In our infrastructure, we have one per kubernetes cluster named
'secrets-${cluster-name}' plus one for our puppet manifests secrets named
'secrets-puppet'.

That makes 8:
- secrets-admin-rk2
- secrets-archive-production-rke2
- secrets-gitlab-production
- secrets-archive-staging-rke2
- secrets-test-staging-rke2
- secrets-gitlab-staging
- secrets-rancher
- secrets-puppet

Prepare
^^^^^^^

In an openbao shell session, for example with `nix shell nixpkgs#openbao`.

.. code-block:: bash

   # Setup the VAULT_ADDR environment variable to avoid duplicating the
   # flag -address in all cli calls.
   # https://openbao.org/docs/commands/#vault_addr # export
   VAULT_ADDR='https://openbao.internal.admin.swh.network'

Login
^^^^^

.. code-block:: bash

   $ bao login -method=oidc
   Complete the login via your OIDC provider. Launching browser to:

       https://auth.softwareheritage.org/auth/realms/SoftwareHeritageStaging/protocol/openid-connect/auth?client_id=test-openbao&...

   Waiting for OIDC authentication to complete...
   Success! You are now authenticated. The token information displayed below
   is already stored in the token helper. You do NOT need to run "bao login" again.
   Future OpenBao requests will automatically use this token.

   Key                  Value
   ---                  -----
   token                redacted
   token_accessor       redacted
   token_duration       768h
   token_renewable      true
   token_policies       ["admin" "admin-openbao-policy" "default"]
   identity_policies    []
   policies             ["admin" "admin-openbao-policy" "default"]
   token_meta_role      admin-openbao

   # Read an existing secret


Read secrets
^^^^^^^^^^^^

Use `bao kv read` to read a secret.

.. code-block:: bash

   $ bao kv get secrets-test-staging-rke2/test
   =========== Secret Path ===========
   secrets-test-staging-rke2/data/test

   ======= Metadata =======
   Key                Value
   ---                -----
   created_time       2026-04-08T15:24:45.561436387Z
   custom_metadata    <nil>
   deletion_time      n/a
   destroyed          false
   version            1

   === Data ===
   Key    Value
   ---    -----
   foo    bar

Write secrets
^^^^^^^^^^^^^

Use `bao kv put` to write a secret.

.. code-block:: bash

   # Create a new secret (allowed by the admin‑openbao policy)
   $ bao kv put secrets-test-staging-rke2/test2 bar=foo
   ========== Secret Path ==========
   secrets-test-staging-rke2/data/test2

   ======= Metadata =======
   Key                Value
   ---                -----
   created_time       2026-04-09T07:49:31.845874594Z
   custom_metadata    <nil>
   deletion_time      n/a
   destroyed          false
   version            1

   # And read it back
   $ bao kv get secrets-test-staging-rke2/test2
   ========== Secret Path ==========
   secrets-test-staging-rke2/data/test2

   ======= Metadata =======
   Key                Value
   ---                -----
   created_time       2026-04-09T07:49:31.845874594Z
   custom_metadata    <nil>
   deletion_time      n/a
   destroyed          false
   version            1

   === Data ===
   Key    Value
   ---    -----
   bar    foo

Notes: secrets-test-staging-rke2 is an actual secret store, adapt accordingly.
