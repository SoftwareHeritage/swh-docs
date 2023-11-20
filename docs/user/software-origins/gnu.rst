.. _user-software-origins-gnu:

GNU projects
============

.. include:: dynamic/gnu_status.inc

|swh| archives all software available on https://ftp.gnu.org. It does so by listing
projects from https://ftp.gnu.org/tree.json.gz and passing them to the
:ref:`Archive loader <user-software-origins-archive>`.

This API provides a ``time`` field for each file, matching the time the file
was uploaded was updated; which is passed as ``last_update`` to the scheduler.
