.. _roadmap-current:
.. _roadmap-2025:

Roadmap 2025
============

(Version 1.0, last modified 2025-04-24)

This document provides an overview of the technical roadmap of the Software
Heritage initiative for the year 2025.

.. contents::
   :depth: 3
..

This year, our roadmap is focused on three main objectives:

- Enlarge the archive: archive more content and be able to archive even more
- Enrich the archive: add new data about the archive content
- Empower archive users: propose new ways to access the archive to allow more
usage

It is mostly driven by several projects:

- CodeCommons: https://codecommons.org/
- SWH-Sec: https://www.softwareheritage.org/2023/04/07/enhancing-cybersecurity-through-swh/
- OSPO-Radar: https://www.softwareheritage.org/2025/04/02/ospo-radar-project-launch/

Software Heritage core development team is divided in four work groups:
* Interfaces: responsible for API and UI/UX
* Data: responsible for building and analyzing datasets
* Archive: responsible for archiving forges and package indices
* Ops: responsible for the infrastructure and the platform running our services

Many items of this roadmap are handled by other teams involved with us in the
CodeCommons and SWH-Sec projects. Some items tagged "Next" are not prioritized
this year but kept here for next year or if other items are delivered faster.



Interfaces work group
---------------------

Coar Notify
^^^^^^^^^^^

- Priority: High
- Tags: Interfaces Work Group, FAIR, Deposit, Enlarge

**Description**

Implement a new API relying on COAR Notify protocol to add new content
to archive or to link content to metadata

**Includes work**

- Implement and deploy new API
- Document it and test it with user
- Add requirements for production usage (monitoring, alerting,
   integration tests)

**KPIs**

- New API
- User can push data with it

Institutional portal (aka OSPO Radar)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: Medium
- Tags: Interfaces work group, Empower

**Description**

Set up an Institutional Portal, a UI feature aiming to present, qualify
and extract software catalogs for specific entities (institutions,
administrations, ..)

**Includes work**

- Gather key users and collect requirements
- Design the specification
- Implement and deploy

**KPIs**

- Institutional portal deployed in production
- Number of user institutions
- Number of origins per institution

Rethink Archive UI
^^^^^^^^^^^^^^^^^^

- Priority: Medium
- Tags: Interfaces Work Group, Empower

**Description**

The main way to access the Software Heritage archive is the user
interface exposed at https://archive.softwareheritage.org The current
interface has a few drawbacks. Some information are not easily
accessible, for instance metadata. It is also difficult to see
connections between origins, for instance which origins share a given
file. We want to think about archive UI/UX and design new features that
we want to add in the future.

**Includes work**

- List easy and hard features to add
- For hard features, describe requirements to make them accessible.
- Draw some design of what we would expect
- Prepare a plan on how to build and release them

**KPIs**

- List of features
- Tasks decomposition to build them


Website needs love
^^^^^^^^^^^^^^^^^^

- Priority: Medium
- Tags: Interfaces Work Group, Empower

**Description**

Our institutional website, www.softwareheritage.org, and our blog need
some rework to ease communication work and increase our reach.

**Includes work**

- Simplify some internal development on the website
- Add some new required plugins

**KPIs**


Expose CVE through Scanner
^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: Low
- Tags: Interfaces work group, SWH-Scanner, Empower, Next

**Description**

Add a feature to SWH Scanner that allows to show CVEs related to scanned
source code, based on CVE information collected in the Software Heritage
archive

**Includes work**

- Design, implement and deploy an api to query CVE information
- Implement a “show CVE” feature in swh-scanner

**KPIs**

- New swh-scanner version in production embedding the “show CVE”
   feature


Review existing documentation according to identified personas
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: Low
- Tags: Interfaces Work Group, Empower, Next

**Description**

The existing documentation is fairly extensive but somewhat unfocused.
There is work scheduled to come up with personas to reflect on various
Software Heritage stakeholders. Once that work is done, the existing
documentation should be reviewed to identify who could be interested in
which parts.

**Includes work**

