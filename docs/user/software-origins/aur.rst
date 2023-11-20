.. _user-software-origins-aur:

AUR
===

.. include:: dynamic/aur_status.inc

This page documents how |swh| archives source packages from the
`AUR (Archlinux User Repository) <https://aur.archlinux.org/>`.
The `Archlinux <https://archlinux.org/>`_ and `Archlinux ARM <https://archlinuxarm.org>`_
distributions are
:ref:`described in their own dedicated documentation <user-software-origins-arch>`,
as they uses a very different packaging architecture.

The AUR lister will send requests to https://aur.archlinux.org/packages-meta-v1.json.gz
to get a list of packages; then tells the AUR loader to creates origins like
https://aur.archlinux.org/hg-evolve.git using tarballs from URLs like
https://aur.archlinux.org/cgit/aur.git/snapshot/hg-evolve.tar.gz

.. note::

   We should probably use https://aur.archlinux.org/packages/hg-evolve as origin URL
   instead of https://aur.archlinux.org/hg-evolve.git

As all metadata about AUR packages is stored within the :file:`PKGBUILD` file that
serves as source, |swh| does
not need to store them as :term:`extrinsic metadata`.

Resources:

* `HTTP API documentation <https://wiki.archlinux.org/title/Aurweb_RPC_interface>`_
