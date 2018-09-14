.. _getting-started:

.. highlight:: bash


Run your own Software Heritage
==============================

This walkthrough will guide from the basic step of obtaining the source code of
the Software Heritage stack to running a local copy of it with which you can
archive source code and browse it on the web. To that end, just follow the
steps detailed below:

.. contents:: :local:


Step 0 --- get the code
-----------------------

The `swh-environment
<https://forge.softwareheritage.org/source/swh-environment/>`_ Git (meta)
repository orchestrates the Git repositories of all Software Heritage modules.
Clone it::

  git clone https://forge.softwareheritage.org/source/swh-environment.git

then recursively clone all Python module repositories. For this step you will
need the `mr <http://myrepos.branchable.com/>`_ tool, see the ``README`` file
of swh-environment for more information::

  cd swh-environment
  readlink -f .mrconfig >> ~/.mrtrust
  mr up

For periodic code you can use the following helper::

  cd swh-environment
  bin/update

From now on you will need to have a ``PYTHONPATH`` environment variable that
allows to find Python modules in the ``swh`` namespace. To that end you can
source the ``pythonpath.sh`` snippet from swh-environment::

  source pythonpath.sh

To make setting ``PYTHONPATH`` easier in the future, you might want to define a
shell alias, e.g.::

  alias swh-pythonpath='cd /path/to/swh-environment/ ; source pythonpath.sh ; cd - > /dev/null'


Step 1 --- install dependencies
-------------------------------

**TO BE WRITTEN**


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

  cd swh-environment/swh-storage/sql/
  sudo -u postgres  bin/db-init 5432 softwareheritage-dev swhdev

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
only objects *added* since the previous visit will be archived upon the next
one.


Step 4 --- browse the archive
-----------------------------

**TO BE WRITTEN**
