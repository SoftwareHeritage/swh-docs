.. _user-software-origins-cran:

CRAN
====

.. include:: dynamic/cran_status.inc

The `Comprehensive R Archive Network <https://cran.r-project.org/>`_ is the package
management system of the R language.

CRAN does not expose a language-agnostic API with the information we need, so for
simplicity/efficiency, |swh|'s CRAN lister loads the weekly dump of the CRAN database
(in RDS format) and parses it with ``rpy2``
Then for each package, it creates an origin with
:file:`https://cran.r-project.org/package={package_name}` as URL.

R packages have intrinsic metadata, mostly the :file:`DESCRIPTION` file in their root
directory, in the `deb822 <https://manpages.debian.org/bookworm/dpkg-dev/deb822.5.en.html>`_
format.
|swh|'s R loader parses it to extract authorship information, but this file is otherwise
not parsed yet.
