.. _archive-journal:


Software Heritage --- Notable Archive Changes
=============================================

Below you can find a time-indexed list of notable events and changes to
archival policies in the Software Heritage Archive. Each of them might have
(had) an impact on how content is archived and explain apparent anomalies or
other changes in archival behaviour over time. They are collected in this
document for historical reasons.


**WARNING:** this document is **work in progress** and not considered complete
yet (tracking: `T2793 <https://forge.softwareheritage.org/T2793>`_).


2020
----

* **2020-10-06 - 2020-11-23:** source code crawlers have been paused to avoid
  an out of disk condition, due to an unexpected delay in the arrival of new
  storage hardware. Push archival (both `deposit` and `save code now`) remained
  in operation. (tracking: `T2656 <https://forge.softwareheritage.org/T2656>`_)

* **2020-06-11:** completed integration with the `IPOL`_ journal, allowing
  paper authors to explicitly `deposit` source code to the archive (
  (`announcement <https://www.softwareheritage.org/2020/06/11/ipol-and-swh/>`_)


2019
----

* **2019-09-10:** completed first ingestion of `Bitbucket`_ Git repositories
  and added Bitbucket as a regularly crawled forge (tracking: `T592
  <https://forge.softwareheritage.org/T592>`_)

* **2019-06-12:** completed first ingestion of `CRAN`_ packages and added CRAN
  as a regularly crawled package repository (tracking: `T1709
  <https://forge.softwareheritage.org/T1709>`_)

* **2019-01-10:** enabled the `save code now`_ service, allowing users to
  explicitly request archival of a specific source code repository
  (`announcement
  <https://www.softwareheritage.org/2019/01/10/save_code_now/>`_)


2018
----

* **2018-10-10:** completed first ingestion of `PyPI`_ packages and added PyPI
  as a regularly crawled package repository (`announcement
  <https://www.softwareheritage.org/2018/10/10/pypi-available-on-software-heritage/>`_)

* **2018-09-25:** completed integration with `HAL`_, allowing paper authors to
  explicitly `deposit` source code to the archive (`announcement
  <https://www.softwareheritage.org/2018/09/28/depositing-scientific-software-into-software-heritage/>`_)

* **2018-03-21:** completed import of `Google Code`_ Mercurial repositories.
  (tracking: `T682 <https://forge.softwareheritage.org/T682>`_)

* **2018-02-20:** completed import of `Debian`_ packages and added Debian as a
  regularly crawled distribution (`announcement
  <https://www.softwareheritage.org/2018/02/20/listing-and-loading-of-debian-repositories-now-live/>`_)


2017
----

* **2017-10-02:** completed import of `Google Code`_ Subversion repositories
  (tracking: `T617 <https://forge.softwareheritage.org/T617>`_)

* **2017-06-06:** completed import of `Google Code`_ Git repositories
  (tracking: `T673 <https://forge.softwareheritage.org/T673>`_)


2016
----

* **2016-04-04:** completed import of the `Gitorious`_ (tracking: `T312
  <https://forge.softwareheritage.org/T312>`_)


2015
----

* **2015-07-28:** started archiving public `GitHub`_ repositories



.. _Bitbucket: https://bitbucket.org
.. _CRAN: https://cran.r-project.org
.. _Debian: https://www.debian.org
.. _GitHub: https://github.com
.. _Gitorious: https://en.wikipedia.org/wiki/Gitorious
.. _Google Code: https://en.wikipedia.org/wiki/Google_Code
.. _HAL: https://hal.archives-ouvertes.fr
.. _IPOL: http://www.ipol.im
.. _PyPI: https://pypi.org
.. _deposit: https://deposit.softwareheritage.org
.. _save code now: http://save.softwareheritage.org/
