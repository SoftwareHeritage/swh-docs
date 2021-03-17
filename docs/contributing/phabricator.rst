.. highlight:: bash

.. _patch-submission:

Submitting patches
==================

`Phabricator`_ is the tool that Software Heritage uses as its
coding/collaboration forge.

Software Heritage's Phabricator instance can be found at
https://forge.softwareheritage.org/

.. _Phabricator: http://phabricator.org/

Code Review in Phabricator
--------------------------

We use the Differential application of Phabricator to perform
:ref:`code reviews <code-review>` in the context of Software Heritage.

* we use Git and ``history.immutable=true``
  (but beware as that is partly a Phabricator misnomer, read on)
* when code reviews are required, developers will be allowed to push
  directly to master once an accepted Differential diff exists

Configuration
+++++++++++++

Arcanist configuration
^^^^^^^^^^^^^^^^^^^^^^

Authentication
~~~~~~~~~~~~~~

First, you should install Arcanist and authenticate it to Phabricator::

   sudo apt-get install arcanist
   arc set-config default https://forge.softwareheritage.org/
   arc install-certificate

arc will prompt you to login into Phabricator via web
(which will ask your personal Phabricator credentials).
You will then have to copy paste the API token from the web page to arc,
and hit Enter to complete the certificate installation.

Immutability
~~~~~~~~~~~~

When using git, Arcanist by default mess with the local history,
rewriting commits at the time of first submission.
To avoid that we use so called `history immutability`_

.. _history immutability: https://secure.phabricator.com/book/phabricator/article/arcanist_new_project/#history-mutability-git

To that end, you shall configure your ``arc`` accordingly::

   arc set-config history.immutable true

Note that this does **not** mean that you are forbidden to rewrite
your local branches (e.g., with ``git rebase``).
Quite the contrary: you are encouraged to locally rewrite branches
before pushing to ensure that commits are logically separated
and your commit history easy to bisect.
The above setting just means that *arc* will not rewrite commit
history under your nose.

Enabling ``git push`` to our forge
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The way we've configured our review setup for continuous integration
needs you to configure git to allow pushes to our forge.
There's two ways you can do this : setting a ssh key to push over ssh,
or setting a specific password for git pushes over https.

SSH key for pushes
~~~~~~~~~~~~~~~~~~

