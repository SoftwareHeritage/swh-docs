.. _loaders:

Software Heritage loaders
*************************

A :term:`loader` is a software component used to ingest content into the |swh| archive.

This page references all available loaders and links to their high-level documentation.

.. rst-class:: swh-logos-table

.. table::
  :align: center

  +--------------------------+-------------------------------+-----------------------------+------------------------------------+
  | Loader name              | Related links                 | Current status              | Related `grants`_                  |
  +==========================+===============================+=============================+====================================+
  | |archive_logo|           | * |archive_loader_source|_    | |archive_loader_status|_    |                                    |
  |                          | * |archive_loader_devdoc|_    |                             |                                    |
  | :ref:`archive_loader`    |                               |                             |                                    |
  +--------------------------+-------------------------------+-----------------------------+------------------------------------+
  | |bzr_logo|               | * |bzr_loader_source|_        | |bzr_loader_status|_        | |bzr_loader_grant|_                |
  |                          | * |bzr_loader_devdoc|_        |                             |                                    |
  | :ref:`bzr_loader`        | * |bzr_loader_dev|_           |                             | (awarded to `Octobus`_)            |
  +--------------------------+-------------------------------+-----------------------------+------------------------------------+
  | |cran_logo|              | * |cran_loader_source|_       | |cran_loader_status|_       |                                    |
  |                          | * |cran_loader_devdoc|_       |                             |                                    |
  | :ref:`cran_loader`       | * |cran_loader_dev|_          |                             |                                    |
  +--------------------------+-------------------------------+-----------------------------+------------------------------------+
  | |crates_logo|            | * |crates_loader_source|_     | |crates_loader_status|_     | |crates_loader_grant|_             |
  |                          | * |crates_loader_source|_     |                             |                                    |
  | :ref:`crates_loader`     | * |crates_loader_dev|_        |                             | (awarded to `Hashbang`_)           |
  +--------------------------+-------------------------------+-----------------------------+------------------------------------+
  | |cvs_logo|               | * |cvs_loader_source|_        | |cvs_loader_status|_        | |cvs_loader_grant|_                |
  |                          | * |cvs_loader_devdoc|_        |                             |                                    |
  | :ref:`cvs_loader`        | * |cvs_loader_dev|_           |                             | (awarded to `Stefan Sperling`_)    |
  +--------------------------+-------------------------------+-----------------------------+------------------------------------+
  | |debian_logo|            | * |debian_loader_source|_     | |debian_loader_status|_     |                                    |
  |                          | * |debian_loader_devdoc|_     |                             |                                    |
  | :ref:`debian_loader`     | * |debian_loader_dev|_        |                             |                                    |
  +--------------------------+-------------------------------+-----------------------------+------------------------------------+
  | |deposit_logo|           | * |deposit_loader_source|_    | |deposit_loader_status|_    |                                    |
  |                          | * |deposit_loader_devdoc|_    |                             |                                    |
  | :ref:`deposit_loader`    | * |deposit_loader_dev|_       |                             |                                    |
  +--------------------------+-------------------------------+-----------------------------+------------------------------------+
  | |git_logo|               | * |git_loader_source|_        | |git_loader_status|_        |                                    |
  |                          | * |git_loader_devdoc|_        |                             |                                    |
  | :ref:`git_loader`        | * |git_loader_dev|_           |                             |                                    |
  +--------------------------+-------------------------------+-----------------------------+------------------------------------+
  | |maven_logo|             | * |maven_loader_source|_      | |maven_loader_status|_      | |maven_loader_grant|_              |
  |                          | * |maven_loader_devdoc|_      |                             |                                    |
  | :ref:`maven_loader`      | * |maven_loader_dev|_         |                             | (awarded to `Castalia Solutions`_) |
  +--------------------------+-------------------------------+-----------------------------+------------------------------------+
  | |mercurial_logo|         | * |mercurial_loader_source|_  | |mercurial_loader_status|_  | |mercurial_loader_grant|_          |
  |                          | * |mercurial_loader_devdoc|_  |                             |                                    |
  | :ref:`mercurial_loader`  | * |mercurial_loader_dev|_     |                             | (awarded to `Octobus`_)            |
  +--------------------------+-------------------------------+-----------------------------+------------------------------------+
  | |nixguix_logo|           | * |nixguix_loader_source|_    | |nixguix_loader_status|_    | |nixguix_loader_grant|_            |
  |                          | * |nixguix_loader_devdoc|_    |                             |                                    |
  | :ref:`nixguix_loader`    | * |nixguix_loader_dev|_       |                             | (awarded to `Tweag`_)              |
  +--------------------------+-------------------------------+-----------------------------+------------------------------------+
  | |npm_logo|               | * |npm_loader_source|_        | |npm_loader_status|_        |                                    |
  |                          | * |npm_loader_devdoc|_        |                             |                                    |
  | :ref:`npm_loader`        | * |npm_loader_dev|_           |                             |                                    |
  +--------------------------+-------------------------------+-----------------------------+------------------------------------+
  | |opam_logo|              | * |opam_loader_source|_       | |opam_loader_status|_       | |opam_loader_grant|_               |
  |                          | * |opam_loader_devdoc|_       |                             |                                    |
  | :ref:`opam_loader`       | * |opam_loader_dev|_          |                             | (awarded to `OCamlPro`_)           |
  +--------------------------+-------------------------------+-----------------------------+------------------------------------+
  | |pypi_logo|              | * |pypi_loader_source|_       | |pypi_loader_status|_       |                                    |
  |                          | * |pypi_loader_devdoc|_       |                             |                                    |
  | :ref:`pypi_loader`       | * |pypi_loader_dev|_          |                             |                                    |
  +--------------------------+-------------------------------+-----------------------------+------------------------------------+
  | |subversion_logo|        | * |subversion_loader_source|_ | |subversion_loader_status|_ |                                    |
  |                          | * |subversion_loader_devdoc|_ |                             |                                    |
  | :ref:`subversion_loader` | * |subversion_loader_dev|_    |                             |                                    |
  +--------------------------+-------------------------------+-----------------------------+------------------------------------+

