:html_theme.sidebar_secondary.remove:

.. _swh-docs:

.. rst-class:: landing-part

Welcome to Software Heritage documentation
==========================================

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: Basics
      :link: landing-basics
      :link-type: ref

      .. image:: images/card_basics_undraw_discoverable.svg
         :width: 69%
         :align: center
         :class: sd-mb-2

      Learn about our mission and our source code archive. Find out about how to
      make your first steps with the archive.

      .. button-ref:: landing-basics
         :ref-type: ref
         :color: secondary
         :expand:

         Discover Software Heritage

   .. grid-item-card:: Preserve
      :link: landing-preserve
      :link-type: ref

      .. image:: images/card_preserve_undraw_moving.svg
         :align: center
         :class: sd-mt-1 sd-mb-4

      All the ways that source code may be added or updated in the archive.

      .. button-ref:: landing-preserve
         :ref-type: ref
         :color: secondary
         :expand:

         Archive source code

   .. grid-item-card:: Browse
      :link: landing-browse
      :link-type: ref

      .. image:: images/card_browse_undraw_file_searching.svg
         :width: 49%
         :align: center
         :class: sd-mb-2

      Our vast archive can be searched and accessed in multiple ways. Use it to reference unambiguously any part of a source code to your peers: fragment of code, directory, release, etc.

      .. button-ref:: landing-browse
         :ref-type: ref
         :color: secondary
         :expand:

         Learn how to search the archive

   .. grid-item-card:: Outreach
      :link: landing-outreach
      :link-type: ref

      .. image:: images/card_outreach_undraw_engineering_team.svg
         :width: 99%
         :align: center
         :class: sd-mt-4 sd-mb-4

      Join our network of partners. Collaborate with the team or become an ambassador. Teach others how to use the archive. Get materials for your next events.

      .. button-link:: http://example.com
         :color: secondary
         :expand:

         Tell the world about Software Heritage

   .. grid-item-card:: Interface
      :link: landing-interface
      :link-type: ref

      .. image:: images/card_interface_undraw_futuristic_interface.svg
         :width: 49%
         :align: center
         :class: sd-mb-4

      Develop or research using Software Heritage. Browse, access or import source code programmatically.

      .. button-ref:: landing-interface
         :ref-type: ref
         :color: secondary
         :expand:

         Use Software Heritage in your applications

   .. grid-item-card:: Develop
      :link: landing-contribute
      :link-type: ref

      .. image:: images/card_contribute_undraw_dev_focus.svg
         :width: 80%
         :align: center
         :class: sd-mt-4 sd-mb-4

      Enhance our collection, preservation, and querying processes.

      .. button-ref:: landing-contribute
         :ref-type: ref
         :color: secondary
         :expand:

         Improve the universal archive of source code


-----------------------------------------------------------------------


.. _landing-basics:

.. rst-class:: landing-part

Discover Software Heritage
==========================

.. grid:: 1 2 2 2
   :padding: 0

   .. grid-item::

      Learn about our mission and our source code archive. Find out about how to
      make your first steps with the archive.

   .. grid-item::

      .. image:: images/card_basics_undraw_discoverable.svg
         :align: right

Why an universal software archive?
----------------------------------

-  `A video to get to know Software
   Heritage <https://www.youtube.com/watch?v=8nlSvYh7VpI>`__
-   `Our mission <https://www.softwareheritage.org/mission/>`__
-  `Our approach <https://www.softwareheritage.org/mission/approach/>`__
-  `The content of the archive at a
   glance <https://archive.softwareheritage.org/#swh-coverage-content>`__

Software Heritage in practice
-----------------------------

-  `Take a guided tour of the archive key
   features <https://archive.softwareheritage.org/?guided_tour=0&guided_tour_next=https://archive.softwareheritage.org/>`__
-  `Overview of the main
   features <https://www.softwareheritage.org/features/>`__
