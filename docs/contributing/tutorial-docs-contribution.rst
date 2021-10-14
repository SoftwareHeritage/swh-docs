.. _doc-contribution:

Tutorial: Best practices when writing SWH docs
==============================================

.. admonition:: Intended audience
   :class: important

   Members of the Software Heritage staff and external contributors
   who wish to contribute by writing documentation.
   
A tutorial on how to contribute documentation into the Software Heritage world.

Step 1: Identify your audience
------------------------------

#. Ask yourself: Who are the readers of the documentation that you are writing?

   In the Software Heritage community, three general types of personas are
   distinguished:

    * **visitors**: people who want to know what is the SWH initiative and archive
    * **users**: people who want to use the SWH features

       * as a service
       * as a module by running a local instance

    * **contributors**: people who are contributing to SWH (either external or swh
      staff)

       * as developers
       * as sys-admins
       * as support role

#. use the persona type to determine the document location in step 2

#. add the intended audience on the top of the page

Step 2: Determine the documentation location
--------------------------------------------

Information should have a permanent home as documentation. Elements that are work in
progress can live in the forge on issues or in hedgedoc, but these are not permanent
locations.

#. Choose high-level location:

Possible permanent locations include:

* The WordPress website: for visitors

* The archive web-app: for visitors and users (of the interface or API)

* The Sphinx docs:

  * *devel* for contributors
  * *users* for users of the infrastructure and all the different services
  * *sysadm* for sys-admins

#. For contributors documentation in devel:

   #. Choose if the subject is a high level (cross-module) section or in a specific
      module

      * if the document is relative to only one module, go and add it in the */docs*
        directory in the module

      * for cross-module documentation, use the swh-docs repository and the appropriate
        sub-directory (e.g architecture)

   #. Decide if a subsection is needed with multiple pages (tutorials, how-tos,
      reference or explanation).

#. For sys-admin (in */sysadm* folder) and user documentation (in */users* folder):

    #. Check if an existing section is already describing the theme that you want to
       document.
    #. Decide if a subsection is needed with multiple pages (tutorials, how-tos,
       reference or explanation).

Step 3: Choose documentation type
---------------------------------

We are following Divio's approach with four major types of documentation:

* Tutorial: allowing newcomers to get started and ease the onboarding contributors and
  users.

* How to: how to solve a specific problem in a step-by-step practical manual.

* Reference: theoretical/technical knowledge which is information oriented.

* Explanation: theoretical knowledge understanding-oriented to analyze, discuss and
  explain different decisions, including background and context.


For more information see `the divio documentation <https://documentation.divio.com/>`_
and/or `Daniele Procida's presentation <https://www.youtube.com/watch?v=t4vKPhjcMZg>`_

.. note::
    We propose using in the following naming scheme depending on the type of document:
        * Tutorial: Tutorial name]
        * How to ...
        * Reference: [Reference name]
        * Explanation: [Explanation name]


Step 4: Create a page or sub-section with multiple pages
--------------------------------------------------------

#. Create a *.rst* file with a short name of your doc in the appropriate directory (see
   step 2). If this is a sub-section, the first file should be an *index.rst* file
   containing the list of the current sub-section files.

#. For not yet ready page, you can create simply create an empty page using the template
   below. The template starts with a reference, so that you can link to this new page
   from elsewhere. The page name should follow the step 3. scheme.

#. For existing page, you can link the new page with the existing one containing the
   desired information.

Empty page template
^^^^^^^^^^^^^^^^^^^

.. code-block:: rst

   .. _empty_page:

   Empty page
   ==========

   .. admonition:: Intended audience
      :class: important

      add the audience target(s) of this page
   
   .. todo::
      This page is a work in progress. For now, please refer to the `existing documentation <https://...>`_.

Empty subsection template
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: rst

   .. _empty_subsection:

   Empty subsection
   ================

   .. toctree::
      :titlesonly:

      tutorial-my-first-tuto
      howto-do-things
      howto-test-stuff
      howto-dance
      reference-info
      reference-best-practices

README in module
^^^^^^^^^^^^^^^^

We want to reduce redundancy in documentation as much as possible. The option we should
strive for is adding a symlink to docs/README.rst in the repo's module. Furthermore,
docs/README.rst should include docs/index.rst, as following:

.. code-block:: rst

   .. _swh-fuse:

   .. include:: README.rst

   .. toctree::
      :maxdepth: 1
      :caption: Overview

      cli
      configuration
      Design notes <design>
      Tutorial <tutorial>


Step 5: Add link to page/sub-section from an index.rst
------------------------------------------------------

Add the file-name to the menu of the parent index.rst

Step 6: Commit change for code review
-------------------------------------

You should open a diff for a documentation change following the instructions in
:ref:`code-review`
