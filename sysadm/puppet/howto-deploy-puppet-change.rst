.. _puppet_deploy_change:

How to deploy a Puppet change
=============================

.. admonition:: Intended audience
   :class: important

   staff members with enough permissions to deploy

Once done with the development changes and those are landed

.. _puppet_deploy_automated:

Automated
~~~~~~~~~

Once your change is landed in the *swh-site* repository, you need to deploy the manifest
on the puppet master.

Then puppet agent will refresh themselves and apply the changes themselves every 30min.

.. code::

   you@pergamon$ sudo swh-puppet-master-deploy

.. _puppet_semi_automated:

Semi-automated
~~~~~~~~~~~~~~

.. code::

   you@localhost$ cd puppet-environment
   you@localhost$ bin/deploy-on machine1 machine2...

Note: `puppet-environment <https://forge.softwareheritage.org/diffusion/SENV/>`_

Remember to pass ``--apt`` to ``bin/deploy-on`` if freshly uploaded Software Heritage
packages are to be deployed. Also, ``bin/deploy-on --help`` is your friend.

.. _puppet_manual_deployment:

Manual
~~~~~~

.. code::

   # if a new or updated version debian package needs deploying
   you@machine$ sudo apt-get update
   # to test/review changes
   you@machine$ sudo swh-puppet-test
   # to apply
   you@machine$ sudo swh-puppet-apply
