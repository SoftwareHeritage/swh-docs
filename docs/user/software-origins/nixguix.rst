.. _user-software-origins-nixguix:

Nix and Guix
============

.. include:: dynamic/nixguix_status.inc

This page documents how |swh| archives source packages from the `GNU Guix`_ and Nix_
distributions.

Those distributions provide functional package managers with similar properties (e.g.
transactional, declarative up to the operating system, reproducible, ...). Definition of
packages is dependent on their respective DSL. As it's not easily parsable nor any
listing api existed, community effort was done to provide regular extraction of origins
listing as json manifest.

|swh|'s :py:class:`swh.lister.nixguix.lister.NixGuix` lister queries respectively those
manifests. As they contain various types of origins, |swh| uses various loaders to
ingest with those origins, url targeting a:

- **simple file:** :py:class:`swh.loader.core.loader.ContentLoader`
  ingests origin of type ``content``.
- **tarball:** :py:class:`swh.loader.core.loader.TarballDirectoryLoader`
  ingests origin with type ``tarball-directory``.
- :ref:`Svn <user-software-origins-svn>` **repository:**
  :py:class:`swh.loader.svn.loader.SvnLoader` ingests origin with type ``svn``.
- :ref:`Svn <user-software-origins-svn>` **repository at a specific revision:**
  :py:class:`swh.loader.svn.directory.SvnExportLoader` ingests origins
  with type ``svn-export``.
- :ref:`Git <user-software-origins-git>` **repository:**
  :py:class:`swh.loader.git.loader.GitLoader` ingests origin with type ``git``.
- :ref:`Git <user-software-origins-git>` **repository at a specific git commit:**
  :py:class:`swh.loader.git.directory.GitCheckoutLoader` ingests origin with type
  ``git-checkout``.
- :ref:`Mercurial <user-software-origins-mercurial>` **repository:**
  :py:class:`swh.loader.mercurial.loader.HgLoader` ingests origin with type ``hg``.
- :ref:`Mercurial <user-software-origins-mercurial>` **repository:**
  :py:class:`swh.loader.mercurial.directory.HgCheckoutLoader>` ingests origin with type
  ``hg-checkout``.

Origin URLs match each main url provided in the manifest.

For some cases like content or tarball urls, there can be mirror urls provided. They are
used as fallback artifact retrieval when the main url is no longer available.

No extrinsic nor intrinsic metadata collection is happening on the lister's side.

For some origin visit types (``content``, ``tarball-directory``, ``svn-export``,
``hg-checkout``, ``git-checkout``), extra intrinsic information like the artifact
checksums (``standard``, e.g. sha256, or ``nar``, specific intrinsic identifier used by
`GNU Guix`_ and Nix_, see :py:class:`swh.loader.core.nar.Nar`), are transmitted to the
loaders.

During their ingestion, if the checksum(s) do not match, the artifact is rejected and
the visit is marked as ``failed``. If not, the artifact is ingested.

The resulting snapshot of the visit is targeting either a content for the loading of a
file (visit type ``content``) either a directory for tarball (visit type
``tarball-directory``) and vcs repository at specific commit (``git-checkout``,
``svn-export``, ``hg-checkout``). Usual standard snapshot happens for vcs (``git``,
``svn``, ``hg``) repository ingestion.

Note also that a new entry is recorded in the ExtID table to map the SWHID content (for
a file) or the SWHID directory (for the other kind) ingested to their their original
checksum.

Sample:

+-----------------+---------------+--------------------------------------------------------------------+-------------+--------------------------------------------+
| extid_type      | extid_version | extid                                                              | target_type | target                                     |
+-----------------+---------------+--------------------------------------------------------------------+-------------+--------------------------------------------+
| checksum-sha256 |             1 | \x00001a5b5be28bde9bc8c353afe546d8fe84e49b269a70393c1616957b0e1cce | directory   | \xbe186100480d766ebdf0cfaeac0c90198f4b42e7 |
+-----------------+---------------+--------------------------------------------------------------------+-------------+--------------------------------------------+
| nar-sha256      |             1 | \x00002584a56a9bce85793515604298f8b3b1e9497e00fc6361a0c2e731c063f3 | directory   | \x1e1ace5b0ef56e188d3cf99059070cc5448d7454 |
+-----------------+---------------+--------------------------------------------------------------------+-------------+--------------------------------------------+

Resources:

* `Gnu Guix git repository <https://git.savannah.gnu.org/cgit/guix.git>`__

* `Nixpkgs git repository <https://github.com/nixos/nixpkgs>`__

* `Remote nixpkgs json manifest <https://nix-community.github.io/nixpkgs-swh/sources-unstable-full.json>`__

- `Remote guix json manifest <https://nix-community.github.io/nixpkgs-swh/>`__

.. _`GNU Guix`: https://guix.gnu.org/
.. _Nix: https://nixos.org/
