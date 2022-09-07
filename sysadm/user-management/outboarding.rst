.. _outboarding:

Reference: Outboarding checklist
================================

.. admonition:: Intended audience
   :class: important

   sysadm members

This page describes outboarding process for staff people, i.e., what to do when they
leave the project.

Administrative
--------------

At the entrance desk, give back:

- Inria access badge and office keys
- cantine card

.. _outboarding_technical_setup:

Technical setup
---------------

- lock \*nix account on project machines

   - Edit puppet data for the user

      - Change password hash to '!' in the swh-private-data repository
      - Change shell to /bin/false

   - let puppet push itself :)

- phabricator: remove user from groups Developers, Members, Interns (if
  applicable)
- revoke `VPN
  <https://intranet.softwareheritage.org/wiki/VPN#Revoking_a_client_certificate>`_
  certificate
- remove "staff" role (and others) from production and staging user accounts on Keycloak

.. _outboarding_development:

Development
-----------

- review open and assigned tasks in `Phabricator <https://forge.softwareheritage.org>`_
  and unassign them as needed.

.. _outboarding_communication:

Communication
-------------

- unsubscribe from `mailing lists
  <https://intranet.softwareheritage.org/wiki/Mailing_lists>`_: swh-team
- uninvite/kick from `IRC channels
  <https://intranet.softwareheritage.org/wiki/IRC_channels>`_: #swh-team

.. _outboarding_see_also:

See also
--------

- `Onboarding <onboarding>`_