.. toctree::
  :maxdepth: 2
  :hidden:

  archive
  bazaar
  cran
  crates
  cvs
  debian
  deposit
  git
  maven
  mercurial
  nixguix
  npm
  opam
  pypi
  subversion

.. |archive_logo| image:: ../logos/archive.png
  :width: 50%
  :target: archive.html
  :alt: Archive loader

.. |bzr_logo| image:: ../logos/bazaar.png
  :width: 50%
  :target: bazaar.html
  :alt: Bazaar loader

.. |cran_logo| image:: ../logos/cran.png
  :width: 50%
  :target: cran.html
  :alt: CRAN loader

.. |cvs_logo| image:: ../logos/cvs.png
  :width: 50%
  :target: cvs.html
  :alt: CVS loader

.. |crates_logo| image:: ../logos/crates.png
  :width: 50%
  :target: crates.html
  :alt: Crates loader

.. |debian_logo| image:: ../logos/debian.png
  :width: 50%
  :target: debian.html
  :alt: Debian loader

.. |deposit_logo| image:: ../logos/deposit.png
  :width: 50%
  :target: deposit.html
  :alt: Deposit loader

.. |git_logo| image:: ../logos/git.png
  :width: 50%
  :target: git.html
  :alt: Git loader

.. |maven_logo| image:: ../logos/maven.png
  :width: 50%
  :target: maven.html
  :alt: Maven loader

.. |mercurial_logo| image:: ../logos/mercurial.png
  :width: 50%
  :target: mercurial.html
  :alt: Mercurial loader

.. |nixguix_logo| image:: ../logos/nixguix.png
  :width: 50%
  :target: nixguix.html
  :alt: NixGuix loader

.. |npm_logo| image:: ../logos/npm.png
  :width: 50%
  :target: npm.html
  :alt: NPM loader

