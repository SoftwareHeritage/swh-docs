.. highlight:: bash

.. admonition:: Intended audience
   :class: important

   Contributors

.. _gitlab-code-submission:

Submitting code to SWH
======================

We use [gitlab](https://gitlab.softwareheritage.org/) ([Community Edition](https://gitlab.com/gitlab-org/gitlab-foss)) as the coding/collaboration forge.

For a new contributor
---------------------

You will need an account in SWH gitlab for contributing code. Please follow the steps below to setup your account.

* [Signup](https://gitlab.softwareheritage.org/users/sign_up) to create a new gitlab user and wait for approval
* Once approved, you will get a notification
* If you are not already, familiarize with git and [gitlab](https://docs.gitlab.com/ee/tutorials/make_your_first_git_commit.html)
* Setup [ssh keys](https://docs.gitlab.com/ee/user/ssh.html) to communicate with SWH Gitlab
* [Optional] Install gitlab cli tools
* Sign the Software Heritage Contributor License Agreement

Development workflow
--------------------

We use a [fork based workflow](https://docs.gitlab.com/ee/user/project/repository/forking_workflow.html) and [merge requests](https://docs.gitlab.com/ee/user/project/merge_requests/) for code contributions. In order to submit a feature or for any edits in the code, please adhere to the steps below

* Create a fork of the project you wish to contribute to in your personal namespace
* Clone your forked repository and start working. It is strongly recommended to work on a [feature branch](https://docs.gitlab.com/ee/gitlab-basics/feature_branch_workflow.html)
* Make commits following the [SWH best practices](https://docs.softwareheritage.org/devel/contributing/python-style-guide.html)
* Push your branch to your forked repository
* Create a merge request against the master branch in the SWH repository
* Make sure the merge request passes all the steps in the build
* Address the review comments, if any, and wait for an approval
* Once approved, a team member will merge your changes to the master branch

Quick start script
------------------

A [script](https://gitlab.softwareheritage.org/swh/devel/swh-environment/-/blob/master/bin/fork-gitlab-repo) using python-gitlab is available to partially automate the above workflow. Using this script is recommended as it simplifies the complexities associated with the build pipelines and multiple remotes. You can use the script by following the steps below

Install python-gitlab

```
$ pip install python-gitlab
```

Create an access token with api and write repository scopes [here](https://gitlab.softwareheritage.org/-/profile/personal_access_tokens)
The script will use this token to create a fork in your namespace and to add jenkins as a user with developer permissions
Create or update the config file ``~/.python-gitlab.cfg`` and add the following content

```
[swh]
url = https://gitlab.softwareheritage.org
private_token = <your generated token>
api_version = 4
```

If you haven't done already, setup the swh-environment. Refer to the <running SWH locally> document for details
[swh-objstorage](https://gitlab.softwareheritage.org/swh/devel/swh-objstorage) is used as an example here. Replace that with the repository you wish to work

Run the script by

```
$ cd swh-environment
$ bin/fork-gitlab-repo -g swh <project name eg:swh-objstorage>
```

This will create a new fork of the SWH repository in your namespace and add a jenkins user to perform automatic builds. You can view the forked project in your personal projects [here](https://gitlab.softwareheritage.org/users/<username>/projects).
Switch to your local copy that is now ready for code contributions. You can find an extra remote named 'forked'. This points to your forked repository and that can be used to push your changes.

```
$ cd <project name eg:swh-objstorage>
$ git remote -v
forked	https://gitlab.softwareheritage.org/<username>/<project_name>.git (fetch)
forked	git@gitlab.softwareheritage.org:/<username>/<project_name>.git (push)
origin	https://gitlab.softwareheritage.org/swh/devel/<project_name>.git (fetch)
origin	git@gitlab.softwareheritage.org:/swh/devel/<project_name>.git (push)
```



SSH key for pushes
~~~~~~~~~~~~~~~~~~

In your forge User Settings page (on the top right, click on your
avatar, then click *Preferences*), you have access to the `SSH Keys
section <https://gitlab.softwareheritage.org/-/profile/keys>`__. You then have
the option to upload a SSH public key, which will authenticate your
pushes from git.

For more convenience (but not mandatory), you can also configure your ssh/git
to use that key pair, for instance by editing the ``~/.ssh/config`` file:

.. code-block::

   # .ssh/config entry for gitlab.softwareheritage.org
   Host gitlab.softwareheritage.org
     User git
     IdentityFile ~/.ssh/swh_gitlab_key
     IdentitiesOnly yes
     PreferredAuthentications publickey


Finally, you should configure git to push over ssh when pushing to
https://gitlab.softwareheritage.org, by running the following command:

.. code-block::

   git config --global url.git@gitlab.softwareheritage.org:.pushInsteadOf https://gitlab.softwareheritage.org

This lets git know that it should use
``git@gitlab.softwareheritage.org:`` as a base url when pushing
repositories cloned from gitlab.softwareheritage.org over https.

If you plan to `sign git revisions or
tags <https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work>`__,
you may also want to `upload your GPG
key <https://gitlab.softwareheritage.org/-/profile/gpg_keys>`__ as well.

Code Review in Gitlab
---------------------

As mentioned above, you can use the standard gitlab contribution
workflow. This is based on having your own copy (fork) of the project
you want to hack on in your projects. The way you manage your fork is
up to you, but we strongly recommend the process described below.

Workflow
~~~~~~~~

* fork the project on https://gitlab.softwareheritage.org (clicking the
   “Fork” button)

* clone the forked repository on your machine:

   .. code-block::

      git clone https://gitlab.softwareheritage.org/<username>/swh-xxx.git
      cd swh-xxx

* add the upstream repository:

   .. code-block::

      git remote add upstream https://gitlab.softwareheritage.org/modules/swh-xxx.git
      git fetch upstream

this allows you to easily fetch new upstream revisions in your local
repository

* work in a feature branch: ``git checkout -b my-feature``

* hack; add tests; commit; hack; rework git history;

* initial review request:

   * push your branch in your forked repository:
      ``git push origin my-feature     [...]     remote:
      To gitlab.softwareheritage.org:<username>/swh-xxx.git
      * [new branch]      my-feature -> my-feature``

   * create a Merge Request from this branch in the gitlab web UI

* react to change requests: hack/commit/hack/commit;

.. _workflow-update-merge-request:
* update your merge request:

   .. code-block::

      git push origin my-feature

or, if you have reworked or rebased the git history of the
``my-feature`` branch:

   .. code-block::

      git push --force-with-lease origin my-feature

* landing change: once the merge request has been approved, it will be
   merged in the upstream main branch ([name=david]: *by who?*); it will
   be merged if and only if the git branch behind the merge request can
   be pushed directly on the upstream main branch (without an actual
   merge) and the resulting revisions all pass CI, to keep the upstream
   git history as clean and linear as possible.

Starting a new feature and submit it for review
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As mentioned above, you should work on your fork of the upstream
project, in dedicated feature branches. In the following document, we
assume you have forked the upstream project in your namespace on
gitlab.softwareheritage.org, and you have cloned the repository with 2
remote tracked repositories:

.. code-block::

   git remove -v
   origin  git@gitlab.softwareheritage.org:<username>/swh-xxx.git (fetch)
   origin  git@gitlab.softwareheritage.org:<username>/swh-xxx.git (push)
   upstream    git@gitlab.softwareheritage.org:swh/modules/swh-xxx.git (fetch)
   upstream    git@gitlab.softwareheritage.org:swh/modules/swh-xxx.git (push)

Use a **one branch per feature** workflow, with well-separated **logical
commits** (:ref:``following those conventions <git-style-guide>``).
Please create one merge request per logical feature/fix to keep the
merge request size to a minimum.

.. code-block::

   git checkout -b my-shiny-feature
   ... hack hack hack ...
   git commit -m 'architecture skeleton for my-shiny-feature'
   ... hack hack hack ...
   git commit -m 'my-shiny-feature: implement module foo'
   ... etc ...

To **submit your code for review** the first time, you need to create a
merge request. This is a 2 steps process:

* first you need to push your branch in your forked project,
* then you need to create the merge request from that branch against
   the main branch upstream.

This is typically a matter of:

.. code-block::

   git push origin my-shiny-feature
   [...]
   remote:
   remote: To create a merge request for my-shiny-feature, visit:
   remote:   https://gitlab.softwareheritage.org/<username>/swh-xxx/-/merge_requests/new?merge_request%5Bsource_branch%5D=my-shiny-feature
   remote:
   To gitlab.softwareheritage.org:douardda/swh-xxx.git
    * [new branch]      my-shiny-feature -> my-shiny-feature

and follow the URL provided to create the merge request from the gitlab
web UI.

Check the CI is green
^^^^^^^^^^^^^^^^^^^^^

When you create (or update) a merge request, the CI should be triggered
automatically and test your proposed changes.

If the result is not OK, it is your responsibility to update and fix
your code to make the merge request ready for review.

Ask for review
^^^^^^^^^^^^^^

Normally, any green merge request is automatically ready for review. By
default, no specific reviewer is assigned to a merge request, meaning
that it can be reviewed by any team member.

You may want to ask specifically for a person to review your merge
request. In this case, you can choose in the merge request web page to
define one (or more) reviewers for your merge request.

Updating your branch to reflect requested changes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Your feature might get accepted as is, YAY! Or, reviewers might request
changes; no big deal!

To implement requested changes in the code, hack on your branch as usual
by:

* adding new commits, and/or
* rewriting old commits with git rebase (to preserve a nice, easy to
   bisect history)
* pulling on master and rebasing your branch against it if meanwhile
   someone landed commits on master:

.. code-block::

   git checkout master
   git pull
   git checkout my-shiny-feature
   git rebase master

When you’re ready to **update your review request**, you just have to
push your modifications in your local branch on gitlab:

.. code-block::

   git push origin my-shiny-feature

or, it you made some git history rework (rebase etc), you need to use:

.. code-block::

   git push --force-with-lease origin my-shiny-feature

The merge request should be updated automatically with your updated
changes.

Draft merge requests
^^^^^^^^^^^^^^^^^^^^

It is possible to prepare a merge request but keep it in a “draft”
state, to make it clear to reviewers it is not ready for review yet.

This can be done either by prefixing the merge request title with
“Draft:”.

You may also use the web UI feature “Mark as draft” (in the “Merge
request actions” menu).

Landing your change onto master
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

xxx

Reviewing locally / landing someone else's changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

xxx

See also
--------

* :ref:`code-review` for guidelines on how code is reviewed when
   developing for Software Heritage
