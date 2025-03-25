.. _deposit-metadata-only:

Make a metadata-only deposit
============================

It’s possible to deposit metadata on an already existing content using the
metadata-only deposit and referencing a repository or a specific artifact.

Checklist
---------

- You have access to your :ref:`account credentials <deposit-account>`
- You have prepared your metadata (if not you need to
  :ref:`prepare your artefacts and metadata <deposit-prepare>`.)
- You have either the CLI installed or a tool to make API calls, we will use curl
  here, but commands could be easily adapted to another application

Make a metadata deposit
-----------------------

.. tab-set::

  .. tab-item:: API

    .. code-block:: console

      # Note the 'In-Progress: false' header, metadata-only deposits can't be partial
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


Will return the following response:

.. tab-set::

  .. tab-item:: API

    .. code-block:: xml

      <entry xmlns="http://www.w3.org/2005/Atom"
            xmlns:sword="http://purl.org/net/sword/"
            xmlns:dcterms="http://purl.org/dc/terms/"
            xmlns:swhdeposit="https://www.softwareheritage.org/schema/2018/deposit"
            >
          <swhdeposit:deposit_id>DEPOSIT_ID</swhdeposit:deposit_id>
          <swhdeposit:deposit_status>done</swhdeposit:deposit_status>
          <swhdeposit:deposit_status_detail>The deposit has been successfully loaded into the Software Heritage archive</swhdeposit:deposit_status_detail>
          <swhdeposit:deposit_swh_id>SWHID</swhdeposit:deposit_swh_id>
          <swhdeposit:deposit_swh_id_context>SWHID_CONTEXT</swhdeposit:deposit_swh_id>
      </entry>

  .. tab-item:: CLI

    .. code-block:: json

      {
        "deposit_id": DEPOSIT_ID,
        "deposit_status": "done",
        "deposit_swh_id": "SWHID",
        "deposit_swh_id_context": "SWHID_CONTEXT",
        "deposit_status_detail": "The deposit has been successfully loaded into the Software Heritage archive"
      }

A ``done`` status means the metadata-only deposit is now integrated in the archive.