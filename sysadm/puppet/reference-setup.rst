.. _puppet-setup:

Puppet setup
============

.. admonition:: Intended audience
   :class: important

   sysadm members

.. _puppet_multiple_repository_setup:

Multiple repository setup
-------------------------

Report to :ref:`setup-repositories` to prepare your machine with puppet-environment.

All the swh-specific repositories are in *swh-*-prefixed repositories. The other
repositories come from other sources and have an *upstream* remote allowing updates (the
*origin* remote is always on the swh git server).

Our puppet workflow is documented in `the README.md file in the puppet-environment
repository
<https://gitlab.softwareheritage.org/infra/puppet/puppet-environment/-/blob/master/README.md>`_.

.. _configure_octocatalog_diff:

Configure octocatalog-diff to ease testing
------------------------------------------

*puppet-environment* contains the whole scaffolding to be able to use `octocatalog-diff
<https://github.com/github/octocatalog-diff>`_ on our manifests. This allows for
quick(er) local iterations while developing complex puppet manifests.

Dependencies
~~~~~~~~~~~~

You need the following packages installed on your machine:

- r10k octocatalog-diff
- puppet

Running
~~~~~~~

The ``bin/octocatalog-diff`` script allows diffing the manifests between two
environments (that is, between two branches of the *swh-site* repository. By default it
diffs between ``production`` and ``staging``.

Default usage:

.. code::

   cd puppet-environment
   # Diff between branches "staging" and "production" for node "pergamon"
   bin/octocatalog-diff pergamon
   # Diff between branches "staging_feature" and "production" for node "worker01"
   bin/octocatalog-diff --to staging_feature worker01

Limitations
~~~~~~~~~~~

Our setup for octocatalog-diff doesn't support exported resources, so you won't see your
fancy icinga checks there. For more evolved checks as those, use our `vagrant vms
definitions
<https://gitlab.softwareheritage.org/infra/puppet/puppet-environment/-/blob/master/README.md?plain=1#L187>`_.
