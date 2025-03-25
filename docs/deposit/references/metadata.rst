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