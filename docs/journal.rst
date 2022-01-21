.. _journal-specs:

Journal Specification
=====================

The |swh| journal is a Kafka_-based stream of events for every added object in
the |swh| Archive and some of its related services, especially indexers.

Each topic_ will stream added elements for a given object type according to the
topic name.

Objects streamed in a topic are serialized versions of objects stored in the
|swh| Archive specified by the main |swh| :py:mod:`data model <swh.model.model>` or
the :py:mod:`indexer object model <swh.indexer.storage.model>`.


In this document we will describe expected messages in each topic, so a
potential consumer can easily cope with the |swh| journal without having to
read the source code or the |swh| :ref:`data model <swh-model>` in details (it
is however recommended to familiarize yourself with this later).

Kafka message values are dictionary structures serialized as msgpack_, with a
few custom encodings. See the section `Kafka message format`_ below for a
complete description of the serialization format.

Note that each example given below show the dictionary before being serialized
as a msgpack_ chunk.


Topics
------

There are several groups of topics:

- main storage Merkle-DAG related topics,
- other storage objects (not part of the Merkle DAG),
- indexer related objects (not yet documented below).

Topics prefix can be either `swh.journal.objects` or
`swh.journal.objects_privileged` (see below).

Anonymized topics
+++++++++++++++++

For topics that transport messages with user information (name and email
address), namely `swh.journal.objects.release`_ and
`swh.journal.objects.revision`_, there are 2 versions of those: one is an
anonymized topic, in which user information are obfuscated, and a pristine
version with clear data.

Access to pristine topics depends on ACLs linked to credentials used to connect
to the Kafka cluster.


List of topics
++++++++++++++

- `swh.journal.objects.origin`_
- `swh.journal.objects.origin_visit`_
- `swh.journal.objects.origin_visit_status`_
- `swh.journal.objects.snapshot`_
- `swh.journal.objects.release`_
- `swh.journal.objects.privileged_release <swh.journal.objects.release>`_
- `swh.journal.objects.revision`_
- `swh.journal.objects.privileged_revision <swh.journal.objects.revision>`_
- `swh.journal.objects.directory`_
- `swh.journal.objects.content`_
- `swh.journal.objects.skipped_content`_
- `swh.journal.objects.metadata_authority`_
- `swh.journal.objects.metadata_fetcher`_
- `swh.journal.objects.raw_extrinsic_metadata`_



Topics for Merkle-DAG objects
-----------------------------

These topics are for the various objects stored in the |swh| Merkle DAG, see
the :ref:`data model <swh-model>` for more details.


`swh.journal.objects.snapshot`
++++++++++++++++++++++++++++++

Topic for :py:class:`swh.model.model.Snapshot` objects.

Message format:

- `branches` [dict] branches present in this snapshot,
- `id` [bytes] the intrinsic identifier of the
  :py:class:`swh.model.model.Snapshot` object

with `branches` being a dictionary which keys are branch names [bytes], and values a dictionary of:

- `target` [bytes] intrinsic identifier of the targeted object
- `target_type` [string] the type of the targeted object (can be "content",
  "directory", "revision", "release", "snapshot" or "alias").

Example:

.. code:: python

   {
    'branches': {
      b'refs/pull/1/head': {
        'target': b'\x07\x10\\\xfc\xae\x1f\xb1\xf9\xb5\xad\x8bI\xf1G\x10\x9a\xba>8\x0c',
        'target_type': 'revision'
        },
      b'refs/pull/2/head': {
        'target': b'\x1a\x868-\x9b\x1d\x00\xfbd\xeaH\xc88\x9c\x94\xa1\xe0U\x9bJ',
        'target_type': 'revision'
        },
      b'refs/heads/master': {
        'target': b'\x7f\xc4\xfe4f\x7f\xda\r\x0e[\xba\xbc\xd7\x12d#\xf7&\xbfT',
        'target_type': 'revision'
        },
      b'HEAD': {
        'target': b'refs/heads/master',
        'target_type': 'alias'
        }
      },
    'id': b'\x10\x00\x06\x08\xe9E^\x0c\x9bS\xa5\x05\xa8\xdf\xffw\x88\xb8\x93^'
   }



