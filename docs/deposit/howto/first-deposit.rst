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
      # 2) Make sure the mimetype matches your file, here <softwareartefact> is a zip
      curl -i -u <username>:<password> \
           -F "file=@<softwareartefact>;type=application/zip;filename=payload" \
           -F "atom=@<metadatafile>;type=application/atom+xml;charset=UTF-8" \
           -H 'In-Progress: false' \
           -XPOST https://deposit.staging.swh.network/1/<collection>/

  .. tab-item:: CLI

    .. code-block:: console

      # 1) Note the 'no-partial' flag
      swh deposit upload \
        --username <username> --password <password> \
        --url https://deposit.staging.swh.network/1 \
        --create-origin <origin> \
        --archive <softwareartefact> \
        --metadata <metadatafile> \
        --no-partial \
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
          <swhdeposit:deposit_id><deposit_id></swhdeposit:deposit_id>
          <swhdeposit:deposit_date>Jan. 1, 2025, 09:00 a.m.</swhdeposit:deposit_date>
          <swhdeposit:deposit_archive>None</swhdeposit:deposit_archive>
          <!-- Note the 'deposited' status -->
          <swhdeposit:deposit_status>deposited</swhdeposit:deposit_status>

          <!-- Edit-IRI -->
          <link rel="edit" href="/1/<collection>/<deposit_id>/metadata/" />
          <!-- EM-IRI -->
          <link rel="edit-media" href="/1/<collection>/<deposit_id>/media/"/>
          <!-- SE-IRI -->
          <link rel="http://purl.org/net/sword/terms/add" href="/1/<collection>/<deposit_id>/metadata/" />
          <!-- State-IRI -->
          <link rel="alternate" href="/1/<collection>/<deposit_id>/status/"/>

          <sword:packaging>http://purl.org/net/sword/package/SimpleZip</sword:packaging>
      </entry>

  .. tab-item:: CLI

    .. code-block:: json

      {
        # Note the 'deposited' status
        'deposit_status': 'deposited',
        'deposit_id': '<deposit_id>',
        'deposit_date': 'Jan. 1, 2025, 09:00 a.m.',
        'deposit_status_detail': None
      }

A `deposited` status means the deposit is complete but still needs to be checked to
ensure data consistency. You can check your deposit status to follow the process.

Check a deposit status
----------------------

Your deposit will go :doc:`through multiple steps </references/workflow>` before appearing in the archive, you can check the status of your deposit and get its SWHID:

.. tab-set::

  .. tab-item:: API

    .. code-block:: console

      curl -i -u <username>:<password> \
           -XGET https://deposit.staging.swh.network/1/<collection>/<deposit_id>/status/

  .. tab-item:: CLI

    .. code-block:: console

      swh deposit status \
        --username <username> --password <password> \
        --url https://deposit.staging.swh.network/1 \
        --deposit-id <deposit_id> \
        --format json

Will return the following response:

.. tab-set::

  .. tab-item:: API

    .. code-block:: http

      HTTP/1.1 200 OK
      Vary: Accept, Cookie
      Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
      Location: /1/<collection>/<deposit_id>/status/
      Content-Type: application/xml

      <entry xmlns="http://www.w3.org/2005/Atom"
            xmlns:sword="http://purl.org/net/sword/"
            xmlns:dcterms="http://purl.org/dc/terms/"
            xmlns:swhdeposit="https://www.softwareheritage.org/schema/2018/deposit"
            >
          <swhdeposit:deposit_id><deposit_id></swhdeposit:deposit_id>
          <swhdeposit:deposit_status>done</swhdeposit:deposit_status>
          <swhdeposit:deposit_status_detail>The deposit has been successfully loaded into the Software Heritage archive</swhdeposit:deposit_status_detail>
          <swhdeposit:deposit_swh_id>swh:1:dir:d83b7dda887dc790f7207608474650d4344b8df9</swhdeposit:deposit_swh_id>
          <swhdeposit:deposit_swh_id_context>swh:1:dir:d83b7dda887dc790f7207608474650d4344b8df9;origin=<origin>;visit=swh:1:snp:68c0d26104d47e278dd6be07ed61fafb561d0d20;anchor=swh:1:rev:e76ea49c9ffbb7f73611087ba6e999b19e5d71eb;path=/</swhdeposit:deposit_swh_id>
      </entry>

  .. tab-item:: CLI

    .. code-block:: json

      {
        "deposit_id": <deposit_id>,
        "deposit_status": "done",
        "deposit_swh_id": "swh:1:dir:d83b7dda887dc790f7207608474650d4344b8df9",
        "deposit_swh_id_context": "swh:1:dir:d83b7dda887dc790f7207608474650d4344b8df9;origin=<origin>;visit=swh:1:snp:68c0d26104d47e278dd6be07ed61fafb561d0d20;anchor=swh:1:rev:e76ea49c9ffbb7f73611087ba6e999b19e5d71eb;path=/",
        "deposit_status_detail": "The deposit has been successfully loaded into the Software Heritage archive"
      }
