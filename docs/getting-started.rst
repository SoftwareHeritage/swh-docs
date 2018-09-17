.. _getting-started:

Run your own Software Heritage
==============================

This tutorial will guide from the basic step of obtaining the source code of
the Software Heritage stack to running a local copy of it with which you can
archive source code and browse it on the web. To that end, just follow the
steps detailed below.

.. highlight:: bash


Step 0 --- get the code
-----------------------

The `swh-environment
<https://forge.softwareheritage.org/source/swh-environment/>`_ Git (meta)
repository orchestrates the Git repositories of all Software Heritage modules.
Clone it::

  git clone https://forge.softwareheritage.org/source/swh-environment.git

then recursively clone all Python module repositories. For this step you will
need the `mr <http://myrepos.branchable.com/>`_ tool. Once you have installed
``mr``, just run::

  cd swh-environment
  bin/update
  
.. IMPORTANT::

   From now on this tutorial will assume that you **run commands listed below
   from within the swh-environment** directory.

For periodic repository updates just re-run ``bin/update``.

From now on you will need to have a ``PYTHONPATH`` environment variable that
allows to find Python modules in the ``swh`` namespace. To that end you can
source the ``pythonpath.sh`` snippet from swh-environment::

  source pythonpath.sh

To make setting ``PYTHONPATH`` easier in the future, you might want to define a
shell alias, e.g.::

  alias swh-pythonpath='cd /path/to/swh-environment/ ; source pythonpath.sh ; cd - > /dev/null'


Step 1 --- install dependencies
-------------------------------

You need to install three types of dependencies: Python modules, Node.js
modules (for the web app), and Postgres (as storage backend).


Python modules
~~~~~~~~~~~~~~

You can install Python modules using ``pip3`` via the following helper::

  sudo bin/pip-install-deps

``pip-install-deps`` accepts additional ``pip3 install`` options so, e.g., if
you want to install Python modules as a user rather than system wide you can do
something like this instead::

  bin/pip-install-deps --user

If you want to see the list of Python dependencies, e.g., to install them by
hand or via your package manager, you can use a related helpe::

  bin/pip-ls-deps


Postgres
~~~~~~~~

You need a running Postgres instance with administrator access (e.g., to create
databases). On Debian/Ubuntu based distributions it should be as easy as::

  sudo apt install postgresql

For other platforms and more details refer to the `PostgreSQL installation
documnetation
<https://www.postgresql.org/docs/current/static/tutorial-install.html>`_.


Node.js modules
~~~~~~~~~~~~~~~

If you want to run the web app to browser your local archive you will need some
Node.js modules, in particular to pack web resources into a single compact
file. To that end the following should suffice::

  sudo apt install nodejs npm
  cd swh-web
  npm install
  cd -

You are now good to go with all needed dependencies on your development
machine!


Step 2 --- set up storage
-------------------------

Then you will need a local storage service that will archive and serve source
code artifacts via a REST API. The Software Heritage storage layer comes in two
parts: a content-addressable object storage on your file system (for file
contents) and a Postgres database (for the graph structure of the archive). See
the :ref:`data-model` for more information. The storage layer is configured via
a YAML configuration file, located at
``~/.config/swh/storage/storage.yml``. Create it with a content like:

.. code-block:: yaml

  storage:
    cls: local
    args:
      db: "host=localhost port=5432 dbname=softwareheritage-dev user=swhdev password=foobar"
      objstorage:
        cls: pathslicing
        args:
          root: /srv/softwareheritage/objects/
          slicing: 0:2/2:4

Make sure that the object storage root exists on the filesystem and is writable
to your user, e.g.::

  sudo mkdir /srv/softwareheritage/objects
  sudo chown "${USER}:" /srv/softwareheritage/objects

You are done with object storage setup! Let's setup the database::

  cd swh-storage/sql/
  sudo -u postgres  bin/db-init 5432 softwareheritage-dev swhdev
  cd -

Let's unpack the second line. You should have Postgres administrator privileges
to be able to create databases, hence the ``sudo -u postgres``; if your user
has Postgres admin privileges, you can avoid ``sudo`` here. ``5432`` is the
default port of the main Postgres cluster, adapt as needed.
``softwareheritage-dev`` is the name of the DB that will be created, it should
match the ``db`` line in ``storage.yml``; same goes for ``swhdev``, the DB user
name. You will be interactively asked for a password for the DB user; you
should provide one that matches the ``db`` line value.

To check that you can successfully connect to the DB (you will be interactively
asked for the DB password)::

  psql -h localhost -p 5432 -U swhdev softwareheritage-dev

Note that you can simplify interactive use and reduce configuration clutter
using Postgres `password
<https://www.postgresql.org/docs/current/static/libpq-pgpass.html>`_ and
`service
<https://www.postgresql.org/docs/current/static/libpq-pgservice.html>`_
configuration files. Any valid `libpq connection string
<https://www.postgresql.org/docs/current/static/libpq-connect.html#LIBPQ-CONNSTRING>`_
will make the ``db`` line of ``storage.yml`` happy.

You can now run the storage server like this::

  python3 -m swh.storage.api.server --host localhost --port 5002 ~/.config/swh/storage/storage.yml


Step 3 --- ingest repositories
------------------------------

You are now ready to ingest your first repository into your local Software
Heritage. For the sake of example, we will ingest a few Git repositories. The
module in charge of ingesting Git repositories is the *Git loader*, Python
module ``swh.loader.git``. Its configuration file is at
``~/.config/swh/loader/git-updater.yml``. Create it with a content like:

.. code-block:: yaml

  storage:
    cls: remote
    args:
      url: http://localhost:5002

It just informs the Git loader to use the storage server running on your
machine. The ``url`` line should match the command line used to run the storage
server.

You can now ingest Git repository on the command line using the command::

  python3 -m swh.loader.git.updater --origin-url GIT_CLONE_URL

For instance, you can try ingesting the following repositories, in increasing
size order (note that the last two might take a few hours to complete and will
occupy several GB on both the Postgres DB and the object storage)::

  python3 -m swh.loader.git.updater --origin-url https://github.com/SoftwareHeritage/swh-storage.git
  python3 -m swh.loader.git.updater --origin-url https://github.com/hylang/hy.git
  python3 -m swh.loader.git.updater --origin-url https://github.com/ocaml/ocaml.git

  # WARNING: next repo is big
  python3 -m swh.loader.git.updater --origin-url https://github.com/torvalds/linux.git

Congratulations, you have just archived your first source code repositories!

To re-archive the same repositories later on you can rerun the same commands:
only *new* objects added since the previous visit will be archived upon the
next one.


Step 4 --- browse the archive
-----------------------------

You can now setup a local web app to browse what you have locally archived. The
web app uses the configuration file ``~/.config/swh/webapp/webapp.yml``. Create
it and fill it with something like:

.. code-block:: yaml

  storage:
    cls: remote
    args:
      url: http://localhost:5002

Nothing new here, the configuration just references the local storage server,
which have been used before for repository ingestion.

You can now run the web app, and browse your local archive::

  make run-django-webpack-devserver
  xdg-open http://localhost:5004

Note that the ``make`` target will first compile a `webpack
<https://webpack.js.org/>`_ with various web assets and thenlaunch the web app;
for webpack compilation you will need the Node.js dependencies discussed above.

As an initial tour of the web app, try searching for one of the repositories
you have ingested (e.g., entering the ``hylang`` or ``ocaml`` keywords in the
search bar). Clicking on the repository name you will be brought back in time,
and you will be able to browse the source code and development history you have
archived.

Enjoy!