- Review each piece of documentation.
- Tag each page with the personas that could be interested.
- Identify undocumented aspects.
- Perform “low-hanging fruit” changes in the documentation.

**KPIs**

- Pages of the documentation tagged with a set of personas.
- List of areas lacking documentation.
- Update of the documentation landing page to better fit the different personas.


Archive work group
------------------

Improve ingestion efficiency
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: Medium
- Tags: CodeCommons, Enlarge, Archive Work Group, Externals

**Description**

GitHub growth is faster than Software Heritage’s current ingestion
capacities, resulting in a lag of more than 140 million origins. In
order to stay an up-to-date archive after the lag catch up, we need to
improve our ingestion efficiency and optimize even more our platform.

**Includes work**

- Measure current bottlenecks
- Plan and implement solution to these bottlenecks

**KPIs**

- Number of ingested origins per unit of time

Support archiving repositories containing SHA1 hash conflicts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: Medium
- Tags: Enlarge, Archive Work Group

**Description**

SHA1 is used to identify duplicated files but this hash function is now
fragile and hash collisions can be crafted. Those hash collisions are of
particular interest and we want to be able to archive them.

**Includes work**

- Archive repositories with hash conflicts in winery storage
- Analyze possibility for other object storages and implement it if
   possible

**KPIs**

Improve Object Storage
^^^^^^^^^^^^^^^^^^^^^^

- Priority: Medium
- Tags: Enlarge, Archive Work Group

**Description**

Our current object storage, winery, starts to show some limitations. We
are reaching limits in scalability and some large scale access patterns
are complicated. Some ongoing studies show that we may improve
compression rate by clustering similar files together.

**Includes work**

- Follow and help studies on object storage compression
- Propose and bench solutions for improved object storage
- Prepare a migration plan

**KPIs**

- Benchmarks

Provide an executive-friendly monitoring of services
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: Medium
- Tags: Enlarge, Archive Work Group, Interfaces Work Group

**Description**

Provide a high-level and easy to find dashboard of running services with
documented key indicators.

**Includes work**

- Gather public site metrics
- Publish and document a dedicated dashboard
- Add links to it on common web applications (web app and docs.s.o)

**KPIs**

- Indicators available for public sites status
- Indicators for archive workers status
- Indicators for archive behavior
- Main dashboard that aggregates the indicators
- Dashboard referenced in common web applications

GitLab crawler
^^^^^^^^^^^^^^

- Priority: High
- Tags: Archive Work Group, SWHSec, Enlarge

**Description**

Recent addition to gitlab from Software Heritage allow us to fetch
metadata from gitlab forges. Now that they are accessible, we want to
fetch them

**Includes work**

- Implement new crawler
- Deploy it

**KPIs**

- Metadata coverage from gitlab forges

Handle pending loaders and listers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: Medium
- Tags: Archive Work Group, Externals, Enlarge

**Description**

Several contributions have been made to archive content from new forges or
package indices but never deployed. Review, update if required and merge all
pending loaders and listers

**Includes work**

- Review loaders
- Decide for each on if we merge, update or discard
- Merge, update and deploy those we want to keep

**KPIs**

- Closed merge requests


Support hash collisions globally
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: Low
- Tags: Archive Work Group, Enlarge, Next

**Description**

Several data points in the Software Heritage are identified by their
hash, in general a sha1. Hash collisions may happen and we need to find
a way to be resilient to them.

**Includes work**

- Analyze hash collisions issues for all Software Heritage object types
   (content, directory, revisions, origins…)
- Propose and implement workarounds

**KPIs**


Data work group
---------------

Diff Service
^^^^^^^^^^^^

- Priority: High
- Tags: Data Work Group, Empower, SWH-Sec

**Description**

Implement a way to compute diff between two revisions

**Includes work**

- Implement algorithm outputting git like diff
- Compute diff on revisions of some important repositories
- Add requirements for production usage (monitoring, alerting,
   integration tests)

**KPIs**

- New API
- User can push data with it


