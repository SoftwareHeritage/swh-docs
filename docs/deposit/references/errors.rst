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

- The API is protected through basic authentication, thus API calls requires username
  and password sent in the Authorization header
- Make sure the credentials you used match the environment you are targeting (staging
  or production)

404 Not Found
-------------

This status code is returned when the resource you're trying to reach is not found.

- Double check the ``<deposit_id>``, ``<collection>`` name or path name in the URL are
  valid

403 Forbidden
-------------

This status code is returned when the resource you're trying to reach exists and you
are properly authenticated but not allowed to access it.

- Double check the ``<deposit_id>``, ``<collection>`` name match your deposits