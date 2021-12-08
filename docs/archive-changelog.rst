.. _archive-changelog:

Archive ChangeLog
=================

Below you can find a time-indexed list of notable events and changes to
archival policies in the Software Heritage Archive. Each of them might have
(had) an impact on how content is archived and explain apparent statistical
anomalies or other changes in archival behavior over time. They are collected
in this document for historical reasons.


2021
----

* **2021-12-11** Completed first archival of the current and historical `Ubuntu
  <https://ubuntu.com/>`_ releases. Regular crawling of those repositories enabled
  (tracking: `T2400 <https://forge.softwareheritage.org/T2400>`_)

* **2021-11-22** Made the package loaders write release objects instead of revisions
  (tracking: `T3638 <https://forge.softwareheritage.org/T3638>`_)

* **2021-11-17:** Completed first archival of the `Opam Coq repository
  <https://coq.inria.fr/opam/released/>`_. Regular crawling of those repositories
  enabled (tracking: `T3717 <https://forge.softwareheritage.org/T3717>`_)

* **2021-10-14:** Completed archival of Bitbucket_ Mercurial repositories
  (tracking: `T3338 <https://forge.softwareheritage.org/T3338>`_)

* **2021-09-25** Completed first archival of the `Opam repository
  <https://opam.ocaml.org>`_. Regular crawling for those repositories
  enabled (tracking: `T3424 <https://forge.softwareheritage.org/T3424>`_)

* **2021-09-23** Completed first archival of the `Logilab Heptapod instance
  <https://forge.extranet.logilab.fr/>`_. Regular crawling for those repositories
  enabled (tracking: `T3597 <https://forge.softwareheritage.org/T3597>`_)

* **2021-09-23** Completed first archival of the `Heptapod instance
  <https://heptapod.host>`_. Regular crawling for those repositories enabled (tracking:
  `T3600 <https://forge.softwareheritage.org/T3600>`_)

* **2021-09-22** Completed first archival of the `FOSS Heptapod instance
  <https://foss.heptapod.net>`_. This is the first forge with mostly mercurial origins.
  Regular crawling for those repositories enabled (tracking: `T3581
  <https://forge.softwareheritage.org/T3581>`_)

* **2021-09-22** Disabled insertion of Git objects with non-canonical representations
  in the SWH data model (tracking: `T399 <https://forge.softwareheritage.org/T399>`)

* **2021-08-03** Completed first archival of SourceForge Mercurial repositories; regular
  crawling for those repositories enabled (tracking: `T3374
  <https://forge.softwareheritage.org/T3374>`_)

* **2021-07-22** Completed first archival of SourceForge Git and Subversion
  repositories; regular crawling for those repositories enabled (tracking:
  `T3374 <https://forge.softwareheritage.org/T3374>`_)


2020
----

* **2020-10-06 - 2020-11-23:** source code crawlers have been paused to avoid
  an out of disk condition, due to an unexpected delay in the arrival of new
  storage hardware. Push archival (both deposit_ and `save code now`_) remained
  in operation. (tracking: `T2656 <https://forge.softwareheritage.org/T2656>`_)

* **2020-09-15:** completed first archival of, and added to regular crawling
  `GNU Guix System`_ (tracking: `T2594
  <https://forge.softwareheritage.org/T2594>`_)

* **2020-06-11:** completed integration with the IPOL_ journal, allowing paper
  authors to explicitly deposit_ source code to the archive (`announcement
  <https://www.softwareheritage.org/2020/06/11/ipol-and-swh/>`__)

* **2020-05-25:** completed first archival of, and added to regular crawling
  NixOS_ (tracking: `T2411 <https://forge.softwareheritage.org/T2411>`_)


2019
----

* **2019-09-10:** completed first archival of Bitbucket_ Git repositories and
  added Bitbucket as a regularly crawled forge (tracking: `T592
  <https://forge.softwareheritage.org/T592>`_)

