.. _roadmap-current:
.. _roadmap-2023:

Roadmap 2023
============

(Version 1.0, last modified 2023-03-13)

This document provides an overview of the technical roadmap of the Software
Heritage initiative for the year 2023.

Live tracking of the roadmap implementation progress during the year is
available from a dedicated `GitLab board
<https://gitlab.softwareheritage.org/groups/swh/-/milestones?sort=name_asc>`_.

.. contents::
   :depth: 3
..

Collect
-------


Add support for write APIs features in GraphQL
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- `View milestone in GitLab <https://gitlab.softwareheritage.org/groups/swh/-/milestones/98>`__
- Lead: jayesh
- Priority: low

**Description:**

Add support for write APIs in GraphQL (eg: an API for save code now) in order to cover 100% of the REST API features in the GraphQL API.

**Includes work:**

- Implement write APIs
- Enforce authorization configuration for restricted access features

**KPIs:**

- GraphQL coverage of 100% of the REST API in production


Tooling for takedown notices
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- `View milestone in GitLab <https://gitlab.softwareheritage.org/groups/swh/-/milestones/56>`__
- Lead: lunar
- Priority: high

**Description:**

Set up a workflow to handle takedown requests and improve automation capabilities of the sysadmin tools for takedown notices processing.

**Includes work:**

- Set up a specification for workflow integration in swh-web
- Implement workflow integration
- Set up technical specification for sysadmin tooling
- Implement missing sysadmin tools (verification and automation)
- Create a sysadmin documentation for takedown notices

**KPIs:**

- Takedown notice handling integrated to swh-web
- Automated sysadmin tools for takedown notices processing


Automate add forge now
^^^^^^^^^^^^^^^^^^^^^^^

- `View milestone in GitLab <https://gitlab.softwareheritage.org/groups/swh/-/milestones/54>`__
- Lead: vsellier
- Priority: low

**Description:**

Set up automation capabilities on Add forge now to ease and facilitate the handling of Add forge now requests

**Includes work:**

- Automate ingestion process
- Automate add forge now workflow
- Setup and deploy automation process in staging
- Deploy automation process in production


**KPIs:**

- Automated Add forge now processing tools and wokflow in production


Minimize archival lag w.r.t. upstream code hosting platforms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- `View milestone in GitLab <https://gitlab.softwareheritage.org/groups/swh/-/milestones/53>`__
- Lead: olasd
- Priority: medium

**Description:**

Improve ingestion efficiency
Make lag monitoring dashboards easy to find (for decision makers)

**Includes work:**

- Implement git protocol V2 for Dulwich
- Optimize scheduling policies
- Optimize loaders

**KPIs:**

- Number of out of date repos (absolute and per platform)
- Total archive lag (e.g., in days)


Extend archive coverage
^^^^^^^^^^^^^^^^^^^^^^^^

- `View milestone in GitLab <https://gitlab.softwareheritage.org/groups/swh/-/milestones/52>`__
- Lead: ardumont
- Priority: medium

**Description:**

Add listers and loaders for not-yet-supported forges/package managers and VCS
Listers and loaders can be developed in house or contributed by external partners, e.g., via dedicated grants.

**Includes work:**

- Validate public review and deploy Listers and loaders pending in staging (Arch, AUR, Crates, Packagist, Rubygems, Fedora, Puppet, Hackage, Golang, Bower, Nix/Guix, CVS, pub.dev)
- Implement new listers and loader

**KPIs:**

- Number of deployed listers
- Number of deployed loaders


Preserve
--------


Explore possibility of replacing SHA1 with SHA1-DC
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- `View milestone in GitLab <https://gitlab.softwareheritage.org/groups/swh/-/milestones/112>`__
- Lead: olasd
- Priority: high

**Description:**

Mainstream platforms like GitHub now use SHA1-DC

**Includes work:**

- Study implications of aligning with the SHA1-DC adoption

**KPIs:**

- Decision/blockers whether to move to SHA1-DC


Regularly scrub journal, storage, and objstorage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- `View milestone in GitLab <https://gitlab.softwareheritage.org/groups/swh/-/milestones/103>`__
- Lead: vlorentz
- Priority: medium

**Description:**

Set up background jobs to regularly check - and repair when necessary - data validity, in all SWH data stores. This includes both blobs (swh-objstorage) and other graph objects (swh-storage) on all the copies (in-house, kafka, azure, upcoming mirrors, etc.)

