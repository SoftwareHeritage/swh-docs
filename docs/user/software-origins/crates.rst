.. _user-software-origins-crates:

Crates
======

.. include:: dynamic/crates_status.inc

`crates.io <https://crates.io/>`__ is the package manager of the `Rust programming language
<https://www.rust-lang.org/>`__.

It relies on `an index hosted on GitHub <https://github.com/rust-lang/crates.io-index>`__,
and provides `database dumps <https://crates.io/data-access>`__, which |swh| uses to
list packages, and create origins using this pattern:
:file:`https://crates.io/crates/{crate}`.
