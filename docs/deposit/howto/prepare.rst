Prepare your metadata and artifacts
===================================



Metadata with archives
----------------------

* compress the files in a supported archive format:

  - zip: common zip archive (no multi-disk zip files).
  - tar: tar archive without compression or optionally any of the
         following compression algorithm gzip (``.tar.gz``, ``.tgz``), bzip2
         (``.tar.bz2``) , or lzma (``.tar.lzma``)


Then you need to prepare a metadata file allowing you to give detailed
information on your deposited source code. A rather minimal Atom with Codemeta
file could be:

.. code-block:: xml

   <?xml version="1.0" encoding="utf-8"?>
   <entry xmlns="http://www.w3.org/2005/Atom"
          xmlns:codemeta="https://doi.org/10.5063/SCHEMA/CODEMETA-2.0"
          xmlns:swh="https://www.softwareheritage.org/schema/2018/deposit">
     <title>Verifiable online voting system</title>
     <id>belenios-01243065</id>
     <codemeta:url>https://gitlab.inria.fr/belenios/belenios</codemeta:url>
     <codemeta:applicationCategory>test</codemeta:applicationCategory>
     <codemeta:keywords>Online voting</codemeta:keywords>
     <codemeta:description>Verifiable online voting system</codemeta:description>
     <codemeta:version>1.12</codemeta:version>
     <codemeta:runtimePlatform>opam</codemeta:runtimePlatform>
     <codemeta:developmentStatus>stable</codemeta:developmentStatus>
     <codemeta:programmingLanguage>ocaml</codemeta:programmingLanguage>
     <codemeta:license>
       <codemeta:name>GNU Affero General Public License</codemeta:name>
     </codemeta:license>
     <author>
       <name>Belenios</name>
       <email>belenios@example.com</email>
     </author>
     <codemeta:author>
       <codemeta:name>Belenios Test User</codemeta:name>
     </codemeta:author>
     <swh:deposit>
       <swh:create_origin>
         <swh:origin url="http://has.archives-ouvertes.fr/test-01243065" />
       </swh:create_origin>
     </swh:deposit>
   </entry>

Please read the :ref:`deposit-metadata` page for a more detailed view on the
metadata file formats and semantics; and :ref:`deposit-create_origin` for
a description of the ``<swh:create_origin>`` tag.

Metadata only
-------------

Note: use reference instead of origin

.. code-block:: xml

   <?xml version="1.0" encoding="utf-8"?>
   <entry xmlns="http://www.w3.org/2005/Atom" xmlns:codemeta="https://doi.org/10.5063/SCHEMA/CODEMETA-2.0" xmlns:schema="http://schema.org/" xmlns:swh="https://www.softwareheritage.org/schema/2018/deposit">
      <id>hal-04083347</id>
      <swh:deposit>
         <swh:reference>
            <swh:object swhid="swh:1:dir:8c89b341b6b560b3ecf360320e2ed80ad4c86e75;origin=https://github.com/DGtal-team/DGtal;visit=swh:1:snp:f80492b7a4f99939464109fe6c7477b239a9759d;anchor=swh:1:rev:2320dba603919c2ee7be6a9cf8af514273ecd7e4"/>
         </swh:reference>
         <swh:metadata-provenance>
            <schema:url>https://hal.archives-ouvertes.fr/hal-04083347</schema:url>
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