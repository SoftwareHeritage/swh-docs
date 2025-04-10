Prepare your metadata and artifacts
===================================

.. admonition:: Protocol reference
   :class: note

   This page will help you prepare a deposit without getting into too much details,
   a :doc:`complete reference of the deposit protocol <../references/protocol>`
   is also available to explain all the technical specifications.

A deposit is constituted of a metadata file and optionally one or more software
artefacts.

The metadata file
-----------------

This is the most important part of a deposit process, see
:doc:`../explanations/why-metadata`.

Here's a complete metadata file example for a metadata-only deposit on ``ORIGIN_URL``:

.. code-block:: xml

   <?xml version="1.0" encoding="utf-8"?>

   <!-- XML Entry -->
   <entry xmlns="http://www.w3.org/2005/Atom"
          xmlns:codemeta="https://doi.org/10.5063/schema/codemeta-2.0"
          xmlns:swh="https://www.softwareheritage.org/schema/2018/deposit">

      <!-- SWH deposit's own properties -->
      <swh:deposit>
         <swh:reference>
            <swh:object swhid="SWHID_CONTEXT"/>
         </swh:reference>

         <!-- Metadata provenance -->
         <swh:metadata-provenance>
            <schema:url>METADATA_URL</schema:url>
         </swh:metadata-provenance>
      </swh:deposit>

      <!-- CodeMeta metadata -->
      <codemeta:name>A required software name</codemeta:name>
      <codemeta:description>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus aliquam tincidunt lacus, ut mollis tellus volutpat a. Mauris ut ornare mauris. Suspendisse elementum lacinia erat, at ornare lorem fringilla vel. Aliquam sagittis dictum cursus. Etiam ut porta libero, ut malesuada augue. In viverra felis justo, a ullamcorper sem consectetur sed. Sed in euismod nunc.</codemeta:description>
      <codemeta:dateCreated>2022-11-17</codemeta:dateCreated>
      <codemeta:datePublished>2023-04-27</codemeta:datePublished>
      <codemeta:license>
         <codemeta:name>GNU Affero General Public License</codemeta:name>
      </codemeta:license>
      <codemeta:keywords>digital geometry,image processing,geometry processing</codemeta:keywords>
      <codemeta:relatedLink>https://example.com</codemeta:relatedLink>
      <codemeta:programmingLanguage>c++</codemeta:programmingLanguage>
      <codemeta:operatingSystem>Linux, Mac OS X, Windows</codemeta:operatingSystem>
      <codemeta:license>
         <codemeta:name>GNU Affero General Public License</codemeta:name>
      </codemeta:license>
      <codemeta:author>
         <codemeta:name>Hedy Lamarr</codemeta:name>
         <codemeta:email>email@example.com</codemeta:email>
      </codemeta:author>

      <!-- Versioning info -->
      <codemeta:version>1.0.0</codemeta:version>
   </entry>

This file can be a bit daunting, let's examine its content in detail.

XML Entry
~~~~~~~~~

.. admonition:: CodeMeta versions
   :class: warning

   For now, the repository server is only compatible with CodeMeta v2, we will soon move to v3 which will become the recommended version.

As we're using the SWORD v2 standard to handle the deposits the format we used for the
metadata file is XML. Used namespaces:

- `atom <http://www.w3.org/2005/Atom>`_ (required)
- `Software Heritage deposit <https://www.softwareheritage.org/schema/2018/deposit>`_
  (required)
- `CodeMeta v2 <https://doi.org/10.5063/schema/codemeta-2.0>`_ (recommended)
- `schema <http://schema.org/>`_ (optional)

.. code-block:: xml

   <?xml version="1.0" encoding="utf-8"?>
   <entry xmlns="http://www.w3.org/2005/Atom"
          xmlns:codemeta="https://doi.org/10.5063/schema/codemeta-2.0"
          xmlns:swh="https://www.softwareheritage.org/schema/2018/deposit">
      <!-- metadata -->
   </entry>

SWH deposit's own properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This namespace is specific to our implementation of the SWORD v2 protocol, it's used
to describe what *kind* of deposit the you are doing:

.. tab-set::

  .. tab-item:: Initial deposit

   This is the first time you're making a code deposit for ``ORIGIN_URL``.

    .. code-block:: xml

      <swh:deposit>
         <swh:create_origin>
            <swh:origin url="ORIGIN_URL" />
         </swh:create_origin>
      </swh:deposit>

  .. tab-item:: New version deposit

   You already made a code deposit for ``ORIGIN_URL`` and you want to send a new
   version.

    .. code-block:: xml

      <swh:deposit>
         <swh:add_to_origin>
            <swh:origin url="ORIGIN_URL" />
         </swh:add_to_origin>
      </swh:deposit>

  .. tab-item:: Metadata-only deposit

   You don't have a software artefact to send, only metadata related to a ``SWHID`` or
   an ``ORIGIN_URL``.

    .. code-block:: xml

      <swh:deposit>
         <swh:reference>
            <swh:object swhid="SWHID_CONTEXT" />
            <!-- or -->
            <swh:object swhid="SWHID" />
            <!-- or -->
            <swh:origin url="ORIGIN_URL" />
         </swh:reference>

         <!-- Metadata provenance -->
         <swh:metadata-provenance>
            <schema:url>METADATA_URL</schema:url>
         </swh:metadata-provenance>
      </swh:deposit>