-  `Access and reuse the source
   code <https://www.softwareheritage.org/faq/#4_Access_and_Reuse>`__
-  `Good practices for archiving and referencing your
   code <https://www.softwareheritage.org/save-and-reference-research-software/>`__
-  `Get a permanent identifier for your source
   code <https://annex.softwareheritage.org/public/tutorials/getswhid_dir.gif>`__
-  `General FAQ <https://www.softwareheritage.org/faq/>`__
-  :ref:`Glossary <glossary>`


-----------------------------------------------------------------------


.. _landing-preserve:

.. rst-class:: landing-part

Archive source code
===================

.. grid:: 1 2 2 2
   :padding: 0

   .. grid-item::

      There are multiple ways to add or update source code in Software Heritage
      archive. Some of them are automated: our tools crawl multiple software
      development plateforms to archive as many open projects as possible.
      Others require manual procedures.

   .. grid-item::

      .. image:: images/card_preserve_undraw_moving.svg
         :align: right

Before anything…
----------------

-  `Good practices for archiving and referencing your
   code <https://www.softwareheritage.org/howto-archive-and-reference-your-code/>`__

Save a code repository
----------------------

-  “Ready to go” options to save your code :

   -  Seamlessly check if a repository that you are browsing is archived
      and up to date using our `Software Heritage browser
      extensions <https://www.softwareheritage.org/browser-extensions/>`__
   -  `Submit a save request on the Software Heritage
      interface <https://archive.softwareheritage.org/save/>`__

-  Automate the archival:

   -  `Trigger a GitHub action that saves the GitHub
      repository <https://github.com/marketplace/actions/save-to-software-heritage>`__
   -  `Trigger archival of a repository automatically : Bitbucket
      endpoint, GitHub endpoint, GitLab
      endpoint <https://archive.softwareheritage.org/api/1/origin/save/doc/>`__

Save multiple projects at a time, save a forge
----------------------------------------------

Save a forge in 2 steps :

1. `Create an account
   <https://auth.softwareheritage.org/auth/realms/SoftwareHeritage/login-actions/registration>`__
2. `Submit a request of archival for to save a complete forge
   <https://archive.softwareheritage.org/add-forge/request/create/>`__

:ref:`Technical insight on the “Add forge now” process
<save-forge>`

Save code used for science
--------------------------

Save a software using ELife, Ipol, HAL. Your content are directly pushed
into the archive by trusted partners using the deposit service of
Software Heritage:

-  `Deposit software using the HAL
   portal <https://www.softwareheritage.org/2018/09/28/depositing-scientific-software-into-software-heritage/>`__
-  `Video tutorial on source code deposit using
   Hal <https://www.youtube.com/watch?v=-Ggn98sR3Eg&list=PLD2VqrZz2-u3bOWtoCoBIh5Flt6iYXsq3>`__

Save legacy source code
-----------------------

Recovering and curating landmark legacy source code : `how to save
legacy code <https://www.softwareheritage.org/swhap/>`__


------------------------------------------------------------------------


.. _landing-browse:

.. rst-class:: landing-part

Search, browse and reference
============================

.. grid:: 1 2 2 2
   :padding: 0

   .. grid-item::

      Search and access the archive, or use it to reference unambiguously any
      part of a source code.

   .. grid-item::

      .. image:: images/card_browse_undraw_file_searching.svg
         :width: 50%
         :align: right

-  `Take the guided tour of the archive web
   interface <https://archive.softwareheritage.org/?guided_tour=0&guided_tour_next=https://archive.softwareheritage.org/>`__
-  `Good practices for archiving and referencing your
   code <https://www.softwareheritage.org/howto-archive-and-reference-your-code/>`__
-  `Make your code identifiable : get a PID for your source
   code <https://annex.softwareheritage.org/public/tutorials/getswhid_dir.gif>`__
-  `Choosing what type of Software Heritage Identifier (SWHID) to
   use <devel/swh-model/persistent-identifiers.html#choosing-what-type-of-swhid-to-use>`__