`swh.journal.objects.release`
+++++++++++++++++++++++++++++

Topic for :py:class:`swh.model.model.Release` objects.

This topics is anonymized. The non-anonymized version of this topic is
`swh.journal.objects_privileged.release`.

Message format:

- `name` [bytes] name (typically the version) of the release
- `message` [bytes] message of the release
- `target` [bytes] identifier of the target object
- `target_type` [string] type of the target, can be "content", "directory",
  "revision", "release" or "snapshot"
- `synthetic` [bool] True if the :py:class:`swh.model.model.Release` object has
  been forged by the loading process; this flag is not used for the id
  computation,
- `author` [dict] the author of the release
- `date` [gitdate] the date of the release
- `id` [bytes] the intrinsic identifier of the
  :py:class:`swh.model.model.Release` object

Example:

.. code:: python

   {
    'name': b'0.3',
    'message': b'',
    'target': b'<\xd6\x15\xd9\xef@\xe0[\xe7\x11=\xa1W\x11h%\xcc\x13\x96\x8d',
    'target_type': 'revision',
    'synthetic': False,
    'author': {
      'fullname': b'\xf5\x8a\x95k\xffKgN\x82\xd0f\xbf\x12\xe8w\xc8a\xf79\x9e\xf4V\x16\x8d\xa4B\x84\x15\xea\x83\x92\xb9',
      'name': None,
      'email': None
      },
    'date': {
      'timestamp': {
        'seconds': 1480432642,
        'microseconds': 0
        },
      'offset': 180,
      'negative_utc': False
      },
    'id': b'\xd0\x00\x06u\x05uaK`.\x0c\x03R%\xca,\xe1x\xd7\x86'
   }


`swh.journal.objects.revision`
++++++++++++++++++++++++++++++

Topic for :py:class:`swh.model.model.Revision` objects.

This topics is anonymized. The non-anonymized version of this topic is
`swh.journal.objects_privileged.revision`.

Message format:

- ``message`` [bytes] the commit message for the revision
- ``author`` [dict] the author of the revision
- ``committer`` [dict] the committer of the revision
- ``date`` [gitdate] the revision date
- ``committer_date`` [gitdate] the revision commit date
- ``type`` [string] the type of the revision (can be "git", "tar", "dsc", "svn", "hg")
- ``directory`` [bytes] the intrinsic identifier of the directory this revision links to
- ``synthetic`` [bool] whether this :py:class:`swh.model.model.Revision` is synthetic or not,
- ``metadata`` [bytes] the metadata linked to this :py:class:`swh.model.model.Revision` (not part of the
  intrinsic identifier computation),
- ``parents`` [list[bytes]] list of parent :py:class:`swh.model.model.Revision` intrinsic identifiers
- ``id`` [bytes] intrinsic identifier of the :py:class:`swh.model.model.Revision`
- ``extra_headers`` [list[(bytes, bytes)]] TODO


Example:

.. code:: python

   {
    'message': b'I now arrange to be able to create a prettyprinted version of the Pascal\ncode to make review of translation of it easier, and I have thought a bit\nmore about coping with Pastacl variant records and the like, but have yet to\nimplement everything. lufylib.red is a place for support code.\n',
    'author': {
      'fullname': b'\xf3\xa7\xde7[\x8b#=\xe48\\/\xa1 \xed\x05NA\xa6\xf8\x9c\n\xad5\xe7\xe0"\xc4\xd5[\xc9z',
      'name': None,
      'email': None
      },
    'committer': {
      'fullname': b'\xf3\xa7\xde7[\x8b#=\xe48\\/\xa1 \xed\x05NA\xa6\xf8\x9c\n\xad5\xe7\xe0"\xc4\xd5[\xc9z',
      'name': None,
      'email': None
      },
    'date': {
      'timestamp': {'seconds': 1495977610, 'microseconds': 334267},
      'offset': 0,
      'negative_utc': False
      },
    'committer_date': {
      'timestamp': {'seconds': 1495977610, 'microseconds': 334267},
      'offset': 0,
      'negative_utc': False
      },
    'type': 'svn',
    'directory': b'\x815\xf0\xd9\xef\x94\x0b\xbf\x86<\xa4j^\xb65\xe9\xf4\xd1\xc3\xfe',
    'synthetic': True,
    'metadata': None,
    'parents': [
      b'D\xb1\xc8\x0f&\xdc\xd4 \x92J\xaf\xab\x19V\xad\xe7~\x18\n\x0c',
      ],
    'id': b'\x1e\x1c\x19<l\xaa\xd2~{P\x11jH\x0f\xfd\xb0Y\x86\x99\x08',
    'extra_headers': [
      [b'svn_repo_uuid', b'2bfe0521-f11c-4a00-b80e-6202646ff360'],
      [b'svn_revision', b'4067']
      ]
   }



`swh.journal.objects.content`
+++++++++++++++++++++++++++++

Topic for :py:class:`swh.model.model.Content` objects.

Message format:

- ``sha1`` [bytes] SHA1 of the :py:class:`swh.model.model.Content`
- ``sha1_git`` [bytes] SHA1_GIT of the :py:class:`swh.model.model.Content`
- ``sha256`` [bytes] SHA256 of the :py:class:`swh.model.model.Content`
- ``blake2s256`` [bytes] Blake2S256 hash of the :py:class:`swh.model.model.Content`
- ``length`` [int] length of the :py:class:`swh.model.model.Content`
- ``status`` [string] visibility status of the :py:class:`swh.model.model.Content` (can be "visible" or "hidden")
- ``ctime`` [timestamp] creation date of the :py:class:`swh.model.model.Content` (i.e. date at which this
  :py:class:`swh.model.model.Content` has been seen for the first time in the |swh| Archive).

Example:

.. code:: python

   {
    'sha1': b'-\xe7\xc1`\x9d\xd7\x7fu+\x05l\x07\xd1}\x95\x16o-u\x1d',
    'sha1_git': b'\xb9B\xa7EOW[\xef\x8b\x98\xa6b\xe9\xc7\xf0\x96g\x06`\xa4',
    'sha256': b'h{\xda\x8d\xaeG\xa4\xc6\x10\x05\xbc\xc9hca\x0em)\xd3A\x08\xd6\x95~(\xe5\xba\xe4\xaa\xcaT\x19',
    'blake2s256': b'\x8cl\xec\xe8S\xcd\xab\x90E\xc2\x8c\xfax\xe3\xbe\xca\x9aJ6\x1a\x9c](6\xc3\xb49\x8b:\xf9\xd8r',
    'length': 3220,
    'status': 'visible',
    'ctime': Timestamp(seconds=1606260407, nanoseconds=818259954)
   }



``swh.journal.objects.skipped_content``
+++++++++++++++++++++++++++++++++++++++

Topic for :py:class:`swh.model.model.SkippedContent` objects.


Message format:

- ``sha1`` [bytes] SHA1 of the :py:class:`swh.model.model.SkippedContent`
- ``sha1_git`` [bytes] SHA1 of the :py:class:`swh.model.model.SkippedContent`
- ``sha256`` [bytes] SHA1 of the :py:class:`swh.model.model.SkippedContent`
- ``blake2s256`` [bytes] SHA1 of the :py:class:`swh.model.model.SkippedContent`
- ``length`` [int] length of the :py:class:`swh.model.model.SkippedContent`
- ``status`` [string] visibility status of the
  :py:class:`swh.model.model.SkippedContent` (can only be "absent")
