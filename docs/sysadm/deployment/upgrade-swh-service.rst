.. _deployment-upgrade-swh-service:

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


The following will first describe the :ref:`common deployment part
<deployment-upgrade-swh-service-code-and-publish-a-release>`. This involves
some python packaging out of a git tag which will be built and push to `PyPI
<https://pypi.org>`_ and our :ref:`swh debian repositories
<howto-debian-packaging>`.

Then follows the actual :ref:`deployment with debian packaging
<deployment-upgrade-swh-service-with-debian-packaging>`. It concludes with the
:ref:`deployment with
kubernetes<deployment-upgrade-swh-service-with-kubernetes>` chapter.

.. _deployment-upgrade-swh-service-distinct-services:

Distinct Services
-----------------

3 kinds services runs on our nodes:

- worker services (loaders, listers, cookers, ...)
- rpc services (scheduler, objstorage, storage, web, ...)
- journal client services (search, scheduler, indexer)

.. _deployment-upgrade-swh-service-code-and-publish-a-release:


Code and publish a release
--------------------------

It's usually up to the developers.

Code an evolution or a bugfix in the impacted git repository (usually the
master branch). Open a diff for review. Land it when accepted. And then
release it following the :ref:`tag and push
<deployment-upgrade-swh-service-tag-and-push>` part.

.. _deployment-upgrade-swh-service-tag-and-push:

Tag and push
~~~~~~~~~~~~

When ready, `git tag` and `git push` the new tag of the module. Then let jenkins
:ref:`publish the artifact <deployment-upgrade-swh-service-publish-artifacts>`.

.. code::

   $ git tag -a vA.B.C  # (optionally) `git tag -a -s` to sign the tag too
   $ git push origin --follow-tags

.. _deployment-upgrade-swh-service-publish-artifacts:

Publish artifacts
~~~~~~~~~~~~~~~~~

Jenkins is in charge of publishing the new release to `PyPI <https://pypi.org>`_ (out of
the tag just pushed). It then builds the debian package and pushes it to our :ref:`swh
debian repositories <howto-debian-packaging>`.


.. _deployment-upgrade-swh-service-troubleshoot:

Troubleshoot
~~~~~~~~~~~~

If jenkins fails for some reason, fix the module be it :ref:`python code
<deployment-upgrade-swh-service-code-and-publish-a-release>` or the
:ref:`debian packaging
<deployment-upgrade-swh-service-troubleshoot-debian-package>`.


.. _deployment-upgrade-swh-service-with-debian-packaging:


Deployment with debian packaging
--------------------------------

This mostly involves deploying new version of debian packages to static nodes.

.. _deployment-upgrade-swh-service-upgrade-services:

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

.. _deployment-upgrade-swh-service-troubleshoot-debian-package:

Debian package troubleshoot
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Update and checkout the *debian/unstable-swh* branch (in the impacted git repository),
then fix whatever is not updated or broken due to a change.

It's usually a missing new package dependency to fix in *debian/control*. Add a new
entry in *debian/changelog*. Make sure gbp builds fine locally. Then tag it and push.
Jenkins will build the package anew.

.. code::

   $ gbp buildpackage --git-tag-only --git-sign-tag  # tag it
   $ git push origin --follow-tags                   # trigger the build

Lather, rinse, repeat until it's all green!

Deploy
------

.. _deployment-upgrade-swh-service-nominal-case:

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

.. _deployment-upgrade-swh-service-configuration-change-required:

Configuration change required
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Either wait for puppet to actually deploy the changes first and then go back to the
nominal case.

Or force a puppet run:

.. code::

   sudo clush -b -w $nodes puppet agent -t

Note: *-t* is not optional

.. _deployment-upgrade-swh-service-long-standing-upgrade:

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

- Execute the long-standing upgrade.
- Go back to the :ref:`nominal case <deployment-upgrade-swh-service-nominal-case>`.
- Restart puppet and the cron services on workers

