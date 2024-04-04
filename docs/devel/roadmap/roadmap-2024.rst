.. _roadmap-current:
.. _roadmap-2024:

Roadmap 2024
============

(Version 1.0, last modified 2024-03-22)

This document provides an overview of the technical roadmap of the Software
Heritage initiative for the year 2024.

.. contents::
   :depth: 3
..

License identification
----------------------

Design a data model for license information
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: medium
- Tags: Licence detection, SWH Sec

**Description:**

Integrate license information to the Software Heritage Data Model, covering all the use cases and levels of license detection

**Includes work:**


- Review state of the art
- Define or identify an ontology for license information
  - must take into account the ability to track license changes over time (including a project changing license without actually changing each files)
- Design and implement the model

**KPIs:**

- Updated data model deployed in production

Collect license information from external platforms (as extrinsic metadata)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: high
- Tags: Licence detection

**Description:**

Collect extrinsic metadata about license from platforms when available (GitHub, package managers..)

**Includes work:**

- Identify the platforms that provide license information
- Update related loaders to collect the license data

**KPIs:**

- Number of platforms that provide license information
- Number of origins for which license metadata has been collected

Mine license information from the archive (as intrinsic metadata)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: high
- Tags: Licence detection

**Description:**

Update indexers in order to generalize file scans for license information with latest tools.
This approach is not exhaustive, because some files do not contain relevant information

**Includes work:**

- Select the most accurate code-scanning engine for license detection (ScanCode, ..). Different strategies might be required for different levels (e.g. scan per project, or scan per file).
- Update the actual license detection indexer
- Deploy and run the updated indexer

**KPIs:**

- Number of contents indexed per license type

Documentation
-------------

Review existing documentation according to identified personas
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: medium
- Tags:

**Description:**

The existing documentation is fairly extensive but somewhat unfocused. There is work scheduled to come up with personas to reflect on various Software Heritage stakeholders. Once that work is done, the existing documentation should be reviewed to identify who could be interested in which parts.

**Includes work:**

- Review each piece of documentation.
- Tag each page with the personas that could be interested.
- Identify undocumented aspects.
- Perform “low-hanging fruit” changes in the documentation.

**KPIs:**

- Pages of the documentation tagged with a set of personas.
- List of areas lacking documentation.
- Update of the documentation landing page to better fit the different personas.

SWH Scanner
-----------

Release a first version of the swh-scanner product
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: high
- Tags: Scanner

**Description:**

Industrialize and improve the swh-scanner CLI to provide a full-featured product ready for regular use.
Octobus is handling a bunch of improvements under a NGI Search grant.

**Includes work:**


- Improve industrialization and portability
- Improve HTTP querying capabilities
- Identify content (origin, version, CVE, licence)
- Handle Exclusion patterns + VCS ignore definitions
- Improve configuration and documentation
- Implement progress indicators
- Provide an enhanced result dashboard

**KPIs:**

* Release and announce a first version of swh-scanner

SWH Sec
-------

Large scale archives retrieval (vault)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: medium
- Tags: SWH Sec

**Description:**

Integrate massive caching facilities to the vault and setup a storage infrastructure in order to enable large-scale recovery of numerous projects

**Includes work:**

* Specify heuristics for vault pre-cooking strategies
* Design and implement vault pre-cooking services
* Design the infrastructure requirements for cooking and storage
* Deploy the vault caching solution in production

**KPIs:**

* Vault caching system in production
* Number of project cooked and stored in the cache

Certified Deposit
-----------------

Specify requirements for certified deposit
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: low
- Tags: Certified deposit

**Description:**

Specify the functional and technical requirements to create a certified timestamped deposit service

**Includes work:**

- Interview stakeholders
- Identify and describe the use cases
- Review state of the art of certified timestamping
- Specify the technical requirements

**KPIs:**

- Validated specification

Institutional Portal
--------------------

Implement and deploy the institutional portal
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: medium
- Tags: Institutional portal

**Description:**

Implement and deploy the software artifacts for the Software Heritage Institutional Portal

**Includes work:**

