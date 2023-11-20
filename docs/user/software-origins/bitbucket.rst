.. _user-software-origins-bitbucket:

Bitbucket
=========

.. include:: dynamic/bitbucket_status.inc

Bitbucket is a Git hosting platform, which used to support Mercurial.

|swh|'s Bitbucket lister queries the https://api.bitbucket.org/2.0/repositories API
endpoint anonymously.

It provides a ``updated_on`` field for each repository, matching the last time
the repository (TODO: or project? does it cover stuff like PRs and issues?) was updated;
which is passed as ``last_update`` to the scheduler.

|swh| does not have a specific loader for Bitbucket; the :ref:`Git
<user-software-origins-git>` loader is used instead.
Therefore, origin URLs are Bitbucket's canonical URL for the corresponding Git
repository: :file:`https://bitbucket.org/{owner}/{name}.git`.

Bitbucket does not support :ref:`Mercurial <user-software-origins-mercurial>` anymore;
but Mercurial repositories used to be loaded with the Mercurial loader and are
`available in the archive <https://archive.softwareheritage.org/browse/search/?q=bitbucket.org&with_visit=true&with_content=true&visit_type=hg>`__.
Additionally, |swh| provides a `dump of raw Mercurial repositories <https://bitbucket-archive.softwareheritage.org/>`_.

Bitbucket provides extrinsic metadata on repositories (owner, description,
``created_on``, size, language, fork policy, parent repository, ...) which are currently
not archived. Consequently, fork detection isn't used to speedup archival of git
repositories yet.

Resources:

* `HTTP API documentation <https://developer.atlassian.com/cloud/bitbucket/rest/api-group-repositories/>`__
