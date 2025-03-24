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

    .. code-block:: http

      <entry xmlns="http://www.w3.org/2005/Atom"
            xmlns:sword="http://purl.org/net/sword/"
            xmlns:dcterms="http://purl.org/dc/terms/"
            xmlns:swhdeposit="https://www.softwareheritage.org/schema/2018/deposit"
            >
          <!-- Note the deposit_id, we'll need it for the other partial deposit -->
          <swhdeposit:deposit_id>DEPOSIT_ID</swhdeposit:deposit_id>
          <swhdeposit:deposit_date>Jan. 1, 2025, 09:00 a.m.</swhdeposit:deposit_date>
          <swhdeposit:deposit_archive>None</swhdeposit:deposit_archive>
          <!-- Note the 'partial' status -->
          <swhdeposit:deposit_status>partial</swhdeposit:deposit_status>

          <!-- Edit-IRI -->
          <link rel="edit" href="/1/COLLECTION/DEPOSIT_ID/metadata/" />
          <!-- EM-IRI -->
          <link rel="edit-media" href="/1/COLLECTION/DEPOSIT_ID/media/"/>
          <!-- SE-IRI -->
          <link rel="http://purl.org/net/sword/terms/add" href="/1/COLLECTION/DEPOSIT_ID/metadata/" />
          <!-- State-IRI -->
          <link rel="alternate" href="/1/COLLECTION/DEPOSIT_ID/status/"/>

          <sword:packaging>http://purl.org/net/sword/package/SimpleZip</sword:packaging>
      </entry>

  .. tab-item:: CLI

    .. code-block:: json

      {
        # Note the 'partial' status
        'deposit_status': 'partial',
        'deposit_id': 'DEPOSIT_ID',
        'deposit_date': 'Jan. 1, 2025, 09:00 a.m.',
        'deposit_status_detail': None
      }
