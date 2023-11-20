.. _user-software-origins-cgit:

Cgit
====

.. include:: dynamic/cgit_status.inc

`CGit <https://git.zx2c4.com/cgit/about/>`_ is a lightweight front-end for Git.

|swh|'s archives CGit instances by scrapping their HTML, starting from the index page,
then looking for Git URLs in each project's page, embedded as ``<link rel='vcs-git'``
HTML tags.
Only the first HTTP(S) URL is kept; or the first URL at all, if there is no HTTP(S) URL.

The CGit lister then dispatches these URLs to the :ref:`Git loader
<user-software-origins-git>`.
CGit project may have their repository hosted on arbitrary other domains (even GitHub);
which is supported by |swh|.

The "summary" page of CGit projects display the last update of each of their branch;
the lister uses this information to pass a ``last_update`` date to the scheduler.

New CGit instances can be submitted to |swh| through the
`Add Forge Now <https://archive.softwareheritage.org/add-forge/request/create/>`_
interface.

Project description, owner information, and mapping between CGit projects and
repositories on third-party domains are currently not archived.
