.. _roadmap-current:
.. _roadmap-2022:

Roadmap 2022
============

(Version 1.0, last modified 2022-04-01)

This document provides an overview of the technical roadmap of the Software
Heritage initiative for the year 2022.

Live tracking of the roadmap implementation progress during the year is
available from a dedicated `Kanban board
<https://forge.softwareheritage.org/project/view/176/>`_.

.. contents::
   :depth: 3
..

Collect
-------

Extend archive coverage (2+2 loaders/listers)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Lead: ardumont
- Tags: coverage
- Task: `T4079 <https://forge.softwareheritage.org/T4079>`__
- Effort: variable, depending on the chosen listers/loaders (4PM ?)
- Priority: Medium

Deploy at least 2 additional loaders (of currently unsupported VCS/package formats) and 2 additional listers (of currently unsupported hosting platforms), expanding the coverage of the Software Heritage archive. Listers and loaders can be developed in house or contributed by external partners, e.g., via dedicated grants.

KPIs:

- Number of new loaders/listers deployed
- Number of origins archived/listed

Minimize archival lag w.r.t. upstream code hosting platforms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Lead: olasd
- Tags: performance, coverage
- Task: `T4080 <https://forge.softwareheritage.org/T4080>`__
- Effort: 3 PM
- Priority: High

Includes work:

- Quantify and monitor in real-time the lag, especially for major platforms (GitHub, GitLab.com, etc.)
- Improve ingestion efficiency (optimize loaders, especially the Git loader, optimize scheduling policies) - `T2207 <https://forge.softwareheritage.org/T2207>`__
- Make lag monitoring dashboards easy to find (for decision makers)

KPIs:

- Number of out of date repos (absolute and per platform)
- Total archive lag (e.g., in days)

Add forge now
^^^^^^^^^^^^^

- Lead: ardumont
- Tags: coverage
- Task: `T1538 <https://forge.softwareheritage.org/T1538>`__
- Effort: 3 PM
- Priority: High

Includes work:

Make it user-driven, simple, and efficient to fully and recurrently archive a new instance of an already supported code hosting platform.

- User-facing web form allowing any user to *propose* the archival of a new forge instance, and moderation web UI to validate archival requests before ingestion. `T4047 <https://forge.softwareheritage.org/T4047>`__
- Admin tooling and UI to deal with received submissions. `T4058 <https://forge.softwareheritage.org/T4058>`__
- Include free-from box suggestion form for forges that are not supported yet (to replace the currently poorly maintained `wiki page <https://wiki.softwareheritage.org/wiki/Suggestion_box:_source_code_to_add>`__). Possibly to be integrated with the user support system elsewhere in the roadmap.

KPIs:

- Number of forges/instances added

Integrate deposit with InvenioRDM
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Lead: moranegg
- Tags: 2021, coverage, deposit
- Task: `T2344 <https://forge.softwareheritage.org/T2344>`__
- Effort: 1-2 PM
- Priority: Medium

Includes work:

Deploy in production support for receiving source code deposits from InvenioRDM instances, and in particular the Zenodo instance.

- Extend CodeMeta vocabulary to qualify author relationships - `T2329 <https://forge.softwareheritage.org/T2329>`__
- Generalize usage of SWHID for referencing SWH archive objects - `T3034 <https://forge.softwareheritage.org/T3034>`__
- Analyze deposit-client on InvenioRDM compatibility - `T3549 <https://forge.softwareheritage.org/T3549>`__

KPIs:

- Complete on paper spec
- Number of deposits from an InvenioRDM instance (can be staging instance)
- Support deployed in InvenioRDM LTS

Admin tooling for takedown notices
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Lead: douardda
- Tags: 2021, legal
- Task: `T3087 <https://forge.softwareheritage.org/T3087>`__
- Effort: 3 PM
- Priority: High

Includes work:

Admin interface, private and public journal of operations.

- Low level support for blacklisting specified contents (not only URLs, also SWHIDs), with support for regexps
- Admin interface to add/remove entries from the blacklist
- A journal of these operations (what was added/removed, when and why, from the blacklist)
- A public webpage that maintains the list of accepted takedown notices

KPIs:

- Takedown tools deployed in production
- Number of processed takedown notices

Preserve
--------

Continuous data validation of all the data stores of SWH
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Lead: vlorentz
- Tags: integrity, monitoring
- Task: `T3841 <https://forge.softwareheritage.org/T3841>`__
- Effort: 2 PM
- Priority: Medium