* Implement the backend services and APIs
* Implement the web UI components
* Setup a staging environment
* Setup the production infrastructure
* Deploy in production

**KPIs:**

* Institutional portal operational in production
* Number of portal instances

Design software architecture for the institutional portal
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: medium
- Tags: Institutional portal

**Description:**

Design the software architecture and UI/UX for the SWH institutional portal

**Includes work:**

* Specify the UI/UX for an configurable webapp according to the specified use cases
* Design the required APIs
* Design the software architecture
* Specify the infrastructure requirements

**KPIs:**

* Validated UI mockup
* Validated technical specification

Specify requirements for institutional portal
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: high
- Tags: Institutional portal

**Description:**

Specify the requirements for a Software Heritage Institutional Portal, to present, qualify and extract software catalogs for specific entities (institutions, administrations, ..)

**Includes work:**

- Identify the categories of institutions that could require an institutional portal
- Collect and analyse each institutions requirements
- Specify use cases for a generic specification

**KPIs:**

- List of described use cases
- Generic specification for a Software Heritage Institutional Portal

Mirrors
-------

Documentation for mirror operators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: low
- Tags: Mirrors

**Description:**

Publish a comprehensive documentation for mirror operators

**Includes work:**

- Update the existing mirrors documentation
- Publish and share the updated documentation

**KPIs:**

- Published and up-to-date mirrors-operating documentation

Mirror tooling for scrubbing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: medium
- Tags: Mirrors

**Description:**

Implement srubbing tools to control the integrity of the mirrors replayed data

**Includes work:**

- Implement a scrubber for ENEA mirror

**KPIs:**

- Coverage of ENEA archive scrubbed

Mirror tooling for mailmap
^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: high
- Tags: Mirrors

**Description:**

Validate a policy and implement tools for mailmaps in the mirrors

**Includes work:**

- Specify and validate the mailmap policy for mirrors
- Validate whether the personal data transfer is ok for existing requests, preempt the issue for further requests
- Design and implement tools for mirrors

**KPIs:**

- Mailmap tools in production on active mirrors

Mirror tooling for takedown
^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: high
- Tags: Mirrors

**Description:**

