.. _faq_user:

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

The roadmap is accessible on the :ref:`development docs <roadmap-2021>`.

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

:swh_web:`Save code now <save/>` requests on known forges
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

.. _faq_addforgenow:

Add Forge Now
=============

What is the frequency at which you re-clone projects?
-----------------------------------------------------

It is variable, regarding a range of complex parameters, but on
average the frequency is between a few days and a couple of weeks.

Is each clone a full clone, or do you do incremental pulls after the initial clone?
-----------------------------------------------------------------------------------

We do incremental pulls after the first visit.

Which IP address range should we mark as safe in our anti-bot protection systems?
---------------------------------------------------------------------------------

Our main IP address range is 128.93.166.0/26 and IPv6 is not yet used.

Is there a risk of request overload on my forge when you process the ingestion?
-------------------------------------------------------------------------------

The add forge now feature uses dedicated workers, configured to limit the
request load, so that the load is bearable even on a small-scale server.

Our repos are already archived in SWH, isn't an Add Forge request redundant?
----------------------------------------------------------------------------

The add forge now feature allows us to regularly discover all repositories
on a forge, which means we will notice when new repositories are created
and be able to save them automatically.

Why forges need to be archived in SWH
-------------------------------------

Software Heritage is a non profit organization, hosted by Inria (french 
research institute), in partnership with Unesco. Our mission is notably to 
preserve software source code as a cultural heritage of human knowledge and 
for the promotion of Open Science. We also defend strong ethical values 
about the usage of the archived data.

As a universal archive, we are committed to archive any publicly available 
source code, especially when this code is published under free/open source 
licence.

If your forge contains non-FOSS projects that you don't want to expose to 
archival or to any "wild" copy, we recommend you to set them as private.

Indeed, publicly available projects can be archived by anyone using the 
Save Code Now feature (archival of a single repository), so we cannot 
guarantee that they won't be archived even if we don't process an Add 
Forge Now request. 

What is the position of SWH towards AI training and LLMs
--------------------------------------------------------

We've recently published a `statement to explain our position towards LLM:
<https://www.softwareheritage.org/2023/10/19/swh-statement-on-llm-for-code/>`__ 

Our principles are the following:

1. Knowledge derived from the Software Heritage archive must be given
   back to humanity, rather than monopolized for private gain. The resulting 
   machine learning models must be made available under a suitable open license, 
   together with the documentation and toolings needed to use them.
2. The initial training data extracted from the Software Heritage archive 
   must be fully and precisely identified by, for example,  publishing the 
   corresponding SWHID identifiers <https://www.swhid.org/> (note that, in the 
   context of Software Heritage, public availability of the initial training data 
   is a given: anyone can obtain it from the archive). This will enable use cases 
   such as: studying biases (fairness), verifying if a code of interest was present 
   in the training data (transparency), and providing appropriate attribution when
   generated code bears resemblance to training data (credit), among others.
3. Mechanisms should be established, where possible, for authors to exclude 
   their archived code from the training inputs before model training begins.

Additionally, I would like to mention that as long as your code is publicly 
available, it might have already been used by private LLMs without matter of consent 
and attribution. Software Heritage represents an ethical alternative, with a strong 
effort to help authors to get more control and traceability on the usage of their 
source code by LLMs.

Furthermore, computer-readable standards for LLM usage restrictions (equivalent of 
robots.txt) should emerge in the near future to bring global answers to these 
concerns.

At this stage, the only way to ensure that your code is not used by any LLM would be 
to set your repositories as private.

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
