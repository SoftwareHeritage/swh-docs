.. _user-software-origins-golang:

Golang
======

.. include:: dynamic/golang_status.inc

The `Go programming language <https://go.dev/>`_ identifies modules using URL-like
strings, called the "module path".
Module paths start with a domain and path to a VCS repository (usually Git) and
optionally path of a directory within that repository. See the
`Go Modules Reference <https://go.dev/ref/mod>`_ for details.

|swh| follows the convention of the Golang ecosystem of proxying through the
proxy.golang.org rather than accessing these repositories directly in order to be
as close as possible to the Go build system.

Go origin URLs in |swh| are module paths prefixed with ``https://pkg.go.dev/``.
For example, the origin URL for module ``github.com/gofiber/fiber`` is
``https://pkg.go.dev/github.com/gofiber/fiber`` (`see it in the archive <https://archive.softwareheritage.org/browse/origin/directory/?origin_url=https://pkg.go.dev/github.com/gofiber/fiber>`__)

In the Golang ecosystem, it is customary to handle breaking changes in a module by
publishing the new module version at a different path; for example
``github.com/gofiber/fiber/v2``.
See `Module version numbering <https://go.dev/doc/modules/version-numbers>`_ for details.
|swh| follows this convention, and uses different origin URLs for new major versions,
such as ``https://pkg.go.dev/github.com/gofiber/fiber/v2`` (`see it in the archive <https://archive.softwareheritage.org/browse/origin/directory/?origin_url=https://pkg.go.dev/github.com/gofiber/fiber/v2>`__)

On the technical side, |swh| fetches the list of known Go modules from
https://index.golang.org/index, and relies on the given timestamps to detect updates
to packages archived in the past.
