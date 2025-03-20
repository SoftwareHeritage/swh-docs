.. _deposit-partial:


Make a multi-step code & metadata deposit
=========================================

.. admonition:: Partial deposits
   :class: Note

   This method of depositing artefacts to the archive is a bit more complicated than
   the :ref:`regular one`, if your artefacts are not larger than 100Mo we would
   recommend sticking to the simpler (one shot) method.

If you have multiple code artefacts or if you need to make your deposit in two or
more times, you can make use of the partial deposit functionality.

Checklist
---------

- You have access to your :ref:`account credentials <deposit-account>`
- You have a software artefact at hand and its associated metadata (if not you need to
  :ref:`prepare your artefacts and metadata <deposit-prepare>`.)
- This is the first time you're depositing for this origin (if you already made
  deposits for this origin you want to
  :ref:`make a new deposit for an existing origin <deposit-version>`)
- You have either the CLI installed or a tool to make API calls, we will use curl
  here, but commands could be easily adapted to another application


Make the deposit in multiple steps
----------------------------------

In the example below we will make a first deposit with a code artefact then a second
one and finally a third one with the metadata.

First partial deposit
~~~~~~~~~~~~~~~~~~~~~

.. tab-set::

  .. tab-item:: API

    .. code-block:: console

      # Note the 'In-Progress: true' header
      curl -i -u <username>:<password> \
           -F "file=@<softwareartefact1>;type=application/zip;filename=payload" \
           -H 'In-Progress: true' \
           -XPOST https://deposit.staging.swh.network/1/<collection>/

  .. tab-item:: CLI

    .. code-block:: console

      # 1) Note the '--partial' flag
      # 2) Note the `--create-origin` flag
      swh deposit upload \
        --username <username> --password <password> \
        --url https://deposit.staging.swh.network/1 \
        --create-origin <origin> \
        --archive <softwareartefact1> \
        --partial \
        --format json

Will return the following response:

.. tab-set::

  .. tab-item:: API

    .. code-block:: http

      HTTP/1.1 201 Created
      Vary: Accept, Cookie
      Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
      Location: /1/<collection>/<deposit_id>/metadata/
      Content-Type: application/xml

      <entry xmlns="http://www.w3.org/2005/Atom"
            xmlns:sword="http://purl.org/net/sword/"
            xmlns:dcterms="http://purl.org/dc/terms/"
            xmlns:swhdeposit="https://www.softwareheritage.org/schema/2018/deposit"
            >
          <!-- Note the deposit_id, we'll need it for the other partial deposit -->
          <swhdeposit:deposit_id><deposit_id></swhdeposit:deposit_id>
          <swhdeposit:deposit_date>Jan. 1, 2025, 09:00 a.m.</swhdeposit:deposit_date>
          <swhdeposit:deposit_archive>None</swhdeposit:deposit_archive>
          <!-- Note the 'partial' status -->
          <swhdeposit:deposit_status>partial</swhdeposit:deposit_status>

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
        # Note the 'partial' status
        'deposit_status': 'partial',
        'deposit_id': '<deposit_id>',
        'deposit_date': 'Jan. 1, 2025, 09:00 a.m.',
        'deposit_status_detail': None
      }

Second partial deposit
~~~~~~~~~~~~~~~~~~~~~~

Instead of creating a new deposit we'll update the previous one referenced by
``<deposit_id>``. In our example, we're making this deposit in three steps, so we will
indicate in our calls that this deposit is still ``partial``. The number of steps
does not matter, the only important thing is to make all calls ``partial`` except the
last one.

.. tab-set::

  .. tab-item:: API

    .. code-block:: console

      # 1) Note the 'In-Progress: true' header
      # 2) Note the '<deposit_id>' in the URL
      # 3) Note the '/media/' in the URL (we're appending a new software artefact)
      curl -i -u <username>:<password> \
           -F "file=@<softwareartefact2>;type=application/zip;filename=payload" \
           -H 'In-Progress: true' \
           -XPOST https://deposit.staging.swh.network/1/<collection>/<deposit_id>/media/

  .. tab-item:: CLI

    .. code-block:: console

      # 1) Note the '--partial' flag
      # 2) Note the `--deposit-id` argument
      # 3) Note the '--archive' argument as we're sending a new software artefact
      swh deposit upload \
        --username <username> --password <password> \
        --url https://deposit.staging.swh.network/1 \
        --archive <softwareartefact2> \
        --deposit-id <deposit_id> \
        --partial \
        --format json

This will return a response similar to the previous one.

Third (and last) partial deposit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This deposit will only consist of the metadata. To indicate this is the last step we
will send include "not partial anymore" parameter in our call.

.. tab-set::

  .. tab-item:: API

    .. code-block:: console

      # 1) Note the 'In-Progress: false' header
      # 2) Note the '<deposit_id>' in the URL
      # 3) Note the '/metadata/' in the URL (we're appending metadata not code)
      curl -i -u <username>:<password> \
           -F "atom=@<metadatafile>;type=application/atom+xml;charset=UTF-8" \
           -H 'In-Progress: false' \
           -XPOST https://deposit.staging.swh.network/1/<collection>/<deposit_id>/metadata/

  .. tab-item:: CLI

    .. code-block:: console

      # 1) Note the '--not-partial' flag
      # 2) Note the `--deposit-id` argument
      # 3) Note the '--metadata' argument, as we're pushing metadata
      swh deposit upload \
        --username <username> --password <password> \
        --url https://deposit.staging.swh.network/1 \
        --metadata <metadatafile> \
        --deposit-id <deposit_id> \
        --not-partial \
        --format json


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


