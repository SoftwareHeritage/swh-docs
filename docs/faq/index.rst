.. _faq:

Frequently Asked Questions
**************************

.. contents::
   :depth: 3
   :local:
..

.. _faq_prerequisites:

Prerequisites for code contributions
====================================

What are the Skills required to be a code contributor?
------------------------------------------------------

Generally, only Python and basic Git knowledge are required to contribute.
Other than that, it really depends on what technical areas you want to work on.

For student internships, the `internships`_ page details specific prerequisites
needed to pick up a topic.

Feel free to contact us via our `development channels
<https://www.softwareheritage.org/community/developers/>`__ to inquiry about
specific skills needed to work on any topic of your interest.

What are the minimum system requirements (hardware/software) to run SWH locally?
--------------------------------------------------------------------------------

Python 3.7 or newer is required. See the :ref:`developer setup documentation
<developer-setup>` for more details.


.. _faq_getting_started:

Getting Started
===============

What are the must read docs before I start contributing?
--------------------------------------------------------

We recommend you read the top links listed at from the :ref:`documentation home page
<swh-docs>` in order: getting started,
contributing, and architecture overview, as well as the data model.

Where can I see the getting started guide for developers?
---------------------------------------------------------

For hacking on the Software Heritage code base you should start from the
:ref:`developer-setup` tutorial.

How do I find an easy task to get started?
------------------------------------------

We maintain a `list of easy tickets
<https://forge.softwareheritage.org/maniphest/query/WcCLxlHnXok9/>`__ to work on, see
the `Easy hacks page <https://wiki.softwareheritage.org/wiki/Easy_hacks>`__ for more
details.

I am skilled in one specific technology, can I find tickets requiring that skill?
---------------------------------------------------------------------------------

Unfortunately, not at the moment. But you can look at the `internships`_
list to look for something matching
this skill, and this may allow you to find topics to search for in the `bug tracking
system`_.

Either way, feel free to contact our developers through any of the
`development channels`_, we would love to work with
you.

Where should I ask for technical help?
--------------------------------------

You can choose one of the following:

* `development channels`_
* `contact form`_ for any enquiries

.. _faq_run_swh:

Running an SWH instance locally
===============================

How do I run a local "toy version" of the archive?
--------------------------------------------------

The :ref:`getting-started` tutorial shows how to run a local instance of the
Software Heritage software infrastructure, using Docker.

I have SWH stack running in my local. How do I get some initial data to play around?
------------------------------------------------------------------------------------

You can setup a job on your local machine, for this you can
:ref:`schedule a listing task <docker-schedule-lister-task>`
for example. Doing so on small forge, will allow you to load some repositories.

Or you can also trigger directly :ref:`loading from the cli <docker-run-loader-cli>`.

I have a SWH stack running in local, How do I setup a lister/loader job?
------------------------------------------------------------------------

See the :ref:`"Managing tasks" chapter <docker-manage-tasks>`
in the Docker environment documentation.

How can I create a user in my local instance?
---------------------------------------------

We cannot right now. Stay either anonymous or use the user "test" (password "test") or
the user ambassador (password "ambassador").

Should I run/test the web app in any particular browser?
--------------------------------------------------------

We expect the web app to work on all major browsers. It uses mostly straightforward
HTML/CSS and a little Javascript for search and source code highlighting, so testing in
a single browser is usually enough.

.. _faq_dataset:

Getting sample datasets
=======================

Is there a way to connect to SWH archived (production) database from my local machine?
--------------------------------------------------------------------------------------

We provide the archive as a dataset on public clouds, see the :ref:`swh-dataset
documentation <swh-dataset>`. We can
also provide read access to one of the main databases on request, `contact us`_.

.. _faq_error_bugs:

Errors and bugs
===============

I found a bug/improvement in the system, where should I report it?
------------------------------------------------------------------

Please report it on our `bug tracking system`_.
First create an account, then create a bug report using the "Create task" button. You
should get some feedback within a week (at least someone triaging your issue). If not,
`get in touch with us <development channels>`_ to
make sure we did not miss it.

.. _faq_legal:

Legal matters
=============

Do I need to sign a form to contribute code?
--------------------------------------------

Yes, on your first diff, you will have to sign such document.
As long as it's not signed, your diff content won't be visible.

Will my name be added to a CONTRIBUTORS file?
---------------------------------------------

You will be asked during review to add yourself.

.. _faq_code_review:

Code Review
===========

I found a straightforward typo fix, should my fix go through the entire code review process?
--------------------------------------------------------------------------------------------

You are welcome to drop us a message at one of the `development
channels`_, we will pick it up
and fix it so you don't have to follow the whole :ref:`code review process <patch-submission>`.

What tests I should run before committing the code?
---------------------------------------------------

Mostly run `tox` (or `pytest`) to run the unit tests suite. When you will propose a
patch in our forge, the continuous integration factory will trigger a build (using `tox`
as well).

I am getting errors while trying to commit. What is going wrong?
----------------------------------------------------------------

Ensure you followed the proper guide to :ref:`setup your
environment <checkout-source-code>`
and try again. If the error persists, you are welcome to drop us a message at one of the
`development channels`_

Is there a format/guideline for writing commit messages?
--------------------------------------------------------

See the :ref:`git-style-guide`

Is there some recommended git branching strategy?
-------------------------------------------------

It's left at the developer's discretion. Mostly people hack on their feature, then
propose a diff from a git branch or directly from the master branch. There is no
imperative. The only imperative is that for a feature to be packaged and deployed, it
needs to land first in the master branch.

how should I document the code I contribute to SWH?
---------------------------------------------------

Any new feature should include documentation in the form of comments and/or docstrings.
Ideally, they should also be documented in plain English in the repository's `docs/`
folder if relevant to a single package, or in the main `swh-docs` repository if it is a
transversal feature.

.. _faq_api:

Software Heritage API
=====================

How do I generate API usage credentials?
----------------------------------------

See the :ref:`Authentication guide <swh-web-client-auth>`.

Is there a page where I can see all the API endpoints?
------------------------------------------------------

See the :swh_web:`API endpoint listing page <save/>`.

What are the usage limits for SWH APIs?
---------------------------------------

Maximum number of permitted requests per hour:

* 120 for anonymous users
* 1200 for authenticated users

It's described in the :swh_web:`rate limit documentation page <api/#rate-limiting>`.

.. It's temporarily here but it should be moved into its own sphinx instance at some
   point in the future.

.. _faq_sysadm:

System Administration
=====================

How does SWH release?
---------------------

Release is mostly done:
- first in docker (somewhat as part of the development process)
- secondly packaged and deployed on staging (mostly)
- thirdly the same package is deployed on production

Is there a release cycle?
-------------------------

When a functionality is ready (tests ok, landed in master, docker run ok), the module is
tagged. The tag is pushed. This triggers a packaging build process. When the package is
ready, depending on the module [1], sysadms deploy the package with the help of puppet.

[1] swh-web module is mostly automatic. Other modules are not yet automatic as some
internal state migration (dbs) often enters the release cycle and due to the data
volume, that may need human intervention.


.. _bug tracking system: https://forge.softwareheritage.org/
.. _contact form: https://www.softwareheritage.org/contact/
.. _contact us: https://www.softwareheritage.org/contact/
.. _development channels: https://www.softwareheritage.org/community/developers/
.. _internships: https://wiki.softwareheritage.org/wiki/Internships
