.. _deposit-prepare:

Prepare your metadata and artifacts
===================================

A deposit is constituted of a metadata file and optionally one or more software
artefacts.


The metadata file
-----------------

This is the most important part of a deposit process, it

- holds extrinsic information about a software artefact or another object in the archive
- indicates what

XML
~~~

As we're using the SWORD v2 protocol to handle the deposits the format we used for the
metadata file is XML. Used namespaces:

- `atom <http://www.w3.org/2005/Atom>` (required)
- `Software Heritage deposit <https://www.softwareheritage.org/schema/2018/deposit>`
  (required)
- `CodeMeta <https://doi.org/10.5063/SCHEMA/CODEMETA-2.0>` (recommended)
- `schema <http://schema.org/>` (optional)
-
.. code-block:: xml

   <?xml version="1.0" encoding="utf-8"?>
   <entry xmlns="http://www.w3.org/2005/Atom"
          xmlns:codemeta="https://doi.org/10.5063/SCHEMA/CODEMETA-2.0"
          xmlns:swh="https://www.softwareheritage.org/schema/2018/deposit"
          xmlns:schema="http://schema.org/">
      <!-- metadata -->
   </entry>


swh:deposit
~~~~~~~~~~~

This namespace is specific to our implementation of the SWORD v2 protocol, it's used
to describe what kind of deposit the you are doing:

- a first code deposit for an ``ORIGIN_URL`` not yet archived by SWH
- a new code deposit (i.e. another version of the software) for an existing
  ``ORIGIN_URL``
- a metadata-only deposit for a ``SWHID`` or an ``ORIGIN_URL``

.. tab-set::

  .. tab-item:: Initial code deposit ``create_origin``

    .. code-block:: xml

      <swh:deposit>
         <swh:create_origin>
            <swh:origin url="ORIGIN_URL" />
         </swh:create_origin>
      </swh:deposit>

  .. tab-item:: New version code deposit ``add_to_origin``

    .. code-block:: xml

      <swh:deposit>
         <swh:add_to_origin>
            <swh:origin url="ORIGIN_URL" />
         </swh:add_to_origin>
      </swh:deposit>

  .. tab-item:: Metadata-only deposit ``reference``

    .. code-block:: xml

      <swh:deposit>
         <swh:reference>
            <swh:object swhid="SWHID_CONTEXT" />
            <!-- or -->
            <swh:object swhid="SWHID" />
            <!-- or -->
            <swh:origin url="ORIGIN_URL" />
         </swh:reference>
         <swh:metadata-provenance>
            <schema:url>an optional metadata provenance URL</schema:url>
         </swh:metadata-provenance>
      </swh:deposit>


CodeMeta
~~~~~~~~

We're using `CodeMeta <https://codemeta.github.io/>` terms to describe the metadata.

.. code-block:: xml

   <codemeta:name>A required name</codemeta:name>
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
   <author>
      <name>Margaret Hamilton</name>
      <email>email@example.com</email>
   </author>
   <codemeta:author>
      <codemeta:name>Hedy Lamarr</codemeta:name>
   </codemeta:author>

Please read the :ref:`deposit-metadata` page for a more detailed view on the
semantics and requirements.

Wrapping all the parts together
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here's an example of a full metadata file for a metadata-only deposit:

