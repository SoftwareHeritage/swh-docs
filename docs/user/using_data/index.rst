.. _using-swh-data:

Using Software Heritage data
============================

This page documents the various ways Software Heritage provides programmatic
access to data in the archive, and pointers to use them.

First, please familiarize yourself with:

* the :ref:`data model <data-model>`,
* the `content policy`_,
* your local data protection legislation, and
* if relevant, your employer's/university's
  guidelines regarding research data.

.. _content policy: https://www.softwareheritage.org/legal/content-policy/

Data sources
------------

Software Heritage provides several ways to access the archive, with different
tradeoffs suitable for different access patterns.

REST API
^^^^^^^^

The `REST API`_ allows non-bulk read access to the whole archive,
as well as requesting archival of specific repositories or forges,
and downloading tarballs of individual repositories.

It is available anonymously, but we recommend `authenticating
<https://archive.softwareheritage.org/api/#authentication>`__ in order to
benefit from higher rate limits, and request access to beta features.

This API provides non-pseudonymized access to archive data; but some
content may be taken down, or author names may be amended, according to
the content policy.

.. _REST API: https://archive.softwareheritage.org/api/

Compressed graph
^^^^^^^^^^^^^^^^

:ref:`swh-graph <swh-graph>` provides three APIs to perform large traversal
on the graph of the archive
-- even in the opposite direction of the data model's DAG.

It also has limited capabilities to read or filter on node/edge labels
(ie. directory and file names, commit messages, ...) and does not
include file content.

For example, it allows getting a list of origins containing a specific
file or directory.

The APIs are:

* an :ref:`HTTP RPC API <swh-graph-api>`, which is available at
  https://archive.softwareheritage.org/api/1/graph/ on request.
  `Contact us`_ and tell us about your use case, we are interested to know
  what you plan to do with it
* a :ref:`gRPC API <swh-graph-grpc-api>`, for language-agnostic access
  to more advanced features
* a :ref:`Java API <swh-graph-java-api>` for full access to its features.

The latter two are currently not hosted publicly.
However, you can run your own using the same data we have on your own computers,
by downloading the "Compressed graph" files from the :ref:`swh-graph-dataset`.

Beware that this is resource-intensive, as the full dataset takes about 150GB
of disk and RAM for each of the two graphs (forward and backward edges);
and swapping severely affects its performance, which defeats the purpose of
swh-graph.

Producing this dataset is computationally intensive, and is not yet automated;
so it is currently published only once a year.

Author/committer name and email are pseudonymized.

.. _contact us: https://www.softwareheritage.org/community/scientists/

Dataset export
^^^^^^^^^^^^^^

The :ref:`swh-graph-dataset` also includes a raw export of all of
the archive's database tables (as ORC files) and graph structure (as compressed CSV).
It does not include file content.

As of 2022-12, the ORC dataset takes about 11TB on disk.

Producing this dataset is also not yet automated; so it is currently published
only once a year.

Author/committer name and email are pseudonymized.

Contents on S3
^^^^^^^^^^^^^^

Finally, to complement the compressed graph and dataset export, we provide
public access to file content via a S3 bucket, accessible at
``s3://softwareheritage/content/<sha1>`` and
``https://softwareheritage.s3.amazonaws.com/content/<sha1>``
where ``<sha1>`` is the hexadecimal representation of the content's
``sha1`` hash (not to be confused with ``sha1_git`` hash used in some places
in the datasets and in SWHID).


Possible bias
-------------

Statistical analyses on the archive may be biased by the way source code is
collected by the archive. This section details the main ones to be aware of
when performing research on the archive.


Code and configuration changes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Software Heritage's codebase evolves over time, and the archive adds support
for new forges regularly.
Major changes are documented in the `archive changelog`_

Typically, this means that source code deleted from a given forge before
Software Heritage started archiving that forge is missing
-- which may lead to code hosted in less popular places to be underrepresented
in the archive.

.. _archive changelog: archive-changelog

Large objects
^^^^^^^^^^^^^

Some source code repositories, such as Chromium's and Linux's git repositories
and their clones, are particularly large.
This is a challenge for :term:`loaders <loader>`, which may fail to load them
at a higher frequency than smaller repositories.

Software Heritage also does not archive any object larger than 300MB, as they
are unlikely to be source code, and would put unreasonable load on the archive.

Non-code objects
^^^^^^^^^^^^^^^^

Software Heritage collects data indiscriminately from code hosting places.
Sometimes, this includes repositories used to host non-code content and/or
binary code.
