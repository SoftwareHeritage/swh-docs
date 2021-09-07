.. _architecture-metadata:

Metadata workflow and architecture
==================================

|swh| calls "metadata" information it collects and extracts that describes and provides additional information on source code.

This metadata is partitioned into three types:

1. development metadata, which is part of the :ref:`data-model`, such as authorship
   and date of revisions and releases,
2. :term:`intrinsic metadata`, which is extracted from a source code repository itself,
   usually mined from metadata files like :file:`package.json` or :file:`Gemfile`.
   It is intrinsically part of the software origin, because both are distributed
   together from the origin's VCS repository or release tarballs.
3. :term:`extrinsic metadata`, which is collected or deposited from external sources.
   It can have a straightforward relationship with the repository (eg. number of stars
   of GitHub origins or checksums of release tarballs),
   or be more distant (provided by a third-party like Wikidata).

This document is only about the latter two.


Raw metadata storage
--------------------

As an archive, |swh| chooses to store original metadata objects unmodified
in its long-term storage databases (:ref:`swh-storage <swh-storage>` and
:ref:`swh-objstorage <swh-objstorage>`).

For intrinsic metadata, this only means it is treated as any other source code content;
ie. there is no difference between a metadata file like :file:`package.json`
and a source code file like :file:`index.js` from the loaders' and the database's
points of view.

Extrinsic metadata, however, are stored in a :ref:`dedicated storage service
<extrinsic-metadata-specification>` (in practice, this is currently in the same database
as the :ref:`data-model`'s Merkle DAG; but in separate tables).

As they are both stored verbatim, they are in various formats depending on their source,
and are not directly usable.


Indexed metadata storages
-------------------------

|swh| also stores metadata in indexed databases, which are directly usable
for searching and querying.
Currently, there are two:

1. the "indexer storage", a postgresql database that acts as a cache, and provides
   limited search functionality
2. :ref:`swh-search <swh-search>`, an advanced search service backed by
   `ElasticSearch`_.

Each of these databases has a consistent schema for ease of use.


Differences between raw and indexed metadata
--------------------------------------------

The raw metadata is the authentic piece of metadata while the indexed metadata
is a processed version, where the raw metadata is translated to a uniform vocabulary.

Both intrinsic and extrinsic metadata can be indexed and translated.

Therefore, most metadata stored twice in |swh|: raw and indexed.
The reason for this apparent duplication is robustness and future-proofing.

Indeed, indexing metadata is a complex process.
By keeping the raw metadata we ensure the possibility to re-compute the metadata
in the future with other vocabularies.
Furthermore, if we did not store the raw metadata, this would mean bugs in indexers
could easily lose data, forever.
Thanks to this redundant architecture, bugs can be fixed and indexers re-ran
from the raw metadata to fix the indexed metadata.

This also makes it easier to add features on metadata mining or change schema
in the future: instead of re-loading
from original sources (which may have disappeared since!), new indexers can simply
read stored metadata into new indexed storages.


Metadata mining
---------------

Some of the stored raw metadata is read and interpreted by worker processes known
as :ref:`indexers <swh-indexer>`.
Currently, they convert this metadata into a common format, `CodeMeta`_.

Some indexers also read source code files to generate metadata about these files,
such as their license, language, etc.

Then, they either send their results directly to a caller, or write it to an
indexed metadata storage (either directly or through :ref:`swh-journal <swh-journal>`).

.. _CodeMeta: https://codemeta.github.io/
.. _ElasticSearch: https://www.elastic.co/elasticsearch/