**Includes work:**

- Implement storage scrubber for Cassandra
- Add scrubbing for the object storage
- Add metrics and Grafana dashboard for scrubbing process
- Automatically repair and recover objects found to be invalid

**KPIs:**

- List of scrubbers deployed in production
- Monitoring tools deployed in production
- Rolling report of operations per datastore including errors found and fixed at each iteration


Publicly available standard for SWHID version 1
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- `View milestone in GitLab <https://gitlab.softwareheritage.org/groups/swh/-/milestones/66>`__
- Lead: rdicosmo
- Priority: high

**Description:**

Publish a stable version of the SWHID version 1 specification, approved by a standard organization body.

**Includes work:**

- Publish publicly available standard
- Start ISO normalization for SWHID V1

**KPIs:**

- Published standard for SWHID version 1


SWH Mirror at GRNET
^^^^^^^^^^^^^^^^^^^^

- `View milestone in GitLab <https://gitlab.softwareheritage.org/groups/swh/-/milestones/65>`__
- Lead: douardda
- Priority: medium

**Description:**

Collaborate with GRNET to create a SWH Mirror

**Includes work:**

- Guidance and contribution to GRNET architecture and infrastructure choices
- Specific developments if necessary (to be determined according to the chosen technical solutions)
- Help to deployment

**KPIs:**

- validated architecture and first POC


SWH Mirror at Duisburg-Essen university
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- `View milestone in GitLab <https://gitlab.softwareheritage.org/groups/swh/-/milestones/64>`__
- Lead: douardda
- Priority: low

**Description:**

Collaborate with Duisburg-Essen university to create a SWH Mirror

**Includes work:**

- Guidance and contribution to UniDue architecture and infrastructure choices
- Specific developments if necessary (to be determined according to the chosen technical solutions)
- Developments of tools for Winery replication (for Ceph-based object storage)
- Help to deployment

**KPIs:**

- validated architecture and first POC


SWH Mirror at ENEA
^^^^^^^^^^^^^^^^^^^

- `View milestone in GitLab <https://gitlab.softwareheritage.org/groups/swh/-/milestones/62>`__
- Lead: douardda
- Priority: high

**Description:**

Collaborate with ENEA to create a SWH Mirror

**Includes work:**

- Finalize object storage copy
- Configure the stack for the mirror public deployment

**KPIs:**

- SWH Mirror deployed on ENEA infrastructure and publicly available


Mirrors tooling
^^^^^^^^^^^^^^^^

- `View milestone in GitLab <https://gitlab.softwareheritage.org/groups/swh/-/milestones/61>`__
- Lead: douardda
- Priority: high

**Description:**

Provide common features required the SWH mirrors

**Includes work:**

- Set up feature flags on the web app and test modules activation/deactivation
- Implement fallback mechanism for objstorage
- Dedicated CI for the mirroring stack

**KPIs:**

- Common features available for specific mirrors instances


Archive cold-copy at CINES via Vitam
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- `View milestone in GitLab <https://gitlab.softwareheritage.org/groups/swh/-/milestones/60>`__
- Lead: douardda
- Priority: medium

**Description:**

Perform a first complete copy of the archive stored in Vitam @ CINES
Maintain the copy up-to-date periodically (on a period TBD)

**Includes work:**

- Validate implementation of ORC format in Vitaam
- Run a Proof of Concept
- Run the complete copy @ CINES
- Configure/schedule the copy update process

**KPIs:**

- First copy stored in Vitam
- Updates calendar defined


Support archiving repositories containing SHA1 hash conflicts on blobs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- `View milestone in GitLab <https://gitlab.softwareheritage.org/groups/swh/-/milestones/58>`__
- Lead: olasd
- Priority: high

**Description:**

Enable the possibility to use multiple hash types for objects checksums in order to get rid of the limitations imposed by having SHA1 as a primary key for the object storage internally.

**Includes work:**

- Implement the remaining low-level layers (model and API are ready)

**KPIs:**

- Multiple hash storage facility in production
- Ability to archive git repos that contains sample SHAttered collisions blobs (they are currently detected and refused)


Share
-----


Propose Web UI sections for dedicated partner collections
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- `View milestone in GitLab <https://gitlab.softwareheritage.org/groups/swh/-/milestones/113>`__
- Lead: bchauvet
- Priority: medium

**Description:**