- ``reason`` [string] message indicating the reason for this content to be a
  :py:class:`swh.model.model.SkippedContent` (rather than a
  :py:class:`swh.model.model.Content`)
- ``ctime`` [timestamp] creation date of the
  :py:class:`swh.model.model.SkippedContent` (i.e. date at which this
  :py:class:`swh.model.model.SkippedContent` has been seen for the first time in
  the |swh| Archive)


Example:

.. code:: python

   {
    'sha1': b'[\x0f\x19I-%+\xec\x9dS\x86\xffz\xcb\xa2\x9f\x15\xcc\xb4&',
    'sha1_git': b'\xa9\xff4\xa7\xff\x85\xb3x\xaa\x91\x0b\xd0ZB!\x04\x8a',
    'sha256': b"\xe6\x876\xb2U-\x87\xb8\xe3\x12\xa0L\rq'\x88\xd4\x95\x92\xdf\x86\xfci\xe3E\x82\xe0\x95^\xbf\x1e\xbe",
    'blake2s256': b'\xe1 \n\x1d5\x8b\x1f\x98\\\x8e\xaa\x1d?8*\xc1\xf7\xb9\x95\r|\x1e\xee^\x10\x10\x19\xc6\x9c\x11\xedX',
    'length': 125146729,
    'status': 'absent',
    'reason': 'Content too large',
    'ctime': Timestamp(seconds=1606260407, nanoseconds=818259954)
   }



`swh.journal.objects.directory`
+++++++++++++++++++++++++++++++

Topic for :py:class:`swh.model.model.Directory` objects.

Message format:

- ``entries`` [list[dict]] list of directory entries
- ``id`` [bytes] intrinsic identifier of this :py:class:`swh.model.model.Directory`

with directory entries being dictionaries:

- ``name`` [bytes] name of the directory entry
- ``type`` [string] type of directory entry (can be "file", "dir" or "rev")
- ``perms`` [int] permissions for this directory entry


Example:

.. code:: python

   {
    'entries': [
     {'name': b'LICENSE',
      'type': 'file',
      'target': b'b\x03f\xeb\x90\x07\x1cs\xaeib\x8eg\x97]0\xf0\x9dg\x01',
      'perms': 33188},
     {'name': b'README.md',
      'type': 'file',
      'target': b'\x1e>\xb56x\xbc\xe5\xba\xa4\xed\x03\xae\x83\xdb@\xd0@0\xed\xc8',
      'perms': 33188},
     {'name': b'lib',
      'type': 'dir',
      'target': b'-\xb2(\x95\xe46X\x9f\xed\x1d\xa6\x95\xec`\x10\x1a\x89\xc3\x01U',
      'perms': 16384},
     {'name': b'package.json',
      'type': 'file',
      'target': b'Z\x91N\x9bw\xec\xb0\xfbN\xe9\x18\xa2E-%\x8fxW\xa1x',
      'perms': 33188}
    ],
    'id': b'eS\x86\xcf\x16n\xeb\xa96I\x90\x10\xd0\xe9&s\x9a\x82\xd4P'
   }



Other Objects Topics
--------------------

These topics are for objects of the |swh| archive that are not part of the
Merkle DAG but are essential parts of the archive; see the :ref:`data model
<swh-model>` for more details.


``swh.journal.objects.origin``
++++++++++++++++++++++++++++++

Topic for :py:class:`swh.model.model.Origin` objects.

Message format:

- ``url`` [string] URL of the :py:class:`swh.model.model.Origin`

Example:

.. code:: python

   {
     "url": "https://github.com/vujkovicm/pml"
   }


``swh.journal.objects.origin_visit``
++++++++++++++++++++++++++++++++++++

Topic for :py:class:`swh.model.model.OriginVisit` objects.

Message format:

- ``origin`` [string] URL of the visited :py:class:`swh.model.model.Origin`
- ``date`` [timestamp] date of the visit
- ``type`` [string] type of the loader used to perform the visit
- ``visit`` [int] number of the visit for this ``origin``

Example:

.. code:: python

   {
    'origin': 'https://pypi.org/project/wasp-eureka/',
    'date': Timestamp(seconds=1606260407, nanoseconds=818259954),
    'type': 'pypi',
    'visit': 505}
   }


``swh.journal.objects.origin_visit_status``
+++++++++++++++++++++++++++++++++++++++++++

Topic for :py:class:`swh.model.model.OriginVisitStatus` objects.

Message format:

- ``origin`` [string] URL of the visited :py:class:`swh.model.model.Origin`
- ``visit`` [int] number of the visit for this ``origin`` this status concerns
- ``date`` [timestamp] date of the visit status update
- ``status`` [string] status (can be "created", "ongoing", "full" or "partial"),
- ``snapshot`` [bytes] identifier of the :py:class:`swh.model.model.Snaphot` this
  visit resulted in (if ``status`` is "full" or "partial")
- ``metadata``: deprecated

Example:

.. code:: python

   {
    'origin': 'https://pypi.org/project/stricttype/',
    'visit': 524,
    'date': Timestamp(seconds=1606260407, nanoseconds=818259954),
    'status': 'full',
    'snapshot': b"\x85\x8f\xcb\xec\xbd\xd3P;Z\xb0~\xe7\xa2(\x0b\x11'\x05i\xf7",
    'metadata': None
   }



Extrinsic Metadata related Topics
---------------------------------

Extrinsic metadata is information about software that is not part of the source
code itself but still closely related to the software. See
:ref:`extrinsic-metadata-specification` for more details on the Extrinsic
Metadata model.

``swh.journal.objects.metadata_authority``
++++++++++++++++++++++++++++++++++++++++++

Topic for :py:class:`swh.model.model.MetadataAuthority` objects.

Message format:

- ``type`` [string]
- ``url`` [string]
- ``metadata`` [dict]

Examples:

.. code:: python

   {
    'type': 'forge',
    'url': 'https://guix.gnu.org/sources.json',
    'metadata': {}
   }

   {
    'type': 'deposit_client',
    'url': 'https://www.softwareheritage.org',
    'metadata': {'name': 'swh'}
   }



``swh.journal.objects.metadata_fetcher``
++++++++++++++++++++++++++++++++++++++++

Topic for :py:class:`swh.model.model.MetadataFetcher` objects.

Message format:

- ``type`` [string]
- ``version`` [string]
- ``metadata`` [dict]

Example:

.. code:: python

   {
    'name': 'swh.loader.package.cran.loader.CRANLoader',
    'version': '0.15.0',
    'metadata': {}
   }



``swh.journal.objects.raw_extrinsic_metadata``
++++++++++++++++++++++++++++++++++++++++++++++

Topic for :py:class:`swh.model.model.RawExtrinsicMetadata` objects.

Message format:

- ``type`` [string]
- ``target`` [string]
- ``discovery_date`` [timestamp]
- ``authority`` [dict]
- ``fetcher`` [dict]
- ``format`` [string]
- ``metadata`` [bytes]
- ``origin`` [string]
- ``visit`` [int]
- ``snapshot`` [SWHID]
- ``release`` [SWHID]
- ``revision`` [SWHID]
- ``path`` [bytes]
- ``directory`` [SWHID]

Example:

.. code:: python

   {
    'type': 'snapshot',
    'id': 'swh:1:snp:f3b180979283d4931d3199e6171840a3241829a3',
    'discovery_date': Timestamp(seconds=1606260407, nanoseconds=818259954),
    'authority': {
      'type': 'forge',
      'url': 'https://pypi.org/',
      'metadata': {}
      },
    'fetcher': {
      'name': 'swh.loader.package.pypi.loader.PyPILoader',
      'version': '0.10.0',
      'metadata': {}
      },
    'format': 'pypi-project-json',
    'metadata': b'{"info":{"author":"Signaltonsalat","author_email":"signaltonsalat@gmail.com"}]}',
    'origin': 'https://pypi.org/project/schwurbler/'
   }





