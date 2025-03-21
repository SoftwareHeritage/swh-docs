.. _deposit-metadata-requirements:

Metadata
========


Intrinsic metadata
------------------






Extrinsic metadata
-------------------


- It is composed of ONLY one Atom XML document
- It MUST comply with :ref:`the metadata requirements <deposit-metadata-requirements>`
- It MUST reference a object or an origin URL
- The reference SHOULD exist in the SWH archive
- The object reference MUST be a SWHID on one of the following artifact types:
  ``origin``, ``snapshot``, ``release``, ``revision``, ``directory``, ``content``
- The SWHID MAY be a :ref:`core identifier <swhids-core>` with or without
  :ref:`qualifiers <swhids-qualifiers>`
- The SWHID MUST NOT reference a fragment of code with the classifier lines


extrinsic-metadata-specification