.. _user-software-origins-launchpad:

Launchpad
=========

.. include:: dynamic/launchpad_status.inc

`Launchpad <https://launchpad.net/>`_ is a Bazaar and Git hosting platform.

It provides a ``bzr_date_last_modified``/``git_date_last_modified`` field for each
repository, matching the last time the repository was updated;
which is passed as ``last_update`` to the scheduler.

|swh| does not have a specific loader for Bitbucket; the :ref:`BZR
<user-software-origins-bzr>` and :ref:`Git <user-software-origins-git>` loaders are used
instead.
Therefore, origin URLs are Launchpad canonical URL for the corresponding Bazaar or Git
repository.
