What's a deposit?
=================

Most of the software source code artifacts present in the |swh| Archive are
gathered by tools run by the SWH project, this is a pull mechanism: it's the
responsibility of the SWH project to gather and collect source code artifacts that way.

Alternatively, SWH allows its trusted partners to send source code artifacts and/or
metadata directly into the Archive with a push-based mechanism. By using this
possibility different actors, holding software artifacts or metadata, can preserve
their assets without having to pass through an intermediate collaborative development
platform, which is already harvested by SWH (e.g GitHub, GitLab, etc.).

**This mechanism is the deposit.**

The result of this action is a :ref:`SWHID <persistent-identifiers>` that can be used
to uniquely and persistently identify that very piece of source code.

This unique identifier can then be used to reference the source code (e.g. in a
scientific paper) and retrieve it using the features of the SWH Archive platform.

The differences between a deposit and simply asking SWH to archive a repository using the pull features of the Archive are:

- a deposited artifact is provided from one of the SWH partners which is regarded as a
  trusted authority,
- a deposited artifact requires metadata properties describing the source code artifact,
- a deposited artifact can be searched with its provided url property on the SWH
  Archive
- it is possible to make a metadata only deposit only about an artefact already
  present in the |swh| archive.

Deposits are made using `SWORD v2`_, an interoperability standard for depositing
content into repositories.

.. _SWORD v2: https://sword.cottagelabs.com/previous-versions-of-sword/sword-v2/

Metadata?
---------

The metadata of a software artefact is the real added value of the deposit service, it
allows a partner to provide extrinsic information on a source code (details about the
author and its affiliation, external ids, mention in a scientific publication, etc.)
which are usually not present in the code itself (intrinsic metadata).

Metadata is indexed by our search engine and provide new ways of finding content in the
archive.

To understand why metadata is so important to us please read :doc:`why-metadata`.

Is it useful for me?
--------------------

You know software source code has an essential role in research and should be archived
properly, alongside data and publications. Software that was built for research as part
of the open science ecosystem should be archived, referenced, described and cited.

When depositing in |swh| you can describe a software artifact properly with specific metadata properties and it will be safely saved in the universal software archive.

Ready to use our deposit services?
----------------------------------

Start by :doc:`../howto/account`.