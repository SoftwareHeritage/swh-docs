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



How to build the doc
--------------------

Install the [Software Heritage development environment][2]

    $ git clone https://gitlab.softwareheritage.org/swh/devel/swh-environment.git
    $ cd swh-environment
    $ ./bin/update  # this will clone needed git repos, inc. swh-docs
    $ cd swh-docs

Ensure you have the required tools to generate images ([graphviz][3]'s `dot`,
[plantuml][4] and [inkscape][5]). On a Debian system:

    $ sudo apt install plantuml graphviz

These additional packages are required on Debian 10.x systems:
- libapr1-dev
- libaprutil1-dev
- libsvn-dev
- postgresql-11
- dia
- postgresql-autodoc

It is also recommended to build the doc using [tox][6], so ensure you have it
installed, eg. on a Debian system:

    $ sudo apt install tox


Then (from the `swh-environment/swh-docs/` directory):

    $ tox -e sphinx-dev

This tox environment will build the documentation from the sources available in
the parent directory (`swh-environment`).

Behind the scene, this tox environment will run the sphinx documentation
building process via [pifpaf][7] to encapsulate the need os Postgresql to
generate database schemas. The documentation building process itself consists
mainly in 3 steps:

### 1. Generate documentation assets for all modules

    $ cd swh-environment
    $ make docs-assets

This will *not* build the documentation in each module (there is `make docs`
for that).


### 2. Build the api docs for all swh python packages

    $ cd swh-docs/docs
    $ make apidoc

### 3. Build the documentation

    $ cd swh-docs/docs
    $ make

The HTML documentation is now available starting from `_build/html/index.html`.


Cleaning up
-----------

    $ cd docs
    $ make distclean

The former (`make clean`) will only clean the local Sphinx build, without
touching other modules. The latter (`make distclean`) will also clean Sphinx
builds in all other modules.


Publishing the doc
------------------

The publication of the documentation is now managed by the [CI][7].


Building standalone package documentation
-----------------------------------------

Each documentation local to a swh package can also be built with [tox][6].

For instance to build the standalone documentation of ``swh-web``, proceed as
follows:

    $ cd swh-environment/swh-web
    $ tox -e sphinx-dev

Sphinx warnings related to unresolved references located in other swh packages are suppressed because expected.

Please also note that Sphinx warnings are turned into errors in that case.

The HTML documentation is now available starting from `docs/_build/html/index.html`.


[1]: http://www.sphinx-doc.org/
[2]: https://gitlab.softwareheritage.org/swh/devel/swh-environment.git
[3]: https://graphviz.org
[4]: http://plantuml.com
[5]: https://inkscape.org/
[6]: https://tox.readthedocs.io/
[7]: https://jenkins.softwareheritage.org/job/DDOC/
