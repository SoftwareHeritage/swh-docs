.. _howto-debian-packaging:

Debian packaging
================

.. admonition:: Intended audience
   :class: important

   staff members who wants to start packaging some swh modules

Package repository
------------------

A package repository is available on
https://debian.softwareheritage.org/.

Unstable / Testing:

.. code::

   deb [trusted=yes] https://debian.softwareheritage.org/ unstable main

Stable / Bullseye:

.. code::

  deb [trusted=yes] https://debian.softwareheritage.org/ bullseye-swh

Oldstable / Buster (current production):

.. code::

   deb [trusted=yes] https://debian.softwareheritage.org/ buster-swh

This package repository is handled via reprepro on
pergamon.internal.softwareheritage.org (base directory:
/srv/softwareheritage/repository).

.. _uploading_packages:

Uploading packages
~~~~~~~~~~~~~~~~~~

Packages are added to the repository using

.. code::

   reprepro -vb /srv/softwareheritage/repository processincoming incoming``.

For packages to be accepted, they need to be :

#. A changes file uploaded to ``/srv/softwareheritage/repository/incoming``:

#. Targeted at one of the supported distributions (unstable, unstable-swh, buster,
   buster-backports, buster-backports-swh)

#. Signed by one of the keys listed in
   ``/srv/softwareheritage/repository/conf/uploaders``

.. _git_repositories_for_debian_packages:

Git repositories for Debian packages
------------------------------------

Our git repository structure for Debian packages is compatible with
``git-buildpackage``.

We have two different ways of handling repositories for Debian packages:

- Packages of python modules where *we* are upstream
- Packages of dependencies from another upstream (this also encompasses upstream Debian
  packages that we wish to backport for deployment)

For these classes of packages, we have two sets of (identical) Jenkins jobs to handle
building and uploading these packages to our package repository. The structure of the
packaging branches for both classes is pretty much the same, the repositories only
differ on how we handle upstream commits:

- Our own modules are merged with the upstream repository
- External dependencies ignore the upstream repository and only have packaging branches.

.. _branch_and_tags_structure:

Branch and tags structure
~~~~~~~~~~~~~~~~~~~~~~~~~

Our debian packaging Jenkins jobs expect the following branches, which are pretty close
to what https://dep-team.pages.debian.net/deps/dep14/ mandates:

- debian/upstream (history of unpacked upstream releases)
- debian/ (history of the packaging of the given suite, e.g. unstable-swh, buster-swh)
- pristine-tar (data to regenerate upstream tarballs from a git export)

The name of the debian/upstream branch doesn't matter as long as it's properly
configured in the ``debian/gbp.conf`` file. It's only really used by ``gbp import-orig``
when importing a new release.

The tags marking upstream releases imported from tarballs for Debian packaging purposes
are named ``debian/upstream/<upstream-version-number>``.

Our Jenkins jobs are triggered on incoming tags named ``debian/<version>``. To generate
the proper tags, use ``gbp buildpackage --git-tag-only``.

The git-buildpackage configuration, ``debian/gbp.conf``, should be the following:

.. code::

   [DEFAULT]
   upstream-branch=debian/upstream
   upstream-tag=debian/upstream/%(version)s
   debian-branch=debian/<current-suite>
   pristine-tar=True

.. _automatic_packaging_for_swh_python_modules:

Automatic packaging for swh python modules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``swh.*`` python modules have an extra jenkins job that updates the packaging
automatically when we do an upstream release. This job only runs ``gbp import-orig``
with the tarball we release to PyPI, and the right options to merge the upstream
history.

To merge changes from the upstream history, we add the following option to ``gbp.conf``.

.. code::

   upstream-vcs-tag=v%(version)s

.. _bootstrapping_debian_branches_for_a_swh_package:

Bootstrapping the Debian packaging branches for a SWH package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When introducing a new Python package in swh-environment, after the first release, one
needs to bootstrap the Debian packaging branches to allow Jenkins to automatically build
Debian packages.

To do so, swh-environment contains a ``bin/debpkg-bootstrap-branches`` script, which
generates a basic Debian branch structure from an existing tag, and files in the
``debian-template/`` directory.

