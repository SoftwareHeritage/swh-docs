.. _alterations:

Alterations of the Software Architecture Archive
================================================


The main objective of an archive is to store facts forever. As such, it can be
viewed as an append-only infrastructure. However, it may be necessary to alter
the content of the archive to account for removal or alteration requests that
may happen `for several reasons`_.

We currently consider 2 types of alterations that may have to be applied to the
archive:

- content removal: some objects stored in the archive should not be visible any
  more; these can be either removed entirely or masked, depending on the
  situation.
- personal identity modification: some personal information (namely the name
  and email of a person) needs not to be visible any more.


.. note::

   We will not discuss in this section the administrative process of receiving,
   handling and processing an alteration request of the Software Heritage
   Archive. We will only focus on the technical aspects of the processes
   involved, and their impact on the architectural design.


.. _`for several reasons`: https://www.softwareheritage.org/legal/content-policy


Types of alteration
-------------------

Content removal
~~~~~~~~~~~~~~~

A content removal request starts from one (or more) origin. All the removal
handling process is based on an origin.

When dealing with a content removal request that needs to be applied to the
archive, the following steps need to be done:

- identify all the objects in the archive (mostly in the :ref:`Merkle DAG
  <swh-merkle-dag>`) that need to be removed,
- build a properly encrypted recovery bundle with all the objects listed previously,
- store and identify this bundle in a dedicated storage,
- remove all the identified :py:class:`Content <swh.model.model.Content>`
  objects from all the :ref:`objstorages <swh-objstorage>` under the legal and
  technical responsibility of |swh|,
- remove all the identified objects from all the :ref:`storages <swh-storage>`
  under the legal and technical responsibility of |swh|,
- remove all the identified objects from all the secondary data silos, namely
  the :ref:`kafka journal <swh-journal>`, them :ref:`search index
  <swh-search>`, the :ref:`compressed graph <swh-graph>` and the :ref:`vault cache
  <swh-vault>`,
- possibly: ensure the origins the removal request is targeting are excluded
  from any future archival

Note that handling archive content removal can also imply masking them
(temporarily or permanently); for example during the examination process of
suppression request, it might be necessary to hide all the impacted objects
until a decision is made for each of them.


Name change
~~~~~~~~~~~

A person may ask for their former identity not to be published any more. When
this request has been handled and accepted, any occurrence of the former
identity of the person associated with archived version control system objects
(such as commits) will be replaced by the new one when using the public
endpoints of the archive (namely, browsing the archive, using public APIs,
using the vault).

Note that currently, only :py:class:`Revision <swh.model.model.Revision>` and
:py:class:`Release <swh.model.model.Release>` objects are affected by the
process.


Read Access - Altering results
------------------------------

The |swh| component responsible for altering returned objects is the
:py:class:`MaskingProxyStorage
<swh.storage.proxies.masking.MaskingProxyStorage>`. It handles both the cases of
content that are still present in the archive but need to not to be published,
and the application of active name change requests. It stores in a dedicated
database a map of email to current display name to used to alter returned
Revision and Release objects, and a series of tables dedicated to handling
masking requests. These allow not to return at all an object from the archive
if it's under a currently active masking request.

As such, all the publicly accessible storage instances -- be it from the web
frontend, the public API (REST and GraphQL) or the :term:`vault` service -- are
using an access path that pass through the ``MaskingProxyStorage``.

Note that for services like the :term:`vault`, it will make it fail to perform the
requested cooking in some cases (especially for git history cooking, where the
cryptographic integrity of the generated git content is altered, thus invalid.)


Write Access - Preventing ingesting origins
-------------------------------------------

When an origin has been identified as forbidden for any future archiving, we
use a dedicated storage proxy in the writing path to the archive to ensure this
cannot happen. The corresponding |swh| component is the
:py:class:`BlockingProxyStorage
<swh.storage.proxies.blocking.BlockingProxyStorage>`. It is a simple proxy
storage keeping a list of forbidden origin URLs in a dedicated database, and
enforcing any matching origin URL to be ingested in the archive.
