.. _onboarding:

Reference: Onboarding checklist
===============================

.. admonition:: Intended audience
   :class: important

   staff members

This page describes the onboarding process for new staff member on the project.

.. _onboarding_goodies:

Goodies
-------

- give out Software Heritage t-shirt and stickers!

.. _onboarding_administrative:

Administrative
--------------

- Inria access badge and office keys
- Sign PV d'installation
- Create Inria account
- `cantine card <https://intranet.softwareheritage.org/wiki/Cantine_card>`_
- `transportation expenses <https://intranet.softwareheritage.org/wiki/Transportation_expenses>`_
- Add picture (150x150px) and short bio to the `people page
  <https://www.softwareheritage.org/people/>`_

- Review the `team charter <https://intranet.softwareheritage.org/wiki/Team_charter>`_

.. _onboarding_technical_setup:

Technical setup
---------------

- Create \*nix account and email alias on project machines (swh-site puppet repo)

   - Set \*nix password for the account (swh-private-data puppet repository)

- Set up email forwarding on `gandi <https://admin.gandi.net/dashboard>`_

- Configure printer:

   - if the machine was configured through puppet: add printer alias per \*nix account
     mapping \*nix account to the inria's ldap account if different

   - Otherwise, check the `SIC documentation`_. If the page looks empty/broken, make
     sure you select "Space language: French" (the English translation is missing)

- Create `Phabricator`_ account

   - add user to phabricator `projects <https://forge.softwareheritage.org/project/>`_:
     Developers, Staff, Reviewers, Interns (if applicable)

- Create `Gitlab`_ account

    - add user to the `Staff group <https://gitlab.softwareheritage.org/groups/teams/staff/-/group_members>`_
    - TODO: Define further group memberships for new users

- `VPN <https://intranet.softwareheritage.org/wiki/VPN>`_ access
- HTTP auth credentials for the `intranet wiki`_
- Create account on the `intranet wiki`_ and ask someone to give you the shared auth credentials
- Create account on the `public wiki`_
- add "staff" role from production and staging user accounts on Keycloak

Extra steps for sysadm:

- Add GPG key to password manager
- Add GPG key to allow debian package upload
  (pergamon:/srv/softwareheritage/repository/conf/uploaders)

.. _onboarding_communication:

Communication
-------------

- Subscribe to `mailing lists`_: swh-devel, swh-team
- Invite to `IRC channels`_
- Create user page on the intranet (see `example
  <https://intranet.softwareheritage.org/wiki/User:StefanoZacchiroli>`_) with personal
  contact information
- Subscribe to `team calendar
  <https://intranet.softwareheritage.org/wiki/Team_calendar>`_

.. _onboarding_training:

Training
--------

- Read  `data model <data-model>`_
- Read `python modules structure
  <https://docs.softwareheritage.org/devel/#dependencies>`_
- Follow `getting started tutorial
  <https://docs.softwareheritage.org/devel/getting-started.html>`_
- Have ``make check`` and ``make test`` pass there in swh-environment
- `Configure arcanist <arcanist-configuration>`_ and submit a first diff
  following the `code review <code-review>`_ workflow

.. _onboarding_see_also:

See also
--------

- `Outboarding <outboarding>`_ (i.e., what to do when a staff member *leave*)

.. _SIC documentation: https://vpn1-roc.national.inria.fr/+CSCO+1h75676763663A2F2F7162702D66762E766165766E2E7365++/display/SU/impression+unifiee#expand-ConfigurerlimpressiondepuisunposteLinux
.. _mailing lists: https://intranet.softwareheritage.org/wiki/Mailing_lists
.. _IRC channels: https://intranet.softwareheritage.org/wiki/IRC_channels
.. _intranet wiki: https://intranet.softwareheritage.org
.. _public wiki: https://wiki.softwareheritage.org
.. _Phabricator: https://forge.softwareheritage.org
.. _Gitlab: https://gitlab.softwareheritage.org
