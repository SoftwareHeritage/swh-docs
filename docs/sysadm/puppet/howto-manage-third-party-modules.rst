.. _puppet_integration_of_third_party_puppet_modules:

.. admonition:: Intended audience
   :class: important

   staff members with enough permissions to deploy

.. admonition:: Warning
   :class: warning

   Deprecated documentation. Since we migrated to gitlab, the referenced script must be
   adapted to work with it.

How to manage Third-Party modules
=================================

Integration of third party puppet modules
-----------------------------------------

We mirror external repositories to our own forge, to avoid having external dependencies
in our deployment.

In the *swh-site* ``Puppetfile``, we pin the installation of those modules to the
highest version (that works with our current puppet/facter version), by using the *:ref*
specifier.

.. _adding_a_new_external_puppet_module:

Adding a new external puppet module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


In the *puppet-environment* repository, the ``bin/import-puppet-module`` takes care of
the following tasks:

- Getting metadata from the `Puppet forge <https://forge.puppetlabs.com/>`_ for the
  module (description, upstream git URL)
- Cloning the repository
- Creating a mirror repository on the Software Heritage forge, with the proper
  permissions and metadata (notably the *Sync to GitHub* flag)
- Pushing the clone to the forge
- Updating the .mrconfig and .gitignore files

To be able to use the script, you need:

- Be a member of the `System Administrators
  <https://forge.softwareheritage.org/project/members/7/>`_ Phabricator group
- Have the :ref:`Arcanist <swh-devel:arcanist-configuration>` API key setup
- A pair of python dependencies: ``python3-phabricator`` and ``python3-requests`` (pull
  them from testing if needed).

Example usage to pull the `elastic/elasticsearch
<https://forge.puppetlabs.com/elastic/elasticsearch>`_ module

::

   bin/import-module elastic-elasticsearch
   git diff # review changes
   git add .mrconfig .gitignore
   git commit -m "Add the elastic/elasticsearch module"
   git push

Once the module is added, you need to register it in the *swh-site* `Puppetfile
<https://gitlab.softwareheritage.org/infra/puppet/puppet-swh-site/-/blob/production/Puppetfile>`_.

You should also check in the module metadata whether any dependencies need importing as
well, which you should do using the same procedure.

.. _updating_external_puppet_modules:

Updating external puppet modules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There's two sides of this coin:

.. _updating_our_git_clone_of_external_puppet_modules:

Updating our git clone of external puppet modules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The *puppet-environment* ``.mrconfig`` file has a ``pullup`` command which does the
right thing.

To update all clones:

::

   mr -j4 pullup

.. _upgrading_external_puppet_modules:

Upgrading external puppet modules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Upgrading external puppet modules happens manually.

In the *puppet-environment* repository, the ``bin/check-module-updates`` script compares
the Puppetfile and the local clones and lists the available updates. (depends on ``ruby
r10k``).

On a staging branch of the *swh-site* repository, update the ``:ref`` value for the
module in the ``Puppetfile`` to the latest tag. You can then run ``octocatalog-diff`` on
a few relevant servers and look for changes.
