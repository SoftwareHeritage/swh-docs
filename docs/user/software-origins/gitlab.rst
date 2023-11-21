.. _user-software-origins-gitlab:
.. _user-software-origins-heptapod:

GitLab
======

.. include:: dynamic/gitlab_status.inc

Gitlab is a Git hosting platform. Its fork Heptapod also supports Mercurial.

|swh|'s Gitlab lister queries the project API (eg. https://gitlab.com/api/v4/projects
for gitlab.com) anonymously.

It provides a ``last_activity_at`` field for each repository, matching the last time
the repository (TODO: or project? does it cover stuff like PRs and issues?) was updated;
which is passed as ``last_update`` to the scheduler.

|swh| does not have a specific loader for Gitlab/Heptapod; the :ref:`Git
<user-software-origins-git>` and :ref:`Mercurial <user-software-origins-mercurial>`
loaders are used instead.
Therefore, origin URLs are Gitlab/Heptapod's canonical URLs for the corresponding Git
or Mercurial repository: :file:`https://{domain}/{owner}/{name}.git`` and
:file:`https://{domain}/{owner}/{name}` respectively.

New Gitlab/Heptapod instances can be submitted to |swh| through the
`Add Forge Now <https://archive.softwareheritage.org/add-forge/request/create/>`_
interface.

|swh| currently does not archive extrinsic metadata from Gitlab or Heptapod due to
`a limitation of the Gitlab API <https://gitlab.com/gitlab-org/gitlab/-/issues/361952>`__.
