Make a multi-step code & metadata deposit
=========================================

.. admonition:: API/CLI reference
   :class: note

   This page will help you make a deposit without getting into too much details,
   the :doc:`API reference <../references/api>` and the
   :doc:`CLI reference <../references/cli>`
   are available to explain all the technical specifications.

.. admonition:: Partial deposits
   :class: note

   This method of depositing artefacts to the archive is a bit more complicated than
   the other one, if your artefacts are not larger than 100Mo we would recommend
   sticking to :doc:`the simpler (one shot) method <first-deposit>`.

If you have multiple code artefacts or if you need to make your deposit in two or
more times, you can make use of the partial deposit functionality.

Checklist
---------

- You have access to your :doc:`account credentials <account>`
- You have a software artefact at hand and its associated metadata (if not you need to
  :doc:`prepare your artefacts and metadata <prepare>`.)
- This is the first time you're depositing for this origin (if you already made
  deposits for this origin you want to
  :doc:`make a new deposit for an existing origin <versions>`)
- You have either the CLI installed or a tool to make API calls, we will use curl
  here, but commands could be easily adapted to another application

Make the deposit in multiple steps
----------------------------------

.. admonition:: Deposit instance URL
   :class: warning

   In the examples below the staging deposit url https://deposit.staging.swh.network
   is used to avoid experimenting on the production instance of the deposit server.
   Make sure you switch to https://deposit.softwareheritage.org when you are ready.

In the example below we will make a first deposit with a code artefact then a second
one and finally a third one with the metadata.

First partial deposit
~~~~~~~~~~~~~~~~~~~~~

.. tab-set::

  .. tab-item:: API

    Note the ``In-Progress: true`` header. Also make sure the mimetype matches your
    file, here ``SOFTWARE_ARTEFACT1`` is a zip archive.

    .. code-block:: console

      curl -i -u USERNAME:PASSWORD \
           -F "file=@SOFTWARE_ARTEFACT1;type=application/zip;filename=payload" \
           -H 'In-Progress: true' \
           -XPOST https://deposit.staging.swh.network/1/COLLECTION/

  .. tab-item:: CLI

    Note the '--partial' flag '--archive' argument, as we're sending a new software
    artefact.

    .. code-block:: console

      swh deposit upload \
        --username USERNAME --password PASSWORD \
        --url https://deposit.staging.swh.network/1 \
        --archive SOFTWARE_ARTEFACT1 \
        --partial \
        --format json

Will return the following response (note the ``partial`` status and the ``deposit_id``
value):

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
        "deposit_status": "partial",
        "deposit_id": "DEPOSIT_ID",
        "deposit_date": "Jan. 1, 2025, 09:00 a.m.",
        "deposit_status_detail": null
      }

Second partial deposit
~~~~~~~~~~~~~~~~~~~~~~

Instead of creating a new deposit we'll update the previous one referenced by
``DEPOSIT_ID``. In our example, we're making this deposit in three steps, so we will
indicate in our calls that this deposit is still ``partial``. The number of steps
does not matter, the only important thing is to make all calls ``partial`` except the
last one.

.. tab-set::

  .. tab-item:: API

    Note the ``In-Progress: true`` header, the ``DEPOSIT_ID`` in the URL and the
    ``/media/`` endpoint as we're sending a new software artefact.
    Also make sure the mimetype matches your file, here ``SOFTWARE_ARTEFACT2`` is a
    tarball.

    .. code-block:: console

      curl -i -u USERNAME:PASSWORD \
           -F "file=@SOFTWARE_ARTEFACT2;type=application/x-tar;filename=payload" \
           -H 'In-Progress: true' \
           -XPOST https://deposit.staging.swh.network/1/COLLECTION/DEPOSIT_ID/media/

  .. tab-item:: CLI

    Note the '--partial' flag, the `--deposit-id` argument and the '--archive'
    argument, as we're sending a new software artefact.

    .. code-block:: console

      swh deposit upload \
        --username USERNAME --password PASSWORD \
        --url https://deposit.staging.swh.network/1 \
        --archive SOFTWARE_ARTEFACT2 \
        --deposit-id DEPOSIT_ID \
        --partial \
        --format json

This will return a response similar to the previous one.

Third (and last) partial deposit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This deposit will only consist of the metadata. To indicate this is the last step we
will send include "not partial anymore" parameter in our call.

.. tab-set::

  .. tab-item:: API

    Note the ``In-Progress: false`` header, the ``DEPOSIT_ID`` in the URL and the
    ``/metadata/`` as we're pushing only metadata.

    .. code-block:: console

      curl -i -u USERNAME:PASSWORD \
           -F "atom=@METADATA_FILE;type=application/atom+xml;charset=UTF-8" \
           -H 'In-Progress: false' \
           -XPOST https://deposit.staging.swh.network/1/COLLECTION/DEPOSIT_ID/metadata/

  .. tab-item:: CLI

    Note the '--not-partial' flag, the `--deposit-id` argument and the '--metadata'
    argument, as we're pushing only metadata.

    .. code-block:: console

      swh deposit upload \
        --username USERNAME --password PASSWORD \
        --url https://deposit.staging.swh.network/1 \
        --metadata METADATA_FILE \
        --deposit-id DEPOSIT_ID \
        --not-partial \
        --format json


Check a deposit status
----------------------

Your deposit will go :doc:`through multiple steps <../references/workflow>` before appearing in the archive, you can check the status of your deposit and get its SWHID:

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
        "deposit_id": "DEPOSIT_ID",
        "deposit_status": "done",
        "deposit_swh_id": "SWHID",
        "deposit_swh_id_context": "SWHID_CONTEXT",
        "deposit_status_detail": "The deposit has been successfully loaded into the Software Heritage archive"
      }

A ``deposited`` status means the deposit is complete but still needs to be checked to
ensure data consistency. You can check your deposit status to follow the process.

Repeat the same calls until the status changes:

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
        "deposit_id": "DEPOSIT_ID",
        "deposit_status": "done",
        "deposit_swh_id": "SWHID",
        "deposit_swh_id_context": "SWHID_CONTEXT",
        "deposit_status_detail": "The deposit has been successfully loaded into the Software Heritage archive"
      }

A ``done`` status means the deposit is now integrated in the archive, so you can
access ``https://deposit.staging.swh.network/SWHID``,
``https://deposit.staging.swh.network/SWHID_CONTEXT``, or
``https://deposit.staging.swh.network/browse/origin/?origin_url=ORIGIN_URL`` to view
the result of it.

What's next ?
-------------

Now that you've made your first deposit you might want to
:doc:`integrate it in your website <integrations>` or
:doc:`push another version of the software <versions>`.
