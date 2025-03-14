What's a code deposit?
======================

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
- a deposited artifact has a codemeta_ metadata entry attached to it,
- a deposited artifact has the same visibility on the SWH Archive than a collected
  repository,
- a deposited artifact can be searched with its provided url property on the SWH
  Archive,
- the deposit API uses the `SWORD v2`_ API, thus requires some tooling to send deposits
  to SWH. These tools are provided with this repository.

.. _SWHID: https://docs.softwareheritage.org/devel/swh-model/persistent-identifiers.html#persistent-identifiers
.. _vault: https://docs.softwareheritage.org/devel/swh-vault/index.html#swh-vault
.. _save code now: https://archive.softwareheritage.org/save/
.. _SWORD v2: http://swordapp.org/sword-v2/