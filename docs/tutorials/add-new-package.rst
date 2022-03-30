.. _tutorial-new-package:

Add a new package
=================

The following document demonstrates how to create a new swh package in the current `swh
phabricator instance`_ and reference it so the `Continuous Integration (CI)`_ is able to
build the new package.

We will need to (optionally) create a project, then create a repository, reference it in
the CI and finally update the documentation repository so the docs get built with that
new package. Optionally, we can also create the necessary debian branches for the debian
build deployment process to work. That's not something immediately urgent when
bootstraping a package though.

.. _create-new-project:

Create a project
----------------

Create a `new Project`_ (seen also as a ``Tag``) and fill in the form:

  - Fill in the "name" field (e.g. ``Origin Sourceforge``, ``Loader XYZ``, ...)

  - Additional hashtags should be filled in with easy to remember hashtags (e.g.
    ``#sourceforge``, ``#loader-xyz``)

  - Add a small description about what the project is about

Create a repository
-------------------

- Create a `new Git repository`_ and fill in the form:

- ``name`` of the repository should be human readable (e.g. ``Git Loader``, ``Gitlab Lister``)

- ``callsign`` should follow the current `naming convention`_

- ``short-name`` should be lower case and dash separated (e.g. ``swh-loader-git``,
  ``swh-lister``, ...)

- ``Tags`` should be filled with:

   - the first project/tag :ref:`you created <create-new-project>`

   - ``Language-Python``: Enable unit tests execution on commit

   - ``Has debian packaging branches``: Activate debian builds in the CI

   -  ``Sync to github``: (optional) Activate mirroring sync to github

- Add the staging area, click in order from ``BUILDS`` (left menu) > ``Staging Area`` >
  ``Edit staging`` > fill in ``Staging Area URI`` with
  https://forge.softwareheritage.org/source/staging.git

- Finally, activate the repository

Add the repo on the swh-environment project
-------------------------------------------

(Only if necessary)

Unless specified otherwise, the following commands need to run from the base directory
``swh-environment``.

-  clone the new repository

.. code:: bash

   git clone https://forge.softwareheritage.org/source/swh-my-new-repo.git

- launch the command ``bin/init-py-repo`` to initialize the repository with a project
  template

.. code:: bash

   bin/init-py-repo swh-new-repo

- Within that new repository, replace the ``swh-py-template`` entry in
  ``docs/index.rst`` with the new package name ``swh-<package>`` (e.g:
  ``swh-scrubber``).

.. code:: bash

   REPO_NAME=swh-new-repo  # edit this part, keep the "swh-" prefix
   sed -i -e "s/swh-py-template/$REPO_NAME/g" docs/index.rst

- Edit the default content of the template (`Example <https://forge.softwareheritage.org/rDCNT142fff84305b793974e6f7b837988e5fb95d8db1>`__)

-  Configure **your local** pre-commit hook

   -  In the ``swh-environment/swh-my-new-repo`` directory, execute:

   .. code:: bash

      grep -q pre-commit.com .git/hooks/pre-commit || pre-commit install

-  Declare the repository on the mr configuration

   - Edit the ``.mrconfig`` file and declare the new repository (just
     duplicate one existing entry and adapt with the new package name)

   - Commit file modification (`Example
     <https://forge.softwareheritage.org/rCJSWHede4a65bc9e103db99dd8b0690caa3a769b378bd>`__)

Install CI jobs
---------------

- In the swh-jenkins-jobs_ repository, open the
  ``jobs/swh-packages.yaml`` and add a section for the new repository as for the others
  (`Example <https://forge.softwareheritage.org/rCJSWHdd5b3a1192cb45c07103be199af8c2a74478746e>`__)

-  Configure the `post-receive hook`_ on the phabricator instance

- `Setting up the debian jenkins jobs`_

Setting up debian builds
------------------------

As mentioned early in the introduction, this configuration can be delayed for when the
package is actually ready to be deployed.

If you want to attend immedialy, follow through the `Setting up the debian build`_
documentation.

Documentation updates
---------------------

- Documentation repository is located in the swh-docs_ repository.

- Add the package dependency in the top-level ``requirements-swh.txt`` (publication
  build) and ``requirements-swh-dev.txt`` (documentation development build).

- Reference the package in the toc tree located in :ref:`docs/api-reference.rst
  <api-reference>`.

- Reference the package in the index with its concise description located in
  :ref:`docs/index.rst <components>`.

::

   :ref:`swh.my_new_repo <swh-my-new-repo>`
       short description of the repository
   ...

   # at the end of the index page
      swh.my_new_repo <swh-my-new-repo/index>

- ensure this builds fine locally (e.g run `tox`, then `make -C docs`)

- Then open a diff to advertise the new documentation entrypoints (`Example
  <https://forge.softwareheritage.org/D7448>`__)


.. _`swh phabricator instance`: https://forge.softwareheritage.org/
.. _`Continuous Integration (CI)`: https://jenkins.softwareheritage.org
.. _`new Project`: https://forge.softwareheritage.org/project/edit/form/3/
.. _`new Git repository`: https://forge.softwareheritage.org/diffusion/edit/form/default/?vcs=git
.. _`naming convention`: https://wiki.softwareheritage.org/wiki/Phabricator_callsign_naming_convention
.. _swh-jenkins-jobs: https://forge.softwareheritage.org/source/swh-jenkins-jobs
.. _`post-receive hook`: https://wiki.softwareheritage.org/wiki/Debian_packaging#Setting_up_the_repository_on_Phabricator
.. _`Setting up the debian jenkins jobs`: https://wiki.softwareheritage.org/wiki/Debian_packaging#Setting_up_the_Jenkins_jobs
.. _`Setting up the debian build`: https://wiki.softwareheritage.org/wiki/Debian_packaging#Git_repositories_for_Debian_packages
.. _swh-docs: https://forge.softwareheritage.org/source/swh-docs/
