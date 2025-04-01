Error codes and solutions
=========================

In case your attempt to deposit an artefact or metadata failed you'll find here
explanations of the error messages and possible remediation.

.. admonition:: Still stuck?
   :class: Note

   In case you are not able to troubleshoot the problems you've encountered yourself
   feel free to reach deposit@softwareheritage.org

401 Unauthorized
----------------

This status code is returned when something went wrong with the credentials you used
or the way you used them.

- the API is protected through basic authentication, thus API calls requires username
  and password sent in the Authorization header
- make sure the credentials you used match the environment you are targeting (staging
  or production)

404 Not Found
-------------

This status code is returned when the resource you're trying to reach is not found.

- double check that the ``DEPOSIT_ID``, ``COLLECTION`` name or path name in the URL are
  valid

403 Forbidden
-------------

This status code is returned when the resource you're trying to reach exists and you
are properly authenticated but not allowed to access it.

- double check that the ``DEPOSIT_ID`` and ``COLLECTION`` name match your deposits

413 Request Entity Too Large
----------------------------

Your software artefact is too large for the server.

- refer to the :doc:`../howto/prepare` section to find the max size
  supported by the server
- split the artefact in multiple parts and follow the :doc:`../howto/multistep-deposit`
  process

415 Unsupported Media Type
--------------------------

This status code is returned when a wrong media type is provided when uploading the
code artefact.

- check the ``type=application/XXX`` header matches your file format
- refer to the :doc:`../howto/prepare` section to find what kind of file formats are
  supported
