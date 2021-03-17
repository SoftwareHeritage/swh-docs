.. _testing-guide:

Software testing guide
======================

Tools landscape
---------------

The testing framework we use is pytest_. It provides many facilities to write tests
efficiently.

It is complemented by hypothesis_, a library for property-based testing in some of
our test suites. Its usage is a more advanced topic.

We also use tox_, the automation framework, to run the
tests along with other quality checks in isolated environments.

The main quality checking tools in use are:

* mypy_, a static type checker. We gradually type-annotate all additions or refactorings
  to the codebase;
* flake8_, a simple code style checker (aka linter);
* black_, an uncompromising code formatter.

They are run automatically through ``tox`` or as ``pre-commit`` hooks in our Git repositories.

The SWH testing framework
-------------------------

This sections shows specifics about our usage of pytest and custom helpers.

The pytest fixture system makes easy to write, share and plug setup and teardown code.
Fixtures are automatically loaded from the project ``conftest`` or ``pytest_plugin`` modules
into any test function by giving its name as argument.

| Several pytest plugins have been defined across SWH projects:
| ``core``, ``core.db``, ``storage``, ``scheduler``, ``loader``, ``journal``.
| Many others, provided by the community are in use:
| ``flask``, ``django``, ``aiohttp``, ``postgresql``, ``mock``, ``requests-mock``, ``cov``, etc.

We make of various mocking helpers:

* ``unittest.mock``: ``Mock`` classes, ``patch`` function;
* ``mocker`` fixture from the ``mock`` plugin: adaptation of ``unittest.mock`` to the
  fixture system, with a bonus ``spy`` function to audit without modifying objects;
* ``monkeypatching`` builtin fixture: modify object attributes or environment, with
  automatic teardown.

Other notable helpers include:

* ``datadir``: to compute the path to the current test's ``data`` directory.
  Available in the ``core`` plugin.
* ``requests_mock_datadir``: to load network responses from the datadir.
  Available in the ``core`` plugin.
* ``swh_rpc_client``: for testing SWH RPC client and servers without incurring IO.
  Available in the ``core`` plugin.
* ``postgresql_fact``: for testing database-backends interactions.
  Available in the ``core.db`` plugin, adapted for performance from the ``postgresql`` plugin.
* ``click.testing.CliRunner``: to simplify testing of Click command-line interfaces.
  It allows to test commands with some level of isolation from the execution environment.
  https://click.palletsprojects.com/en/7.x/api/#click.testing.CliRunner

Testing guidelines
------------------

General considerations
^^^^^^^^^^^^^^^^^^^^^^

We mostly do functional tests, and unit-testing when more ganularity is needed. By this,
we mean that we test each functionality and invariants of a component, without isolating
it from its dependencies systematically. The goal is to strike a balance between test
effectiveness and test maintenance. However, the most critical parts, like the storage
service, get more extensive unit-testing.

Organize tests
^^^^^^^^^^^^^^

* In order to test a component (module, class), one must start by identifying its sets of
  functionalities and invariants (or properties).
* One test may check multiples properties or commonly combined functionalities, if it can
  fit in a short descriptive name.
* Organize tests in multiple modules, one for each aspect or subcomponent tested.
  e.g.: initialization/configuration, db/backend, service API, utils, cli, etc.

Test data
^^^^^^^^^

Each repository has its own ``tests`` directory, some such as listers even have one for
each lister type.

* Put any non-trivial test data, used for setup or mocking, in (potentially compressed)
  files in a ``data`` directory under the local testing directory.
* Use ``datadir`` fixtures to load them.

Faking dependencies
^^^^^^^^^^^^^^^^^^^

* Make use of temporary directories for testing code relying on filesystem paths.
* Mock only already tested and expensive operations, typically IO with external services.
* Use ``monkeypatch`` fixture when updating environment or when mocking is overkill.
* Mock HTTP requests with ``requests_mock`` or ``requests_mock_datadir``.

Final words
^^^^^^^^^^^

If testing is difficult, the tested design may need reconsideration.

Other SWH resources on software quality
---------------------------------------

| https://wiki.softwareheritage.org/wiki/Python_style_guide
| https://wiki.softwareheritage.org/wiki/Git_style_guide
| https://wiki.softwareheritage.org/wiki/Arcanist_setup
| https://wiki.softwareheritage.org/wiki/Code_review
| https://wiki.softwareheritage.org/wiki/Jenkins
| https://wiki.softwareheritage.org/wiki/Testing_the_archive_features

.. _pytest: https://pytest.org
.. _tox: https://tox.readthedocs.io
.. _hypothesis: https://hypothesis.readthedocs.io
.. _mypy: https://mypy.readthedocs.io
.. _flake8: https://flake8.pycqa.org
.. _black: https://black.readthedocs.io
