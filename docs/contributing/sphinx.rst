.. _sphinx-gotchas:

Sphinx gotchas
==============

Here is a list of common gotchas when formatting Python docstrings for [http://www.sphinx-doc.org/en/stable/ Sphinx] and the [http://www.sphinx-doc.org/en/stable/ext/napoleon.html Napoleon] style.

Sphinx
------

Lists
+++++

All sorts of `lists <http://www.sphinx-doc.org/en/stable/rest.html#lists-and-quote-like-blocks>`_
require an empty line before the first bullet and after the last one,
to be properly interpreted as list.
No indentation is required for list elements w.r.t. surrounding text,
and line continuations should be indented like the first character
after the bullet

Bad::

   this is a bad example that will not be interpreted as a list
   preceding text
   - foo
   - bar
   - baz
   following text

Good::

   this is some text preceding the list

   - foo
   - bar
   - baz
   - this is a rather long-ish paragraph inserted in the list
     with line continuation
   - qux

   this is some text following the list

Bad::

   - foo
   - nested lists also requires empty lines, but they are missing here
     - inner list 1
     - inner list 2
   - outer list continues here

Good::

   surrounding text

   - foo
   - nested lists also requires empty lines

     - inner list 1
     - inner list 2

   - outer list continues here

   surrounding text

Verbatim source code
++++++++++++++++++++

Verbatim `code blocks <http://www.sphinx-doc.org/en/stable/rest.html#source-code>`_,
e.g., for code examples, requires double colon at the end of a line,
then an empty line, and then the code block itself, indented:

Bad::

   This does not work as there is a single column and no empty line before code:
       def foo(bar, baz):
           qux = bar + baz

           return qux

Good::

   a nice example of python code follows::

       def foo(bar, baz):
           qux = bar + baz

           return qux

   here we can restart text flow

*Inline code samples* use double backquotes, and not single ones.

Bad::

   you have to instantiate the method `def foo(bar): pass`
   in order to use this abstract class

Good:

   you have to instantiate the method ``def foo(bar): pass``
   in order to use this abstract class

``**kwargs``, ``**args``
+++++++++++++++++++++++++

`Asterisks needs to be escaped <http://www.sphinx-doc.org/en/stable/rest.html#inline-markup>`_
to avoid capture by emphasis markup.
In case of multiple adjacent asterisks, escaping the first one is enough.

Bad::

   additional **kwargs are copied in the returned dictionary

Good::

   additional \**kwargs are copied in the returned dictionary

Code cross-references
+++++++++++++++++++++

Backquotes are not enough to cross-reference a Python entity
(class, function, module, etc.); you need to use
`Sphinx domains <http://www.sphinx-doc.org/en/stable/domains.html>`_ for that,
and in particular the `Python domain <http://www.sphinx-doc.org/en/stable/domains.html#the-python-domain>`_

Bad::

   see the `do_something` function and the `swh.useless` module
   for more information

Good::

   see the :func:`do_something` function and the :mod:`swh.useless` module
   for more information

Good::

   you can avoid a long, fully-qualified anchor setting an
   :func:`explicit label <swh.long.namespace.function>` for a link

See also: the `list of Python roles <http://www.sphinx-doc.org/en/stable/domains.html#cross-referencing-python-objects>`_
that you can use to cross-reference Python objects.
Note that you can (and should) omit the <code>:py:</code> prefix,
as Python is the default domain.

Note also that when building Sphinx documentation
for individual Software Heritage modules in isolation,
cross-references to other modules will *not* be resolvable.
But they will be resolvable when building the unified documentation
from ``swh-docs``

Napoleon
--------

Docstring sections
++++++++++++++++++

See the `list of docstring sections <http://www.sphinx-doc.org/en/stable/ext/napoleon.html#docstring-sections>`_
supported by Napoleon.
Everything else will *not* be typeset with a dedicated heading,
you will have to do so explicitly using reStructuredText markup.

Args
++++

Entries in Args section do *not* start with bullets, but just with argument names (as any other Napoleon section).
Continuation lines should be indented.

Bad::

   Args:
       - foo (int): first argument
       - bar: second argument
       - baz (bool): third argument

Good::

   Args:
       foo (int): first argument
       bar: second argument, which happen to have a fairly
           long description of what it does
       baz (bool): third argument

Returns
+++++++

In Returns section you need to use ":" carefully as, if present, it will be interpreted as a separator between return type and description. Also, the description of return value should not start on the same line of "Returns:", but on the subsequent one, indented.

Bad::

   Returns:
       this does not work (colon will be interpreted as type/desc separator), a dict with keys:

       - foo
       - bar

Good::

   Returns:
       this works (there is no colon) a dict with keys

       - foo
       - bar

Good::

   Returns:
       dict: this works again (*first* colon identifies the type) a dict with keys:

       - foo
       - bar

Bad::

   Returns: this is not good either, you need to start a paragraph

Raises
++++++

You need a ":" separator between exception names and their description.

Bad::

   Raises:
       ValueError if you botched it
       RuntimeError if we botched it


Good::

   Raises:
       ValueError: if you botched it
       RuntimeError: if we botched it

See also
--------

* :ref:`python-style-guide`