-  `Navigating through Software Heritage: behind the
   scenes <https://www.softwareheritage.org/2019/05/28/mining-software-metadata-for-80-m-projects-and-even-more/>`__

Need help? Want to make a proposal? Ask the community using the `users mailing-list <https://sympa.inria.fr/sympa/info/swh-users>`__


------------------------------------------------------------------------


.. _landing-outreach:

.. rst-class:: landing-part

Tell the world
==============

.. grid:: 1 2 2 2
   :padding: 0

   .. grid-item::

      Wherever you have a technical background or not, help us spread the word
      about Software Heritage. Encourage developers to archive their source
      code. Find researchers and practitioners interested in using an immense
      collection of source code.

   .. grid-item::

      .. image:: images/card_outreach_undraw_engineering_team.svg
         :align: right

Ambassador program
------------------

-  `Become an ambassador <https://www.softwareheritage.org/ambassadors/>`__

-  `Ambassadors mailing list <https://sympa.inria.fr/sympa/info/swh-ambassadors>`__
-  `Outreach material (only available to ambassadors) <https://www.softwareheritage.org/ambassador-material/>`__
-  `Outreach material on a Git repository <https://github.com/moranegg/swh-ambassadors/tree/main/Materials>`__

Presentations
-------------

-  `Archive of presentation
   slides <https://annex.softwareheritage.org/public/talks/>`__


------------------------------------------------------------------------


.. _landing-interface:

.. rst-class:: landing-part

Use in your applications
========================

.. grid:: 1 2 2 2
   :padding: 0

   .. grid-item::

      Interact with our source code archive from your applications or research projects.

   .. grid-item::

      .. image:: images/card_interface_undraw_futuristic_interface.svg
         :align: right

Browse API
----------

-  `Terms of use for Software Heritage
   API <https://www.softwareheritage.org/aspects-juridiques/software-heritage-api-terms-of-use/>`__
-  `Web API <https://archive.softwareheritage.org/api/>`__. Access the
   API overview or discover the full `endpoints
   index <https://archive.softwareheritage.org/api/1/>`__

Data model and identifiers
--------------------------

-  `Our data
   model <devel/swh-model/data-model.html#data-model>`__
-  :ref:`Software Heritage IDentifiers
   (SWHID) <persistent-identifiers>` specifications
-  Compute a SWHID locally using the `swh identify <devel/swh-model/cli.html>`__ command-line tool.

Deposit API
-----------

-  :ref:`Import source code programmatically <deposit-user-manual>`


------------------------------------------------------------------------


.. _landing-contribute:

.. rst-class:: landing-part

Improve the universal archive
=============================

.. grid:: 1 2 2 2
   :padding: 0

   .. grid-item::

      There are many ways to help Software Heritage. However small or large,
      contributions are welcome and very much appreciated.

   .. grid-item::

      .. image:: images/card_contribute_undraw_dev_focus.svg
         :align: right

-  :ref:`Our
   roadmap <roadmap-current>`
-  :ref:`Developer documentation <swh-docs-devel>`. Where
   you will find developer-oriented documentation to understand the SWH
   environment.
-  `Get started <devel/getting-started>`__

Contributing development skills:

-  :ref:`Software architecture overview <architecture-overview>`
-  `Developers portal <https://www.softwareheritage.org/community/developers/>`__
-  `Development
   mailing-list <https://sympa.inria.fr/sympa/info/swh-devel>`__. Join
   the community
-  :ref:`Development FAQ <faq>`

Contributing resources and infrastructure:

-  :ref:`Mirror operations <mirror_operations>`



------------------------------------------------------------------------

..
   The following is needed to define the “toctree” that
   Sphinx will use to create the navigation structure.


Table of contents
=================

.. toctree::
   :maxdepth: 2

   devel/index
   devel/api-reference
   user/index
   sysadm/index
