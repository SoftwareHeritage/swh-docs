.. _upgrade-swh-service:

Upgrade swh service
===================

.. admonition:: Intended audience
   :class: important

   sysadm staff members

Workers
-------

Dedicated workers [1] run our *swh-worker@loader_{git, hg, svn, npm, ...}* services.
When a new version is released, we need to upgrade their package(s).

[1] Here are the following group name (in `clush
<https://clustershell.readthedocs.io/en/latest/index.html>`_ terms):

-  *@swh-workers* for the production workers
-  *@azure-workers* for the production ones running on azure
-  *@staging-loader-workers* for the staging ones

See :ref:`deploy-new-lister` for a practical example.

Code and publish
----------------

.. _fix-or-evolve-code:

Code an evolution of fix an issue in the python code within the git repository's master
branch. Open a diff for review, land it when accepted, and start back at :ref:`tag and push
<tag-and-push>`.

.. _tag-and-push:

Tag and push
~~~~~~~~~~~~

When ready, `git tag` and `git push` the new tag of the module.

.. code::

   $ git tag vA.B.C
   $ git push origin --follow-tags

.. _publish-and-deploy:

Publish and deploy
~~~~~~~~~~~~~~~~~~

Let jenkins publish and deploy the debian package.

.. _troubleshoot:

Troubleshoot
~~~~~~~~~~~~

If jenkins fails for some reason, fix the module be it :ref:`python code
<fix-or-evolve-code>` or the :ref:`debian packaging <troubleshoot-debian-package>`.

.. _troubleshoot-debian-package:

Debian package troubleshoot
~~~~~~~~~~~~~~~~~~~~~~~~~~~

In that case, upgrade and checkout the *debian/unstable-swh* branch, then fix whatever
is not updated or broken due to a change. It's usually a missing new package dependency
to fix in *debian/control*). Add a new entry in *debian/changelog*. Make sure gbp builds
fine. Then tag it. Jenkins will build the package anew.

.. code::

   $ gbp buildpackage --git-tag-only --git-sign-tag  # tag it
   $ git push origin --follow-tags                   # trigger the build

Deploy
------

.. _nominal_case:

Nominal case
~~~~~~~~~~~~

Update the machine dependencies and restart service. That usually means
as sudo user:

.. code::

   $ apt-get update
   $ apt-get dist-upgrade -y
   $ systemctl restart swh-worker@loader_${type}

Note that this is for one machine you ssh into.

We usually wrap those commands from the sysadmin machine pergamon [3] with the *clush*
command, something like:

.. code::

   $ sudo clush -b -w @swh-workers 'apt-get update; env DEBIAN_FRONTEND=noninteractive \
       apt-get -o Dpkg::Options::="--force-confdef" \
       -o Dpkg::Options::="--force-confold" -y dist-upgrade'

[3] pergamon is already *clush* configured to allow multiple ssh connections in parallel
on our managed infrastructure nodes.

.. _configuration-change-required:

Configuration change required
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Either wait for puppet to actually deploy the changes first and then go back to the
nominal case.

Or force a puppet run:

.. code::

   sudo clush -b -w @swh-workers puppet agent -t

Note: *-t* is not optional

.. _long-standing-migration:

Long-standing migration
~~~~~~~~~~~~~~~~~~~~~~~

In that case, you may need to stop all services for migration which could take some time
(because lots of data is migrated for example).

You need to momentarily stop puppet (which runs every 30 min to apply manifest changes)
and the cron service (which restarts down services) on the workers nodes.

Report yourself to the :ref:`storage database migration <storage-database-migration>`
for a concrete case of database migration.

.. code::

   $ sudo clush -b -w @swh-workers 'systemctl stop cron.service; puppet agent --disable'

Then:

-  Execute the database migration.
-  Go back to the nominal case.
-  Restart puppet and the cron on workers

.. code::

   $ sudo clush -b -w @swh-workers 'systemctl start cron.service; puppet agent --enable'

