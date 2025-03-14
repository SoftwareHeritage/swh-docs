Make a metadata-only deposit
============================

Requisites
----------

1. Have your account credentials, the origin url and prepared artefacts at hand.
2. Either the CLI installed or a tool to make API calls (curl, HTTPie, etc.)

Make a metadata deposit
-----------------------

.. tab-set::

  .. tab-item:: CLI

    .. code-block:: console

      swh deposit ...

  .. tab-item:: API

    .. code-block:: console

      # Note the 'In-Progress: false' header
      curl -i -u <username>:<pass> \
           -F "file=@deposit.json;type=application/zip;filename=payload" \
           -F "atom=@atom-entry.xml;type=application/atom+xml;charset=UTF-8" \
           -H 'In-Progress: false' \
           -XPOST https://deposit.softwareheritage.org/1/hal/


Check its status
----------------

Your deposit will go :doc:`through multiple steps </references/workflow>` before appearing in the archive, You can check the status of your deposit ang get its SWHID :

.. tab-set::

  .. tab-item:: CLI

    .. code-block:: console

      swh deposit ...

  .. tab-item:: API

    .. code-block:: console

      curl -i -u hal:<pass> \
           -F "file=@deposit.json;type=application/zip;filename=payload" \
           -F "atom=@atom-entry.xml;type=application/atom+xml;charset=UTF-8" \
           -H 'In-Progress: false' \
           -XPOST https://deposit.softwareheritage.org/1/hal/

