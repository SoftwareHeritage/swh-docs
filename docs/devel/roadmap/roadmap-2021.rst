.. _roadmap-2021:

Roadmap 2021
============

(Version 1.0, last modified 05/04/2021)

This document provides an overview of the technical roadmap of Software Heritage for
2021.

The `Kanban board <https://forge.softwareheritage.org/project/board/160/query/all/>`_
is seen through our forge.


.. contents::
   :depth: 3
..


Collect
-------

Faster and more reliable save code now
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- tags: openscience
- task: `T3082 <https://forge.softwareheritage.org/T3082>`_
- lead: ardumont
- effort: 1 PM

Includes work:

- set up dedicated fast track pipeline for save code now
- improve save code now monitoring (user and admin)

Improve deposit integration, management and display
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- tags: openscience
- task: `T3128 <https://forge.softwareheritage.org/T3128>`_
- lead: moranegg
- effort: 3 PM

Includes work:

-  full invenioRDM integration `T2344 <https://forge.softwareheritage.org/T2344>`_
-  metadata only deposit `T2540 <https://forge.softwareheritage.org/T2540>`_

Save forge now
^^^^^^^^^^^^^^

- tags: expand
- task: `T1538 <https://forge.softwareheritage.org/T1538>`_
- lead: ardumont
- effort: 1 PM - tooling & process

Admin tooling for takedown notices (URLs)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- tags: contract, compliance
- task: `T3087 <https://forge.softwareheritage.org/T3087>`_
- lead: anlambert
- effort: 2 PM

Includes work:

- admin interface
- journal of operations
- web page with list of accepted TDN

Preserve
--------

Complete and up-to-date archive copy on S3
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- tags: stability
- task: `T3085 <https://forge.softwareheritage.org/T3085>`_
- lead: douardda
- effort: 1 PM

Includes work:

- live update of the objects
- regular dumps of the (anonymized) Merkle graph

Scale-out graph storage in production
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- tags: scalability
- task: `T2214 <https://forge.softwareheritage.org/T2214>`_
- lead: vlorentz
- effort: 3 PM

Includes work:


- Cassandra: `T1892 <https://forge.softwareheritage.org/T1892>`_ (*maybe with external help*)

Scale-out object storage prototype
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- tags: stability, scalability, *externalized*
- task: `T3054 <https://forge.softwareheritage.org/T3054>`_
- lead: dachary
- effort: 3 PM

Cold storage archive in Vitam instance at CINES
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- tags: contract
- task: `T3113 <https://forge.softwareheritage.org/T3113>`_
- lead: douardda
- effort: 4 PM

Mirrors
^^^^^^^

- tags: stability, scalability
- depends: scale-out object storage
- task: `T3116 <https://forge.softwareheritage.org/T3116>`_
- lead: douardda
- effort: 3 PM

Includes work:

- get up and running at least one mirror

SWHID v2
^^^^^^^^

- tags: stability, evolution, datamodel
- task: `T3134 <https://forge.softwareheritage.org/T3134>`_
- lead: zack
- effort: 6 PM

 Includes work:

- complete on paper spec
- align with new git hashes
- including migration plan from v1
- understand impact on internal microservice architecture
- keep correspondence with v1 (there may be multiple v2 for one v1!)
- reviewed by crypto experts

Integrity
^^^^^^^^^

- tags: stability, reliability
- task: `T3135 <https://forge.softwareheritage.org/T3135>`_
- lead: olasd
- effort: 2 PM

Includes work:

- making sure objects aren’t corrupted before insertion `T399 <https://forge.softwareheritage.org/T399>`_
- ... and that existing ones are not part of `T75 <https://forge.softwareheritage.org/T75>`_
- make corruption check periodically


Share
-----

swh-graph in production
^^^^^^^^^^^^^^^^^^^^^^^

- tags: scalability
- task: `T2220 <https://forge.softwareheritage.org/T2220>`_
- lead: zack
- effort: 2 PM

Efficient and reliable Vault download
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- tags: stability
- task: `T3096 <https://forge.softwareheritage.org/T3096>`_
- lead: vlorentz
- effort: 3 PM

Includes work:

- swh-graph may speed up a lot operations

Web API 2.0
^^^^^^^^^^^

- tags: reliability, interoperability
- task: `T2194 <https://forge.softwareheritage.org/T2194>`_
- lead: anlambert
- effort: 4 PM

