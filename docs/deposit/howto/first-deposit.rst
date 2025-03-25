.. _deposit-first:

Make a first code & metadata deposit
====================================

Checklist
---------

- You have access to your :ref:`account credentials <deposit-account>`
- You have a software artefact at hand and its associated metadata (if not you need to
  :ref:`prepare your artefacts and metadata <deposit-prepare>`.)
- This is the first time you're depositing for this origin (if you already made
  deposits for this origin you want to
  :ref:`make a new deposit for an existing origin <deposit-version>`)
- The software artefact is not larger than 100Mo (if not you need to
  :ref:`make a multi-step deposit <deposit-partial>`)
- You have either the CLI installed or a tool to make API calls, we will use curl
  here, but commands could be easily adapted to another application

Send the artefact and the metadata
----------------------------------

.. admonition:: Deposit instance URL
   :class: warning

   In the examples below the staging deposit url https://deposit.staging.swh.network
   is used to avoid experimenting on the production instance of the deposit server.
   Make sure you switch to https://deposit.softwareheritage.org when you are ready.

.. tab-set::

  .. tab-item:: API

    .. code-block:: console

      # 1) Note the 'In-Progress: false' header
      # 2) Make sure the mimetype matches your file, here SOFTWARE_ARTEFACT is a zip
      curl -i -u USERNAME:PASSWORD \
           -F "file=@SOFTWARE_ARTEFACT;type=application/zip;filename=payload" \
           -F "atom=@METADATA_FILE;type=application/atom+xml;charset=UTF-8" \
           -H 'In-Progress: false' \
           -XPOST https://deposit.staging.swh.network/1/COLLECTION/

  .. tab-item:: CLI

    .. code-block:: console

      # 1) Note the 'no-partial' flag
      swh deposit upload \
        --username USERNAME --password PASSWORD \
        --url https://deposit.staging.swh.network/1 \
        --archive SOFTWARE_ARTEFACT \
        --metadata METADATA_FILE \
        --no-partial \
        --format json

Will return the following response (note the ``deposited`` status):

.. tab-set::

  .. tab-item:: API

    .. code-block:: xml

      <entry xmlns="http://www.w3.org/2005/Atom"
            xmlns:sword="http://purl.org/net/sword/"
            xmlns:dcterms="http://purl.org/dc/terms/"
            xmlns:swhdeposit="https://www.softwareheritage.org/schema/2018/deposit"
            >
          <swhdeposit:deposit_id>DEPOSIT_ID</swhdeposit:deposit_id>
          <swhdeposit:deposit_date>Jan. 1, 2025, 09:00 a.m.</swhdeposit:deposit_date>
          <swhdeposit:deposit_archive>None</swhdeposit:deposit_archive>
          <swhdeposit:deposit_status>deposited</swhdeposit:deposit_status>

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
        "deposit_status": "deposited",
        "deposit_id": "DEPOSIT_ID",
        "deposit_date": "Jan. 1, 2025, 09:00 a.m.",
        "deposit_status_detail": None
      }

A ``deposited`` status means the deposit is complete but still needs to be checked to
ensure data consistency before it gets integrated in the archive. You can check your
deposit status to follow the process.

Check a deposit status and get its SWHID
----------------------------------------

Your deposit will go :doc:`through multiple steps </references/workflow>` before appearing in the archive, you can check the status of your deposit and get its SWHID:

.. tab-set::

  .. tab-item:: API

    .. code-block:: console

      curl -i -u USERNAME:PASSWORD \
           -XGET https://deposit.staging.swh.network/1/COLLECTION/DEPOSIT_ID/status/

  .. tab-item:: CLI

    .. code-block:: console

      swh deposit status \
        --username USERNAME --password PASSWORD \
        --url https://deposit.staging.swh.network/1 \
        --deposit-id DEPOSIT_ID \
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

A ``done`` status means the deposit is now integrated in the archive, so you can
access ``https://archive.softwareheritage.org/SWHID``,
``https://archive.softwareheritage.org/SWHID_CONTEXT``, or
``https://archive.softwareheritage.org/browse/origin/?origin_url=ORIGIN_URL`` to view
the result of it.

What's next ?
-------------

Now that you've made your first deposit you might want to
:ref:`integrate it in your website <deposit-integrations>` or
:ref:`push another version of the software <deposit-version>`.