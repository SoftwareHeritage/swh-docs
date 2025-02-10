Citation workflow and architecture
==================================

Quick reminder on metadata objects
----------------------------------

Metadata in *Software Heritage* is explained in detail in the document :ref:`Metadata workflow and
architecture <architecture-metadata>`. There are two types of metadata that are useful for citation, intrinsic and extrinsic. These two types can come from two
sources: the archive itself (raw metadata) and the
indexer (indexed metadata).

For each metadata type and metadata source, metadata can be extracted for a specific
object (``snapshot``, ``release``, ``revision``, ``directory``,
``content``), using its SWHID, or using the repository URL (``origin``).
In the latter case, it will return the metadata for the latest version
(latest visit snapshot) of the repository root directory on the main
branch.

Citation use cases
------------------

.. list-table:: Citation use cases
    :header-rows: 1
    :stub-columns: 1

    * - ID
      - As a
      - I can
      - so that
    * - UC1 (v1, v2)
      - Researcher
      - retrieve a citation or BibTeX export for a software artifact directly on SWH interface
      - the software will be cited with correct attribution
    * - UC2 (v1, v2)
      - Publisher (Episciences)
      - retrieve a citation or BibTeX export for a software artifact programmatically
      - expose BibTeX
    * - UC3
      - Aggregator (OpenAire)
      - retrieve intrinsic metadata from SWH programmatically
      - the software record will be enriched

Citation v1: data flow
----------------------

In this version, *Software Heritage* can generate a citation in BibTeX
format from the raw intrinsic metadata available in the archive. The raw
intrinsic metadata used for citation will be a found ``codemeta.json``
file or, alternatively, a found ``citation.cff`` file in the repository.

As per metadata extraction:

* When given an ``origin`` URL, the citation will be generated from the latest version of the repository root directory metadata on the main branch.
* When given a SWHID object of type ``snapshot``, ``release`` or ``revision``, the citation will be generated from the repository root directory metadata, associated with that version.
* When given a ``directory`` object, if the SWHID is qualified with an anchor (explained in the document :ref:`SoftWare Heritage persistent IDentifiers (SWHIDs) <persistent-identifiers>`, the citation will be generated from the repository root directory metadata, associated with the anchor version.

.. warning::
    However, if no anchor was specified, it will be generated directly from the metadata found in that directory.

* When given a ``content`` object, if the SWHID is qualified with an anchor, the citation will be generated from metadata of the repository root directory. If no anchor was specified, the citation cannot be generated due to a lack of information.

Citation v1: architecture
-------------------------

*Software Heritage* provides a web API (through :ref:`swh.web <swh-web>`) to generate
a citation, given an ``origin`` URL or a qualified SWHID.

The corresponding API endpoints are:

* ``/api/1/raw-intrinsic-metadata/citation/origin/`` (example: ``/api/1/raw-intrinsic-metadata/citation/origin/?citation_format=bibtex&origin_url=https://github.com/rdicosmo/parmap``)
* ``/api/1/raw-intrinsic-metadata/citation/swhid/SWHID/`` (example: ``/api/1/raw-intrinsic-metadata/citation/swhid/?citation_format=bibtex&target_swhid=swh:1:dir:2dc0f462d191524530f5612d2935851505af41dd;origin=https://github.com/rdicosmo/parmap;visit=swh:1:snp:2128ed4f25f2d7ae7c8b7950a611d69cf4429063/``)

Currently, the only allowed citation format value is BibTeX
(``citation_format=bibtex``).

This API uses intermediate utility methods:

* in :ref:`swh.web <swh-web>`, to retrieve raw intrinsic metadata, given an ``origin`` URL or a qualified SWHID, which return original ``codemeta.json`` and ``citation.cff`` files.
* in :ref:`swh.indexer <swh-indexer>`, to convert a ``codemeta.json`` or a ``citation.cff`` file into a BibTeX citation.

Codemeta/citation.cff to BibTeX mapping
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A ``citation.cff`` file will be first converted into a ``codemeta.json``
document. The ``CFF`` to ``CodeMeta`` mapping can be found in the
`codemeta
repository <https://github.com/codemeta/codemeta/blob/master/crosswalks/Citation%20File%20Format%201.2.0.csv>`_.

The ``CodeMeta`` to ``BibTeX`` mapping, used for the converter, is
`currently under
review <https://github.com/codemeta/codemeta/pull/363>`_.

Note on BibTeX ``@software``, ``@softwareversion`` and ``@codefragment`` usage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The generated BibTeX citation can be of type ``@software``,
``@softwareversion`` or ``@codefragment``. The rule is the following:

* If SWHID is not specified,

  * And if version is specified, then it will be ``@softwareversion``.
  * Otherwise, it will be ``@software``.

* If SWHID is specified

  * And is of type ``snapshot``, then it will be ``@software``.
  * And is of type ``release``, ``revision`` or ``directory``, then it will be ``@softwareversion``.
  * And is of type ``content``, then it will be ``@codefragment``.

A generated BibTeX example
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bibtex

   @software{REPLACEME,
       author = "Di Cosmo, Roberto and Danelutto, Marco",
       organization = "Inria and University Paris Diderot and University of Pisa",
       license = "LGPL-2.0-only",
       date = "2011-07-18",
       year = "2011",
       month = "07",
       repository = "git+https://github.com/rdicosmo/parmap.git",
       title = "Parmap",
       swhid = "swh:1:snp:01b2cc89f4c423f1bda4757edd86ae4013b919b0;origin=https://github.com/rdicosmo/parmap"
   }

Citation v1: UI
---------------

Citation should be available in the webapp through a new *Citation* tab
under the *Permalinks* tab, that should open the *Permalinks/Citation*
box.

Future
------

In the current v1 version, citation is generated from raw intrinsic metadata, i.e. ``codemeta.json`` or ``citation.cff`` file.

.. mermaid::

    quadrantChart
        title Metadata types and sources for citation generation
        x-axis Raw --> Indexed
        y-axis Extrinsic --> Intrinsic
        codemeta.json: [0.25, 0.9]
        citation.cff: [0.25, 0.75]

*Metadata types and sources for citation generation v1*

The next versions of the citation feature should include:

* New supported citation formats.
* Citation styles?
* On the API/backend side:

  * v2: Generating citations from indexed intrinsic and extrinsic metadata (merging behaviour to be defined).
  * v3: Authorities.
