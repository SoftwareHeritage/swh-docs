Make a metadata-only deposit
===================

Requisites
----------

1. Have your account credentials, the origin url and prepared artefacts at hand.
2. Either the CLI installed or a tool to make API calls (curl_, HTTPie_, etc.)

Make a metadata deposit
-------------------

.. tabs::
   .. code-tab:: CLI
      swh deposit ...
   .. code-tab:: API
      # Note the 'In-Progress: false' header
      curl -i -u <username>:<pass> \
            -F "file=@deposit.json;type=application/zip;filename=payload" \
            -F "atom=@atom-entry.xml;type=application/atom+xml;charset=UTF-8" \
            -H 'In-Progress: false' \
            -XPOST https://deposit.softwareheritage.org/1/hal/


Check its status
----------------

Your deposit will go :doc:`through multiple steps </references/workflow>` before appearing in the archive, You can check the status of your deposit ang get its SWHID :

.. tabs::

   .. code-tab:: CLI
         swh deposit status ...

   .. code-tab:: API

        curl -i -u hal:<pass> \
            -F "file=@deposit.json;type=application/zip;filename=payload" \
            -F "atom=@atom-entry.xml;type=application/atom+xml;charset=UTF-8" \
            -H 'In-Progress: false' \
            -XPOST https://deposit.softwareheritage.org/1/hal/


:: _curl: https://curl.se/
:: _HTTPie: https://httpie.io/