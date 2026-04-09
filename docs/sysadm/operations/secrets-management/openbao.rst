.. _openbao-general-description:

General OpenBao description
===========================

.. admonition:: Intended audience
   :class: important

   sysadm staff members

.. _openbao-what-is-it:

What is openbao?
----------------

OpenBao_ is an open-source secret management system that provides secure storage,
dynamic secrets, and encryption-as-a-service capabilities.  It is a
community-driven fork of HashiCorp Vault, offering API-compatible features
such as:

- **High availability** – leader/follower replication and integrated storage.
- **Identity-based access** – policies driven by tokens, AppRoles, or external auth
  methods (LDAP, OIDC, Kubernetes, etc.).
- **Secure secret storage** – encrypted at rest with configurable backends.
- **Encryption as a service** – transit endpoint for on-the-fly data encryption.

The project aims to provide a fully open-source alternative that can be
deployed in on-premises or cloud environments, supporting both containerised
and traditional service architectures.

It has been chosen to store our current infrastructure secrets.

.. _openbao-installation:

Installation
------------

One OpenBao_ instance has been deployed in the kubernetes admin cluster of the
swh infrastructure through the swh-charts repository.

It's been configured with high-availability (1 master, 2 replicas).

.. _openbao-keycloak:

Keycloak
--------

OpenBao_ delegates the authentication through oidc to our :ref:`keycloak`
instance.  Currently, only keycloak users with the `openbao/admin-openbao`
client role can manage secrets.

.. _OpenBao: https://openbao.org/