CodeMeta
~~~~~~~~

We're using `CodeMeta <https://codemeta.github.io/>`_ terms to describe the metadata.
For example:

.. code-block:: xml

   <codemeta:name>A required software name</codemeta:name>
   <codemeta:url>ORIGIN_URL</codemeta:url>
   <codemeta:applicationCategory>test</codemeta:applicationCategory>
   <codemeta:keywords>Some keywords, separated, by, commas</codemeta:keywords>
   <codemeta:description>An optional description.</codemeta:description>
   <codemeta:version>1.12</codemeta:version>
   <codemeta:developmentStatus>stable</codemeta:developmentStatus>
   <codemeta:programmingLanguage>ocaml</codemeta:programmingLanguage>
   <codemeta:license>
      <codemeta:name>GNU Affero General Public License</codemeta:name>
   </codemeta:license>
   <codemeta:author>
      <codemeta:name>Hedy Lamarr</codemeta:name>
      <codemeta:email>email@example.com</codemeta:email>
   </codemeta:author>

.. list-table:: Required fields
   :header-rows: 1

   * - Name
     - Description
   * - codemeta:name
     - The name of this software
   * - codemeta:author
     - The author(s) of this software


.. list-table:: Recommended fields
   :header-rows: 1

   * - Name
     - Description
   * - codemeta:version
     - The version of the software, used to differentiate multiple deposits of a same
       ``ORIGIN_URL``, see versioning below
   * - codemeta:description
     - Short or long description of the software
   * - codemeta:license
     - The license(s) of the software

See the `full CodeMeta terms list <https://codemeta.github.io/terms/>`_ for a complete
reference of the available properties.

Versioning
~~~~~~~~~~

The ``codemeta:version`` property is used to differentiate multiple deposits of a same
``ORIGIN_URL``. Use cases:

- the software has been updated, you want a make a new deposit of it, you need to
  increment the ``codemeta:version`` property (if the property is missing we will
  use a version number reflecting the number of deposits made for this origin)
- a mistake was made in a previous deposit, you can use make a new one using the same
  ``codemeta:version`` value. The new snapshot will only contain the latest deposit
  with this version number

Here is `a snapshot view a an origin`_ listing all distinct versions deposited by HAL
for the origin ``https://hal.archives-ouvertes.fr/hal-04088473``

.. _a snapshot view a an origin: https://archive.softwareheritage.org/browse/snapshot/f4680770f994ab60a835844168c8b68ee24ac0b8/releases/?origin_url=https://hal.archives-ouvertes.fr/hal-04088473&snapshot=f4680770f994ab60a835844168c8b68ee24ac0b8

Please note that using the same ``codemeta:version`` value for multiple deposits will
not delete the previous one(s) from the archive: they will still be accessible using
their SWHID, but they will not appear in the future snapshots.

Metadata provenance
~~~~~~~~~~~~~~~~~~~

To indicate where the metadata is coming from, deposit clients can use a
``<swhdeposit:metadata-provenance>`` element in ``<swhdeposit:deposit>`` whose content
is the object the metadata is coming from.

For example, when the metadata is coming from Wikidata, then the
provenance should be the page of a
`Q-entity <https://www.wikidata.org/wiki/Wikidata:Identifiers>`_ or when the
metadata is coming from a curated repository like HAL, then it should be the HAL
project.

For example, to deposit metadata on `GNU Hello <https://archive.softwareheritage.org/browse/origin/directory/?origin_url=https://ftp.gnu.org/gnu/hello/>`_:

.. code:: xml

   <swh:deposit>
      <swh:metadata-provenance>
         <schema:url>https://www.wikidata.org/wiki/Q16988498</schema:url>
      </swh:metadata-provenance>
   </swh:deposit>

Software artefact
-----------------

Now that your metadata file is ready you'll need to prepare your code artefact by
packaging the files in a supported archive format:

- ``zip``: common zip archive (no multi-disk zip files).
- ``tar``: tar archive without compression or compressed using ``gzip``, ``bzip2`` or
  ``lzma``

Our server will reject files larger than 100MB, so if your artefact is larger than that
you will have to split it in multiple files and follow the multi-step deposit process.

Tools
-----

To use the deposit services you will need to make API calls or use our command line
interface (CLI):

- software used to make API calls: `curl <https://curl.se/>`_,
  `httpie <https://httpie.io/>`_, etc.
- `swh-deposit <https://pypi.org/project/swh.deposit/>`_ CLI: ``pip install swh-deposit``

Next step
---------

You are now ready to make your first deposit!

- You have a single artefact to upload, then follow :doc:`first deposit <first-deposit>`
- Your artefacts were too large for a simple deposit, then go to
  :doc:`make a multi-step deposit <multistep-deposit>`
- You only have metadata to deposit then head to
  :doc:`metadata-only deposit <metadata-deposit>`