PySpark Tooling
^^^^^^^^^^^^^^^

- Priority: Medium
- Tags: Data Work Group, Next

**Description**

We use pyspark for some large scale data handling. Our usage is
currently not distributed and we need to develop our tooling to be able
to execute large scale pyspark jobs on our infrastructure

**Includes work**

- Be able to run distributed pyspark jobs on our kubernetes cluster
- Access to pyspark web UI during job
- Metrics of pyspark jobs
- History server to access finished jobs metrics
- Object storage to store job inputs, outputs, transient data…
- JupyterHub
- Way to use content object storage easily and efficiently in jobs

**KPIs**


Ops work group
--------------

Prepare hosting move
^^^^^^^^^^^^^^^^^^^^

- Priority: High
- Tags: Ops Work Group

**Description**

Our current hosting will be closed, we need to get ready to move it when
it will happen

**Includes work**

- Evaluate hosting solutions
- Prepare a plan for the move
- Study how to minimize the service interruption
- Tackle logistics issues
- List required investments

**KPIs**

- Actionable plan
- Advantages and disadvantages of several solutions

Documentation for mirror operators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: Medium
- Tags: Ops Work Group

**Description**

Managing and operating a mirror is a complicated task and it is time
consuming to help them. We need to improve the documentation to give
more autonomy to mirror operators.

**Includes work**

- Review each piece of documentation with mirror operator and Software Heritage Ops
- Update documentation

**KPIs**


CodeCommons
-----------

Unified Data Model
^^^^^^^^^^^^^^^^^^

- Priority: High
- Tags: CodeCommons, Enrich, Externals

**Description**

Building a unified data model to enrich the Software Heritage core data
model is a keystone of the CodeCommons project. It consists in
collecting metadata from many sources and to store them in a unified
model, in a way that makes the data available for efficient indexing and
querying. The purpose of this unified data model is to generate
qualified and specialized datasets, filtered with a wide range of
criteria in order to produce highly specialized datasets.

The scope of the CodeCommons Unified Data Model includes:

- Project Context data (extrinsic): data from various collaboration
   platforms (forges, bug trackers…)
- Research articles and other context (extrinsic): structured metadata
   from publications metadata and its connection to software artifacts
- Code Qualification (intrinsic): code-related data,including
   dependencies detection, language identification and quality
   measurement
- Licence detection (intrinsic): structured data model for licence
   information, at both file-level and project level

**Includes work**

- Design architecture for the Unified Data Model
- Implement and deploy the Unified Data Model components

**KPIs**

Project context metadata
^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: High
- Tags: CodeCommons, Enrich, Externals

**Description**

This task of the CodeCommons project includes collecting context data
from various collaboration platforms (forges, bug trackers…) and storing
it in a unified data model. It aims at adding helpful information to
qualify source codes in regards with projects activity, including
issues, pull requests and discussions.

Among the identified collaboration platforms, GitHub context data will
be stored using GHArchive.

**Includes work**

- Design the unfied data model for project context metadata, based on a
   benchmark of existing models like ForgeFed
- Implement and deploy crawlers for project context metadata for each
   identified platform
- Run a massive crawling and store the data in the unified data model

**KPIs**

- List of supported collaboration platforms
- Number of origins covered in the archive

License metadata
^^^^^^^^^^^^^^^^

- Priority: High
- Tags: CodeCommons, Enrich, Externals

**Description**

CodeCommons aims to detect license, copyright, and package metadata on
the whole Software Heritage Archive, critical to ensure the transparency
and traceability for sovereign and sustainable AI.

This will be done using ScanCode, in partnership with AboutCode, a
well-reputed, non-profit, public benefit organisation with ample
experience designing and architecting FOSS tools for analysing and
organising software and the webs of components each software package
depends on, providing a great advancement for software supply chain and
license compliance across the software ecosystem.

The ScanCode for CodeCommons project includes running a massive license
scan on the whole Software Heritage Archive.

To ensure the efficiency and efficacy of this massive scan, this project
also improves the accuracy and quality of ScanCode’s license detection.

