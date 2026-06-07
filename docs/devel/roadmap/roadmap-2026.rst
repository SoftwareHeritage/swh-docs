.. _roadmap-current:
.. _roadmap-2026:

Roadmap 2026
============

(Version 1.0, last modified 2026-03-24)

This document provides an overview of the technical roadmap of the Software
Heritage initiative for the year 2026.

.. contents::
   :depth: 3
..

Main objectives
===============

This year, our roadmap is focused on two main objectives: consolidation and growth.

Consolidation
^^^^^^^^^^^^^

Software Heritage has reached its 10-year anniversary, and as its user base grows, so does the need for absolute reliability. It’s time to step back and consolidate our infrastructure and services. We’re prioritizing scalability and robustness to ensure smoother operations and a more streamlined tech organization.

Different items will be prioritized this year:

* Parts of the platform require rework to be as efficient as possible.
* We need to improve the usability of the current development and execution environment to make it more reliable and efficient for us.
* We need to develop some missing features or tools that block other developments.
* We have to minimize risk and reduce technical debt that arises in all such long-term projects.
* We see some long-term issues coming ahead that need to be tackled now.

This is a long-term endeavor. Not everything will be done this year, and we plan this to be a several-year project.

Growth
^^^^^^

We will also develop services to ensure the economic sustainability of Software Heritage. We need to develop new revenue streams to strengthen its long-term sustainability. Those services will demonstrate the value of archiving beyond conservation, proving it useful beyond archiving and a key element for users.

Projects
========

We are involved in several funded projects this year:

* `CodeCommons <https://codecommons.org/>`__
* `OSPO-Radar <https://www.softwareheritage.org/2025/04/02/ospo-radar-project-launch/>`__
* `SWH-Sec <https://www.softwareheritage.org/2023/04/07/enhancing-cybersecurity-through-swh/>`__
* `Sec4AI4Sec <https://www.sec4ai4sec-project.eu>`__

Growth projects
===============

Software Asset Dashboard
^^^^^^^^^^^^^^^^^^^^^^^^

This application is a part of the OSPO-Radar project. It aims to build a tool to help academic institutions create and showcase their software collections.

Users will be able to describe collections of software, for instance, free software that their institution is contributing to. Then they will be able to annotate software assets with metadata, use the interface to extract software citation and build institutional sites that list them.

Development began last year with discussions with future users to scope, design and specify the product. We will move to the implementation phase this year.

Software Insights Report
^^^^^^^^^^^^^^^^^^^^^^^^

The SWH Archive being an extensive and unique knowledge base about all publicly available source code, it can be used to provide organizations with insights about the projects they are contributing to. This takes the form of specific reports that let them find all the repositories their members have contributed to, with statistics on languages, licenses, and the forges they use...

This helps them showcase their contributions and analyze their output.

Vulnerability Graph
^^^^^^^^^^^^^^^^^^^

Last year, in the projects SWH-Sec and Sec4AI4Sec, we developed ways to map vulnerabilities to elements of the archive. For instance, we studied methods for identifying revisions that introduce a CVE from the fixing revision using the `SZZ algorithm <https://www.st.cs.uni-saarland.de/papers/msr2005/>`__. We want to continue this work and make it available in the archive. Then we will think about how to make it available, for instance, through the `scanner <https://docs.softwareheritage.org/devel/swh-scanner/>`__.

Dataset Factory
^^^^^^^^^^^^^^^^

The goal is to provide a way for users to request datasets from Software Heritage for research or to train large language models. We want to support requests like: “Provide a dataset of the most important [500k] files in [python, golang, C++] licensed in [MIT, BSD] used in domains [astronomy, GIS] with no known vulnerabilities updated in [the last 2 years]”.

Link to other features
^^^^^^^^^^^^^^^^^^^^^^

Many of the previous projects are connected to features we are working on. We will continue work on the CodeCommons project to enrich the archive with metadata about licenses, languages, or project context. We will also continue the catch-up on GitHub lag using AdAstra HPC. This year will be more focused on effectively computing all this information on the whole archive and making it available in the archive.


Consolidation projects for Q1 and Q2
====================================

These are the various items we will work on during the first quarter about consolidation.

Backups
^^^^^^^

Some parts of the infrastructure are only copied to our mirror network. The data is not at risk, but retrieving it and rebuilding the service would take a long time in the event of a catastrophic failure, since we lack the tooling to restore it. We are working on a proper backup with easy and fast restoration.

Devops processes
^^^^^^^^^^^^^^^^

We will adopt a more DevOps-oriented process and start allowing developers to deploy their own applications. We started by opening our Kubernetes clusters to developers. We will next streamline secret management in our infrastructure and experiment with a DevOps-oriented process for the new OSPO-Radar application.

Automation
^^^^^^^^^^

We continue to streamline our development and infrastructure by automating what can be automated. This quarter, we continue to work on automating the graph compression process and evaluate using `Renovate <https://docs.renovatebot.com/>`__ to manage the maintenance of dependencies.

Documentation
^^^^^^^^^^^^^

The existing documentation is fairly extensive but somewhat unfocused. We will review it, analyze how it can be improved, and update some parts.

GitHub ingestion speed
^^^^^^^^^^^^^^^^^^^^^^

GitHub's growth is faster than Software Heritage’s current ingestion capacities, resulting in a lag of more than 140 million origins. To maintain an up-to-date archive after the lag catch-up, we need to improve ingestion efficiency and further optimize our platform.

Git SHA256
^^^^^^^^^^

Git is moving to a new internal hash function, and we need to implement a way to continue ingesting those repositories. We will start by discussing the solutions before implementing them.

To be continued with other consolidation items next quarters...
