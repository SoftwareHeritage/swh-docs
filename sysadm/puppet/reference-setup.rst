.. _puppet-setup:

Puppet setup
============

.. admonition:: Intended audience
   :class: important

   sysadm members

.. _mutiple_repository_setup:

Multiple repository setup
-------------------------

Our puppet environment is split into multiple repos (one repo per module), plus one
"root" repository for multi-repository management.

First, clone the base repository, containing the configuration file for myrepos and a
README file.

::

   $ git clone ssh://git@forge.softwareheritage.org/diffusion/SENV/puppet-environment.git

Then, use that configuration to clone all the repositories:

::

   $ cd puppet-environment
   $ readlink -f .mrconfig >> ~/.mrtrust
   $ mr up

(the *mr* command is in the `myrepos Debian package
<https://packages.debian.org/buster/myrepos>`_).

All the swh-specific repositories are in *swh-*-prefixed repositories. The other
repositories come from other sources and have an *upstream* remote allowing updates (the
*origin* remote is always on the swh git server).

Our puppet workflow is documented in `the README.md file in the puppet-environment
repository
<https://forge.softwareheritage.org/diffusion/SENV/browse/master/README.md>`_.

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
<https://forge.softwareheritage.org/source/puppet-environment/browse/master/README.md$187>`_.
