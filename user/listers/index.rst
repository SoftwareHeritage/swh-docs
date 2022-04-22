.. _listers:

Software Heritage listers
*************************

A :term:`lister` is a software component used for the discovering of software origins to
load into the |swh| archive.


This page references all available listers and links to their high-level documentation.

.. rst-class:: swh-logos-table

.. table::
  :align: center

  +---------------------------+--------------------------------+------------------------------+------------------------------------+
  | Lister name               | Related links                  | Current status               | Related `grants`_                  |
  +===========================+================================+==============================+====================================+
  | |bitbucket_logo|          | * |bitbucket_lister_source|_   | |bitbucket_lister_status|_   |                                    |
  |                           | * |bitbucket_lister_devdoc|_   |                              |                                    |
  | :ref:`bitbucket_lister`   | * |bitbucket_lister_dev|_      |                              |                                    |
  +---------------------------+--------------------------------+------------------------------+------------------------------------+
  | |cgit_logo|               | * |cgit_lister_source|_        | |cgit_lister_status|_        |                                    |
  |                           | * |cgit_lister_devdoc|_        |                              |                                    |
  | :ref:`cgit_lister`        | * |cgit_lister_dev|_           |                              |                                    |
  +---------------------------+--------------------------------+------------------------------+------------------------------------+
  | |cran_logo|               | * |cran_lister_source|_        | |cran_lister_status|_        |                                    |
  |                           | * |cran_lister_devdoc|_        |                              |                                    |
  | :ref:`cran_lister`        | * |cran_lister_dev|_           |                              |                                    |
  +---------------------------+--------------------------------+------------------------------+------------------------------------+
  | |crates_logo|             | * |crates_lister_source|_      | |crates_lister_status|_      | |crates_lister_grant|_             |
  |                           | * |crates_lister_devdoc|_      |                              |                                    |
  | :ref:`crates_lister`      | * |crates_lister_dev|_         |                              | (awarded to `Hashbang`_)           |
  +---------------------------+--------------------------------+------------------------------+------------------------------------+
  | |debian_logo|             | * |debian_lister_source|_      | |debian_lister_status|_      |                                    |
  |                           | * |debian_lister_devdoc|_      |                              |                                    |
  | :ref:`debian_lister`      |                                |                              |                                    |
  +---------------------------+--------------------------------+------------------------------+------------------------------------+
  | |gitea_logo|              | * |gitea_lister_source|_       | |gitea_lister_status|_       |                                    |
  |                           | * |gitea_lister_devdoc|_       |                              |                                    |
  | :ref:`gitea_lister`       |                                |                              |                                    |
  +---------------------------+--------------------------------+------------------------------+------------------------------------+
  | |github_logo|             | * |github_lister_source|_      | |github_lister_status|_      |                                    |
  |                           | * |github_lister_devdoc|_      |                              |                                    |
  | :ref:`github_lister`      | * |github_lister_dev|_         |                              |                                    |
  +---------------------------+--------------------------------+------------------------------+------------------------------------+
  | |gitlab_logo|             | * |gitlab_lister_source|_      | |gitlab_lister_status|_      |                                    |
  |                           | * |gitlab_lister_devdoc|_      |                              |                                    |
  | :ref:`gitlab_lister`      | * |gitlab_lister_dev|_         |                              |                                    |
  +---------------------------+--------------------------------+------------------------------+------------------------------------+
  | |gnu_logo|                | * |gnu_lister_source|_         | |gnu_lister_status|_         |                                    |
  |                           | * |gnu_lister_devdoc|_         |                              |                                    |
  | :ref:`gnu_lister`         | * |gnu_lister_dev|_            |                              |                                    |
  +---------------------------+--------------------------------+------------------------------+------------------------------------+
  | |launchpad_logo|          | * |launchpad_lister_source|_   | |launchpad_lister_status|_   |                                    |
  |                           | * |launchpad_lister_devdoc|_   |                              |                                    |
  | :ref:`launchpad_lister`   |                                |                              |                                    |
  +---------------------------+--------------------------------+------------------------------+------------------------------------+
  | |maven_logo|              | * |maven_lister_source|_       | |maven_lister_status|_       | |maven_lister_grant|_              |
  |                           | * |maven_lister_devdoc|_       |                              |                                    |
  | :ref:`maven_lister`       | * |maven_lister_dev|_          |                              | (awarded to `Castalia Solutions`_) |
  +---------------------------+--------------------------------+------------------------------+------------------------------------+
  | |npm_logo|                | * |npm_lister_source|_         | |npm_lister_status|_         |                                    |
  |                           | * |npm_lister_devdoc|_         |                              |                                    |
  | :ref:`npm_lister`         | * |npm_lister_dev|_            |                              |                                    |
  +---------------------------+--------------------------------+------------------------------+------------------------------------+
  | |opam_logo|               | * |opam_lister_source|_        | |opam_lister_status|_        | |opam_lister_grant|_               |
  |                           | * |opam_lister_devdoc|_        |                              |                                    |
  | :ref:`opam_lister`        |                                |                              | (awarded to `OCamlPro`_)           |
  +---------------------------+--------------------------------+------------------------------+------------------------------------+
  | |packagist_logo|          | * |packagist_lister_source|_   | |packagist_lister_status|_   |                                    |
  |                           | * |packagist_lister_devdoc|_   |                              |                                    |
  | :ref:`packagist_lister`   |                                |                              |                                    |
  +---------------------------+--------------------------------+------------------------------+------------------------------------+
  | |pypi_logo|               | * |pypi_lister_source|_        | |pypi_lister_status|_        |                                    |
  |                           | * |pypi_lister_devdoc|_        |                              |                                    |
  | :ref:`pypi_lister`        | * |pypi_lister_dev|_           |                              |                                    |
  +---------------------------+--------------------------------+------------------------------+------------------------------------+
  | |sourceforge_logo|        | * |sourceforge_lister_source|_ | |sourceforge_lister_status|_ | |sourceforge_lister_grant|_        |
  |                           | * |sourceforge_lister_devdoc|_ |                              |                                    |
  | :ref:`sourceforge_lister` | * |sourceforge_lister_dev|_    |                              | (awarded to `Octobus`_)            |
  +---------------------------+--------------------------------+------------------------------+------------------------------------+
  | |tuleap_logo|             | * |tuleap_lister_source|_      | |tuleap_lister_status|_      |                                    |
  |                           | * |tuleap_lister_devdoc|_      |                              |                                    |
  | :ref:`tuleap_lister`      |                                |                              |                                    |
  +---------------------------+--------------------------------+------------------------------+------------------------------------+



