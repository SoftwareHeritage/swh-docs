.. _puppet_tutorial:

Tutorial: Making my first change in Puppet
==========================================

.. admonition:: Intended audience
   :class: important

   staff members

.. _puppet_development:

Development
~~~~~~~~~~~

The development happens in the swh-site repository.


So checkout the swh-site repository, and starts the development in the staging branches.
It's to diff against the production branch:

.. code::

   you@localhost$ cd swh-site && git pull
   you@localhost$ git checkout production && git merge origin/production
   # both staging and production should be in sync
   you@localhost$ git checkout staging && git merge origin/staging
   # you can now start hacking
   you@localhost$ # *hack on puppet Git repo*
   you@localhost$ rake validate
   you@localhost$ git commit

Test changes with octocatalog-diff
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As you developed your changes in the staging branch, you can now *diff* against the
production branch:

.. code::

   cd puppet-environment
   # Diff between branches "staging" and "production" for node "pergamon"
   bin/octocatalog-diff pergamon
   # Diff between branches "staging_feature" and "production" for node "worker01"
   bin/octocatalog-diff --to staging_feature worker01

This requires your :ref:`octocatalog setup to be ready <configure_octocatalog_diff>`.

Test changes in Vagrant
~~~~~~~~~~~~~~~~~~~~~~~

For more involved checks, we can test the changes using :ref:`vagrant
<puppet_how_to_test_puppet_changes_in_vagrant>`.

Ask for review
~~~~~~~~~~~~~~

As for standard development, ask for a review so someone can validate your changes.

Please, during the diff phase, update the *test plan* paragraph with your
octocatalog-diff output. There can be more than one machines, so please give those
especially the one either impacted or not impacted by changes.

.. code::

   # (optional) ask for review
   you@localhost$ arc diff...

Land
~~~~

Once you are satisfied with your changes and they passed review, simply push the
changes. Merge both the production and staging branches together.

.. code::

   you@localhost$ cd swh-site
   # you should develop on the staging branches first
   you@localhost$ git checkout staging && git rebase production
   # keep in sync the staging and production branches
   you@localhost$ git checkout production && git merge staging
   # land the changes
   you@localhost$ git push origin staging production
