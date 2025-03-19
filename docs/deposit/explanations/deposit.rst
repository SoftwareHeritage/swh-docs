What's a deposit?
=================

Most of the software source code artifacts present in the SWH Archive are gathered by
the mean of `loader`_ workers run by the SWH project from source code origins identified
by `lister`_ workers. This is a pull mechanism: it's the responsibility of the SWH
project to gather and collect source code artifacts that way.

Alternatively, SWH allows its partners to push source code artifacts and metadata
directly into the Archive with a push-based mechanism. By using this possibility
different actors, holding software artifacts or metadata, can preserve their assets
without having to pass through an intermediate collaborative development platform, which
is already harvested by SWH (e.g GitHub, GitLab, etc.).

**This mechanism is the code deposit.**

The main idea is the deposit is an authenticated access to an API allowing the user to
provide source code artifacts -- with metadata -- to be ingested in the SWH Archive. The
result of that is a `SWHID`_ that can be used to uniquely and persistently identify that
very piece of source code.

This unique identifier can then be used to `reference the source code
<https://hal.archives-ouvertes.fr/hal-02446202>`_ (e.g. in a `scientific paper
<https://www.softwareheritage.org/2020/05/26/citing-software-with-style/>`_) and
retrieve it using the `vault`_ feature of the SWH Archive platform.

The differences between a piece of code uploaded using the deposit rather than simply
asking SWH to archive a repository using the `save code now`_ feature are:

- a deposited artifact is provided from one of the SWH partners which is regarded as a
  trusted authority,
- a deposited artifact requires metadata properties describing the source code artifact,
- a deposited artifact has a CodeMeta_ metadata entry attached to it,
- a deposited artifact has the same visibility on the SWH Archive than a collected
  repository,
- a deposited artifact can be searched with its provided url property on the SWH
  Archive,
- the deposit API uses the `SWORD v2`_ API, thus requires some tooling to send deposits
  to SWH. These tools are provided with this repository.

A partner may wish to deposit only metadata about an origin or object already present in the Software Heritage archive.

The **metadata-only deposit** is a special deposit where no content is provided and the data transferred to Software Heritage is only the metadata about an object in the archive.

Is it useful for me?
--------------------

Source code is fragile; it can disappear. It is important to note that software source code has an essential role in research and should be archived properly, alongside data and publications. Software that was built for research as part of the open science ecosystem should be archived, referenced, described and cited.

When depositing in Software Heritage you can describe a software artifact properly with specific metadata properties and it will be safely saved in the universal software archive.