.. toctree::
  :maxdepth: 2
  :hidden:

  bitbucket
  cgit
  cran
  crates
  debian
  gitea
  github
  gitlab
  gnu
  launchpad
  maven
  npm
  opam
  packagist
  phabricator
  pypi
  sourceforge
  tuleap

.. |bitbucket_logo| image:: ../logos/bitbucket.png
  :width: 50%
  :target: bitbucket.html
  :alt: Bitbucket lister

.. |cgit_logo| image:: ../logos/cgit.png
  :width: 50%
  :target: cgit.html
  :alt: Cgit lister

.. |cran_logo| image:: ../logos/cran.png
  :width: 50%
  :target: cran.html
  :alt: CRAN lister

.. |crates_logo| image:: ../logos/crates.png
  :width: 50%
  :target: crates.html
  :alt: Crates lister

.. |debian_logo| image:: ../logos/debian.png
  :width: 50%
  :target: debian.html
  :alt: Debian lister

.. |gitea_logo| image:: ../logos/gitea.png
  :width: 50%
  :target: gitea.html
  :alt: Gitea lister

.. |github_logo| image:: ../logos/github.png
  :width: 50%
  :target: github.html
  :alt: GitHub lister

.. |gitlab_logo| image:: ../logos/gitlab.png
  :width: 50%
  :target: gitlab.html
  :alt: GitLab lister

.. |gnu_logo| image:: ../logos/gnu.png
  :width: 50%
  :target: gnu.html
  :alt: GNU lister

.. |launchpad_logo| image:: ../logos/launchpad.png
  :width: 50%
  :target: launchpad.html
  :alt: Launchpad lister

.. |maven_logo| image:: ../logos/maven.png
  :width: 50%
  :target: maven.html
  :alt: Maven lister

.. |npm_logo| image:: ../logos/npm.png
  :width: 50%
  :target: npm.html
  :alt: NPM lister