.. |opam_logo| image:: ../logos/opam.png
  :width: 50%
  :target: opam.html
  :alt: Opam loader

.. |pypi_logo| image:: ../logos/pypi.png
  :width: 50%
  :target: pypi.html
  :alt: PyPI loader

.. |subversion_logo| image:: ../logos/subversion.png
  :width: 50%
  :target: subversion.html
  :alt: Subversion loader

.. |archive_loader_source| replace:: Source code
.. _archive_loader_source: https://forge.softwareheritage.org/source/swh-loader-core/browse/master/swh/loader/package/archive/

.. |archive_loader_devdoc| replace:: Developer doc
.. _archive_loader_devdoc: https://docs.softwareheritage.org/devel/apidoc/swh.loader.package.archive.html

.. |archive_loader_status| replace:: in production
.. _archive_loader_status: https://archive.softwareheritage.org/browse/search/?with_visit=true&with_content=true&visit_type=tar


.. |bzr_loader_source| replace:: Source code
.. _bzr_loader_source: https://forge.softwareheritage.org/source/swh-loader-bzr/

.. |bzr_loader_devdoc| replace:: Developer doc
.. _bzr_loader_devdoc: https://docs.softwareheritage.org/devel/swh-loader-bzr/index.html

.. |bzr_loader_dev| replace:: Development
.. _bzr_loader_dev: https://forge.softwareheritage.org/project/profile/164/

.. |bzr_loader_status| replace:: in production
.. _bzr_loader_status: https://archive.softwareheritage.org/browse/search/?with_visit=true&with_content=true&visit_type=bzr

.. |bzr_loader_grant| replace:: Alfred P. Sloan Foundation
.. _bzr_loader_grant: https://www.softwareheritage.org/2021/01/21/archiving-sourceforge-and-supporting-bazaar/


.. |cran_loader_source| replace:: Source code
.. _cran_loader_source: https://forge.softwareheritage.org/source/swh-loader-core/browse/master/swh/loader/package/cran/

.. |cran_loader_devdoc| replace:: Developer doc
.. _cran_loader_devdoc: https://docs.softwareheritage.org/devel/apidoc/swh.loader.package.cran.html

.. |cran_loader_dev| replace:: Development
.. _cran_loader_dev: https://forge.softwareheritage.org/project/profile/132/

.. |cran_loader_status| replace:: in production
.. _cran_loader_status: https://archive.softwareheritage.org/browse/search/?with_visit=true&with_content=true&visit_type=cran


.. |crates_loader_source| replace:: Source code
.. _crates_loader_source: https://forge.softwareheritage.org/source/swh-loader-core/browse/master/swh/loader/package/crates/

.. |crates_loader_devdoc| replace:: Developer doc
.. _crates_loader_devdoc: https://docs.softwareheritage.org/devel/apidoc/swh.loader.package.crates.html

.. |crates_loader_dev| replace:: Development
.. _crates_loader_dev: https://forge.softwareheritage.org/project/profile/182/

.. |crates_loader_status| replace:: in development
.. _crates_loader_status: https://forge.softwareheritage.org/T4104

.. |crates_loader_grant| replace:: Alfred P. Sloan Foundation
.. _crates_loader_grant: ttps://www.softwareheritage.org/2022/02/03/hashbang-expanding-coverage-software-heritage-archive/


.. |cvs_loader_source| replace:: Source code
.. _cvs_loader_source: https://forge.softwareheritage.org/source/swh-loader-cvs/

.. |cvs_loader_devdoc| replace:: Developer doc
.. _cvs_loader_devdoc: https://docs.softwareheritage.org/devel/swh-loader-cvs/index.html

.. |cvs_loader_dev| replace:: Development
.. _cvs_loader_dev: https://forge.softwareheritage.org/project/profile/166/

.. |cvs_loader_status| replace:: in staging
.. _cvs_loader_status: https://webapp.staging.swh.network/browse/search/?with_visit=true&with_content=true&visit_type=cvs

