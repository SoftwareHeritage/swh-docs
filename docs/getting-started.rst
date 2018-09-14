.. _getting-started:

.. highlight:: bash

Run your own Software Heritage
==============================

This walkthrough will guide from the basic step of obtaining the source code of
the Software Heritage stack to running a local copy of it in which you can
ingest source code of existing repositories and browse them using the archive
web application.


Step 0 - get the code
---------------------

The `swh-environment
<https://forge.softwareheritage.org/source/swh-environment/>`_ Git (meta)
repository orchestrates the Git repositories of all Software Heritage modules.
Clone it::

  git clone https://forge.softwareheritage.org/source/swh-environment.git

then recursively clone all Python module repositories. For this step you will
need the `mr <http://myrepos.branchable.com/>`_ tool, see the `README` file of
swh-environment for more information::

  cd swh-environment
  readlink -f .mrconfig >> ~/.mrtrust
  mr up

For periodic code updates in the future you can use the following helper::

  cd swh-environment
  bin/update


Step 1 - set up storage
-----------------------

Then you will need a local storage to archive source code artifacts. It comes
in two parts: a content-addressable object storage on your file system (for
file contents) and a Postgres database (for the graph structure of the
archive). See the :ref:`data-model` for more information.

**TO BE WRITTEN**


Step 2 - ingest repositories
----------------------------

**TO BE WRITTEN**


Step 3 - browse the archive
---------------------------

**TO BE WRITTEN**