Once the script has created the new unstable packaging branches, test the build locally
following the instructions in the :ref:`local_package_building` section of this
documentation. Once you've handled any build issues (e.g. missing build-dependencies),
you can tag the first debian release and push all branches so that Jenkins can do a
clean build. The backports branches will get created automatically by the Jenkins jobs
once the unstable build succeeds.

.. code::

   gbp buildpackage --git-tag-only --git-sign-tags
   git push origin --set-upstream --follow-tags pristine-tar:pristine-tar debian/upstream:debian/upstream debian/unstable-swh:debian/unstable-swh

.. _bootstrapping_a_dependency_packaging_repository:

Bootstrapping a dependency packaging repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Bootstrapping the packaging repository for a dependency is analogous to regular Debian
practices:

Download the upstream tarball. For PyPI, use the redirector at
*http://pypi.debian.net/<pkgname>/*:

.. code::

   wget http://pypi.debian.net/pytest-postgresql/pytest-postgresql-1.3.4.tar.gz

Create a new git repository:

.. code::

   git init pytest-postgresql
   cd pytest-postgresql

Import the original upstream version:

.. code::

   git checkout -b debian/unstable-swh
   gbp import-orig --pristine-tar --upstream-branch=debian/upstream --upstream-tag=debian/upstream/%(version)s --debian-branch=debian/unstable-swh ../pytest-postgresql-1.3.4.tar.gz
   # What will be the source package name? [pytest-postgresql]
   # What is the upstream version? [1.3.4]
   # gbp:info: Importing '../pytest-postgresql-1.3.4.tar.gz' to branch 'debian/upstream'...
   # gbp:info: Source package is pytest-postgresql
   # gbp:info: Upstream version is 1.3.4
   # gbp:info: Successfully imported version 1.3.4 of ../pytest-postgresql-1.3.4.tar.gz

Bootstrap the debian directory:

.. code::

   mkdir -p debian/source
   echo '3.0 (quilt)' > debian/source/format
   echo 9 > debian/compat
   cat > debian/gbp.conf << EOF
   [DEFAULT]
   upstream-branch=debian/upstream
   upstream-tag=debian/upstream/%(version)s
   debian-branch=debian/unstable-swh
   pristine-tar=True
   EOF
   cp /usr/share/doc/debhelper/examples/rules.tiny debian/rules
   vim debian/control
   # [...] adapt debian/control from another package
   dch --create --package pytest-postgresql --newversion 1.3.4-1+swh1 --distribution unstable-swh
   vim debian/copyright
   # [...] adapt debian/copyright from another package
   git add debian
   git commit -m "Initial packaging for pytest-postgresql"

You can then go on to try building the package.

.. code::

   gbp buildpackage --git-builder='sbuild -As'

Once the package builds, if you want to check your package's conformance to Debian
policy, you can run ``lintian`` on the changes:

.. code::

   lintian -EI ../pytest-postgresql_1.3.4-1+swh1_amd64.changes

Note that you have to ignore warnings about unknown distributions, as we're building
specifically for our repository.

We need to use a ``+swh1`` version suffix to avoid clashing with potential upstream
Debian package versions.

.. _bootstrapping_the_backport_branches:

Bootstrapping the backport branches
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

During most of the operation, backports should happen automatically as we have a Jenkins
job that generates backports on successful builds. However, when creating a packaging
repository, we need to bootstrap the branches once, before Jenkins is able to do the
work automatically.

The backport branches should (ideally) be bootstrapped from a debian tag that has
successfully built on Jenkins.

Checkout the new branch:

.. code::

   git checkout debian/<version-number>
   git checkout -b debian/buster-swh

Update the gbp config to match the branch:

.. code::

   sed -i s/unstable-swh/buster-swh/ debian/gbp.conf

Generate the initial backports entry. Use the current Debian version number (10 for
buster, 11 for bullseye, ...)

.. code::

   dch -l "~bpo10" -D buster-swh --force-distribution 'Rebuild for buster-swh'

You should then be able to try a local package build, and if that succeeds, to push the
tag for Jenkins to autobuild.

.. _setting_up_the_repository_on_phabricator:

Setting up the repository on Phabricator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Deprecation notice
   :class: warning

   This is no longer necessary as we migrated to gitlab

The repository on Phabricator needs the following settings:

- Callsign: non-empty; prefix should be P according to `Phabricator callsign convention
  <https://wiki.softwareheritage.org/wiki/Phabricator_callsign_naming_convention>`_
- Short name: non-empty (used to make pretty git clone URLs; ideally matching the source
  package name)
- Repository tags: "Has debian packaging branches" (allows Jenkins to push on the
  ``debian/*`` branches)
- Policy:

   - View: Public (no login required)
   - Edit: Developers
   - Push: All users (actual restrictions are handled by Herald rules)

- Activate the repository
- Look up the path to the repository on the storage tab

You need to setup the post-receive hook for Jenkins to be able to
trigger on tag pushes

.. code::

   ssh -p 2222 -t tate.internal.softwareheritage.org \
     phabricator-setup-hook /srv/phabricator/repos/<repo-id> <post-receive-hook>

Note:

- there exists 3 types of hooks:

   - *post-receive-swh-modules* for swh modules developed by the team
   - *post-receive-debian-deps* for external modules packaged by the team
   - *post-receive-swh-docker-image-modules* for modules which creates docker images

- remember that access to tate is on port 2222.

The repo ID can be found on the repo's "storage" property page on phabricator, typically
(for SHORTNAME in {model, core, loader-core, loader-core, storage, ...}):

https://forge.softwareheritage.org/source/swh-SHORTNAME/manage/storage/

.. _setting_up_the_jenkins_jobs:

Setting up the Jenkins jobs
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Jenkins `jobs are accessible through the ui
<https://jenkins.softwareheritage.org/view/Debian%20dependency%20packages/>`_:


They are declared in the `swh-jenkins-jobs repository
<https://gitlab.softwareheritage.org/swh/infra/ci-cd/swh-jenkins-jobs>`_.

Jobs for dependency packages are configured in ``jobs/dependency-packages.yaml``. You
can add a section as follows:

.. code::

   - project:
       name: <callsign>
       display-name: <short-name>
       pkg: <source-name>
       python_module: <python-module>
       jobs:
         - 'dependency-jobs-{name}'

For example:

.. code::

   - project:
       name: DLDBASE
       display-name: swh-loader-core
       repo_name: swh-loader-core
       pkg: loader.core
       python_module: swh.loader.core
       jobs:
         - 'swh-jobs-{name}'

Other samples can be found in the dedicated repository.

- usual swh package: `swh.core <https://gitlab.softwareheritage.org/swh/infra/ci-cd/swh-jenkins-jobs/-/blob/master/jobs/swh-packages.yaml#L15-22>`_
- peculiar swh package (with name divergences): `swh.icinga_plugins <https://gitlab.softwareheritage.org/swh/infra/ci-cd/swh-jenkins-jobs/-/blob/master/jobs/swh-packages.yaml#L88-95>`_

Use the regular review process to land your changes. Once your changes are pushed, a
dedicated Jenkins job will generate the jobs from the configuration.

If your package needs extra repositories to build, you can add them as comma-separated
values to the ``deb-extra-repositories`` setting, with the following notes:

- When building packages for the **"*.swh"** suites, the Software Heritage Debian repository
  is automatically enabled.
- When building packages for backports suites, the backports repository is automatically
  enabled.

.. _updating_a_dependency_packaging_repository:

Updating a dependency packaging repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Place yourself on the debian/unstable-swh branch and "gbp import-origin" a more recent
upstream release tarballs.

For example (current version on 0.0.5, upstream bumped to 0.0.7):

.. code::

   gbp import-origin https://files.pythonhosted.org/../attrs-strict-0.0.7.tar.gz

This will update the following branches:

-  debian/upstream
-  pristine-tar
-  debian/unstable-swh

This also includes the necessary tags (``debian/upstream/0.0.7``).

You then need to push all branches/tags to the repository:

.. code::

   git push origin --all --follow-tags

Ensure the :ref:`update builds fine <local_package_building>` And :ref:`tags accordingly
the debian/unstable-swh branch when ok <remote_package_building>`.

Jenkins will then keep up on building the package.

.. _local_package_building:

Local package building
~~~~~~~~~~~~~~~~~~~~~~

To locally test a package build, go on the appropriate debian packaging branch, and run

.. code::

   gbp buildpackage --git-builder=sbuild -As --no-clean-source

``gbp buildpackage`` passes all options not starting with ``--git-`` to the builder.
Some useful options are the following:

- ``--git-ignore-new`` builds from the working tree, with all the uncommitted changes.
  Useful for quick iteration when something just doesn't work.

- ``--no-clean-source`` doesn't run debian/rules clean outside of the chroot, so you
  don't have to clutter your dev machine with all build dependencies

- ``--build-dep-resolver=aptitude`` can be necessary when using extra
  repositories, especially backports.

- ``--extra-repository="repository specification"`` adds the given repository in the
  chroot before building.

- ``--extra-repository-key="repository signing key"`` adds the given key as a trusted
  gpg key for package sources.

- ``--extra-package=<.deb file or directory>`` makes the given package (or all .deb
  packages in the given directory) available for dependency resolution. Useful when
  testing builds with a dependency chain.

- ``--force-orig-source`` forces addition of the ``.orig.tar.gz`` file in the
  ``.changes`` file (useful when trying to upload a backport)

See ``gbp help buildpackage`` and ``man sbuild`` for a full description of all options

For **sid**, it would be:

.. code::

   git checkout debian/unstable-swh
   gbp buildpackage --git-builder=sbuild -As \
     --no-clean-source --force-orig-source \
     --extra-repository='deb [trusted=yes] https://debian.softwareheritage.org/ unstable main'

or if you need some third-party repository, say cassandra (for swh-storage):

.. code::

   gbp buildpackage --git-builder=sbuild -As \
     --no-clean-source --force-orig-source \
     --extra-repository='deb [trusted=yes] https://debian.softwareheritage.org/ unstable main' \
     --extra-repository='deb [arch=amd64 trusted=yes] https://debian.cassandra.apache.org 41x main'

For **buster**, it would be (note the usage of aptitude as resolver as the
backports repository is used):

.. code::

   git checkout debian/buster-swh
   gbp buildpackage --git-builder=sbuild -As --build-dep-resolver=aptitude \
     --no-clean-source --force-orig-source \
     --extra-repository='deb https://deb.debian.org/ buster-backports main' \
     --extra-repository='deb [trusted=yes] https://debian.softwareheritage.org/ buster-swh main'

For **bullseye**, it would be (also note the usage of aptitude as resolver as the
backports repository is used):

.. code::

   git checkout debian/bullseye-swh
   gbp buildpackage --git-builder=sbuild -As --build-dep-resolver=aptitude \
     --no-clean-source --force-orig-source \
     --extra-repository='deb https://deb.debian.org/ bullseye-backports main' \
     --extra-repository='deb [trusted=yes] https://debian.softwareheritage.org/ bullseye-swh main'

.. Warning:: At time of writing, most software packages have no bullseye branch yet.

**TODO**: Rewrite bin/make-package as bin/swh-gbp-buildpackage wrapping ``gbp
buildpackage`` with the most common options.

.. _remote_package_building:

Remote package building
~~~~~~~~~~~~~~~~~~~~~~~

Jenkins builds packages when the repository receives a tag.

Once the local build succeeds, tag the package with:

.. code::

   gbp buildpackage --git-tag-only --git-sign-tags

Alternatively, you can add the ``--git-tag`` option to your ``gbp buildpackage`` command
so the tag happens automatically on a successful build.

Then, push your tag, and Jenkins jobs should get triggered

.. code::

   git push --tags

.. _build_environment_setup:

Build Environment setup
-----------------------

Our automated packaging setup uses sbuild, which is also used by the Debian build
daemons themselves. This section shows how to set it up for local use.

.. _sbuild_setup:

sbuild setup
~~~~~~~~~~~~

.. code::

   # Install the package
   sudo apt-get install sbuild
   # Add your user to the sbuild group, to allow him to use the sbuild commands
   sudo sbuild-adduser $USER
   # You have to logout and log back in
   # Prepare chroots
   sudo mkdir /srv/chroots
   sudo mkdir /srv/chroots/var
   # Optionally create a separate filesystem for /srv/chroots and move the
   # sbuild/schroot data to that partition
   sudo rsync -avz --delete /var/lib/schroot/ /srv/chroots/var/schroot/
   sudo rm -r /var/lib/schroot
   sudo ln -sf /srv/chroots/var/schroot /var/lib/schroot
   sudo rsync -avz --delete /var/lib/sbuild/ /srv/chroots/var/sbuild/
   sudo rm -r /var/lib/sbuild
   sudo ln -sf /srv/chroots/var/sbuild /var/lib/sbuild
   # end optionally
   # Create unstable/sid chroot
   sudo sbuild-createchroot --include apt-transport-https,ca-certificates sid /srv/chroots/sid http://deb.debian.org/debian/
   # Create bullseye chroot
   sudo sbuild-createchroot --include apt-transport-https,ca-certificates bullseye /srv/chroots/bullseye http://deb.debian.org/debian/
   # Create buster chroot
   sudo sbuild-createchroot --include apt-transport-https,ca-certificates buster /srv/chroots/buster http://deb.debian.org/debian/

If you use /etc/hosts to resolve **\*.internal.softwareheritage.org** hosts:

.. code::

   echo hosts >> /etc/schroot/sbuild/nssdatabases

.. _schroot_setup:

schroot setup
~~~~~~~~~~~~~

Now that the sbuild base setup is done. You now need to configure schroot to use an
overlay filesystem, which will avoid copying the chroots at each build.

You need to update the configuration (in ``/etc/schroot/chroot.d/*-sbuild-*``) with the
following directives:

.. code::

   source-groups=root,sbuild
   source-root-groups=root,sbuild
   union-type=overlay

This allows the sbuild group to edit the contents of the source chroot (for instance to
update it) and sets up the overlay.

You should also use this opportunity to add "aliases" to your chroot, so that sbuild
will directly support the distributions we're using (unstable-swh,
buster-backports-swh, ...):

For unstable:

.. code::

   aliases=unstable-amd64-sbuild,UNRELEASED-amd64-sbuild,unstable-swh-amd64-sbuild

For bullseye:

.. code::

   aliases=bullseye-swh-amd64-sbuild,bullseye-backports-amd64-sbuild,bullseye-backports-swh-amd64-sbuild

For buster:

.. code::

   aliases=buster-swh-amd64-sbuild,buster-backports-amd64-sbuild,buster-backports-swh-amd64-sbuild

.. _dependencies_cache:

dependencies cache
^^^^^^^^^^^^^^^^^^

Add the following line to schroot's fstab /etc/schroot/sbuild/fstab to permit reuse of
existing fetched dependencies:

.. code::

   /var/cache/apt/archives /var/cache/apt/archives none rw,bind 0 0

You can also run apt-cacher-ng, which will avoid locking issues when several chroots try
to access the package cache at once. You then need to add the proxy configuration to apt
by adding a file in ``/etc/apt/apt.conf.d`` on each chroot.

.. _schroot_update:

schroot update
~~~~~~~~~~~~~~

You should update your chroot environments once in a while (to avoid repeating over and
over the same step during your package build):

.. code::

   sudo sbuild-update -udcar sid; sudo sbuild-update -udcar buster

.. _environment_setup:

environment setup
~~~~~~~~~~~~~~~~~

The Debian tools use a few variables to preset your name and email. Add this to your
``.<shell>rc``:

.. code::

   export DEBFULLNAME="Debra Hacker"
   export DEBEMAIL=debra.hacker@example.com

Make sure this data matches an uid for your GPG key. Else, you can use the
``DEBSIGN_KEYID=`` variable. (Future version of gpg2, e.g. 2.2.5 can refuse to sign with
the short key id).

.. _overlay_in_tmpfs_for_faster_builds:

overlay in tmpfs for faster builds
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can add this to your fstab to put the overlay hierarchy in RAM:

.. code::

   tmpfs /var/lib/schroot/union/overlay tmpfs uid=root,gid=root,mode=0750,nr_inodes=0 0 0