**Includes work**

- Benchmark, adapt and optimize ScanCode for large scale analysis on
   Software Heritage archive
- Run scan at file level on the whole Software Heritage archive
- Run scan at project level on relevant versions of Software Heritage
   origins
- Assemble and store the result in a unified data model

**KPIs**

- Number of files scanned
- Number of software versions scanned

Research publications metadata
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: Medium
- Tags: CodeCommons, Enrich, Externals

**Description**

This task of the CodeCommons project aims to identify to which thematics
a software project is related, by collecting metadata from research
publications, referenced by several platforms (e.g. HAL, Open Alex).

The collected data will be structured in a unified data model.

**Includes work**

- Design the unfied data model for publications metadata, based on a
   benchmark of existing models like OpenAlex
- Implement and deploy crawlers for publications metadata for each
   identified platform
- Run a massive crawling and store the data in the unified data model

**KPIs**

- List of supported publications platforms
- Number of referenced publications
- Number of origins covered in the archive

Software versions metadata
^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: High
- Tags: CodeCommons, Enrich, Externals

**Description**

Many references to specific software versions use version name of
software projects. The current Software Heritage model doesn’t provide
explicit and formal version identification.

The goal of this task is to add version information to the Software
Heritage data model, providing relevant information adapted to various
levels of granularity.

**Includes work**

- Identify external data sources providing accurate information
- Identify and validate heuristics for Software Versions identification
   analysis in archive contents
- Design a data model for Software versions Data model
- Map software versions to objects in the archive

**KPIs**

- Number of software projects identified
- Number of versions identified


Catchup with GitHub lag
^^^^^^^^^^^^^^^^^^^^^^^

- Priority: High
- Tags: CodeCommons, Enlarge, Archive Work Group, Externals

**Description**

GitHub growth is faster than Software Heritage’s current ingestion
capacities, resulting in a lag of more than 140 million origins. In
order to return to an up-to-date archive, the CodeCommons project
includes the usage of CINES HPC infrastructure to massively clone and
ingest the missing repositories.

**Includes work**

- List the missing GitHub origins in Software Heritage archive
- Implement and deploy massive ingestion tools at CINES
- Clone and ingest the missing origins at CINES
- Generate dedudplicated datasets for retrieval in the main archive

**KPIs**

- Number of ingested GitHub origins
- Number of origins not archived


Expose full archive for large scale analysis
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: High
- Tags: CodeCommons, Enrich, Tooling, Data Work Group

**Description**

CINES’s Adastra HPC infrastructure has been made available to
CodeCommons for providing the compute and storage capabilities required
for CodeCommons massive data processing and additional metadata
collection around Software Heritage. This item covers the prerequisite
actions on CINES HPC, which consist of depositing a full copy of the
main archive (contents and graph) and deploy the tooling for large scale
archive access.

**Includes work**

- Copy archive contents at CINES
- Copy archive compressed graph at CINES
- Improve and adapt SWH-Fuse for optimized large-scale access to the
   archive

**KPIs**

- Full copy of the archive available at CINES
- SWH-Fuse deployed at CINES
- Performance metrics for SWH-Fuse

Similarity analysis
^^^^^^^^^^^^^^^^^^^

- Priority: Low
- Tags: CodeCommons, Enrich, Externals

**Description**