.. |cvs_loader_grant| replace:: Alfred P. Sloan Foundation
.. _cvs_loader_grant: https://www.softwareheritage.org/2020/12/10/sloan-subgrant-cvs-subversion-loaders/


.. |debian_loader_source| replace:: Source code
.. _debian_loader_source: https://forge.softwareheritage.org/source/swh-loader-core/browse/master/swh/loader/package/debian/

.. |debian_loader_devdoc| replace:: Developer doc
.. _debian_loader_devdoc: https://docs.softwareheritage.org/devel/apidoc/swh.loader.package.debian.html

.. |debian_loader_dev| replace:: Development
.. _debian_loader_dev: https://forge.softwareheritage.org/project/profile/25/

.. |debian_loader_status| replace:: in production
.. _debian_loader_status: https://archive.softwareheritage.org/browse/search/?with_visit=true&with_content=true&visit_type=debian


.. |deposit_loader_source| replace:: Source code
.. _deposit_loader_source: https://forge.softwareheritage.org/source/swh-loader-core/browse/master/swh/loader/package/deposit/

.. |deposit_loader_devdoc| replace:: Developer doc
.. _deposit_loader_devdoc: https://docs.softwareheritage.org/devel/apidoc/swh.loader.package.deposit.html

.. |deposit_loader_dev| replace:: Development
.. _deposit_loader_dev: https://forge.softwareheritage.org/project/profile/77/

.. |deposit_loader_status| replace:: in production
.. _deposit_loader_status: https://archive.softwareheritage.org/browse/search/?with_visit=true&with_content=true&visit_type=deposit


.. |git_loader_source| replace:: Source code
.. _git_loader_source: https://forge.softwareheritage.org/source/swh-loader-git/

.. |git_loader_devdoc| replace:: Developer doc
.. _git_loader_devdoc: https://docs.softwareheritage.org/devel/swh-loader-git/index.html

.. |git_loader_dev| replace:: Development
.. _git_loader_dev: https://forge.softwareheritage.org/project/profile/17/

.. |git_loader_status| replace:: in production
.. _git_loader_status: https://archive.softwareheritage.org/browse/search/?with_visit=true&with_content=true&visit_type=git


.. |maven_loader_source| replace:: Source code
.. _maven_loader_source: https://forge.softwareheritage.org/source/swh-loader-core/browse/master/swh/loader/package/maven/

.. |maven_loader_devdoc| replace:: Developer doc
.. _maven_loader_devdoc: https://docs.softwareheritage.org/devel/apidoc/swh.loader.package.maven.html

.. |maven_loader_dev| replace:: Development
.. _maven_loader_dev: https://forge.softwareheritage.org/project/profile/185/

.. |maven_loader_status| replace:: in staging
.. _maven_loader_status: https://webapp.staging.swh.network/browse/search/?with_visit=true&with_content=true&visit_type=maven

.. |maven_loader_grant| replace:: Alfred P. Sloan Foundation
.. _maven_loader_grant: https://www.softwareheritage.org/2021/07/22/archiving-the-maven-ecosystem/


.. |mercurial_loader_source| replace:: Source code
.. _mercurial_loader_source: https://forge.softwareheritage.org/source/swh-loader-mercurial/

.. |mercurial_loader_devdoc| replace:: Developer doc
.. _mercurial_loader_devdoc: https://docs.softwareheritage.org/devel/swh-loader-mercurial/index.html

.. |mercurial_loader_dev| replace:: Development
.. _mercurial_loader_dev: https://forge.softwareheritage.org/project/profile/66/

.. |mercurial_loader_status| replace:: in production
.. _mercurial_loader_status: https://archive.softwareheritage.org/browse/search/?with_visit=true&with_content=true&visit_type=hg

.. |mercurial_loader_grant| replace:: NLnet Foundation
.. _mercurial_loader_grant: https://www.softwareheritage.org/2020/03/26/experts-join-forces-to-expand-the-software-heritage-archive/


.. |nixguix_loader_source| replace:: Source code
.. _nixguix_loader_source: https://forge.softwareheritage.org/source/swh-loader-core/browse/master/swh/loader/package/nixguix/

