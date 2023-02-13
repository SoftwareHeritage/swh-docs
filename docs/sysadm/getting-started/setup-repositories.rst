.. _setup-repositories:

Reference: Setup sysadm repositories
====================================

.. admonition:: Intended audience
   :class: important

   new sysadm member

This page describes the steps to clone locally all sysadm repositories.

.. _multiple_repository_setup:

Multiple umbrella repositories setup
------------------------------------

We use multiple umbrella repositories to manage specific repositories for dedicated
perimeters:

- sysadm-environment_: Deployment related and credentials repositories
  (k8s-cluster-conf, ...)
- puppet-environment_ : Various swh puppet and third-party repositories (swh-site, ...)
- ci-environment_: CI (Jenkins) related repositories (jobs, dockerfile, ...)


Clone umbrella repositories
---------------------------

Clone each of those repositories. They each contain a .mrconfig file and a README file.

::

   $ git clone https://gitlab.softwareheritage.org/swh/infra/sysadm-environment.git
   $ git clone https://gitlab.softwareheritage.org/swh/infra/puppet/puppet-environment.git
   $ git clone https://gitlab.softwareheritage.org/swh/infra/ci-cd/ci-environment.git

Then, use the `mr` (myrepos) command that uses the .mrconfig file to clone the
repositories managed by myrepos:

::

   $ for repository in sysadm-environment puppet-environment ci-environment; \
     do
       pushd $repository ; \
       readlink -f .mrconfig >> ~/.mrtrust ; \
       mr up ; \
       popd ; \
     done

(the *mr* command is in the `myrepos Debian package
<https://packages.debian.org/buster/myrepos>`_).

.. _puppet-environment: https://gitlab.softwareheritage.org/infra/puppet/puppet-environment
.. _sysadm-environment: https://gitlab.softwareheritage.org/infra/sysadm-environment
.. _ci-environment: https://gitlab.softwareheritage.org/swh/infra/ci-cd/ci-environment
