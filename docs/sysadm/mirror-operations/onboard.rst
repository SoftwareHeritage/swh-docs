.. _mirror_onboard:

How to onboard a mirror
=======================

.. admonition:: Intended audience
   :class: important

   sysadm staff members

A mirror needs credentials to access our journal and to retrieve the contents.

They are manually created by a software Heritage System Administrator.
**Different credentials must be provided for staging and production.**

The URLs to communicate to the mirror operator are defined in :ref:`service-url`
in the 'Public URLs' sections, ``Journal TLS`` entries and ``swh-objstorage read-only``.

How to create the credentials
-----------------------------

Refer to the :ref:`credentials creation howto <deployment-howto-add-journal-user-credential>`

How to use the credentials
--------------------------

Refer to the :ref:`journal client authentication configuration <journal-client-authentication>`.

How to create the objstorage credentials
----------------------------------------

The read-only public storages are protected by an basic authentication mechanism.
To allow a mirror to retrieve the content files, they need to have valid credentials.

These credentials are managed and deployed by puppet.

To add a credential in the puppet configuration:

- for staging:

  - locate the ``swh::deploy::objstorage::reverse_proxy::basic_auth::users``
    property in the `data/deployment/staging/common.yaml` file
  - add the username in the list

- for production
   - locate the ``swh::deploy::objstorage::reverse_proxy::basic_auth::users``
     property in the `data/common/common.yaml` file
   - add the username in the list

- Add an entry ``swh::deploy::objstorage::reverse_proxy::basic_auth::<<username>>``
  in the ``private/swh-private-data/common.yaml``
- in the ``private`` directory of your puppet sources, execute the following command
  to refresh the censored credentials (used by octocatalog-diff and vagrant):

.. code-block:: bash

   private_data/generate-public-data swh-private-data swh-private-data-censored

- Deploy the changes to the puppet master

