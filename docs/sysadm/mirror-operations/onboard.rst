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

The credentials are stored in the kubernetes credentials repository in the
`<cluster name>/ingress-objstorage-ro-auth-secrets.yml` file.

- The username should match the kafka username without the numerical suffix
- Store the password in the global credential store in one these paths:
  - `operations/objstorage.softwareheritage.org/<username>` for the production
  - `operations/objstorage.staging.swh.network/<username>` for the staging
- Generate the htaccess stanza with the following command

.. code-block:: shell

    htpassword -n <username>

- Add the result in the `ingress-objstorage-ro-auth-secrets.yml` file.
  During the postgresql / cassandra transition, the password must be added in the two sections
  of the file.
- Commit the file and push. The credentials will be automatically deployed by ArgoCD a couple of
  minutes later.
- Check the credentials are working with:

.. code:: shell

    curl -u <username>:<password>  https://objstorage.softwareheritage.org                                                                                                                                                                                 11:08:57
    SWH Objstorage API server  <--- This is the correct answer