Includes work:

- Set up background jobs to regularly check data validity in all SWH data stores.
- This includes both blobs (swh-objstorage) and other graph objects (swh-storage) on all the copies (in-house, kafka, azure, upcoming mirrors, etc.).
- Estimate ETA for scrubbing of the entire archive.

KPIs:

- Scrubbers deployed in production
- Monitoring tools deployed in production
- % of the archive scrubbed

Support archiving repositories containing SHA1 hash conflicts on blobs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Lead: olasd
- Tags: crypto
- Task: `T3775 <https://forge.softwareheritage.org/T3775>`__
- Effort: 1.5 PM
- Priority: High

Includes work:

This involves getting rid of the limitations imposed by having SHA1 as a primary key for the object storage internally.

KPIs

- Ability to archive git repos that contains sample SHAttered collisions blobs (they are currently detected and refused)

Up-to-date anonymized archive copy on Amazon S3 (except blobs)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Lead: seirl
- Tags: 2021, archivecopy
- Task: `T3085 <https://forge.softwareheritage.org/T3085>`__
- Effort: 3 PM
- Priority: Low

Includes work:

Periodic dumps of the (anonymized) Merkle graph on the Amazon public cloud.

- Fully automate export of the graph dataset
- Document how to export the graph edge dataset
- Define a scheduling periodicity

KPIs:

- Automatic exports scheduled
- S3 copy up to date w/ last scheduled export

Archive cold-copy at CINES via Vitam
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Lead: douardda
- Tags: 2021, archivecopy
- Task: `T3414 <https://forge.softwareheritage.org/T3414>`__
- Effort: 2PM
- Priority: Medium

Includes work:

Perform a first complete copy of the archive stored in Vitam @ CINES
Maintain the copy up-to-date periodically (on a period TBD)

KPIs:

- First copy stored in Vitam
- Updates calendar defined

Mirrors
^^^^^^^

- Lead: douardda
- Tags: 2021, mirror
- Task: `T3116 <https://forge.softwareheritage.org/T3116>`__
- Effort: 2 PM
- Priority: High

Includes work:

Deploy in production at least 2 mirrors.

- Finalize ENEA Mirror deployment
- Launch Snyk mirror project
- handle takedown notice synchronization ?
- Add feature flags on web UI

KPIs:

- ENEA Mirror in production
- Snyk mirror in production

Publicly available standard for SWHID version 1
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Lead: zack
- Tags: 2021, standard, swhid
- Task: `T3960 <https://forge.softwareheritage.org/T3960>`__
- Effort: 1 PM
- Priority: High

Includes work:

Publish a stable version of the SWHID version 1 specification, approved by a standard organization body.

KPIs:

- Published standard for SWHID version 1

SWHID version 2
^^^^^^^^^^^^^^^

- Lead: zack
- Tags: 2021, swhid, crypto
- Task: `T3134 <https://forge.softwareheritage.org/T3134>`__
- Effort: 4 PM
- Priority: Low

Includes work:

Complete on paper specification for SWHID version 2, including migrating to a stronger hash than SHA1.

- Complete on paper spec
- Aligned with work done on new git hashes
- Migration plan from/cohabitation with v1 (N.B.: we need to maintain SWHID v1 support forever anyway)
- Understand impact on internal microservice architecture (related to `T1805 <https://forge.softwareheritage.org/T1805>`__, in particular use SWHIDs everywhere (core SWHIDs, without qualifiers))
- Keep correspondence with v1 (there may be multiple v2 for one v1)
- Reviewed by crypto experts

KPIs:

- Written SWHID version 2 specification

Share
-----

Show metadata on Web UI
^^^^^^^^^^^^^^^^^^^^^^^

- Lead: vlorentz
- Tags: share, present, webui
- Task: `T4081 <https://forge.softwareheritage.org/T4081>`__
- Effort: 3 PM
- Priority: Low

Includes work:

Layer 1: show intrinsic and extrinsic metadata for artifact on web UI (design, implementation and deployment) Layer 2: add linked data capabilities (Semantic Web solutions)

- Design metadata view for Web UI
- Allow export of metadata (in multiple formats - APA/ BibTeX/ CodeMeta/ CFF)
- Assistance and contribution to CodeMeta

KPIs:

- Amount of metadata accessible on Web UI

Provide a state-of-the-art UX for web search
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Lead: jayesh
- Tags: search
- Task: `T3952 <https://forge.softwareheritage.org/T3952>`__
- Effort: 3 PM
- Priority: Medium