.. |opam_logo| image:: ../logos/opam.png
  :width: 50%
  :target: opam.html
  :alt: Opam lister

.. |packagist_logo| image:: ../logos/packagist.png
  :width: 50%
  :target: packagist.html
  :alt: Packagist lister

.. |phabricator_logo| image:: ../logos/phabricator.png
  :width: 50%
  :target: phabricator.html
  :alt: Phabricator lister

.. |pypi_logo| image:: ../logos/pypi.png
  :width: 50%
  :target: pypi.html
  :alt: PyPI lister

.. |sourceforge_logo| image:: ../logos/sourceforge.png
  :width: 50%
  :target: sourceforge.html
  :alt: SourceForge lister

.. |tuleap_logo| image:: ../logos/tuleap.png
  :width: 50%
  :target: tuleap.html
  :alt: Tuleap lister

.. |bitbucket_lister_source| replace:: Source code
.. _bitbucket_lister_source: https://forge.softwareheritage.org/source/swh-lister/browse/master/swh/lister/bitbucket/

.. |bitbucket_lister_devdoc| replace:: Developer doc
.. _bitbucket_lister_devdoc: https://docs.softwareheritage.org/devel/apidoc/swh.lister.bitbucket.html

.. |bitbucket_lister_dev| replace:: Development
.. _bitbucket_lister_dev: https://forge.softwareheritage.org/project/profile/67/

.. |bitbucket_lister_status| replace:: in production
.. _bitbucket_lister_status: https://archive.softwareheritage.org/coverage/?focus=bitbucket#bitbucket


.. |cgit_lister_source| replace:: Source code
.. _cgit_lister_source: https://forge.softwareheritage.org/source/swh-lister/browse/master/swh/lister/cgit/

.. |cgit_lister_devdoc| replace:: Developer doc
.. _cgit_lister_devdoc: https://docs.softwareheritage.org/devel/apidoc/swh.lister.cgit.html

.. |cgit_lister_dev| replace:: Development
.. _cgit_lister_dev: https://forge.softwareheritage.org/project/profile/22/

.. |cgit_lister_status| replace:: in production
.. _cgit_lister_status: https://archive.softwareheritage.org/coverage/?focus=cgit#cgit


.. |cran_lister_source| replace:: Source code
.. _cran_lister_source: https://forge.softwareheritage.org/source/swh-lister/browse/master/swh/lister/cran/

.. |cran_lister_devdoc| replace:: Developer doc
.. _cran_lister_devdoc: https://docs.softwareheritage.org/devel/apidoc/swh.lister.cran.html

.. |cran_lister_dev| replace:: Development
.. _cran_lister_dev: https://forge.softwareheritage.org/project/profile/132/

.. |cran_lister_status| replace:: in production
.. _cran_lister_status: https://archive.softwareheritage.org/coverage/?focus=CRAN#CRAN


.. |crates_lister_source| replace:: Source code
.. _crates_lister_source: https://forge.softwareheritage.org/source/swh-lister/browse/master/swh/lister/crates/

.. |crates_lister_devdoc| replace:: Developer doc
.. _crates_lister_devdoc: https://docs.softwareheritage.org/devel/apidoc/swh.lister.crates.html

.. |crates_lister_dev| replace:: Development
.. _crates_lister_dev: https://forge.softwareheritage.org/project/profile/183/

.. |crates_lister_status| replace:: in development
.. _crates_lister_status: https://forge.softwareheritage.org/T1424

.. |crates_lister_grant| replace:: Alfred P. Sloan Foundation
.. _crates_lister_grant: https://www.softwareheritage.org/2022/02/03/hashbang-expanding-coverage-software-heritage-archive/


.. |debian_lister_source| replace:: Source code
.. _debian_lister_source: https://forge.softwareheritage.org/source/swh-lister/browse/master/swh/lister/debian/

.. |debian_lister_devdoc| replace:: Developer doc
.. _debian_lister_devdoc: https://docs.softwareheritage.org/devel/apidoc/swh.lister.debian.html

.. |debian_lister_status| replace:: in production
.. _debian_lister_status: https://archive.softwareheritage.org/coverage/?focus=debian#debian