.. |nixguix_loader_devdoc| replace:: Developer doc
.. _nixguix_loader_devdoc: https://docs.softwareheritage.org/devel/apidoc/swh.loader.package.nixguix.html

.. |nixguix_loader_dev| replace:: Development
.. _nixguix_loader_dev: https://forge.softwareheritage.org/project/profile/152/

.. |nixguix_loader_status| replace:: in production
.. _nixguix_loader_status: https://archive.softwareheritage.org/browse/search/?with_content=true&visit_type=nixguix

.. |nixguix_loader_grant| replace:: NLnet Foundation
.. _nixguix_loader_grant: https://www.softwareheritage.org/2020/06/18/welcome-nixpkgs/


.. |npm_loader_source| replace:: Source code
.. _npm_loader_source: https://forge.softwareheritage.org/source/swh-loader-core/browse/master/swh/loader/package/npm/

.. |npm_loader_devdoc| replace:: Developer doc
.. _npm_loader_devdoc: https://docs.softwareheritage.org/devel/apidoc/swh.loader.package.npm.html

.. |npm_loader_dev| replace:: Development
.. _npm_loader_dev: https://forge.softwareheritage.org/project/profile/121/

.. |npm_loader_status| replace:: in production
.. _npm_loader_status: https://archive.softwareheritage.org/browse/search/?with_visit=true&with_content=true&visit_type=npm


.. |opam_loader_source| replace:: Source code
.. _opam_loader_source: https://forge.softwareheritage.org/source/swh-loader-core/browse/master/swh/loader/package/opam/

.. |opam_loader_devdoc| replace:: Developer doc
.. _opam_loader_devdoc: https://docs.softwareheritage.org/devel/apidoc/swh.loader.package.opam.html

.. |opam_loader_dev| replace:: Development
.. _opam_loader_dev: https://forge.softwareheritage.org/project/profile/167/

.. |opam_loader_status| replace:: in production
.. _opam_loader_status: https://archive.softwareheritage.org/browse/search/?with_visit=true&with_content=true&visit_type=opam

.. |opam_loader_grant| replace:: Alfred P. Sloan Foundation
.. _opam_loader_grant: https://www.softwareheritage.org/2021/04/20/connecting-ocaml/


.. |pypi_loader_source| replace:: Source code
.. _pypi_loader_source: https://forge.softwareheritage.org/source/swh-loader-core/browse/master/swh/loader/package/pypi/

.. |pypi_loader_devdoc| replace:: Developer doc
.. _pypi_loader_devdoc: https://docs.softwareheritage.org/devel/apidoc/swh.loader.package.pypi.html

.. |pypi_loader_dev| replace:: Development
.. _pypi_loader_dev: https://forge.softwareheritage.org/project/profile/88/

.. |pypi_loader_status| replace:: in production
.. _pypi_loader_status: https://archive.softwareheritage.org/browse/search/?with_visit=true&with_content=true&visit_type=pypi


.. |subversion_loader_source| replace:: Source code
.. _subversion_loader_source: https://forge.softwareheritage.org/source/swh-loader-svn/

.. |subversion_loader_devdoc| replace:: Developer doc
.. _subversion_loader_devdoc: https://docs.softwareheritage.org/devel/swh-loader-svn/index.html

.. |subversion_loader_dev| replace:: Development
.. _subversion_loader_dev: https://forge.softwareheritage.org/project/profile/37/

.. |subversion_loader_status| replace:: in production
.. _subversion_loader_status: https://archive.softwareheritage.org/browse/search/?with_visit=true&with_content=true&visit_type=svn


.. _grants: https://www.softwareheritage.org/grants/

.. _Castalia Solutions: https://castalia.solutions/
.. _Hashbang: https://hashbang.fr/
.. _OCamlPro: https://ocamlpro.com/
.. _Octobus: https://octobus.net/
.. _Stefan Sperling: https://stefansperling.de/
.. _Tweag: https://www.tweag.io/