.. code::

   $ sudo clush -b -w @swh-workers 'systemctl start cron.service; puppet agent --enable'


.. _deployment-upgrade-swh-service-with-kubernetes:

Deployment with Kubernetes
--------------------------

This new deployment involves docker images which are exposing script/services which are
running in a virtual python frozen environment. Those versioned images are then
referenced in a specific helm chart which is deployed in a kubernetes rancher cluster.

That cluster runs on machines nodes (with :ref:`specific labels
<deployment-upgrade-swh-service-labels-on-nodes>`) onto which are scheduled
pods with containers inside. Those containers are the ones spawning the docker
image as applications.

Those docker images are built out of a declared Dockerfile in the `swh-apps`_
repository.

You can either:

- :ref:`Add a new application<deployment-upgrade-swh-service-add-new-swh-application>`
- :ref:`Update an application<deployment-upgrade-swh-service-update-swh-application>`
- :ref:`Release a new version of an application<deployment-upgrade-swh-service-build-and-publish-docker-image-app>`

.. _deployment-upgrade-swh-service-add-new-swh-application:

Add new swh application
~~~~~~~~~~~~~~~~~~~~~~~

From the repository `swh-apps`_, create a new Dockerfile.

Depending on the :ref:`services
<deployment-upgrade-swh-service-distinct-services>` to package, other existing
applications can serve as template:

- loader: use `git loader <https://gitlab.softwareheritage.org/swh/infra/swh-apps/-/blob/master/apps/swh-loader-git/>`_.
- rpc service: use `graphql <https://gitlab.softwareheritage.org/swh/infra/swh-apps/-/blob/master/apps/swh-graphql/>`_
- journal client: use `storage replayer <https://gitlab.softwareheritage.org/swh/infra/swh-apps/-/blob/master/apps/swh-storage-replayer>`_

It's time to build and publish a docker image. It's a multiple steps process
that can be executed locally starting with the :ref:`frozen set of
dependencies requirements to generate
<deployment-upgrade-swh-service-update-app-frozen-requirements>`.

.. _deployment-upgrade-swh-service-update-swh-application:

Update swh application
~~~~~~~~~~~~~~~~~~~~~~

If you need to update the swh application, edit its ``swh-apps/apps/$app/Dockerfile`` or
``swh-apps/apps/$app/entrypoint.sh`` to adapt according to change.

Note:
If a new requirement is necessary, update the ``swh-apps/apps/$app/requirements.txt``
(source of the generated ``requirements-frozen.txt``). Note that those should be kept to
a minimal and it may be that such change should happen upstream in the swh modules
instead.

Once your update is done, commit and push the change, then :ref:`build and publish the
new docker image <deployment-upgrade-swh-service-build-and-publish-docker-image-app>`.

.. _deployment-upgrade-swh-service-build-and-publish-docker-image-app:

Build and publish docker image (recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the `dedicated jenkins job
<https://jenkins.softwareheritage.org/job/swh-apps/job/build-docker-image/build?delay=0sec>`_
to update the app's frozen requirements, build the docker image with that set and
publish that image to the swh gitlab registry.

Once the application image is published in the registry, you need to
:ref:`update the impacted chart
<deployment-upgrade-swh-service-update-impacted-chart>`.

.. _deployment-upgrade-swh-service-update-impacted-chart:

Update impacted chart
~~~~~~~~~~~~~~~~~~~~~

In the `swh-chart`_ repository, update the `values file
<https://gitlab.softwareheritage.org/swh/infra/ci-cd/swh-charts/-/blob/production/values-swh-application-versions.yaml>`_
with the corresponding new changed version.

Check that the nodes are properly labelled to receive the application. Then :ref:`ArgoCD
<argocd-config>` will be in charge of deploying the changes in a rolling upgrade
fashion.

.. _deployment-upgrade-swh-service-update-app-frozen-requirements:

Update app's frozen requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We'll first need a "app-manager" container with some dependencies set (due to some
limitations in our stack):

.. code::

   $ cd swh-apps/scripts
   $ docker build -t app-manager .

Out of this container, we are able to generate the frozen requirements for the
$APP_NAME (e.g. *loader_{git, svn, cvs, ...}*, *lister*, *indexer* ...):

.. code::

   $ cd swh-apps
   $ docker run --rm -v $PWD:/src app-manager generate-frozen-requirements $APP_NAME

You have built your frozen requirements that can be committed. Next, we will
:ref:`generate the image updated with that frozen environment
<deployment-upgrade-swh-service-generate-image>`.

.. _deployment-upgrade-swh-service-generate-image:

Generate image
~~~~~~~~~~~~~~

Build the docker image with the frozen environment and then :ref:`publish it
<deployment-upgrade-swh-service-publish-image>`:

.. code::

   $ IMAGE_NAME=<application>  # e.g. loader_git, loader_svn, ...
   $ IMAGE_VERSION=YYYYMMDD.1  # Template of the day, e.g. `$(date '+%Y%m%d')`
   $ REGISTRY=container-registry.softwareheritage.org/swh/infra/swh-apps
   $ FULL_IMAGE_VERSION=$REGISTRY/$IMAGE_NAME:$IMAGE_VERSION
   $ FULL_IMAGE_LATEST=$REGISTRY/$IMAGE_NAME:latest
   $ cd swh-apps/apps/<application-name>/
   # This will create the versioned image locally
   $ docker build -t $FULL_IMAGE .
   # Tag with the latest version
   $ docker tag $FULL_IMAGE_VERSION $FULL_IMAGE_LATEST

.. _gitlab-registry:

Gitlab registry
~~~~~~~~~~~~~~~

You must have a gitlab account and generate a personal access token with at least
`write` access to the `gitlab registry
<https://gitlab.softwareheritage.org/swh/infra/swh-apps/container_registry/>`_.

.. _deployment-upgrade-swh-service-publish-image:

Publish image
~~~~~~~~~~~~~

You must first login your docker to the swh :ref:`gitlab registry <gitlab-registry>` and
then push the image:

.. code::

   $ docker login  # login to the gitlab registry (prompted for personal access token)
   passwd: **********
   $ docker push $FULL_IMAGE
   $ docker push $FULL_IMAGE_LATEST

Do not forget to :ref:`commit the changes and tag
<deployment-upgrade-swh-service-commit-changes-and-tag>`.

Finally, let's :ref:`update the impacted chart
<deployment-upgrade-swh-service-update-impacted-chart>` with the new docker
image version.

.. _deployment-upgrade-swh-service-commit-changes-and-tag:

Commit and tag
~~~~~~~~~~~~~~

Commit and tag the changes.

.. _deployment-upgrade-swh-service-labels-on-nodes:

Labels on nodes
~~~~~~~~~~~~~~~

For now, we are using dedicated labels on nodes to run specific applications:

- swh/rpc=true: rpc services, e.g. graphql
- swh/cooker=true: cooker worker
- swh/indexer=true: indexer journal client
- swh/lister=true: lister worker
- swh/loader=true: loader worker
- swh/loader-metadata=true: loader-metadata worker

In the following example:

- cluster in {archive-staging-rke2, archive-production-rke2})
- $node is an actual node hostname e.g. rancher-node-staging-rke2-worker[1, ...] or
  rancher-node-metal0{1,2} (for production)
- $new-label is a label of the form: ``swh/$service=true``

To check the actual list of labels

    kubectl --context $cluster get nodes --show-labels

To install a label on a node:

    kubectl --context $cluster label --overwrite node \
      $node $new-label


.. _swh-apps: https://gitlab.softwareheritage.org/swh/infra/swh-apps/
.. _swh-chart: https://gitlab.softwareheritage.org/infra/ci-cd/swh-charts
