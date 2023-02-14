.. _tutorial-new-package:

Add a new package
=================

The following document demonstrates how to create a new Python package for
Software Heritage, hereafter named ``swh-foo``.

We will need to create a project, initialize the new repository, reference
the project in the Continuous Integration system and finally add the
project to the documentation.

.. _create-new-project:

Create a project
----------------

Creating the project should be done using the ``gitlab`` command-line tool
provided by the `python-gitlab <https://python-gitlab.readthedocs.io/>`_ module.
Make sure to have the configuration working and an access token with ``api`` as
scope.

To create the project:

.. code:: bash

   PROJECT_NAME=swh-foo
   DESCRIPTION="Software Heritage Foo management library"
   NAMESPACE_ID="$(gitlab --output json namespace get --id 'swh/devel' | jq .id)"
   gitlab project create \
       --name "$PROJECT_NAME" \
       --path "$PROJECT_NAME" \
       --namespace "$NAMESPACE_ID" \
       --description "$DESCRIPTION" \
       --issues-access-level enabled \
       --auto-devops-enabled false \
       --wiki-access-level disabled \
       --requirements-access-level disabled \
       --pages-access-level disabled \
       --operations-access-level disabled \
       --container-registry-access-level disabled \
       --visibility public

Initialize the repository with our template
-------------------------------------------

The following commands need to run from the base directory
``swh-environment``.

1. Clone the new repository:

   .. code:: bash

      git clone https://gitlab.softwareheritage.org/swh/devel/swh-foo.git

2. Use ``bin/init-py-repo`` to initialize the repository with a project template:

   .. code:: bash

      bin/init-py-repo swh-foo

3. Install the pre-commit hook:

   .. code:: bash

      pre-commit install

Customize the template
----------------------

Now look for the string ``foo`` in all files and file names and replace it with
the name of the new package. Push these commits directly to the repository as
initial content.

For an example, you can see `what was done for swh-counters <https://gitlab.softwareheritage.org/swh/devel/swh-counters/-/commit/142fff84305b>`__.

Add the repo on the swh-environment project
-------------------------------------------

Declare the repository on the *mr* configuration:

- Edit the ``.mrconfig`` file and declare the new repository. For an example, `look
  at the addition of swh-graphql
  <https://gitlab.softwareheritage.org/swh/devel/swh-environment/-/commit/d812839f02ae6d0f20891a0f14391a94a359d611>`__.

- Create a merge request with the changes.

.. note::
   Adding the repository in ``.mrconfig`` will break ``swh-docs`` builds until
   the new module is registered in the documentation as explained below.

Install CI jobs
---------------

- In  swh-jenkins-jobs_, open `jobs/swh-packages.yaml <https://gitlab.softwareheritage.org/swh/infra/ci-cd/swh-jenkins-jobs/-/blob/master/jobs/swh-packages.yaml>`__ and add a section like the others for the new repository.

.. note::
   Jobs will automatically be recreated when changes are pushed to the
   ``swh-jenkins-jobs`` repository. See `Jenkins documentation <ci_jenkins>`_
   for details.

Make an initial release
-----------------------

Releases are made automatically by Jenkins when a tag is pushed to a module
repository. Making an initial release is thus done by doing:

.. code:: bash

   git tag v0.0.0
   git push origin --tags v0.0.0

.. note::
   Before adding a new module to the documentation, at least one release must
   have been made. Otherwise, the documentation will not build as it won’t be
   able to fetch the Python package from PyPI nor determine the version number.
   This is why we need to make an initial release before moving forward.

Update the documentation
------------------------

The documentation is in the swh-docs_ project. Each Python module get a section
of the documentation automatically generated from its source code.

To add a new module to the documentation:

- Add the package to the dependencies in ``requirements-swh.txt`` (publication
  build) and ``requirements-swh-dev.txt`` (documentation development build).

- Reference the package in the ``toctree`` located in ``docs/devel/api-reference.rst``

- Add the package with a concise description to the index of the development part, located in
  ``docs/devel/index.rst``.

  ::

     :ref:`swh.foo <swh-foo>`
         short description of the repository

- Ensure this builds fine locally (run ``tox run`` and ``tox run -e sphinx-dev``)

- Open a merge request with the above changes.


.. _`Continuous Integration (CI)`: https://jenkins.softwareheritage.org
.. _swh-jenkins-jobs: https://gitlab.softwareheritage.org/swh/infra/ci-cd/swh-jenkins-jobs
.. _swh-docs: https://gitlab.softwareheritage.org/swh/devel/swh-docs