* **2019-06-30:** completed first archival of, and added to regular crawling,
  several GitLab_ instances: `0xacab.org <https://0xacab.org>`_, `framagit.org
  <https://framagit.org>`_, `gite.lirmm.fr <https://gite.lirmm.fr>`_,
  `gitlab.common-lisp.net <https://gitlab.common-lisp.net>`_,
  `gitlab.freedesktop.org <https://gitlab.freedesktop.org>`_, `gitlab.gnome.org
  <https://gitlab.gnome.org>`_, `gitlab.inria.fr <https://gitlab.inria.fr>`_,
  `salsa.debian.org <https://salsa.debian.org>`_

* **2019-06-12:** completed first archival of CRAN_ packages and added CRAN as
  a regularly crawled package repository (tracking: `T1709
  <https://forge.softwareheritage.org/T1709>`_)

* **2019-06-11:** completed a full archival of GNU_ source code releases from
  `ftp.gnu.org`_, and added it to regular crawling (tracking: `T1722
  <https://forge.softwareheritage.org/T1722>`_)

* **2019-05-27:** completed a full archival of NPM_ packages and added it as a
  regularly crawled package repository (tracking: `T1378
  <https://forge.softwareheritage.org/T1378>`_)

* **2019-01-10:** enabled the `save code now`_ service, allowing users to
  explicitly request archival of a specific source code repository
  (`announcement
  <https://www.softwareheritage.org/2019/01/10/save_code_now/>`__)


2018
----

* **2018-10-10:** completed first archival of PyPI_ packages and added PyPI as
  a regularly crawled package repository (`announcement
  <https://www.softwareheritage.org/2018/10/10/pypi-available-on-software-heritage/>`__)

* **2018-09-25:** completed integration with HAL_, allowing paper authors to
  explicitly deposit_ source code to the archive (`announcement
  <https://www.softwareheritage.org/2018/09/28/depositing-scientific-software-into-software-heritage/>`__)

* **2018-08-31:** completed first archival of public GitLab_ repositories from
  `gitlab.com <https://gitlab.com>`_ and added it as a regularly crawled forge
  (tracking: `T1111 <https://forge.softwareheritage.org/T1111>`_)

* **2018-03-21:** completed archival of `Google Code`_ Mercurial repositories.
  (tracking: `T682 <https://forge.softwareheritage.org/T682>`_)

* **2018-02-20:** completed archival of Debian_ packages and added Debian as a
  regularly crawled distribution (`announcement
  <https://www.softwareheritage.org/2018/02/20/listing-and-loading-of-debian-repositories-now-live/>`__)


2017
----

* **2017-10-02:** completed archival of `Google Code`_ Subversion repositories
  (tracking: `T617 <https://forge.softwareheritage.org/T617>`_)

* **2017-06-06:** completed archival of `Google Code`_ Git repositories
  (tracking: `T673 <https://forge.softwareheritage.org/T673>`_)


2016
----

* **2016-04-04:** completed archival of the Gitorious_ (tracking: `T312
  <https://forge.softwareheritage.org/T312>`_)


2015
----

* **2015-11-06:** archived all GNU_ source code releases from `ftp.gnu.org`_
  (tracking: `T90 <https://forge.softwareheritage.org/T90>`_)
* **2015-07-28:** started archiving public GitHub_ repositories



.. _Bitbucket: https://bitbucket.org
.. _CRAN: https://cran.r-project.org
.. _Debian: https://www.debian.org
.. _GNU Guix System: https://guix.gnu.org/
.. _GNU: https://en.wikipedia.org/wiki/Google_Code
.. _GitHub: https://github.com
.. _GitLab: https://gitlab.com
.. _Gitorious: https://en.wikipedia.org/wiki/Gitorious
.. _Google Code: https://en.wikipedia.org/wiki/Google_Code
.. _HAL: https://hal.archives-ouvertes.fr
.. _IPOL: http://www.ipol.im
.. _NPM: https://www.npmjs.com
.. _NixOS: https://nixos.org/
.. _PyPI: https://pypi.org
.. _deposit: https://deposit.softwareheritage.org
.. _ftp.gnu.org: http://ftp.gnu.org
.. _save code now: https://save.softwareheritage.org
