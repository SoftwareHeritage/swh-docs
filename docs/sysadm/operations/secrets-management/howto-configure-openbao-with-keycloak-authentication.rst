.. _howto-configure-openbao-with-keycloak-authentication:

Howto configure openbao with keycloak authentication
====================================================

.. admonition:: Intended audience
   :class: important

   staff members

Openbao authentication is managed through the swh ref:`keycloak` instance.

.. _keycloak-openbao-setup:

Keycloak - OpenBao OIDC Integration
===================================

On Keycloak UI
--------------

- Create a new client (e.g. ``openbao-client``).

.. image:: ../../images/secrets-management/01-new-openbao-client.png
   :alt: Add Keycloak Openbao Client
   :align: center
   :class: screenshot

.. image:: ../../images/secrets-management/05-summary-openbao-client.png
   :alt: Keycloak client configuration summary
   :align: center
   :class: screenshot

- Configure it **roughly** as described in the first section of the
  `OpenBao documentation <https://openbao.org/docs/auth/jwt/oidc-providers/keycloak/>`_.

.. image:: ../../images/secrets-management/02-add-client-role-to-openbao-client.png
   :alt: Add client role to keycloak openbao-client
   :align: center
   :class: screenshot

- Create an associated client role called ``admin-openbao``.

.. image:: ../../images/secrets-management/03-configure-client-role.png
   :alt: Configure Keycloak role
   :align: center
   :class: screenshot

- Add a mapper on the client:

   * Use the default-shipped **Client Roles** mapper.

   * Set **Token claim name** to ``client_roles``.

   * Enable **Add to ID token** (other “Add to … token” options are not needed).

.. image:: ../../images/secrets-management/04-summary-client-role-mapper.png
   :alt: Add Client role mapper
   :align: center
   :class: screenshot

- Assign this client role to at least one sysadm user (for testing purpose).

.. image:: ../../images/secrets-management/06-configure-keycloak-user-with-openbao-admin-client-role.png
   :alt: Configure users with the admin-openbao client role
   :align: center
   :class: screenshot

On OpenBao's side
-----------------

Admin should connect to one of the bao pods in the infrastructure.

Configure OIDC on the OpenBao pod
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   export TOKEN="obtain-this-from-keycloak-ui-on-new-client-tab-credentials"
   bao write auth/oidc/config \
       oidc_client_id="openbao-client" \
       oidc_client_secret="$TOKEN" \
       default_role="admin-openbao" \
       oidc_discovery_url='https://auth.softwareheritage.org/auth/realms/SoftwareHeritage'

Ensure the configuration is as expected.

.. code-block:: bash

   / $ bao read auth/oidc/config
   Key                              Value
   ---                              -----
   bound_issuer                     n/a
   default_role                     admin-openbao
   jwks_ca_pem                      n/a
   jwks_url                         n/a
   jwt_supported_algs               []
   jwt_validation_pubkeys           []
   namespace_in_state               true
   oidc_client_id                   openbao
   oidc_discovery_ca_pem            n/a
   oidc_discovery_url               https://auth.softwareheritage.org/auth/realms/SoftwareHeritage
   oidc_response_mode               n/a
   oidc_response_types              []
   override_allowed_server_names    []
   provider_config                  map[]
   status                           valid

Create an admin policy
^^^^^^^^^^^^^^^^^^^^^^

Role in openbao are managed access through bao policies. The new role
admin-openbao should have crud access to credentials.

.. code-block:: bash

   bao policy write admin-openbao-policy -<<EOF
   path "*" {
       capabilities = ["list", "read", "create", "update"]
   }
   EOF

Configure the associated role
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We associate such `admin-openbao-policy` to the `admin-openbao` role.

.. code-block:: bash

   bao write auth/oidc/role/admin-openbao \
       role_type="oidc" \
       user_claim="sub" \
       policies="admin-openbao-policy" \
       oidc_scopes="profile,email" \
       allowed_redirect_uris="https://openbao.internal.admin.swh.network/v1/auth/oidc/callback,https://openbao.internal.admin.swh.network/ui/vault/auth/oidc/oidc/callback,http://localhost:8250/oidc/callback"


Bind the client role via a claim
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We want to restrict access to specific users with a specific (keycloak) client
role. In this case, the keycloak users with `admin-openbao` client role.

So, we add a ``bound_claim`` check (JSON) to ensure the user has the correct
permission.  Use the token claim name defined in the Keycloak UI
(``client_roles``) and the **Keycloak** client role name (``admin-openbao`` -
not the OpenBao role).

.. code-block:: bash

   # This updates the existing role with such claim
   bao write auth/oidc/role/admin-openbao -<<EOF
   {"bound_claims": { "client_roles": ["admin-openbao"] }}
   EOF

Test
----

Web UI
^^^^^^

1. Open the OpenBao UI and select the **OIDC** authentication method.

2. Leave the *role* field empty (fill it only if you have defined a second
   role with fewer privileges).

*If the user has the required client role, login succeeds and the UI loads.*

  They can login and actually read or write openbao secrets.

*If the role is missing, the user will see an error such as:*

  > Vault login failed. error validating claims: claim "client_roles" is
  missing

  They cannot login so it's fine.


Command-line
^^^^^^^^^^^^

From the :ref:`comfort of your own shell<howto-manage-secrets-in-openbao>`,
this can be tested out.
