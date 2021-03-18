.. _git-style-guide:

Git style guide
===============

Various information about how we use Git to develop Software Heritage.

Commits
-------

Make your commits adhere to this `How to Write a Git Commit Message <http://chris.beams.io/posts/git-commit/>`_

Link commits to tasks
+++++++++++++++++++++

You can reference Phabricator tasks from your commits,
using a `dedicated syntax <https://secure.phabricator.com/T5132>`_
When you do so, please put the task action on a separate line,
so that it is clearly visible.

Make sure commits that are enough to close a bug do so using a line like::

   Closes T123456

If you just want to "ping" a task, updating it with the fact that
a related commit has been pushed, use::

   Related to T123456

References
----------

* `special syntax you can use in commit messages to cause effects <https://secure.phabricator.com/T5132>`_
