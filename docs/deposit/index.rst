.. _swh-docs-deposit:

Deposit
=======

.. toctree::
   :hidden:

   explanations/index
   howto/index
   references/index
   tutorials/index


.. thumbnail:: images/software_life_cycle_en-1024x810.png

The deposit service allows a client (a repository, e.g. HAL) to submit software source archives and its associated metadata to the Software Heritage archive.

Metadata can be also submitted referencing a repository url (origin) or a
:ref:`SWHIDs <persistent-identifiers>`.

Explanations
------------

Read more about the deposit principles and usages.

.. toctree::
   :maxdepth: 1

   explanations/deposit.rst
   explanations/why-metadata.rst


HowTo guides
------------

To assist informed users with their deposits.

.. toctree::
   :maxdepth: 1

   howto/account.rst
   howto/prepare.rst
   howto/deposit-code.rst
   howto/deposit-metadata.rst
   howto/versions.rst
   howto/integrations.rst
   howto/participate.rst


References
----------

Technical documentation and references.

.. toctree::
   :maxdepth: 1

   references/workflow.rst
   references/metadata.rst
   references/examples.rst
   references/api.rst
   references/cli.rst
   references/errors.rst

Tutorials
---------

Practical exercises to make your first deposits.

.. toctree::
   :maxdepth: 1

   tutorials/cli.rst
   tutorials/api.rst

.. only:: deposit_doc

   Indices and tables
   ------------------

   * :ref:`genindex`
   * :ref:`search`