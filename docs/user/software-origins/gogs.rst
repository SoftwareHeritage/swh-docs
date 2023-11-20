.. _user-software-origins-gogs:

Gogs
====

.. include:: dynamic/gogs_status.inc

Gogs (Go Git Service) is a Git hosting platform.

|swh|'s Gogs lister queries the project API (eg. https://try.gogs.io/api/v1/repos/search
for try.gogs.io), usually with an authentication token as Gogs does not allow anonymous
access.

It provides an ``updated_at`` field for each repository, matching the last time
the repository (TODO: or project? does it cover stuff like PRs and issues?) was updated;
which is passed as ``last_update`` to the scheduler.

|swh| does not have a specific loader for Gitea; the :ref:`Git
<user-software-origins-git>` loader is used instead.
Therefore, origin URLs are Gogs's canonical URLs for the corresponding Git
repository: :file:`https://{domain}/{owner}/{name}.git``

New Gogs instances can be submitted to |swh| through the
`Add Forge Now <https://archive.softwareheritage.org/add-forge/request/create/>`_
interface.

|swh| does not yet archive extrinsic project metadata (eg. project description) from Gogs.