Additionally to Software Heritage’s strong commitment to transparency
and respect of the authors in training datasets for LLMs for code (as
stated more than a year ago:
https://www.softwareheritage.org/2023/10/19/swh-statement-on-llm-for-code/),
CodeCommons includes to provide mechanisms of similarity detection for
generated code, in order to ensure a proper attribution to the authors
of the original source code. We are planning to use text and syntax
analysis methods for similarity, but also to challenge machine learning
approach that may complete the results.

**Includes work**

- Design and implement tools for code Similarity analysis
- Benchmark results from different approaches
- Prepare the integration of provenance for attribution of generated
   code

**KPIs**

- Documented benchmark results

Code Qualification
^^^^^^^^^^^^^^^^^^

- Priority: Medium
- Tags: CodeCommons, Enrich, Externals

**Description**

In order to provide qualified datasets according to multiple criteria
based on the code qualification, the Software Heritage will be enriched
with metadata extracted from an in-depth analysis of the source code
archive, including the following topics: - Programming languages
identification - Dependencies detection - Code quality metrics

**Includes work**

- Programming languages:

   - Benchmarck existing tools and select the most relevant ones
   - Run language identification analysis at scale on Software Heritage
      contents
   - Store and index the results in a unified data model

- Dependencies detection

   - Customize ScanCode tools for scaling to Software Heritage
   - Run a file-level analysis on the archive contents
   - Run a project level analysis on the graph (projects filesystems
      browsing)
   - Store and index the results in a unified data model

- Code quality metrics extraction

   - Identify relevant code quality metrics, possibly:

      - Static analysis
      - Code coverage
      - Design patterns identification

**KPIs**

- % of the archive covered for each subject

Automate Datasets generation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: Medium
- Tags: CodeCommons, Enrich, Dataset factory, Data work group

**Description**

We need to produce datasets regularly and reliably to be more efficient and to
clarify which datasets users can expect. Provide tooling for an automated
production and publishing of derived datasets

**Includes work**

- Design and implement the required automation tools
- Setup and configure an automation pipeline
- Provide a dashboard for monitoring
- Document datasets for clear interface

**KPIs**

- Number of derived datasets automatically published

Generate contents Datasets
^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: High
- Tags: CodeCommons, Enrich, Dataset factory, Data work group

**Description**

Create a tool that generates a dataset embedding file contents, based
on a list of SWHIDs.

**Includes work**

- Enable SWHID mapping on existing objectstorage (currently indexed by
   hash)
- Design and implement a generation engine for datasets embedidng
   contents
- Benchmark and optimize performance for large-scale usage

**KPIs**

- Performance metrics

Integrate CodeCommons in main archive
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: High
- Tags: CodeCommons, Enlarge, Next

**Description**

Most CodeCommons tools for metadata crawling and archive analysis will
be run on Adastra HPC at CINES. On the one hand, the computed metadata
will need to retrieved in the main archive, and on the other hand, the
toolsused for a massive processing on the whole archive copy will need
to be integrated to Software Heritage standard ingestion pipeline in
order to keep maintaining the CodeCommos metadata up-to-date on the long
term. This taske also includes the retrieval of the GitHub lag
ingestion.

**Includes work**

- Retrieve archive core data from CINES
- Retrieve unified metadata from CINES
- Design architecture and infrastructure for retrieving full archive
   and unified metadata
- Integrate CodeCommons tools in the standard ingestion pipeline

**KPIs**

- Main archive core data up-to-date with CINES
- Main archive metadata up-to-date with CINES
- Tools integrated to the ingestion pipeline

SWHSec
------

Collect and store CVE metadata
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: High
- Tags:  Data work group, SWHSec, Enrich

**Description**

Collect CVE metadata from relevant external datasources, map it to
Software Heritage data model and link CVEs to relevant revisions
(introducing and fixing revisions).

**Includes work**

- Design a data model for CVE
- Implement crawlers for CVE data sources
- Store metadata

**KPIs**

- Number of CVE stored
- Number of Objects linked to a CVE

Vulnerability Dataset extraction
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Priority: High
- Tags: Data work group, SWHSec, Enrich

**Description**

Develop a tool that extracts the relevant introducing/fixing commits
from Software Heritage for a input dataset of vulnerabilities
description.via the Software Heritage archive, in a dataset featuring
information will be available on either the version (or commit)
introducing the vulnerability or the version (or commit) fixing the
vulnerability, or both.

**Includes work**

- Design and implement the detetction mechanisms
- Benchmark the tools by generating raw datasets
- Validate and deliver the tool

**KPIs**

- Introducing commits detection ratio
- Fixing commits detection ratio
- Number of CVEs supported