.. code-block:: xml

   <?xml version="1.0" encoding="utf-8"?>
   <entry xmlns="http://www.w3.org/2005/Atom"
          xmlns:codemeta="https://doi.org/10.5063/SCHEMA/CODEMETA-2.0"
          xmlns:schema="http://schema.org/"
          xmlns:swh="https://www.softwareheritage.org/schema/2018/deposit">
      <id>hal-04083347</id>
      <swh:deposit>
         <swh:reference>
            <swh:object swhid="SWHID_CONTEXT"/>
         </swh:reference>
         <swh:metadata-provenance>
            <schema:url>ORIGIN_URL</schema:url>
         </swh:metadata-provenance>
      </swh:deposit>
      <author>
         <name>HAL</name>
         <email>hal@example.com</email>
      </author>
      <codemeta:name>DGtal release 1.3</codemeta:name>
      <codemeta:description>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus aliquam tincidunt lacus, ut mollis tellus volutpat a. Mauris ut ornare mauris. Suspendisse elementum lacinia erat, at ornare lorem fringilla vel. Aliquam sagittis dictum cursus. Etiam ut porta libero, ut malesuada augue. In viverra felis justo, a ullamcorper sem consectetur sed. Sed in euismod nunc.</codemeta:description>
      <codemeta:dateCreated>2022-11-17</codemeta:dateCreated>
      <codemeta:datePublished>2023-04-27</codemeta:datePublished>
      <codemeta:license>
         <codemeta:name>GNU Lesser General Public License v3.0 or later</codemeta:name>
      </codemeta:license>
      <schema:identifier>
         <codemeta:type>schema:PropertyValue</codemeta:type>
         <schema:propertyID>HAL-ID</schema:propertyID>
         <schema:value>hal-04083347</schema:value>
      </schema:identifier>
      <codemeta:applicationCategory>info.info-cg</codemeta:applicationCategory>
      <codemeta:applicationCategory>info.info-dm</codemeta:applicationCategory>
      <codemeta:applicationCategory>info.info-gr</codemeta:applicationCategory>
      <codemeta:applicationCategory>info.info-ti</codemeta:applicationCategory>
      <codemeta:keywords>digital geometry,image processing,geometry processing</codemeta:keywords>
      <codemeta:codeRepository>https://github.com/DGtal-team/DGtal</codemeta:codeRepository>
      <codemeta:relatedLink>https://dgtal.org</codemeta:relatedLink>
      <codemeta:programmingLanguage>c++</codemeta:programmingLanguage>
      <codemeta:operatingSystem>Linux, Mac OS X, Windows</codemeta:operatingSystem>
      <codemeta:version>1</codemeta:version>
      <codemeta:softwareVersion>1.3</codemeta:softwareVersion>
      <codemeta:dateModified>2023-06-08</codemeta:dateModified>
      <codemeta:developmentStatus>Actif</codemeta:developmentStatus>
      <codemeta:author>
         <codemeta:name>David Coeurjolly</codemeta:name>
         <codemeta:affiliation>Origami</codemeta:affiliation>
      </codemeta:author>
      <codemeta:author>
         <codemeta:name>Jacques-Olivier Lachaud</codemeta:name>
      </codemeta:author>
      <codemeta:author>
         <codemeta:name>Bertrand Kerautret</codemeta:name>
      </codemeta:author>
      <codemeta:author>
         <codemeta:name>J. Miguel Salazar</codemeta:name>
      </codemeta:author>
      <codemeta:author>
         <codemeta:name>Isabelle Sivignon</codemeta:name>
         <codemeta:affiliation>GIPSA-GAIA</codemeta:affiliation>
      </codemeta:author>
      <codemeta:author>
         <codemeta:name>Robin Lamy</codemeta:name>
      </codemeta:author>
      <codemeta:author>
         <codemeta:name>Baptiste Genest</codemeta:name>
      </codemeta:author>
      <codemeta:author>
         <codemeta:name>Phuc Ngo</codemeta:name>
         <codemeta:affiliation>ADAGIO</codemeta:affiliation>
         <codemeta:affiliation>LORIA</codemeta:affiliation>
      </codemeta:author>
      <codemeta:author>
         <codemeta:name>Pablo Hernandez Cerdan</codemeta:name>
      </codemeta:author>
      <codemeta:author>
         <codemeta:name>Jérémy Fix</codemeta:name>
      </codemeta:author>
      <codemeta:contributor>
         <codemeta:name>David Coeurjolly</codemeta:name>
      </codemeta:contributor>
   </entry>


Software artefact
-----------------

.. admonition:: File size limit
   :class: warning

   Our server will reject files larger than 100MB, if your artefact is larger than that
   you will have to split it in multiple files then follow the "multi-step deposit"
   process.

First you'll need to prepare your code artefact by packaging the files in a supported
archive format:

  - zip: common zip archive (no multi-disk zip files).
  - tar: tar archive without compression or optionally any of the
         following compression algorithm gzip (``.tar.gz``, ``.tgz``), bzip2
         (``.tar.bz2``) , or lzma (``.tar.lzma``)

