.. _upgrade-swh-service:

Upgrade swh service
===================

.. admonition:: Intended audience
   :class: important

   sysadm staff members


The document describes the deployment for most of our swh services (rpc services,
loaders, listers, indexers, ...).

There exists currently 2 ways (as we are transitioning from the first to the second):

- static: From git tag to deployment through debian packaging
- elastic: From git tag to deployment through kubernetes.


The following will first describe the :ref:`common deployment part <code-and-publish>`.
This involves some python packaging out of a git tag which will be built and push to
`PyPI <https://pypi.org>`_ and our :ref:`swh debian repositories
<howto-debian-packaging>`.

Then follows the actual :ref:`deployment with debian packaging
<deployment-with-debian-packaging>`. It concludes with the :ref:`deployment with
kubernetes<deployment-with-kubernetes>` chapter.

.. _distinct-services:

Distinct Services
-----------------

3 kinds services runs on our nodes:

- worker services (loaders, listers, cookers, ...)
- rpc services (scheduler, objstorage, storage, web, ...)
- journal client services (search, scheduler, indexer)

.. _code-and-publish:


Code and publish
----------------

Code an evolution of fix an issue in the python code within the git repository's master
branch. Open a diff for review, land it when accepted, and start back at :ref:`tag and
push <tag-and-push>`.

.. _tag-and-push:

Tag and push
~~~~~~~~~~~~

When ready, `git tag` and `git push` the new tag of the module. And let jenkins
:ref:`publish the artifact <publish-artifacts>`.

.. code::

   $ git tag -a vA.B.C  # (optionally) `git tag -a -s` to sign the tag too
   $ git push origin --follow-tags

.. _publish-artifacts:

Publish artifacts
~~~~~~~~~~~~~~~~~

Jenkins is in charge to publishing to `PyPI <https://pypi.org>`_ the new release (out of
the tag). And then building the debian packaging and push it package to our :ref:`swh
debian repositories <howto-debian-packaging>`.


.. _troubleshoot:

Troubleshoot
~~~~~~~~~~~~

If jenkins fails for some reason, fix the module be it :ref:`python code
<fix-or-evolve-code>` or the :ref:`debian packaging <troubleshoot-debian-package>`.


.. _deployment-with-debian-packaging:

Deployment with debian packaging
--------------------------------

This mostly involves deploying new version of debian packages to static nodes.

.. _upgrade-services:

Upgrade services
~~~~~~~~~~~~~~~~

When a new version is released, we need to upgrade the package(s) and restart services.

worker services (production):

- *swh-worker@loader_{git, hg, svn, npm, ...}*
- *swh-worker@lister*
- *swh-worker@vault_cooker*

journal clients (production):

- *swh-indexer-journal-client@{origin_intrinsic_metadata_,extrinsic_metadata_,...}*

rpc services (both environment):

- *gunicorn-swh-{scheduler, objstorage, storage, web, ...}*


From the pergamon node, which is configured for `clush
<https://clustershell.readthedocs.io/en/latest/index.html>`_, one can act on multiple
nodes through the following group names:

- *@swh-workers* for the production workers (listers, loaders, ...)
- *@azure-workers* for the production ones running on azure (indexers, cookers)
- ...

See :ref:`deploy-new-lister` for a practical example.

.. _troubleshoot-debian-package:

Debian package troubleshoot
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Update and checkout the *debian/unstable-swh* branch (in the impacted git repository),
then fix whatever is not updated or broken due to a change.

It's usually a missing new package dependency to fix in *debian/control*). Add a new
entry in *debian/changelog*. Make sure gbp builds fine locally. Then tag it and push.
Jenkins will build the package anew.

.. code::

   $ gbp buildpackage --git-tag-only --git-sign-tag  # tag it
   $ git push origin --follow-tags                   # trigger the build

Lather, rinse, repeat until it's all green!

Deploy
------

.. _nominal-case:

Nominal case
~~~~~~~~~~~~

Update the machine dependencies and restart service. That usually means as sudo user:

.. code::

   $ apt-get update
   $ apt-get dist-upgrade -y
   $ systemctl restart $service

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

   sudo clush -b -w $nodes puppet agent -t

Note: *-t* is not optional

.. _long-standing-upgrade:

Long-standing upgrade
~~~~~~~~~~~~~~~~~~~~~

In that case, you may need to stop the impacted services. For example, for long standing
data model migration which could take some time.

You need to momentarily stop puppet (which by default runs every 30 min to apply
manifest changes) and the cron service (which restarts down services) on the workers
nodes.

Report yourself to the :ref:`storage database migration <storage-database-migration>`
for a concrete case of database migration.

.. code::

   $ sudo clush -b -w @swh-workers 'systemctl stop cron.service; puppet agent --disable'


Then:

-  Execute the long-standing upgrade.
-  Go back to the :ref:`nominal case <nominal-case>`.
-  Restart puppet and the cron services on workers

.. code::

   $ sudo clush -b -w @swh-workers 'systemctl start cron.service; puppet agent --enable'


.. _deployment-with-kubernetes:

Deployment with Kubernetes
--------------------------

.. warning:: FIXME Enter into details + add a small summary graph

- swh-apps: Add new apps (new Dockerfile)
- swh-apps: Build frozen requirements for a new release of a swh service
- swh-apps: Build impacted docker images with that frozen set of requirements
- Commit and tag
- Push built docker image into our gitlab registry
- swh-charts: Add/Update the image versions
- Commit and push
