.. _python-style-guide:

Python style guide
==================

Coding style and best practices for writing Python code for Software Heritage.

General rules
-------------

* As a general rule, follow the
  `Google Python Style Guide <http://google.github.io/styleguide/pyguide.html>`_.
* Target **Python 3**. Do not care about backward compatibility with Python 2.

Black
+++++

As of April 2020, we use `Black <https://black.readthedocs.io/>`_
as automated code formatter for all Software Heritage Python code.
CI, tox, and other linting tools are configured to fail
if code is not formatted as black would.

Note that, as part of this, *maximum line length is 88 characters*,
rather than the default of 79.

Specific rules
--------------

As supplement/overrides to the above general rules,
follow the additional recommendations below.

Lint
++++

* Make sure your code is `flake8 <https://flake8.readthedocs.org/>`_
  and `Black <https://black.readthedocs.io/>`_ clean.

Tests
+++++

* use ``pytest`` as test runner

* put ``tests/`` dir down deep in the module hierarchy, near to the code being tested

* whenever possible, follow all the guidelines in
  `Stargirl Flowers' Python testing style guide <https://blog.thea.codes/my-python-testing-style-guide/>`_

Classes
+++++++

* Since we target Python 3, there is no need to
  `inherit from 'object' explicitly <http://google.github.io/styleguide/pyguide.html?showone=Classes#Classes>`_

Docstrings
----------

* docstrings should produce a nice API documentation when run through
  `Sphinx <http://www.sphinx-doc.org/en/stable/>`_, in particular:
* docstrings should be written in
  `reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_
* docstrings should use the
  `Napoleon style <https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html>`_
  (Google variant) to document arguments, return values, etc.

* see also: a `comprehensive style example <https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html>`_
* see also: :ref:`sphinx-gotchas`
