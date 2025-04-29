What's COAR Notify?
===================

`COAR Notify`_ is an initiative focused on developing and promoting the adoption of a
standardized, interoperable, and decentralized approach to connect different research
outputs and services.

The `COAR Notify Protocol`_ is based on two well-established W3C standards:
`Linked Data Notifications`_ and `ActivityStreams`_.


Key benefits
------------

- by creating a consistent method for communicating links between research outputs,
  COAR Notify improves the discoverability of these outputs.
- it facilitates the implementation of open science practices by connecting different
  versions and related research outputs, regardless of their location.
- COAR Notify promotes a decentralized network where different systems can communicate
  directly, reducing reliance on central authorities
- It enables the development of new services, such as overlay journals, knowledge
  aggregation, and expert locators, by providing a standardized communication layer.


Integration to the |swh| archive
--------------------------------

By sending metadata on a software artefact in a COAR notification you can provide
extrinsic information on a source code (like mention in a scientific publication)
which are usually not present in the code itself (intrinsic metadata).

Metadata is indexed by our search engine and provide new ways of finding and working
with content in the archive.


Implemented workflows
---------------------

The first implemented workflow is the ingestion of a relationship between a scientific
publication and a software as described in the
`Managing the lifecycle of software assets`_ documentation of the SoFAIR project.


Ready to use our COAR Notify service?
-------------------------------------

Start by :doc:`../howto/account`.


.. _COAR Notify: https://coar-repositories.org/what-we-do/notify/
.. _COAR Notify Protocol : https://coar-notify.net/
.. _Linked Data Notifications: https://www.w3.org/TR/ldn/
.. _ActivityStreams: https://www.w3.org/TR/activitystreams-core/
.. _Managing the lifecycle of software assets: https://sofair.org/the-sofair-documentation-managing-the-lifecycle-of-software-assets-a-workflow-guide-for-developers/