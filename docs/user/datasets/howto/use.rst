Use a dataset
=============

Download a dataset
------------------

Requirements
~~~~~~~~~~~~

As most of our datasets are currently hosted and available on an Amazon S3 bucket, you will need to install either `awscli`_ or :ref:`swh-datasets <swh-datasets>`.

Find a dataset
~~~~~~~~~~~~~~

All the datasets published by Software Heritage are listed at `datasets.softwareheritage.org`_.

Download the desired dataset
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once you have found the dataset you want to download, check its "Download" subsection, which will provide the command to run to download the dataset (both with `awscli`_ and :ref:`swh-datasets <swh-datasets>`).

Example
~~~~~~~

If you want to download the compressed graph corresponding to the entire archive as of May 18, 2025, you can:

- Visit https://datasets.softwareheritage.org/graphs/compressed/#2025-05-18-compressed
- Run one of the specified commands:

  - ``aws s3 cp --recursive --no-sign-request s3://softwareheritage/graph/2025-05-18/compressed/ 2025-05-18-compressed``
  - ``swh datasets download-graph 2025-05-18``

.. admonition:: Warning
  :class: important

  The dataset used in the example above is 14 TB, so be sure to have enough space, time and bandwidth before trying to download it.

Advanced usage
--------------

Once you have a dataset available, you can refer to :ref:`swh-graph <swh-graph>` and :ref:`swh-datasets <swh-datasets>` to use it.


.. _awscli : https://pypi.org/project/awscli/
.. _datasets.softwareheritage.org : https://datasets.softwareheritage.org/
