.. _faq:

Frequently Asked Questions
**************************

.. contents::
   :depth: 3
   :local:
..

.. _faq_roadmap:

Roadmap
=======

Where can I find the SWH roadmap?
---------------------------------

The roadmap is accessible on the :ref:`development docs <swh-devel:roadmap-2021>`.

.. _faq_savecodenow:

Save Code Now
=============

What file formats are supported with the save code now?
-------------------------------------------------------

The save code now is intended publicly for code repositories with git, mercurial or svn
version control systems. For authenticated user with role ambassador, it is possible to
do save code now requests on zip or tarballs.

Is there a license existence check (the one included in the source code)?
-------------------------------------------------------------------------

No.

How are Save code now requests handled?
---------------------------------------

`Save code now <https://archive.softwareheritage.org/save/>`__ requests on known forges
for origins are scheduled as soon as possible. Unknown origins are put in a moderation
queue waiting for human vetting (Ambassadors or staff).

what file formats are supported with the save code now?
-------------------------------------------------------

The "save code now" supports public code repositories with git, mercurial or svn version
control systems. Ambassadors, however can also deposits for a given origins multiple
artifacts (zip, tarballs).

My "Save code now" request is stuck in pending status. what should I do?
------------------------------------------------------------------------

If the repository you want to save is already in the authorized list (e.g. GitLab,
GitHub, ...), the repositories will be saved without approval, so this should not last
more than a few hours. If it's not the case, requests should be approved within a few
days (minus French bank holidays), and loaded in a few hours.

If your repository is still pending after this time, this is most likely a bug. `Get in
touch with us <https://www.softwareheritage.org/community/developers/>`__ to check
whether we are aware of this potential issue or are working on it.

.. _faq_search:

Search
======

I cannot find all my "releases" in a git repository archived in Software Heritage, what should I do?
----------------------------------------------------------------------------------------------------

Do not worry, the repository has been saved in full. What you are witnessing is just a
terminological difference between what platforms like GitHub calls “releases” (any non
annotated git tag) and what we call “releases” (a node in the Merkle tree, which
corresponds to a git annotated tag). Let’s say your “release” is FinalSubmission. If you
click on the branch dropdown menu on the Software Heritage Web interface you’ll find
what you are looking listed as “refs/tags/FinalSubmission”. If you want a “release” to
appear in our web interface you should create your tags using “git tag -a”, instead of
simply “git tag” (and then archive your repository again).

How can I search the SWH archive? is it possible to search over metadata?
-------------------------------------------------------------------------

At the moment searching is possible using the url of a repository, package or deposit
(a.k.a the origin of the source code). You can use the checkbox "search in metadata
(instead of URL)" to search over intrinsic metadata.
