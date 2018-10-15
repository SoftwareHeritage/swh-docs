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


Step 1 --- install system dependencies
--------------------------------------

You need to install three types of dependencies: some base packages, Node.js
modules (for the web app), and Postgres (as storage backend).

Package dependencies
~~~~~~~~~~~~~~~~~~~~

Software Heritage requires some dependencies that are usually packaged by your
package manager. On Debian/Ubuntu-based distributions::

  sudo apt-get install curl ca-certificates
  curl https://deb.nodesource.com/setup_8.x | sudo bash
  curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
  sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
  sudo apt update
  sudo apt install python3 python3-venv libsvn-dev postgresql-10 nodejs \
                   libsystemd-dev

Postgres
~~~~~~~~

You need a running Postgres instance with administrator access (e.g., to create
databases). On Debian/Ubuntu based distributions, the previous step
(installation) should be enough.

For other platforms and more details refer to the `PostgreSQL installation
documentation
<https://www.postgresql.org/docs/current/static/tutorial-install.html>`_.

You also need to have access to a superuser account on the database. For that,
the easiest way is to create a PostgreSQL account that has the same name as
your username::

    sudo -u postgres createuser --createdb --superuser $USER

You can check that this worked by doing, from your user (you should not be
asked for a password)::

    psql postgres

Node.js modules
~~~~~~~~~~~~~~~

If you want to run the web app to browser your local archive you will need some
Node.js modules, in particular to pack web resources into a single compact
file. To that end the following should suffice::

  cd swh-web
  npm install
  cd -

You are now good to go with all needed dependencies on your development
machine!


Step 2 --- install Python packages in a virtualenv
--------------------------------------------------

From now on you will need to work in a `virtualenv
<https://docs.python.org/3/library/venv.html>`_ containing the Python
environment with all the Software Heritage modules and their dependencies. To
that end you can do (once)::

  python3 -m venv .venv

Then, activate the virtualenv (do this every time you start working on Software
Heritage)::

  source .venv/bin/activate

You can now install Software Heritage Python modules, their dependencies and
the testing-related dependencies using::

  pip install $( bin/pip-swh-packages --with-testing )


Step 3 --- set up storage
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
      db: "dbname=softwareheritage-dev"
      objstorage:
        cls: pathslicing
        args:
          root: /srv/softwareheritage/objects/
          slicing: 0:2/2:4

Make sure that the object storage root exists on the filesystem and is writable
to your user, e.g.::

  sudo mkdir -p /srv/softwareheritage/objects
  sudo chown "${USER}:" /srv/softwareheritage/objects

You are done with object storage setup! Let's setup the database::

  swh-storage/sql/bin/db-init softwareheritage-dev

``softwareheritage-dev`` is the name of the DB that will be created, it should
match the ``db`` line in ``storage.yml``

To check that you can successfully connect to the DB (you should not be asked
for a password)::

  psql softwareheritage-dev

You can now run the storage server like this::

  python3 -m swh.storage.api.server --host localhost --port 5002 ~/.config/swh/storage/storage.yml


Step 4 --- ingest repositories
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


Step 5 --- browse the archive
-----------------------------

You can now setup a local web app to browse what you have locally archived. The
web app uses the configuration file ``~/.config/swh/web/web.yml``. Create it
and fill it with something like:

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
