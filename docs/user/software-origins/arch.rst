.. _user-software-origins-arch:

Archlinux
=========

.. include:: dynamic/arch_status.inc

This page documents how |swh| archives source packages from the
`Archlinux <https://archlinux.org/>`_ and `Archlinux ARM <https://archlinuxarm.org>`_
distribution.
The `AUR (Archlinux User Repository) <https://aur.archlinux.org/>`_ is
:ref:`described in its own dedicated documentation <user-software-origins-aur>`,
as it uses a very different packaging architecture.

|swh| currently has a lister and a loader for Archlinux packages, but they list and load
binary packages; and need to be modified to list and load source packages instead.

Origin URLs match the one of the canonical web page displaying information about each
package. For example: https://archlinux.org/packages/core/x86_64/coreutils/
and https://aur.archlinux.org/packages/hg-evolve.

As all metadata about Archlinux packages is stored within the package (in
:file:`PKGBUILD` in the source, or :file:`.PKGINFO` in the binary package), |swh| does
not need to store them as :term:`extrinsic metadata`.

Resources:

* `HTTP API documentation <https://wiki.archlinux.org/title/Official_repositories_web_interface>`_