In your forge User settings page (On the top right, click on your avatar,
then click *Settings*), you have access to a *Authentication* >
*SSH Public Keys* section (Direct link:
``hxxps://forge.softwareheritage.org/settings/user/<your username>/page/ssh/``).
You then have the option to upload a SSH public key,
which will authenticate your pushes.

You then need to configure ssh/git to use that key pair,
for instance by editing the ``~/.ssh/config`` file.

Finally, you should configure git to push over ssh when pushing to
https://forge.softwareheritage.org, by running the following command::

   git config --global url.git@forge.softwareheritage.org:.pushInsteadOf https://forge.softwareheritage.org

This lets git know that it should use ``git@forge.softwareheritage.org:``
as a base url when pushing repositories cloned from
forge.softwareheritage.org over https.

VCS password for pushes
~~~~~~~~~~~~~~~~~~~~~~~

If you're not comfortable setting up SSH to upload your changes,
you have the option of setting a VCS password.
This password, *separate from your account password*,
allows Phabricator to authenticate your uploads over HTTPS.

In your forge User settings page (On the top right, click on your avatar,
then click *Settings*), you need to use the *Authentication* > *VCS Password*
section to set your VCS password (Direct link:
``hxxps://forge.softwareheritage.org/settings/user/<your username>/page/vcspassword/``).

If you still get a 403 error on push, this means you need
a forge administrator to enable HTTPS pushes for the repository
(which wasn't done by default in historical repositories).
Please drop by on IRC and let us know!

Workflow
++++++++

* work in a feature branch: ``git checkout -b my-feat``
* initial review request: hack/commit/hack/commit ;
  ``arc diff origin/master``
* react to change requests: hack/commit/hack/commit ;
  ``arc diff --update Dxx origin/master``
* landing change: ``git checkout master ; git merge my-feat ; git push``

Starting a new feature and submit it for review
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use a **one branch per feature** workflow, with well-separated
**logical commits** (:ref:`following those conventions <git-style-guide>`).
Please open one diff per logical commit to keep the diff size to a minimum.

.. code-block::

   git checkout -b my-shiny-feature
   ... hack hack hack ...
   git commit -m 'architecture skeleton for my-shiny-feature'
   ... hack hack hack ...
   git commit -m 'my-shiny-feature: implement module foo'
   ... etc ...

Please, follow the
To **submit your code for review** the first time::

   arc diff origin/master

arc will prompt for a **code review message**. Provide the following information:

* first line: *short description* of the overall work
  (i.e., the feature you're working on).
  This will become the title of the review
* *Summary* field (optional): *long description* of the overall work;
  the field can continue in subsequent lines, up to the next field.
  This will become the "Summary" section of the review
* *Test Plan* field (optional): write here if something special is needed
  to test your change
* *Reviewers* field (optional): the (Phabricator) name(s) of
  desired reviewers.
  If you don't specify one (recommended) the default reviewers will be chosen
* *Subscribers* field (optional): the (Phabricator) name(s) of people that
  will be notified about changes to this review request.
  In most cases it should be left empty

For example::

   mercurial loader

   Summary: first stab at a mercurial loader (T329)

   The implementation follows the plan detailed in F2F discussion with @foo.

   Performances seem decent enough for a first trial (XXX seconds for YYY repository
   that contains ZZZ patches).

   Test plan:

   Reviewers:

   Subscribers: foo

After completing the message arc will submit the review request
and tell you its number and URL::

   [...]
   Created a new Differential revision:
           Revision URI: https://forge.softwareheritage.org/Dxx

.. _arc-update:

Updating your branch to reflect requested changes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Your feature might get accepted as is, YAY!
Or, reviewers might request changes; no big deal!

Use the Differential web UI to follow-up to received comments, if needed.

To implement requested changes in the code, hack on your branch as usual by:

* adding new commits, and/or
* rewriting old commits with git rebase (to preserve a nice, easy to bisect history)
* pulling on master and rebasing your branch against it if meanwhile someone
  landed commits on master:

.. code-block::

   git checkout master
   git pull
   git checkout my-shiny-feature
   git rebase master


When you're ready to **update your review request**::

   arc diff --update Dxx HEAD~

Arc will prompt you for a message: describe what you've changed
w.r.t. the previous review request, free form.
Your message will become the changelog entry in Differential
for this new version of the diff.

Differential only care about the code diff, and not about the commits
or their order.
Therefore each "update" can be a completely different series of commits,
possibly rewritten from the previous submission.

Dependencies between diffs
^^^^^^^^^^^^^^^^^^^^^^^^^^

Note that you can manage diff dependencies within the same module
with the following keyword in the diff description::

   Depends on Dxx

That allows to keep a logical view in your diff.
It's not strictly necessary (because the tooling now deals with it properly)
but it might help reviewers or yourself to do so.

Landing your change onto master
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once your change has been approved in Differential,
you will be able to land it onto the master branch.

Before doing so, you're encouraged to **clean up your git commit history**,
reordering/splitting/merging commits as needed to have separate
logical commits and an easy to bisect history.
Update the diff :ref:`following the prior section <arc-update>`
(It'd be good to let the ci build finish to make sure everything is still green).

Once you're happy you can **push to origin/master** directly, e.g.::

   git checkout master
   git merge --ff-only my-shiny-feature
   git push

``--ff-only`` is optional, and makes sure you don't unintentionally
create a merge commit.

Optionally you can then delete your local feature branch::

   git branch -d my-shiny-feature

Reviewing locally / landing someone else's changes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can do local reviews of code with arc patch::

   arc patch Dxyz

This will create a branch **arcpatch-Dxyz** containing the changes
on your local checkout.

You can then merge those changes upstream with::

   git checkout master
   git merge --ff arcpatch-Dxyz
   git push origin master

or, alternatively::

   arc land --squash


See also
--------

* :ref:`code-review` for guidelines on how code is reviewed
  when developing for Software Heritage