Includes work:

- Make the textual search language of archive.s.o a first-class citizen, including:
- Simplify syntax
- Conduct UX audits and user-testing of the web search UI
- Note: this does *not* include extending the type of data currently indexed and used for search (e.g., no filenames, no file content, etc.; they can come later/separately).

KPIs:

- SWH search using QL available in production
- Default user experience for archive.s.o textual searches

Self-host Software Stories software stack
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Lead: moranegg
- Tags: communication, wikidata, docs
- Task: `T3954 <https://forge.softwareheritage.org/T3954>`__
- Effort: 1 PM
- Priority: Medium

Includes work:

- Deploy `stories instance <https://github.com/ScienceStories/swh-stories>`__ in production on the SWH infrastructure.

KPIs:

- Software stories app deployed in production on SWH infra
- Content of current stories migrated to SWH instance

Webhook-based notification for long-running user tasks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Lead: anlambert
- Tags: deposit, vault, savecodenow
- Task: `T3955 <https://forge.softwareheritage.org/T3955>`__
- Effort: 1-3 PM
- Priority: High

Includes work:

- Create a reusable webhook architecture
- Add support for webhook-based notifications of long-running user tasks, including:

  - Deposit
  - Vault cooking
  - Save code now
  - Add forge now
  - Origin visit

KPIs:

- Number of services that support webhook-based notifications

Collect and index forge metadata
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Lead: vlorentz
- Tags: 2021
- Task: `T2202 <https://forge.softwareheritage.org/T2202>`__
- Effort: 9 PM
- Priority: High

Includes work:

- Collect extrinsic metadata from at least 1 forge (e.g., GitHub or GitLab project metadata)
- Index them into a sensible and searchable ontology/data model (could be codemeta, if suitable, or something else if needed)
- Cross-reference them to archived objects via SWHID
- Enable searches based on indexed metadata

KPIs:

- Number of forges supported
- Metadata fields collected

Prior art detection
^^^^^^^^^^^^^^^^^^^

- Lead: zack
- Tags: 2021
- Task: `T3136 <https://forge.softwareheritage.org/T3136>`__
- Effort: 5 PM
- Priority: Medium

Includes work:

Provide a full-circle user toolchain for prior-art detection in the realm of software source code.

- `revamp swh-scanner result dashboard <https://wiki.softwareheritage.org/wiki/Dashboard_UI_for_the_Code_Scanner_(GSoC_task)>`__
- Integrate with swh-provenance
- Integrate with swh-graph

KPIs:

- Release and announce a beta version of swh-scanner

Documentation
-------------

docs.s.o: provide a landing page, dispatching to devel/user/sysadmin/mirrors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Lead: bchauvet
- Tags: docs, sys-admin
- Task: `T3867 <https://forge.softwareheritage.org/T3867>`__
- Effort: 0.5 PM
- Priority: Medium

Includes work:

- Provide a nice landing page for all documentation at docs.s.o, dispatching by user type.
- Drop the redirection docs.s.o -> docs.s.o/devel.
- Depends on populating the /sysadm, /user and /mirrors parts.

KPIs:

- Landing page in production (https://docs.softwareheritage.org)

docs.s.o/sysadm: improve sysadmin documentation website
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Lead: vsellier
- Tags: docs, sys-admin
- Task: `T4082 <https://forge.softwareheritage.org/T4082>`__
- Effort: 1 PM
- Priority: Medium

Includes work:

- General goal: onboarding material + transparency about how we run the archive.
- Target user: team member, partners (e.g.mirror operators), or contributor who needs a clear view of the infrastructure architecture.

This task will be completed when it:

- Documents the configuration system of each component.
- Documents hardware architecture.
- Documents CI architecture (and other major services currently not documented).

KPIs:

- List of minimum documented items
- Number of available documented items

docs.s.o/user: bootstrap user documentation website
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Lead: moranegg
- Tags: docs, user
- Task: `T3972 <https://forge.softwareheritage.org/T3972>`__
- Effort: 2 PM
- Priority: Medium

Includes work:

The currently available user documentation only provides a FAQ. It should contain at least:

- An overall non-technical description of the archive and the core elements of its architecture
- A set of howto/getting started pages on main subjects (search, browse, push code in the archive, retrieve code and artifacts from the archive, metadata)
- Link to existing documentation on the main w.s.o. site as appropriate.

KPIs:

- List of minimum documented items
- Number of available documented items

High-level overview of available listers/loaders
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Lead: anlambert
- Tags: 2021, docs, sys-admin
- Task: `T3117 <https://forge.softwareheritage.org/T3117>`__
- Effort: 0.5 PM
- Priority: High

Includes work:

Publish a web page (under docs.s.o somewhere) providing a high-level overview of which listers/loaders are available (implemented, deployed, running, etc.) with pointers to the corresponding modules/implementations.

KPIs:

- Online web page

Technical Debt
--------------

Refactor swh-web code
^^^^^^^^^^^^^^^^^^^^^

- Lead: anlambert
- Tags: webapp, refactoring
- Task: `T3949 <https://forge.softwareheritage.org/T3949>`__
- Effort: 3 PM
- Priority: Medium

Includes work:

Have a smaller, more modular code base

- Split the public API code from the frontend code base
- Reduce code duplication (eg. between API and frontend)
- Externalize conversion utilities towards swh-core

KPIs:

- Separate repositories for frontend and web API

New public API (GraphQL + thin layer)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Lead: jayesh
- Tags: api, refactoring
- Task: `T4083 <https://forge.softwareheritage.org/T4083>`__
- Effort: 4 PM
- Priority: Medium

Includes work:

Provide a common unified (GraphQL based) public API

- Create a GraphQL based API
- Integrate actual API on graphQL

KPIs:

- GraphQL API in production

Organize 4+ short peer programming code-audit sprints
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Lead: bchauvet
- Tags: refactoring
- Task: `T3956 <https://forge.softwareheritage.org/T3956>`__
- Effort: 2.5 PM
- Priority: n/a (one 2-day sprint every 2 months)

Includes work:

- Go through the entire codebase and identify changes that should be done and dead code
- Correct identified issues or, failing that, document them with dedicated tasks
- Identify one theme per sprint

KPIs:

- Sprints done

Organize 4+ sentry-cleaning sprints
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Lead: bchauvet
- Tags: project-management, monitoring
- Task: `T3957 <https://forge.softwareheritage.org/T3957>`__
- Effort: 2.5 PM
- Priority: n/a (one 2-day sprint every 2 months)

Includes work:

We currently have a lot of `open Sentry issues <https://sentry.softwareheritage.org/organizations/swh/issues/>`__, but this is very raw data that isn’t very usable or visible. They should be cleaned up so that under normal conditions, the number of reported issues stays “minimal”.

KPIs:

- Sprints done
- Number of sentry issues (before/after)

Tooling and Infrastructure
--------------------------

GitLab migration
^^^^^^^^^^^^^^^^

- Lead: olasd
- Tags: 2021
- Task: `T2225 <https://forge.softwareheritage.org/T2225>`__
- Effort: 3 PM
- Priority: Medium

Includes work:

- Review the current workflow for the migration
- Prepare new team workflows for some “sample” projects
- Drive the migration to completion

  - Sysadmin projects migration (iteration #1)
  - Remaining projects migration (iteration #2)

KPIs:

- Number of migrated projects
- Phabricator switched to read-only

Polish developer-facing CI automation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Lead: olasd
- Tags: development environment, CI
- Task: `T4084 <https://forge.softwareheritage.org/T4084>`__
- Effort: 3 PM
- Priority: Low

Includes work:

- More automation to keep all linting / testing tools (black, flake8, tox, …) up to date and consistent
- CI support for multiple python versions (and possibly some dependency versions)
- Faster CI for diffs (e.g., consider use of `testmon <https://testmon.org/>`__ to only run tests affected by changes)
- Investigation of more linters or flake8 plugins
- Cypress performance (parallel testing)

KPIs:

- To be defined

Continuous Deployment
^^^^^^^^^^^^^^^^^^^^^

- Lead: vsellier
- Task: `T2231 <https://forge.softwareheritage.org/T2231>`__
- Tags: CI, CD, packaging
- Effort: 6 PM
- Priority: Low

Includes work:

Improve bug detection Validate the future elastic infrastructure components

- Migrate away from Debian packaging for deployment
- Build a docker image per deployable service
- Build the deployment tooling
- Reset and redeploy the stack after commits
- Execute acceptance tests

KPIs:

- Operational CD platform
- CD integrated to gitlab

Continuous Integration for sysadmin tools
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Lead: vsellier
- Tags: sysadmin, CI, tooling
- Task: `T3834 <https://forge.softwareheritage.org/T3834>`__
- Effort: 2 PM
- Priority: Low

Includes work:

Add CI for sysadmin tasks:

- Puppet configuration
- Vagrant projects
- Terraform plans
- Container (docker) image production

Create sustainable plan for hardware provisioning/rotation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Lead: olasd
- Tags: sysadmin, hardware
- Task: `T3959 <https://forge.softwareheritage.org/T3959>`__
- Effort: 0.5 PM
- Priority: High

Write a policy for hardware procurement with the following in mind:

- Make sure that we properly track our current pool of hardware, and its warranty status
- Make sure we don’t get surprised by lapsing warranties
- Make sure that we don’t end up having to renew a bunch of machines *all at once*
- Allow better budget previsions

KPIs:

- Shared documented policy

Elastic loaders and listers
^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Lead: ardumont
- Tags: sysadmin, performance, elasticity
- Task: `T3592 <https://forge.softwareheritage.org/T3592>`__
- Effort: 3 PM
- Priority: High

Includes work:

- Deploy the listers and loaders in containers
- Deploy on a couple of bare metal servers (?)
- Easily adapt the load to the resources and the waiting tasks

KPIs:

- Running elastic infrastructure in production for loaders and listers
- Cluster / elastic workers monitoring (number of running workers, statsd, …)

Cassandra in production as primary storage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Lead: vsellier
- Tags: 2021, storage, sysadmin
- Task: `T2214 <https://forge.softwareheritage.org/T2214>`__
- Effort: 3 PM
- Priority: High

Includes work:

- Have the Cassandra storage in production as primary storage
- Set up equivalent MVP in staging

KPIs:

- Cassandra primary storage in production

Scale-out objstorage in production as primary objstorage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Lead: olasd
- Tags: 2021, objstorage, sysadmin
- Task: `T3054 <https://forge.softwareheritage.org/T3054>`__
- Effort: 2 PM
- Priority: High

Includes work:

- Have the Ceph-based objstorage in production as primary storage
- Set up equivalent MVP in staging (maybe use the same Ceph cluster for this)

KPIs:

- Ceph-based obj-storage in production

Provenance in production
^^^^^^^^^^^^^^^^^^^^^^^^

- Lead: douardda
- Tags: 2021, provenance
- Task: `T3112 <https://forge.softwareheritage.org/T3112>`__
- Effort: 3 PM
- Priority: High

Includes work:

Have the provenance index in production with less then a month of lag
Set up equivalent MVP in staging

- Produce documentation
- Finalize revisions layer processing
- Investigate/solve revisions performance issues
- Process origins layer
- Flatten directories
- Production setup (deployment / scripts)
- Implement a querying API

KPIs:

- Revisions processed per second
- % of archive covered
- Published documentation

Graph compression in production
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Lead: seirl
- Tags: 2021, graph compression
- Task:`T2220 <https://forge.softwareheritage.org/T2220>`__
- Effort: 2 PM
- Priority: High

Includes work:

- Have the graph compression pipeline running in production with less then a month of lag
- Deployment, hosting and pipeline tooling
- Handle the situation for staging

KPIs:

- Graph compression pipeline in production
- Last update date / number of updates per year

Mirror tooling in production
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Lead: douardda
- Tags: 2021, mirror
- Task: `T4085 <https://forge.softwareheritage.org/T4085>`__
- Effort: 2 PM
- Priority: High

Includes work:

- Document the setup, the administration and the maintenance of a mirror (sprint + maintenance)
- Handle the situation for staging
- Organize the mirror operators community

KPIs:

- Mirror on staging
- Organized community

User support ticket system and process
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Lead: bchauvet
- Tags: support, user
- Task: `T3730 <https://forge.softwareheritage.org/T3730>`__
- Effort: 1 PM
- Priority: Medium

Includes work:

- Create a user-facing ticket system to support user requests and bug reports (e.g., a support@ address that automatically create support tasks that we can triage and follow)
- Define the process to:

  - Ensure some basic quality of service (e.g., time to first answer)
  - Pending tasks are not forgotten.

KPIs:

- User support feature available on web UI

Reliable user-level monitoring of services
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Lead: vsellier
- Tags: 2021, support, user
- Task: `T3129 <https://forge.softwareheritage.org/T3129>`__
- Effort: 1 PM
- Priority: High

Includes work:

High-level view of which services are running or not, and integration with status.softwareheritage.org

KPIs:

- Services dashboard in production
