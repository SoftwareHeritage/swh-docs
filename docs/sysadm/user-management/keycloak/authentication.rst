.. _keycloak:

Authentication
==============

.. admonition:: Intended audience
   :class: important

   Staff members

.. contents::
   :depth: 3
..

Software Heritage uses `Keycloak <https://www.keycloak.org/>`__, an open
source identity and access management solution, to identify and
authenticate users on its services (for instance the
:swh_web:`archive's Web API <api/>`
and the :ref:`deposit server <swh-deposit>`).

Keycloak implements the `OpenID Connect <https://openid.net/connect/>`__
specification, a simple identity layer on top of the OAuth 2.0 protocol.
It allows to get single sign-on (SSO) on various services.

The base URL to interact with that authentication service is
https://auth.softwareheritage.org/auth/.

Introduction
------------

Keycloak defines three important concepts to know about:

Realm
  It manages a set of users, credentials, roles, and groups. A user belongs
  to and logs into a realm. Realms are isolated from one another and can only manage and
  authenticate the users that they control.

Client
  Entities that can request Keycloak to authenticate a user. Most often,
  clients are applications and services that want to use Keycloak to secure themselves and
  provide a single sign-on solution. Clients can also be entities that just want to
  request identity information or an access token so that they can securely invoke other
  services on the network that are secured by Keycloak.

Role
  It identifies a type or category of users. Applications (e.g. webapp,
  deposit) often assign access and permissions to specific roles rather than individual
  users as dealing with users can be too fine grained and hard to manage. There is a
  global namespace for roles and each client also has its own dedicated namespace where
  roles can be defined.

.. _software_heritage_realms:

Software Heritage Realms
------------------------

Two realms are available for Software Heritage:

-  `SoftwareHeritageStaging <https://auth.softwareheritage.org/auth/admin/SoftwareHeritageStaging/console/>`__,
   for testing purposes

-  `SoftwareHeritage <https://auth.softwareheritage.org/auth/admin/SoftwareHeritage/console/>`__,
   for production use

The links above target the Admin console of each realm from which everything can be
configured.
