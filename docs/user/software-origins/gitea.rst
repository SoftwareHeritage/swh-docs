.. _user-software-origins-gitea:

Gitea
=====

.. include:: dynamic/gitea_status.inc

Gitea is a Git hosting platform forked from Gogs.

|swh|'s Gitea lister queries the project API (eg. https://try.gitea.io/api/v1/repos/search
for try.gitea.io) anonymously.

It provides an ``updated_at`` field for each repository, matching the last time
the repository (TODO: or project? does it cover stuff like PRs and issues?) was updated;
which is passed as ``last_update`` to the scheduler.

|swh| does not have a specific loader for Gitea; the :ref:`Git
<user-software-origins-git>` loader is used instead.
Therefore, origin URLs are Gitea's canonical URLs for the corresponding Git
repository: :file:`https://{domain}/{owner}/{name}.git``

New Gitea instances can be submitted to |swh| through the
`Add Forge Now <https://archive.softwareheritage.org/add-forge/request/create/>`_
interface.

|swh| also archives extrinsic project metadata (eg. project description) from Gitea.
