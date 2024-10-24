.. highlight:: bash

.. admonition:: Intended audience
   :class: important

   Contributors

.. _gitlab-code-submission:

Submitting code to SWH
======================

We use `gitlab <https://gitlab.softwareheritage.org/>`__ (`Community
Edition <https://gitlab.com/gitlab-org/gitlab-foss>`__) as the
coding/collaboration forge.

For a new contributor
---------------------

You will need an account in SWH gitlab for contributing code or
documentation. Please follow the steps below to setup your account.

-  `Signup <https://gitlab.softwareheritage.org/users/sign_up>`__ to
   create a gitlab account.
-  Account approve and land is manual and could take a while. Once
   approved, you will get a notification.
-  If you are not already, familiarize with
   `git <https://git-scm.com/book/en/v2>`__ and
   `gitlab <https://docs.gitlab.com/ee/tutorials/make_your_first_git_commit.html>`__.
-  Setup `ssh keys <https://docs.gitlab.com/ee/user/ssh.html>`__ to
   communicate with SWH Gitlab.
-  Sign the Software Heritage Contributor License Agreement. Please
   contact us to know more about this.

.. _patch-submission:

Development workflow
--------------------

We use a `fork based
workflow <https://docs.gitlab.com/ee/user/project/repository/forking_workflow.html>`__
and `merge
requests <https://docs.gitlab.com/ee/user/project/merge_requests/>`__
for code contributions. In order to submit a feature or for any edits in
the code, please adhere to the steps below:

-  Create a fork of the project you wish to contribute to in your
   personal namespace.
-  Clone your forked repository and start working. It is strongly
   recommended to work on a `feature
   branch <https://docs.gitlab.com/ee/gitlab-basics/feature_branch_workflow.html>`__.
-  Make commits following the `SWH best
   practices <https://docs.softwareheritage.org/devel/contributing/python-style-guide.html>`__.
-  Push your branch to your forked repository.
-  Create a merge request against the SWH repository.
-  Make sure the merge request passes the CI build.
-  Address the review comments, if any, and wait for an approval.
-  Once approved, a team member will merge your changes to the master
   branch.

Quick start script
------------------

note: If you haven’t done already, setup the swh-environment before
this. Refer to the :ref:`getting started <getting-started>` for details.

A `script <https://gitlab.softwareheritage.org/swh/devel/swh-environment/-/blob/master/bin/fork-gitlab-repo>`__
using `python-gitlab <https://github.com/python-gitlab/python-gitlab>`__
is available to partially automate the above workflow. Using this script
is recommended as it simplifies the complexities associated with the
build pipelines and multiple remotes. You can use the script by
following the steps below:

Create an access token with api and write repository scopes
`here <https://gitlab.softwareheritage.org/-/profile/personal_access_tokens>`__.
The script will use this token to create a fork in your namespace and to
add jenkins as a user with developer permissions. Create or update the
config file :file:`~/.python-gitlab.cfg` and add the following content.

.. code-block::

   [swh]
   url = https://gitlab.softwareheritage.org
   private_token = <your generated token>
   api_version = 4

In the following command line excerpts, we will use
`swh-objstorage <https://gitlab.softwareheritage.org/swh/devel/swh-objstorage>`__
as example. Please, replace that with the repository you wish to work
with.

Run the script by

.. code-block::

   $ cd swh-environment
   $ bin/update   # Used to update all the repos under the environment to their latest version
   $ bin/fork-gitlab-repo -g swh swh-objstorage
   $ bin/fork-gitlab-repo -g swh .  # To contribute to swh-environment itself (eg. add a repository)

This will create a new fork of the SWH repository in your namespace and
add a jenkins user to perform automatic builds. You can view the forked
project in your personal projects
`here <https://gitlab.softwareheritage.org/users/%3Cusername%3E/projects>`__.
Switch to your local copy that is now ready for code contributions. You
can find an extra remote named ‘forked’. This points to your forked
repository and that can be used to push your changes.

.. code-block::

   $ cd swh-objstorage
   $ git remote -v
   forked  https://gitlab.softwareheritage.org/<username>/swh-objstorage.git (fetch)
   forked  git@gitlab.softwareheritage.org:/<username>/swh-objstorage.git (push)
   origin  https://gitlab.softwareheritage.org/swh/devel/swh-objstorage.git (fetch)
   origin  git@gitlab.softwareheritage.org:/swh/devel/swh-objstorage.git (push)


SSH key for pushes
~~~~~~~~~~~~~~~~~~

In your forge User Settings page (on the top right, click on your
avatar, then click *Preferences*), you have access to the
`SSH Keys section <https://gitlab.softwareheritage.org/-/profile/keys>`__.
You then have the option to upload a SSH public key, which will
authenticate your pushes from git.

For more convenience (but not mandatory), you can also configure your
ssh/git to use that key pair, for instance by editing the
``~/.ssh/config`` file:

.. code-block::

   # .ssh/config entry for gitlab.softwareheritage.org
   Host gitlab.softwareheritage.org
   User git IdentityFile ~/.ssh/swh_gitlab_key
   IdentitiesOnly yes
   PreferredAuthentications publickey

Finally, you should configure git to push over ssh when pushing to
https://gitlab.softwareheritage.org, by running the following command:

.. code-block::

   git config --global url.git@gitlab.softwareheritage.org:.pushInsteadOf https://gitlab.softwareheritage.org

This lets git know that it should use
``git@gitlab.softwareheritage.org:`` as a base url when pushing
repositories cloned from gitlab.softwareheritage.org over https.

If you plan to
`sign git revisions or tags <https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work>`__,
you may also want to
`upload your GPG key <https://gitlab.softwareheritage.org/-/profile/gpg_keys>`__
as well.

Make a release
--------------

.. warning:: Only staff members are allowed to make new releases

Releases are made automatically by Jenkins when a tag is pushed to a module repository.

We are using the `semantic versioning <https://semver.org>`_ scheme to name our
releases, please ensure that the name of your tag correctly indicates its compatibility
with the previous version.

Tags themselves should be signed and provide a meaningful annotation with, for example,
an itemized summary of changes (rather than rehashing the whole git log), breaking
changes in a separate section, etc.

First, create the tag:

.. code-block::

   # get the latest version number
   git describe --tags  # returns v1.2.3-x-yyy
   # list changes between master and v1.2.3
   git range-diff v1.2.3...master
   # use the output to write your annotation and create a new signed tag, here for a
   # minor version upgrade
   git tag -a -s v1.3.0
   # push it
   git push origin tag v1.3.0

Then you'll see jobs on Jenkins (Incoming tag, GitLab builds, Upload to PyPI)
indicating that the release process is ongoing.

Next, deployment container images are updated.

And finally a new merge request will automatically be created in 
`Helm charts for swh packages`_ so that the devops team can proceed with deployment.

.. _Helm charts for swh packages: https://gitlab.softwareheritage.org/swh/infra/sysadm-environment
