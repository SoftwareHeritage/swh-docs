.. _user-software-origins-hackage:

Hackage
=======

.. include:: dynamic/hackage_status.inc

`Hackage <https://hackage.haskell.org/>`_ is the main package manager for the
Haskell ecosystem.

|swh| archives Hackage by querying ``https://hackage.haskell.org/packages/search``, which
returns the list of packages updated since a given date.
It then dispatches loading tasks to a dedicated loader, which downloads a list of revisions
from :file:`https://hackage.haskell.org/package/{pkgname}-{version}/revisions/` and packages
themselves from
:file:`https://hackage.haskell.org/package/{pkgname}-{version}/{pkgname}-{version}.tar.gz`.

Metadata from Hackage is archived as part of each package (in ``.cabal`` files).

Resources:

* `Source code of Hackage <https://github.com/haskell/hackage-server>`_

Source code from Hackage is currently only archived on |swh|'s staging infrastructure.
