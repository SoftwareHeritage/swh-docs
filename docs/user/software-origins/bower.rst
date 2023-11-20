.. _user-software-origins-bower:

Bower
=====

.. include:: dynamic/bower_status.inc

`Bower <https://bower.io/>`_ is a package manager for the Javascript ecosystem,
which doesn't host its own packages.
Instead, it points to Git repositories hosted externally (eg. on GitHub).

|swh| archives Bower by querying ``https://registry.bower.io/packages``, which returns
the complete database of the registry: name and repository URL of every package
registered on it.
It then dispatches loading tasks to the :ref:`Git loader <user-software-origins-git>`.

|swh| currently does not archive the mapping from package names to repository URLs.

Resources:

* `Source code of the Bower registry <https://github.com/bower/registry>`_
