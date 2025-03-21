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