Includes work:

- OpenAPI specification - implementation

Expose metadata and make them searchable
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- tags: openscience
- task: `T3097 <https://forge.softwareheritage.org/T3097>`_
- lead: vlorentz
- effort: 3 PM

Includes work:

- index extrinsic metadata in swh-search/Elasticsearch from the journal `T2073 <https://forge.softwareheritage.org/T2073>`_
- create API endpoint to access raw_extrinsic_metadata `T2938 <https://forge.softwareheritage.org/T2938>`_
- show metadata in the web UI `T2088 <https://forge.softwareheritage.org/T2088>`_

Full text search prototype
^^^^^^^^^^^^^^^^^^^^^^^^^^

- tags: feature, wishlist
- task: `T2204 <https://forge.softwareheritage.org/T2204>`_
- lead: anlambert
- effort: 3 PM

Includes work:

- requires integration with swh-graph and/or provenance index

Organize
--------

Collect extrinsic metadata
^^^^^^^^^^^^^^^^^^^^^^^^^^

- tags: compliance
- task: `T2202 <https://forge.softwareheritage.org/T2202>`_
- lead: vlorentz
- effort: 3 PM

Includesd work:
- working pipeline
- at least 1 instance running ClearlyDefined
- forge metadata (info on the main page, etc.)

Provenance in production
^^^^^^^^^^^^^^^^^^^^^^^^

- tags: contract, feature
- task: `T3112 <https://forge.softwareheritage.org/T3112>`_
- lead: zack
- effort: 6 PM

Prior art
^^^^^^^^^

- tags: compliance
- depends: provenance \| swh-graph in production
- task: `T3136 <https://forge.softwareheritage.org/T3136>`_
- lead: zack
- effort: 3 PM

Includes work:

- pinpoint origin of selected source code artifacts
- possibly integrated with swh-scanner

Measurement
-----------

Efficient archive counters (HyperLogLog)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- tags: measure, comm
- task: `T2912 <https://forge.softwareheritage.org/T2912>`_
- lead: vsellier
- effort: 1 PM

Distribution of origins by forge
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- tags: measure, comm
- task: `T3127 <https://forge.softwareheritage.org/T3127>`_
- lead: anlambert
- effort: 1 PM

Stats on regular crawling by forge
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- tags: measure, comm
- task: `T1363 <https://forge.softwareheritage.org/T1363>`_
- lead: olasd
- effort: 1 PM

Includes work:

- lag, periodicity, # of changes since last visit, etc.

View deposits per user (admin and user)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- tags: measure, support
- task: `T3128 <https://forge.softwareheritage.org/T3128>`_
- lead: ardumont
- effort: 1 PM

Reliable user-level monitoring of services
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- tags: stability
- task: `T3129 <https://forge.softwareheritage.org/T3129>`_
- lead: vsellier
- effort: 2 PM

Includes work:

- status.softwareheritage.org

Documentation
-------------

Write use case-specific documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- tags: comm, web, doc
- task: `T2234 <https://forge.softwareheritage.org/T2234>`_
- lead: moranegg
- effort: 2 PM

Includes FAQ for: - users - ambassadors

Improve quality of code documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- tags: doc, *externalized*
- task: TODO
- lead: TBD
- effort: 2PM

Includes work:

- doc(string) audit - team training about doc writing

Documentation strategy
^^^^^^^^^^^^^^^^^^^^^^

- tags: doc
- task: `T2624 <https://forge.softwareheritage.org/T2624>`_
- lead: moranegg
- effort: 1 PM

Includes work:

- respective role of docs.s.o, wiki, www.s.o, etc.

Community
---------

Tooling for fundraising campaigns
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- tags: web
- task: `T3077 <https://forge.softwareheritage.org/T3077>`_
- lead: anlambert
- effort: 1 PM

Dedicated page to list status of supported listers/loaders
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- tags: web, doc
- task: `T3117 <https://forge.softwareheritage.org/T3117>`_
- lead: anlambert
- effort: 1 PM

Includes work:

- `T1870 <https://forge.softwareheritage.org/T1870>`_
- design web page
- process to maintain up to date
- make clearly visible and link to Sloan subgrants

Tooling
-------

Migration to GitLab
^^^^^^^^^^^^^^^^^^^

- tags: forge, development
- task: `T2225 <https://forge.softwareheritage.org/T2225>`_
- lead: olasd
- effort: 1PM

