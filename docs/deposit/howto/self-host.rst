Self-host swh-deposit
=====================

TODO



Register a client account
-------------------------

1. Retrieve the deposit client login (through email exchange or any other media).

2. Require a :ref:`provider url <swh-deposit-provider-url-definition>` from the deposit
   client (through email exchange or any other media).

3. Within the keycloak `production instance <https://auth.softwareheritage.org/auth/admin/SoftwareHeritage/console/#/realms/SoftwareHeritage>`_ or `staging
   instance <https://auth.softwareheritage.org/auth/admin/SoftwareHeritageStaging/console/#/realms/SoftwareHeritageStaging>`_, add the `swh.deposit.api` role to the deposit
   client login.

4. Create an :ref:`associated deposit collection
   <swh-deposit-add-client-and-collection>` in the deposit instance.

5. Create :ref:`a deposit client <swh-deposit-add-client-and-collection>` with the
   provider url in the deposit instance.

6. To ensure everything is ok, ask the deposit client to check they can access at least
   the service document iri (authenticated).