Setup SWH mirrors tooling for takedown requests in accordance with the [documented process](https://docs.softwareheritage.org/sysadm/mirror-operations/takedown-notices.html).

**Includes work:**

- Design a workflow for a secure transfer of takedown requests data to mirrors
- Implement the workflow and deploy the solution for existing mirrors
- Provide mirrors with the SWH tools for takedown requests processing

**KPIs:**

- Takedown notification pipeline in production for active mirrors
- Takedown processing tools available for active mirrors
- Usage statistics

SWH Mirror at Duisburg-Essen university
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: medium
- Tags: Mirrors

**Description:**

Collaborate with Duisburg-Essen university to create a SWH Mirror

**Includes work:**

* Guidance and contribution to UniDue architecture and infrastructure choices
* Specific developments if necessary (to be determined according to the chosen technical solutions)
* Developments of tools for Winery replication (for Ceph-based object storage)
* Help to deployment

**KPIs:**

* validated architecture and first POC

Mirror instance at GRNET
^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: high
- Tags: Mirrors

**Description:**

Collaborate with GRNET to create a SWH Mirror

**Includes work:**

* Guidance and contribution to GRNET architecture and infrastructure choices
* Specific developments if necessary (to be determined according to the chosen technical solutions)
* Help to deployment

**KPIs:**

* validated architecture and first POC

SWH.org Website
---------------

Refactor the architecture of the SWH website
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: high
- Tags: SWH.org website

**Description:**

Refactor the architecture of the SWH Wordpress website, in order to integrate the latest upgrades and integrate new features to ease the content edition and management.
Ideally it should use no or a very limited amount of extensions (for ease of self-maintainance). This migration work will be outsourced to an external provider.

**Includes work:**

- Specify the technical and functional requirements
- Cleanup the actual wordpress (unused pages and categories)
- Update the testing platform to match the production website
- Coordinate and validate the work of the provider

**KPIs:**

- Upgraded website in production
- New features available in production

SWH Archive Website
-------------------

Setup a Software Citation UI feature
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: high
- Tags: SWH archive website

**Description:**

Provide users with a web UI feature that enables to generate and export citations for Software artifacts (SWHID) in multiple formats, and display the citation requests per project

**Includes work:**

- Design the right interface
- Implement the UI feature in swh-web
- Display the number of citation requests for a project

**KPIs:**

- Available user-friendly UI for Software citation
- Supported citation formats
- Number of citation requests per project

Design presentation of Metadata on Web UI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: medium
- Tags: SWH archive website

**Description:**

Design presentation of intrinsic and extrinsic metadata for any artifact on web UI and add linked data capabilities (Semantic Web solutions)

**Includes work:**

* Specify the expected use cases
* Design metadata view for Web UI
* Allow export of metadata (in multiple formats - APA/ BibTeX/ CodeMeta/ CFF)
* Assistance and contribution to CodeMeta
* Add linked data capabilities

**KPIs:**

* Specification and POC

Takedown notice management UI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: high
- Tags: Mirrors, SWH archive website

**Description:**

Set up a workflow to handle takedown requests, manageable via a web UI

**Includes work:**

* Validate the takedown workflow specification
* Implement a web UI using a common workflow management tool (see product-management/swh-archive-website#3)
* Specify the mechanism to trigger the takedown through the web UI, taking into account that a service able to remove data from the archive requires a lot of care

**KPIs:**

* Takedown notice handling integrated to swh-web

SWH Core Platform
-----------------

Automate the production and publication of derived datasets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: high
- Tags: SWH Sec

**Description:**

Provide tooling for an automated production and publishing of derived datasets

**Includes work:**

- Design and implement the required automation tools
- Setup and configure an automation pipeline
- Provide a dashboard for monitoring

**KPIs:**

- Number of derived datasets automatically published

Map software versions to objects in the archive
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: medium
- Tags: SWH Sec, Scanner

**Description:**

Several key use cases require to be able to identify objects in the archive related to specific software versions.
This mapping needs to be implemented in the archive

**Includes work:**

- Design and implement updates on the data model to store software version information
- Specify heuristics and methods to establish the mapping between a software version and an object in the archive
- Implement and run the tools to store the information

**KPIs:**

- Number of software and versions identified in the archive

Investigate on forge discovery automation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: low
- Tags:

**Description:**

Investigate on solutions for forges discovery automation, based on IP scanning tools

**Includes work:**

- Identify and benchmark available tools
- Setup a POC

**KPIs:**

- POC

Precompute relevant characteristics of the graph
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: medium
- Tags:

**Description:**

Compute and store relevant characteristics of the graph, including size estimations and depth.

For each node:

- expanded size (size of cooking as a directory/tarball)
- effective/de-duplicated size (size of cooking as a git-bare repo)
- subgraph size (number of nodes + edges)
- depth of the subgraph
- depth of the subgraph made of objects only of the same type *eg. only commits* (generation number)

**Includes work:**

* Design and implement the required data model upgrades
* Design and implement tools for computing the actual graph
* Design and implement a solution to compute data in flight

**KPIs:**

* % of the graph computed

Improve ingestion efficiency
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: medium
- Tags: SWH Sec

**Description:**

Improve ingestion efficiency to reduce the lag on major forges

**Includes work:**

- Optimize loaders
- Optimize scheduling policies

**KPIs:**

- Number of out of date repos (absolute and per platform)
- Total archive lag (e.g., in days)

Design and implement a unified software datamodel
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: medium
- Tags: Licence detection, SWH Sec

**Description:**

Create a unified data model to integrate software-related metadata (licence, CVE, issues, pull requests, discussions, comments...) for indexing, querying and retrieval.

**Includes work:**

- Design a comprehensive and extensive data model (maybe drawing inspiration from or reusing ForgeFed specifications)
- Implement the model in the SWH data model storage architecture

**KPIs**

- types of data stored in the model

Deploy a unified software data model storage infrastructure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: medium
- Tags: Licence detection, SWH Sec

**Description:**

Establish a scalable, robust and sustainable infrastructure to support the enrichment and intensive use of the Software Heritage archive for software-related metadata.

**Includes work:**

- Identify and study possible architectural solutions for a unified model storage
- Validate and design a solution for a unified software data model storage architecture
- Specify and validate the required infrastructure for unified software data model storage
- Deploy the required infrastructure for unified software data model storage

**KPIs:**

- Infrastructure available in production
- Performance indicators for massive queries

Enrich the archive with CVE metadata
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: medium
- Tags: SWH Sec

**Description:**

Integrate CVE metadata in the archive.

**Includes work:**

- Design and implement a model to store CVE metadata
- Design and implement a crawler to collect CVE metadata
- Ingest the CVE metadata

**KPIs:**

- % of CVE ingested in the archive

Enable inclusion filters in listers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: low
- Tags:

**Description:**

Actual listers only enable to define exclusion filters (ex: archive all origins but those from a given directory).

In some cases, we need to apply inclusion filters (ex : archive only origins located in a given  directory)

**Includes work:**

- Design and implement an inclusion filter for all relevant listers

**KPIs:**

- Number of inclusion filters applied in production

Recover the ingestion backlog
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: medium
- Tags: SWH Sec

**Description:**

Increase the horsepower for ingestion capacity in order to recover the ingestion backlog, temporarily using a large-scale computing platform.

**Includes work:**

- Specify infrastructure requirements to deploy as many loaders as possible (wrt the storage bandwidth capcity)
- Deploy the ingestion tooling on the infrastructure
- Run the ingestion

**KPIs:**

- GitHub lag recovered
- Amount of resources used (CPU time, duration..)

Implement rate-limiting in swh-vault
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: medium
- Tags:

**Description:**

Implement a rate-limiting mechanism in swh-vault based on the computed size estimations of the nodes before cooking. The purpose of this feature is to prevent overload in some edge cases and possibly establish a rate-limiting system to avoid abusive usage of the vault.

**Includes work:**

* Implement the cost-calculator
* Implement the rate-limiting
* Make it configurable according to the user profile

**KPIs:**

* Rate-limiting activated on swh-vault in production
* Number of rejected cooking requests
* Number of cooked projects

Cassandra in production as primary storage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: high
- Tags:

**Description:**

Use Cassandra as primary storage in production, in replacement of PostgreSQL

*2023 history: https://gitlab.softwareheritage.org/groups/swh/-/milestones/82#tab-issues*

**Includes work:**

* Benchmark the Cassandra infrastructure
* Switch to Cassandra in production for primary storage

**KPIs:**

* Replayed data validated
* Live staging archive instance in parallel of the legacy postgresql instance
* Live production archive instance in parallel of the legacy postgresql instance
* Cassandra primary storage in staging
* Cassandra primary storage in production

Scale-out objstorage in production as primary objstorage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: high
- Tags:

**Description:**

Have the Ceph-based objstorage for SWH (Winery) in production as primary storage and set up equivalent MVP in staging (maybe use the same Ceph cluster for this)

*2023 history: https://gitlab.softwareheritage.org/groups/swh/-/milestones/83#tab-issues*

**Includes work:**

* Benchmark Ceph-based objstorage
* Switch to Ceph-based objstorage as primary storage
* Handle Mirroring

**KPIs:**

* Ceph-based obj-storage in production as primary storage

Extend archive check and repair tools
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: high
- Tags:

**Description:**

Set up background jobs to regularly check - and repair when necessary - data validity, in all SWH data stores. This includes both blobs (swh-objstorage) and other graph objects (swh-storage) on all the copies (in-house, kafka, azure, upcoming mirrors, etc.)

*2023 history: https://gitlab.softwareheritage.org/groups/swh/-/milestones/103#tab-issues*

**Includes work:**

* Add scrubbing for the object storage
* Add metrics and Grafana dashboard for scrubbing process
* Automatically repair and recover objects found to be invalid (fixers)

**KPIs:**

* List of scrubbers deployed in production
* Monitoring tools deployed in production
* Rolling report of operations per datastore including errors found and fixed at each iteration

Support archiving repositories containing SHA1 hash conflicts on blobs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: high
- Tags:

**Description:**

Enable the possibility to use multiple hash types for objects checksums in order to get rid of the limitations imposed by having SHA1 as a primary key for the object storage internally.

**Includes work:**

- Add tests on multiplexed object storages with different primary keys
- Deployment of sha256-based swh.objstorage at CEA
- Migrate swh.journal to use composite object keys for the content topic

**KPIs:**

* Multiple hash storage facility in production
* Ability to archive git repos that contains sample SHAttered collisions blobs (they are currently detected and refused)

Release a Bulk On-demand Archival feature
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: high
- Tags:

**Description:**

Provide a solution for bulk archival of large amounts of origins, using the same logic as Save Code Now but different queues in order to avoid swamping the Save Code Now queue, whose purpose is to almost instantly archive a single origin at a time.

**Includes work:**

- Specify the user requirements
- Design a technical solution
- Implement the tooling and an API
- Define the access restrictions to the feature
- Deploy the solution in production

**KPIs:**

- Total number of origins archived using bulk save code now
- Average number of origins per bulk request

Design and implement a provenance search API v1
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: medium
- Tags: Scanner

**Description:**

Provide an API that enables to retrieve the probable first origin for a given content, based on swh-provenance and swh-graph.

**Includes work:**

- Validate the provenance index data
- Design the provenance API endpoints
- Implement the provenance REST API and the required backend APIs
- Design and deploy a provenance infrastructure in production
- Deploy the Provenance REST API v1 in production

**KPIs:**

- API available in production

Provide an executive-friendly monitoring of services
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: low
- Tags:

**Description:**

Provide a high-level and easy to find dashboard of running services with documented key indicators.

**Includes work:**

* Gather public site metrics
* Publish and document a dedicated dashboard
* Add links to it on common web applications (web app and docs.s.o)

**KPIs:**

* Indicators available for public sites status
* Indicators for archive workers status
* Indicators for archive behavior
* Main dashboard that aggregates the indicators
* Dashboard referenced in common web applications

Graph export and graph compression in production
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: high
- Tags: SWH Sec

**Description:**

Have the graph compression pipeline running in production with less then a month of lag Deployment, hosting and pipeline tooling

*2023 history: https://gitlab.softwareheritage.org/groups/swh/-/milestones/59#tab-issues*

**Includes work:**

* Finish the refactoring (rewriting in Rust)
* Setup an automatic scheduled generation
* Provide a dashboard for monitoring

**KPIs:**

* Graph compression pipeline in production
* Last update date / number of updates per year

Setup swh webhook for vault cooking
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: low
- Tags: SWH archive website

**Description:**

Implement a webhook for vault cooking based on swh-webhooks architecture

**Includes work:**

- Write and validate a specification
- Design the user interface to configure the webhook in the SWH webapp
- Implement and deploy the solution

**KPIs:**

- Webhook deployed in production
- Usage statistics

Setup swh webhook for Deposit
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: low
- Tags: SWH archive website

**Description:**

Implement a webhook for deposit based on swh-webhooks architecture

**Includes work:**

- Write and validate a specification
- Design the user interface to configure the webhook in the SWH webapp
- Implement and deploy the solution

**KPIs:**

- Webhook deployed in production
- Usage statistics

Sysadmin tooling for Takedown notices
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: high
- Tags:

**Description:**

The swh-alter module has been developed to improve automation capabilities of the sysadmin tools for takedown notices processing.
It's a CLI tool that provides an admin interface for takedown actions, aiming at covering deletion capabilities for both the storage (Postrges, Cassandra, Kafka journal client) and the object storage (ZFS, Ceph/Winery, Azure and S3). It also provides an encrypted recovery bundle mechanism to be able to rollback deletion upon error.

**Includes work:**

- Wire deletion in Elastic Search
- Wire deletion on Azure and S3
- End-to-end testing on staging
- Configure for production environment

**KPIs:**

* Production-ready sysadmin swh-alter tooling
* Number of takedown requests processed using swh-alter