Design and test the creation of dedicated collections pages (list of origins associated to/provided by a partner)

**Includes work:**

- design a web ui feature for specific software collection (list of origins) based on custom criteria (intrinsic and/or extrinsic metadata)

**KPIs:**

- Specification and mockup for this feature


Create a cost-calculator in the Vault
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- `View milestone in GitLab <https://gitlab.softwareheritage.org/groups/swh/-/milestones/106>`__
- Lead: vlorentz
- Priority: medium

**Description:**

Implement a cost-calculator feature in swh-vault in order to estimate the cost of computing before cooking an artifact. The purpose of this feature is to prevent overload in some edge cases and possibly establish a rate-limiting system to avoid abusive usage of the vault.

**Includes work:**

- Design calculation rules
- Implement the cost-calculator
- Make it configurable according to the user profile

**KPIs:**

- Cost-calculation activated on swh-vault in production


Publish derived datasets
^^^^^^^^^^^^^^^^^^^^^^^^^

- `View milestone in GitLab <https://gitlab.softwareheritage.org/groups/swh/-/milestones/94>`__
- Lead: vlorentz
- Priority: medium

**Description:**

Setup tools to automate the publication of derived datasets, and generate specific datasets for research purposes throughout the year, on request by rdicosmo and zack

**Includes work:**

- Finalize and maintain the automation pipeline (Luigi) for datasets generation
- Build new datasets when requested

**KPIs:**

- Generation pipeline available in production
- Scheduled and regularly published derived datasets


Collect and index forge metadata
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- `View milestone in GitLab <https://gitlab.softwareheritage.org/groups/swh/-/milestones/91>`__
- Lead: vlorentz
- Priority: high

**Description:**

Collect and index metadata from more forges and package managers in order to expand metadata coverage.

**Includes work:**

- Provide a prioritized list of forges/package managers to process
- Improve the performance of indexers to reduce lag vs metadata collection
- Implement and deploy indexers for not supported forges/package managers

**KPIs:**

- number of new forges supported / % indexed for each
- number of new package managers supported / % indexed for each


Evaluate the storage of indexed metadata in a triple-store
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- `View milestone in GitLab <https://gitlab.softwareheritage.org/groups/swh/-/milestones/89>`__
- Lead: vlorentz
- Priority: medium

**Description:**

Evaluate the opportunity of storing indexed metadata in a triple store, instead of the actual ElasticSearch architecture, to prevent crashes due to embedded JSON-LD documents treated as regular JSON, and add support of relations between documents.