Kafka message format
--------------------

Each value of a Kafka message in a topic is a dictionary-like structure
encoded as a msgpack_ byte string.

Keys are ASCII strings.

All values are encoded using default msgpack type system except for long
integers for which we use a custom format using msgpack `extended type`_ to
prevent overflow while packing some objects.


Integer
+++++++

For long integers (that do not fit in the ``[-(2**63), 2 ** 64 - 1]`` range), a
custom `extended type`_ based encoding scheme is used.

The ``type`` information can be:

- ``1`` for positive (possibly long) integers,
- ``2`` for negative (possibly long) integers.

The payload is simply the bytes (big endian) representation of the absolute
value (always positive).

For example (adapted to standard integers for the sake of readability; these
values are small so they will actually be encoded using the default msgpack
format for integers):

- ``12345`` would be encoded as the extension value ``[1, [0x30, 0x39]]`` (aka ``0xd5013039``)
- ``-42`` would be encoded as the extension value ``[2, [0x2A]]`` (aka ``0xd4022a``)


Datetime
++++++++

There are 2 type of date that can be encoded in a Kafka message:

- dates for git-like objects (:py:class:`swh.model.model.Revision` and
  :py:class:`swh.model.model.Release`): these dates are part of the hash
  computation used as identifier in the Merkle DAG. In order to fully support
  git repositories, a custom encoding is required. These dates (coming from the
  git data model) are encoded as a dictionary with:

  - ``timestamp`` [dict] POSIX timestamp of the date, as a dictionary with 2 keys
    (``seconds`` and ``microseconds``)

  - ``offset`` [int] offset of the date (in minutes)

  - ``negative_utc`` [bool] only True for the very edge case where the date has a
    zero but negative offset value (which does not makes much sense, but
    technically the git format permits)

  Example:

  .. code:: python

     {
       'timestamp': {'seconds': 1480432642, 'microseconds': 0},
       'offset': 180,
       'negative_utc': False
     }

  These are denoted as ``gitdate`` below.

- other dates (resulting of the |swh| processing stack) are encoded using
  msgpack's Timestamp_ extended type.

  These are denoted as ``timestamp`` below.

  Note that these dates used to be encoded as a dictionary (beware: keys are bytes):

  .. code:: python

     {
      b"swhtype": "datetime",
      b"d": '2020-09-15T16:19:13.037809+00:00'
     }


Person
++++++

:py:class:`swh.model.model.Person` objects represent a person in the |swh|
Merkle DAG, namely a :py:class:`swh.model.model.Revision` author or committer,
or a :py:class:`swh.model.model.Release` author.

:py:class:`swh.model.model.Person` objects are serialized as a dictionary like:

.. code:: python

   {
    'fullname': 'John Doe <john.doe@example.com>',
    'name': 'John Doe',
    'email': 'john.doe@example.com'
   }

For anonymized topics, :py:class:`swh.model.model.Person` entities have seen
anonymized prior to being serialized. The anonymized
:py:class:`swh.model.model.Person` object is a dictionary like:

.. code:: python

   {
    'fullname': <hashed value>,
    'name': null,
    'email': null
   }


where the ``<hashed value>`` is computed from original values as a sha256 of the
original's ``fullname``.




.. _Kafka: https://kafka.apache.org
.. _topic: https://kafka.apache.org/documentation/#intro_concepts_and_terms
.. _msgpack: https://msgpack.org/
.. _`extended type`: https://github.com/msgpack/msgpack/blob/master/spec.md#extension-types
.. _`Timestamp`: https://github.com/msgpack/msgpack/blob/master/spec.md#timestamp-extension-type
