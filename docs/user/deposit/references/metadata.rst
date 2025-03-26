.. _deposit-metadata-reference:

Metadata reference
==================

Format
------

While the SWORDv2 specification recommends the use of DublinCore_,
we prefer the CodeMeta_ vocabulary, as we already use it in other components
of Software Heritage.

While CodeMeta is designed for use in JSON-LD, it is easy to reuse its vocabulary
and embed it in an XML document, in three steps:

1. use the `JSON-LD compact representation`_ of the CodeMeta document with
   ``@context: "https://doi.org/10.5063/SCHEMA/CODEMETA-2.0"`` and no other context;
   which implies that:

   1. Codemeta properties (whether in the ``https://codemeta.github.io/terms/``
      or ``http://schema.org/`` namespaces) are unprefixed terms
   2. other properties in the ``http://schema.org/`` namespace use `compact IRIs`_
      with the ``schema`` prefix
   3. other properties are absolute
2. replace ``@context`` declarations with a XMLNS declaration with
   ``https://doi.org/10.5063/SCHEMA/CODEMETA-2.0`` as namespace
   (eg. ``xmlns="https://doi.org/10.5063/SCHEMA/CODEMETA-2.0"``
   or ``xmlns:codemeta="https://doi.org/10.5063/SCHEMA/CODEMETA-2.0"``)
3. if using a non-default namespace, apply its prefix to any unprefixed term
   (ie. any term defined in https://doi.org/10.5063/SCHEMA/CODEMETA-2.0 )
4. add XMLNS declarations for any other prefix (eg. ``xmlns:schema="http://schema.org/"``
   if any property in that namespace is used)
5. unfold JSON lists to sibling XML subtrees


Example Codemeta document
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: json

   {
      "@context": "https://doi.org/10.5063/SCHEMA/CODEMETA-2.0",
      "name": "My Software",
      "author": [
         {
            "name": "Author 1",
            "email": "foo@example.org"
         },
         {
            "name": "Author 2"
         }
      ]
   }

becomes this XML document:

.. code:: xml

   <?xml version="1.0"?>
   <atom:entry xmlns:atom="http://www.w3.org/2005/Atom"
               xmlns="https://doi.org/10.5063/SCHEMA/CODEMETA-2.0">
     <name>My Software</name>
     <author>
       <name>Author 1</name>
       <email>foo@example.org</email>
     </author>
     <author>
       <name>Author 2</name>
     </author>
   </atom:entry>

Or, equivalently:

.. code:: xml

   <?xml version="1.0"?>
   <entry xmlns="http://www.w3.org/2005/Atom"
          xmlns:codemeta="https://doi.org/10.5063/SCHEMA/CODEMETA-2.0">
     <codemeta:name>My Software</codemeta:name>
     <codemeta:author>
       <codemeta:name>Author 1</codemeta:name>
       <codemeta:email>foo@example.org</codemeta:email>
     </codemeta:author>
     <codemeta:author>
       <codemeta:name>Author 2</codemeta:name>
     </codemeta:author>
   </entry>


Note that in both these examples, ``codemeta:name`` is used even though
the property is actually ``http://schema.org/name``.

swh:deposit
~~~~~~~~~~~

This namespace is specific to our implementation of the SWORD v2 protocol, it's used
to describe what kind of deposit the you are doing.

A first code deposit for an ``ORIGIN_URL`` not yet archived by SWH using
``<swh:create_origin>``:

.. code-block:: xml

   <swh:deposit>
      <swh:create_origin>
         <swh:origin url="ORIGIN_URL" />
      </swh:create_origin>
   </swh:deposit>

A new code deposit (i.e. another version of the software) for an existing
``ORIGIN_URL``:

.. code-block:: xml

   <swh:deposit>
      <swh:add_to_origin>
         <swh:origin url="ORIGIN_URL" />
      </swh:add_to_origin>
   </swh:deposit>

A metadata-only deposit for a ``SWHID`` or an ``ORIGIN_URL`` using ``<swh:reference>``:

.. code-block:: xml

   <swh:deposit>
      <swh:reference>
         <swh:object swhid="SWHID_CONTEXT" />
         <!-- or -->
         <swh:object swhid="SWHID" />
         <!-- or -->
         <swh:origin url="ORIGIN_URL" />
      </swh:reference>
   </swh:deposit>

To indicate where the metadata is coming from, deposit clients can use a
``<swhdeposit:metadata-provenance>`` element in ``<swhdeposit:deposit>`` whose content
is the object the metadata is coming from, preferably using the ``http://schema.org/``
namespace.

For example, when the metadata is coming from Wikidata, then the
``<swhdeposit:metadata-provenance>`` should be the page of a Q-entity, such as
``https://www.wikidata.org/wiki/Q16988498`` (not the Q-entity
``http://www.wikidata.org/entity/Q16988498`` itself, as the Q-entity **is** the
object described in the metadata)
Or when the metadata is coming from a curated repository like HAL, then
``<swhdeposit:metadata-provenance>`` should be the HAL project.

In particular, Software Heritage expects the ``<swhdeposit:metadata-provenance>`` object
to have a ``http://schema.org/url`` property, so that it can appropriately link
to the original page.

For example, to deposit metadata on GNU Hello:

.. code:: xml

   <?xml version="1.0"?>
   <entry xmlns="http://www.w3.org/2005/Atom"
          xmlns:schema="http://schema.org/">

     <!-- ... -->

     <swh:deposit>
       <swh:metadata-provenance>
         <schema:url>https://www.wikidata.org/wiki/Q16988498</schema:url>
       </swh:metadata-provenance>
     </swh:deposit>

     <!-- ... -->

   </entry>

Here is a more complete example of a metadata-only deposit on version 2.9 of GNU Hello,
to show the interaction with other fields,

.. code:: xml

   <?xml version="1.0"?>
   <entry xmlns="http://www.w3.org/2005/Atom"
          xmlns:swh="https://www.softwareheritage.org/schema/2018/deposit"
          xmlns:schema="http://schema.org/"
          xmlns:codemeta="https://doi.org/10.5063/SCHEMA/CODEMETA-2.0">

     <swh:deposit>
       <swh:reference>
         <swh:object swhid="swh:1:dir:9b6f93b12a500f560796c8dffa383c7f4470a12f;origin=https://ftp.gnu.org/gnu/hello/;visit=swh:1:snp:1abd6aa1901ba0aa7f5b7db059250230957f8434;anchor=swh:1:rev:3d41fbdb693ba46fdebe098782be4867038503e2" />
       </swh:reference>

       <swh:metadata-provenance>
         <schema:url>https://www.wikidata.org/wiki/Q16988498</schema:url>
       </swh:metadata-provenance>
     </swh:deposit>

     <codemeta:name>GNU Hello</codemeta:name>
     <codemeta:id>http://www.wikidata.org/entity/Q16988498</codemeta:id>
     <codemeta:url>https://www.gnu.org/software/hello/</codemeta:url>

     <!-- is part of the GNU project -->
     <codemeta:isPartOf>http://www.wikidata.org/entity/Q7598</codemeta:isPartOf>

   </entry>

Properties
----------

Recognized properties for CodeMeta ``SoftwareSourceCode`` and ``SoftwareApplication``
includes the following terms from https://schema.org. These terms are part of the
CodeMeta specification and can be used without any prefix, we are keeping the prefix
here for clarity.

.. list-table:: Required fields
   :header-rows: 1

   * - Name
     - Description
   * - codemeta:name
     - The name of this software (possible alternative: ``atom:title``)
   * - codemeta:author
     - The author(s) of this software (possible alternative: ``atom:author``)


.. list-table:: Recommended fields
   :header-rows: 1

   * - Name
     - Description
   * - codemeta:version
     - The version of the software, used to differentiate multiple deposits of a same
       ``ORIGIN_URL``
   * - codemeta:description
     - Short or long description of the software
   * - codemeta:license
     - The license(s) of the software

See the `full CodeMeta terms list <https://codemeta.github.io/terms/>`_ for a complete
reference of the available properties.

.. _JSON-LD compact representation: https://www.w3.org/TR/json-ld11/#compacted-document-form
.. _compact IRIs: https://www.w3.org/TR/json-ld11/#compact-iris
.. _DublinCore: https://www.dublincore.org/
.. _CodeMeta: https://codemeta.github.io/