Therefore, I would like to try using a proper triple-store. [Virtuoso](https://virtuoso.openlinksw.com) in particular looks promising, as it support both SPARQL and full-text search.

**Includes work:**

- Try and evaluate a proper triple-store (Virtuoso) on a testing infrastructure
- According to the conclusions of the evaluation, decide whether to choose this triple-store solution

**KPIs:**

- Decision to switch to a triple-store for indexed metadata storage


Release a first version of the swh-scanner product
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- `View milestone in GitLab <https://gitlab.softwareheritage.org/groups/swh/-/milestones/72>`__
- Lead: bchauvet
- Priority: high

**Description:**

Industrialize and improve the swh-scanner CLI to provide a full-featured product ready for regular use.

**Includes work:**

- Improve the concurrency model on edge cases
- Set up an enhanced result dashboard
- Implement advanced filtering capabilities
- Provide an exhaustive documentation
- Add provenance information (depending on provenance progress)

**KPIs:**

- Release and announce a first version of swh-scanner


Webhook-based notification for long-running user tasks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- `View milestone in GitLab <https://gitlab.softwareheritage.org/groups/swh/-/milestones/71>`__
- Lead: anlambert
- Priority: high

**Description:**

Create a reusable event-based webhook architecture and implement it on adequate SWH features

**Includes work:**

- Identify technical issues and design options
- Specification and implementation of a standard core
- Implementation for origin visit
- Implementation for add forge now
- Implementation for save code now
- Implementation for vault cooking
- Implementation for deposit

**KPIs:**

- Number of services that support webhook-based notifications


Self-host Software Stories software stack
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- `View milestone in GitLab <https://gitlab.softwareheritage.org/groups/swh/-/milestones/70>`__
- Lead: bchauvet
- Priority: high

**Description:**

Deploy a `Software Stories instance <https://github.com/ScienceStories/swh-stories>`__ hosted on the SWH infrastructure

**Includes work:**

- Define and document the infrastructure requirements
- Deploy and document (Operations / backups / ...)
- Migrate the current stories to the SWH instance
- Establish the migration plan / redirection plan

**KPIs:**
- SWH stories site available
- Documentation written
- Current stories migrated to the SWH instance
- Public software stories instance migrated to the SWH instance



Design presentation of Metadata on Web UI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- `View milestone in GitLab <https://gitlab.softwareheritage.org/groups/swh/-/milestones/68>`__
- Lead: moranegg
- Priority: high

**Description:**

Design presentation of intrinsic and extrinsic metadata for any artifact on web UI and add linked data capabilities (Semantic Web solutions)

**Includes work:**

- Specify the expected use cases
- Design metadata view for Web UI
- Allow export of metadata (in multiple formats - APA/ BibTeX/ CodeMeta/ CFF)
- Assistance and contribution to CodeMeta
- Add linked data capabilities

**KPIs:**

- Specification and POC


Documentation
-------------


Provide a landing page for docs.s.o
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- `View milestone in GitLab <https://gitlab.softwareheritage.org/groups/swh/-/milestones/73>`__
- Lead: lunar
- Priority: high

**Description:**

Provide a user-friendly landing page for all documentation at docs.s.o, providing guidelines for each user type.

**Includes work:**

- Finalize and publish the landing page content
- Improve the organization of the left-column menus

**KPIs:**

- Landing page in production


Technical debt
--------------


Setup efficient and consistent swh-storage pagination
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- `View milestone in GitLab <https://gitlab.softwareheritage.org/groups/swh/-/milestones/96>`__
- Lead: jayesh
- Priority: high

**Description:**

Define and implement an efficient structure for pagination in the data sources for swh-storage.

Pagination in the data sources (eg storage) is not very consistent and client friendly. Defining and implementing an efficient structure will be a good improvement. This will also involve re-factoring some clients.

**Includes work:**

- Design an efficient pagination architecture
- Refactor obj-storage to implement the pagination
- Identify and refactor existing clients that use swh-storage pagination

**KPIs:**

- New pagination solution in production for swh-storage
- Existing clients updated to use this solution


Improve support for malformed git commits
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- `View milestone in GitLab <https://gitlab.softwareheritage.org/groups/swh/-/milestones/92>`__
- Lead: vlorentz
- Priority: high

**Description:**

Improve the git loader to make it able to deal with edge-case commits that cause Dulwich to crash due to unnecessary data validation.

**Includes work:**

- Fix all crashes of the git loader caused by malformed git objects
- Support commits whose "author" or "committer" field is missing

**KPIs:**

- ratio of crashes on commits ingestion by the git loader (before/after)


Tooling and infrastructure
--------------------------


Dynamic infrastructure
^^^^^^^^^^^^^^^^^^^^^^^

- `View milestone in GitLab <https://gitlab.softwareheritage.org/groups/swh/-/milestones/105>`__
- Lead: vsellier
- Priority: high

**Description:**

Setup a dynamically scalable infrastructure for Software Heritage services

**Includes work:**

- Setup an elastic workers infrastructure
- Configure Kubernetes clusters
- Monitoring/Alerting solution for container-based services
- Ingest the logs of the dynamic components into the current elk infrastructure

**KPIs:**

- Dashboard displaying the status of the dynamic components
  - Number of listers running
  - Number of loaders running
  - RPC services status
- Logs ingested and correctly parsed in kibana
- Clusters fully backuped



Use a common workflow management tool for swh-web
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- `View milestone in GitLab <https://gitlab.softwareheritage.org/groups/swh/-/milestones/100>`__
- Lead: lunar
- Priority: medium

**Description:**

Find and integrate a common workflow management tool in swh-web for future modules that will require a workflow logic (takedown notices process, user support, etc.)

**Includes work:**

- Investigate the existing tools, measuring advantages and drawbacks for each
- Integrate the most relevant tool in swh-web
- Document the usage with a sample module

**KPIs:**

- Integrated workflow tool, ready to use, in swh-web


Provide a management-friendly monitoring dashboard of services
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- `View milestone in GitLab <https://gitlab.softwareheritage.org/groups/swh/-/milestones/86>`__
- Lead: vsellier
- Priority: high

**Description:**

Provide a high-level and easy to find dashboard of running services with documented key indicators.

**Includes work:**

- Gather public site metrics
- Publish and document a dedicated dashboard
- Add links to it on common web applications (web app and docs.s.o)

**KPIs:**

- Indicators available for public sites status
- Indicators for archive workers status
- Indicators for archive behavior
- Main dashboard that aggregates the indicators
- Dashboard referenced in common web applications


Provenance in production
^^^^^^^^^^^^^^^^^^^^^^^^^

- `View milestone in GitLab <https://gitlab.softwareheritage.org/groups/swh/-/milestones/84>`__
- Lead: douardda
- Priority: high

**Description:**

Publish swh-provenance services in production, including revision and origin layers.

**Includes work:**

- Build and deploy content index based on a winnowing algorithm
- Filter provenance pipeline to process only tags and releases
- Setup a production infrastructure for the kafka-based revision layer (including monitoring)
- Refactor and process the origin layer
- Release provenance documentation

**KPIs:**

- Provenance services available in production
- % of archive covered


Scale-out objstorage in production as primary objstorage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- `View milestone in GitLab <https://gitlab.softwareheritage.org/groups/swh/-/milestones/83>`__
- Lead: olasd
- Priority: high

**Description:**

Have the Ceph-based objstorage for SWH (Winery) in production as primary storage and set up equivalent MVP in staging (maybe use the same Ceph cluster for this)

**Includes work:**

- Deploy Ceph objstorage/Winery on CEA infrastructure
- Benchmark Ceph-based objstorage
- Switch to Ceph-based objstorage as primary storage
- Handle Mirroring

**KPIs:**

- Ceph-based obj-storage in production


Cassandra in production as primary storage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- `View milestone in GitLab <https://gitlab.softwareheritage.org/groups/swh/-/milestones/82>`__
- Lead: vsellier
- Priority: high

**Description:**

Use Cassandra as primary storage in production, in replacement of PostgreSQL

**Includes work:**

- Finalize and validate the replayed data
- Install the new bare metal servers for staging and production
- Deploy a Cassandra-based production instance for tests
- Benchmark the Cassandra infrastructure
- Switch to Cassandra in production for primary storage

**KPIs:**

- Replayed data validated
- Live staging archive instance in parallel of the legacy postgresql instance
- Live production archive instance in parallel of the legacy postgresql instance
- Cassandra primary storage in staging
- Cassandra primary storage in production


Design and test a Continuous Deployment infrastructure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- `View milestone in GitLab <https://gitlab.softwareheritage.org/groups/swh/-/milestones/80>`__
- Lead: vsellier
- Priority: medium

**Description:**

Set up a Continuous Deployment infrastructure in order to improve bug detection and validate the future elastic infrastructure components

**Includes work:**

- Migrate away from Debian packaging for deployment (to pypi packages?)
- Build a docker image per deployable service
- Build the deployment tooling
- Reset and redeploy the stack after commits
- Execute acceptance tests
- Identify if a deployment can be done by the ci or needs human interaction (mostly detect if a migration is present)
- Integration tests

**KPIs:**

- Docker image build triggered by a new version deployed in pypi
- Docker image build by the CI
- Component versions updated by the CI
- Automatically redeployed staging on new release
- Staging / whatever environment testing before pushing to production


Design and test next generation CI Automation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- `View milestone in GitLab <https://gitlab.softwareheritage.org/groups/swh/-/milestones/79>`__
- Lead: olasd
- Priority: low

**Description:**

Design and tests solutions in order to improve the actual Continuous Integration tools to match the infrastructure evolutions and provide more features

**Includes work:**

- Actual CI state of the art and requirements specification
- Evaluation of a migration from Jenkins to GitLab CI (and effective migration if relevant)
- Code audit tools integration (static and/or dynamic analysis)

**KPIs:**

- Gitlab CI used or tested in one or more sysadmin projects
- Evaluation matrix (Pros/Cons) for a migration from jenkins to gitlab ci or other tool
- Pros/Cons to deploy a code audit tool


Graph export and graph compression in production
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- `View milestone in GitLab <https://gitlab.softwareheritage.org/groups/swh/-/milestones/59>`__
- Lead: vlorentz
- Priority: high

**Description:**

Have the graph compression pipeline running in production with less then a month of lag Deployment, hosting and pipeline tooling

**Includes work:**

- Add JVM monitoring
- Finish automation scripts
- Deploy on a dedicated machine

**KPIs:**

- Graph compression pipeline in production
- Last update date / number of updates per year

