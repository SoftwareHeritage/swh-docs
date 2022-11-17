.. _tools_upgrade:

How to manage upgrades of tools and software inventory
======================================================

How to use this page
--------------------

At regular intervals, a sysadmin must:

- Check the list of components to add new ones and delete eventual removed components
- Check the version of the components currently in use and compare it to the last available version
- If an upgrade is needed or recommended, create a task in the forge and reference it on the table
- Update the changelog section accordingly to the changes

SWH components
--------------


+------------------------+----------------------+------------------------+------------------------------------------------------------+-------+
| Software               | version (2021-12-29) | Last available version | Should upgrade ?                                           | Tasks |
+========================+======================+========================+============================================================+=======+
| kafka                  | 2.6.0                | 3.0.0                  | yes a lot of cve were fixed and it is an exposed service   |       |
+------------------------+----------------------+------------------------+------------------------------------------------------------+-------+
| Elasticsearch (search) | 7.15.2               | 7.16                   | we should follow the movement to avoid accumulating delay  |       |
+------------------------+----------------------+------------------------+------------------------------------------------------------+-------+
| redis                  | 5.0.3                | 6.2.6                  | N/A debian package                                         |       |
+------------------------+----------------------+------------------------+------------------------------------------------------------+-------+


Infra components
----------------

+---------------------+----------------------+------------------------+----------------------------+-------+
| Software            | version (2021-12-29) | Last available version | Should upgrade ?           | Tasks |
+=====================+======================+========================+============================+=======+
| Elasticsearch (ELK) | 7.15.2               | 7.16                   | yes                        |       |
+---------------------+----------------------+------------------------+----------------------------+-------+
| Logstash (ELK)      | 7.15.2               | 7.16                   | yes                        |       |
+---------------------+----------------------+------------------------+----------------------------+-------+
| filebeat (ELK)      | 7.15.2               | 7.16                   | yes                        |       |
+---------------------+----------------------+------------------------+----------------------------+-------+
| journalbeat (ELK)   | 7.15.2               | None                   | Subsumed by filebeat 7.16+ |       |
+---------------------+----------------------+------------------------+----------------------------+-------+
| Hedgedoc            | 1.9.2                | 1.9.2                  | N/A                        |       |
+---------------------+----------------------+------------------------+----------------------------+-------+
| OPNSense            | 21.7.7               | 21.7.7                 | N/A                        |       |
+---------------------+----------------------+------------------------+----------------------------+-------+
| sentry              | 21.12.0              | 21.12.0                | N/A                        |       |
+---------------------+----------------------+------------------------+----------------------------+-------+
| netbox              | 3.1.2                | 3.1.2                  | N/A                        |       |
+---------------------+----------------------+------------------------+----------------------------+-------+

Out of scope:
-------------

========== ==============
Software   Reason
========== ==============
icinga     debian package
prometheus debian package
grafana    debian package
jenkins    debian package
========== ==============

Links
-----

* Sentry versions: https://github.com/getsentry/sentry/releases/
* Netbox versions: https://github.com/netbox-community/netbox/releases/
* OPNSense versions: https://docs.opnsense.org/CE_releases.html
* Elasticsearch versions: https://www.elastic.co/guide/en/elasticsearch/reference/current/release-highlights.html

changelog
---------

* 2021-10-04 - Page creation
* 2021-10-11 - @olasd added journalbeat, added rationale for sentry, moved grafana to debian packages
* 2021-12-29 - @olasd upgraded sentry, hedgedoc, OPNSense, netbox; mentioned ELK upgrades; moved jenkins to debian packages
