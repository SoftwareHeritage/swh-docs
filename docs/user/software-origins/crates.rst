.. _user-software-origins-crates:

Crates
======

.. include:: dynamic/crates_status.inc

`crates.io <https://crates.io/>`_ is the package manager of the `Rust programming language
<https://www.rust-lang.org/>`_.

It relies on `an index hosted on GitHub <https://github.com/rust-lang/crates.io-index>`_,
and provides `database dumps <https://crates.io/data-access>`_, which |swh| uses to
list packages, and create origins using this pattern:
:file:`https://crates.io/crates/{crate}`.
