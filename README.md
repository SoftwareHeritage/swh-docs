swh-docs
========

This module contains (the logics for generating) the Software Heritage
development documentation.

Specifically, it contains some general information about Software Heritage
internals (stuff that would not fit in any other specific software component of
the Software Heritage stack) and bundle them together component-specific
documentation coming from other modules of the stack.

All documentation is written and typeset using [Sphinx][1]. General
documentation is shipped as part of this module. Module-specific documentation
is centralized here via symlinks to the `docs/` dirs of individual modules.
Therefore to build the full documentation you need a working and
complete [Software Heritage development environment][2].

[1]: http://www.sphinx-doc.org/
[2]: https://forge.softwareheritage.org/source/swh-environment/


How to build the doc
--------------------

    $ cd docs
	$ make html

Behind the scene, this will do two things:

### 1. Generate sphinx-apidoc rst documents for all modules

    $ cd swh-environment
	$ make docs-apidoc

This will *not* build the documentation in each module (there is `make docs`
for that), but will use `sphinx-apidoc` to generate documentation indexes for
each (sub)modules in the various Software Heritage components.

As `sphinx-apidoc` refuses to overwrite old documents, before proceeding you
might need to clean up old cruft with:

    $ cd swh-environment
    $ make docs-clean


### 2. Build the documentation

    $ cd swh-docs/docs
    $ make

The HTML documentation is now available starting from `_build/html/index.html`.


Cleaning up
-----------

    $ cd docs
    $ make clean
    $ make distclean

The former (`make clean`) will only clean the local Sphinx build, without
touching other modules. The latter (`make distclean`) will also clean Sphinx
builds in all other modules.


Publishing the doc
------------------

    $ cd docs
    $ make install
    $ xdg-open https://docs.softwareheritage.org/devel/

For the above to work you need to have ssh access into the machine
hosting <https://docs.softwareheritage.org> (currently `pergamon`), and write
access do the document root directory of that virtual host (currently granted
to all members of the `swhdev` UNIX group on Software Heritage machines).