.. |gitea_lister_source| replace:: Source code
.. _gitea_lister_source: https://forge.softwareheritage.org/source/swh-lister/browse/master/swh/lister/gitea/

.. |gitea_lister_devdoc| replace:: Developer doc
.. _gitea_lister_devdoc: https://docs.softwareheritage.org/devel/apidoc/swh.lister.gitea.html

.. |gitea_lister_status| replace:: in production
.. _gitea_lister_status: https://archive.softwareheritage.org/coverage/?focus=gitea#gitea


.. |github_lister_source| replace:: Source code
.. _github_lister_source: https://forge.softwareheritage.org/source/swh-lister/browse/master/swh/lister/github/

.. |github_lister_devdoc| replace:: Developer doc
.. _github_lister_devdoc: https://docs.softwareheritage.org/devel/apidoc/swh.lister.github.html

.. |github_lister_dev| replace:: Development
.. _github_lister_dev: https://forge.softwareheritage.org/project/profile/21/

.. |github_lister_status| replace:: in production
.. _github_lister_status: https://archive.softwareheritage.org/coverage/?focus=github#github


.. |gitlab_lister_source| replace:: Source code
.. _gitlab_lister_source: https://forge.softwareheritage.org/source/swh-lister/browse/master/swh/lister/gitlab/

.. |gitlab_lister_devdoc| replace:: Developer doc
.. _gitlab_lister_devdoc: https://docs.softwareheritage.org/devel/apidoc/swh.lister.gitlab.html

.. |gitlab_lister_dev| replace:: Development
.. _gitlab_lister_dev: https://forge.softwareheritage.org/project/profile/83/

.. |gitlab_lister_status| replace:: in production
.. _gitlab_lister_status: https://archive.softwareheritage.org/coverage/?focus=gitlab,heptapod#gitlab


.. |gnu_lister_source| replace:: Source code
.. _gnu_lister_source: https://forge.softwareheritage.org/source/swh-lister/browse/master/swh/lister/gnu/

.. |gnu_lister_devdoc| replace:: Developer doc
.. _gnu_lister_devdoc: https://docs.softwareheritage.org/devel/apidoc/swh.lister.gnu.html

.. |gnu_lister_dev| replace:: Development
.. _gnu_lister_dev: https://forge.softwareheritage.org/project/profile/70/

.. |gnu_lister_status| replace:: in production
.. _gnu_lister_status: https://archive.softwareheritage.org/coverage/?focus=GNU#GNU


.. |launchpad_lister_source| replace:: Source code
.. _launchpad_lister_source: https://forge.softwareheritage.org/source/swh-lister/browse/master/swh/lister/launchpad/

.. |launchpad_lister_devdoc| replace:: Developer doc
.. _launchpad_lister_devdoc: https://docs.softwareheritage.org/devel/apidoc/swh.lister.launchpad.html

.. |launchpad_lister_status| replace:: in production
.. _launchpad_lister_status: https://archive.softwareheritage.org/coverage/?focus=launchpad#launchpad


.. |maven_lister_source| replace:: Source code
.. _maven_lister_source: https://forge.softwareheritage.org/source/swh-lister/browse/master/swh/lister/maven/

.. |maven_lister_devdoc| replace:: Developer doc
.. _maven_lister_devdoc: https://docs.softwareheritage.org/devel/apidoc/swh.lister.maven.html

.. |maven_lister_dev| replace:: Development
.. _maven_lister_dev: https://forge.softwareheritage.org/project/profile/184/

.. |maven_lister_status| replace:: in staging
.. _maven_lister_status: https://webapp.staging.swh.network/coverage/?focus=maven#maven

.. |maven_lister_grant| replace:: Alfred P. Sloan Foundation
.. _maven_lister_grant: https://www.softwareheritage.org/2021/07/22/archiving-the-maven-ecosystem/


.. |npm_lister_source| replace:: Source code
.. _npm_lister_source: https://forge.softwareheritage.org/source/swh-lister/browse/master/swh/lister/npm/

.. |npm_lister_devdoc| replace:: Developer doc
.. _npm_lister_devdoc: https://docs.softwareheritage.org/devel/apidoc/swh.lister.npm.html

.. |npm_lister_dev| replace:: Development
.. _npm_lister_dev: https://forge.softwareheritage.org/project/profile/111/

