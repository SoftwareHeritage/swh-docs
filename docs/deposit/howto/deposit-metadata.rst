.. _deposit-metadata-only:

Make a metadata-only deposit
============================

It’s possible to deposit metadata on an already existing content using the
metadata-only deposit and referencing a repository or a specific artifact:

- It is composed of ONLY one Atom XML document
- It MUST comply with :ref:`the metadata requirements <deposit-metadata-requirements>`
- It MUST reference a object or an origin URL
- The reference SHOULD exist in the SWH archive
- The object reference MUST be a SWHID on one of the following artifact types:
  ``origin``, ``snapshot``, ``release``, ``revision``, ``directory``, ``content``
- The SWHID MAY be a :ref:`core identifier <swhids-core>` with or without
  :ref:`qualifiers <swhids-qualifiers>`
- The SWHID MUST NOT reference a fragment of code with the classifier lines

Requisites
----------

1. Access to :ref:`account credentials <deposit-account>`
2. Have the origin url and prepared artefacts at hand, we will refer to it as ``<origin>`` and ``<metadatafile>`` hereafter
3. Either the CLI installed or a tool to make API calls, we will use curl here, but
   commands could be easily adapted to another application.

Make a metadata deposit
-----------------------

.. tab-set::

  .. tab-item:: API

    .. code-block:: console

      # Note the 'In-Progress: false' header
      curl -i -u <username>:<pass> \
           -F "atom=@<metadatafile>;type=application/atom+xml;charset=UTF-8" \
           -H 'In-Progress: false' \
           -XPOST https://deposit.softwareheritage.org/1/<collection>/

  .. tab-item:: CLI

    .. code-block:: console

      swh deposit metadata-only
        --username <user> --password <pass> \
        --url https://deposit.staging.swh.network/1 \
        --metadata <metadatafile> \
        --format json