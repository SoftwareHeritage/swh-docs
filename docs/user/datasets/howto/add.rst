Add a dataset
=============

.. todo::
  This section is a work in progress...

To add a dataset, you have to submit a merge request in `swh-dataportal`_ which
modifies the `data.yml`_ file with the appropriate info (cf. ref).

Example
-------

Adding an entry for a Provenance index dataset derived from the full graph
export from 18/05/2025 and containing all releases and revisions can be done by
adding the following snippet to `data.yml`_:

.. code-block:: console

  2025-05-18-provenance/all:
    derived_of: 2025-05-18-compressed


.. _swh-dataportal : https://gitlab.softwareheritage.org/swh/devel/swh-dataportal/
.. _data.yml : https://gitlab.softwareheritage.org/swh/devel/swh-dataportal/-/blob/6ef76de8395cb6ede92cc4bb3f9754077a762e8e/swh/dataportal/data.yml