.. |npm_lister_status| replace:: in production
.. _npm_lister_status: https://archive.softwareheritage.org/coverage/?focus=npm#npm


.. |opam_lister_source| replace:: Source code
.. _opam_lister_source: https://forge.softwareheritage.org/source/swh-lister/browse/master/swh/lister/opam/

.. |opam_lister_devdoc| replace:: Developer doc
.. _opam_lister_devdoc: https://docs.softwareheritage.org/devel/apidoc/swh.lister.opam.html

.. |opam_lister_status| replace:: in production
.. _opam_lister_status: https://archive.softwareheritage.org/coverage/?focus=opam#opam

.. |opam_lister_grant| replace:: Alfred P. Sloan Foundation
.. _opam_lister_grant: https://www.softwareheritage.org/2021/04/20/connecting-ocaml/


.. |packagist_lister_source| replace:: Source code
.. _packagist_lister_source: https://forge.softwareheritage.org/source/swh-lister/browse/master/swh/lister/packagist/

.. |packagist_lister_devdoc| replace:: Developer doc
.. _packagist_lister_devdoc: https://docs.softwareheritage.org/devel/apidoc/swh.lister.packagist.html

.. |packagist_lister_status| replace:: in staging
.. _packagist_lister_status: https://webapp.staging.swh.network/coverage/?focus=Packagist#Packagist


.. |phabricator_lister_source| replace:: Source code
.. _phabricator_lister_source: https://forge.softwareheritage.org/source/swh-lister/browse/master/swh/lister/phabricator/

.. |phabricator_lister_devdoc| replace:: Developer doc
.. _phabricator_lister_devdoc: https://docs.softwareheritage.org/devel/apidoc/swh.lister.phabricator.html

.. |phabricator_lister_status| replace:: in production
.. _phabricator_lister_status: https://archive.softwareheritage.org/coverage/?focus=phabricator#phabricator


.. |pypi_lister_source| replace:: Source code
.. _pypi_lister_source: https://forge.softwareheritage.org/source/swh-lister/browse/master/swh/lister/pypi/

.. |pypi_lister_devdoc| replace:: Developer doc
.. _pypi_lister_devdoc: https://docs.softwareheritage.org/devel/apidoc/swh.lister.pypi.html

.. |pypi_lister_dev| replace:: Development
.. _pypi_lister_dev: https://forge.softwareheritage.org/project/profile/54/

.. |pypi_lister_status| replace:: in production
.. _pypi_lister_status: https://archive.softwareheritage.org/coverage/?focus=pypi#pypi


.. |sourceforge_lister_source| replace:: Source code
.. _sourceforge_lister_source: https://forge.softwareheritage.org/source/swh-lister/browse/master/swh/lister/sourceforge/

.. |sourceforge_lister_devdoc| replace:: Developer doc
.. _sourceforge_lister_devdoc: https://docs.softwareheritage.org/devel/apidoc/swh.lister.sourceforge.html

.. |sourceforge_lister_dev| replace:: Development
.. _sourceforge_lister_dev: https://forge.softwareheritage.org/project/profile/75/

.. |sourceforge_lister_status| replace:: in production
.. _sourceforge_lister_status: https://archive.softwareheritage.org/coverage/?focus=sourceforge#sourceforge

.. |sourceforge_lister_grant| replace:: Alfred P. Sloan Foundation
.. _sourceforge_lister_grant: https://www.softwareheritage.org/2021/08/12/archiving-sourceforge/


.. |tuleap_lister_source| replace:: Source code
.. _tuleap_lister_source: https://forge.softwareheritage.org/source/swh-lister/browse/master/swh/lister/tuleap/

.. |tuleap_lister_devdoc| replace:: Developer doc
.. _tuleap_lister_devdoc: https://docs.softwareheritage.org/devel/apidoc/swh.lister.tuleap.html

.. |tuleap_lister_status| replace:: in development
.. _tuleap_lister_status: https://forge.softwareheritage.org/T3334


.. _Castalia Solutions: https://castalia.solutions/
.. _Hashbang: https://hashbang.fr/
.. _OCamlPro: https://ocamlpro.com/
.. _Octobus: https://octobus.net/

.. _grants: https://www.softwareheritage.org/grants/