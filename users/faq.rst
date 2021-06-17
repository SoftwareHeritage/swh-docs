.. _faq:

Frequently Asked Questions
==========================

What file formats are supported with the save code now?
-------------------------------------------------------

The save code now is intended publicly for code repositories with git, mercurial or svn
version control systems. For authenticated user with role ambassador, it is possible to
do save code now requests on zip or tarballs.

I cannot find all my “releases” in a git repository archived in Software Heritage, what should I do?
----------------------------------------------------------------------------------------------------

Do not worry, the repository has been saved in full. What you are witnessing is just a
terminological difference between what platforms like GitHub calls “releases” (any non
annotated git tag) and what we call “releases” (a node in the Merkle tree, which
corresponds to a git annotated tag). Let’s say your “release” is FinalSubmission. If you
click on the branch dropdown menu on the Software Heritage Web interface you’ll find
what you are looking listed as “refs/tags/FinalSubmission”. If you want a “release” to
appear in our web interface you should create your tags using “git tag -a”, instead of
simply “git tag” (and then archive your repository again).

Where can I find the SWH roadmap?
---------------------------------

The roadmap is accessible on the `docs
<https://docs.softwareheritage.org/devel/roadmap/roadmap-2021.html>`__.


