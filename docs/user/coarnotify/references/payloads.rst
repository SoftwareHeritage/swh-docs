Payloads
========

Our COAR Notify Server is an implementation of the
`COAR Notify Protocol v1.0.1 <https://coar-notify.net/specification/1.0.1/>`__, please
refer to their specification to identify all the required keys and their meanings.

This documentation will provide extra requirements for the kind of COAR Notifications
we handle.

Mention of a software in a scientific publication
-------------------------------------------------

- ``id`` MUST be a UUID
- ``type`` indicate this is an Announce Relationship COAR Notification
- ``origin`` describes the system which has sent the notification
- ``target`` describes the system which is intended to receive the notification, our
  inbox for instance
- ``actor`` describes the party responsible for this activity
- ``object`` describes the relationship itself, ``subject`` is the identifier of your
  resource which cites/mentions our resource ``object`` (a
  :ref:`SWHID <persistent-identifiers>` or an :term:`origin` URL)
- ``context`` identifies the resource on the ``origin`` which is the subject of the
  relationship

Valid relationship types
------------------------

To describe the relationship between a scientific publication and software, we utilize
the `DataCite relation type vocabulary <datacite-relations>`_ alongside Schema.org's
``citation`` and CodeMeta's ``referencePublication``:

- ``https://schema.org/citation``
- ``https://codemeta.github.io/terms/referencePublication``
- ``https://schema.datacite.org/linked-data/vocab/relationType/Cites``
- ``https://schema.datacite.org/linked-data/vocab/relationType/Continues``
- ``https://schema.datacite.org/linked-data/vocab/relationType/IsSupplementTo``
- ``https://schema.datacite.org/linked-data/vocab/relationType/Describes``
- ``https://schema.datacite.org/linked-data/vocab/relationType/References``
- ``https://schema.datacite.org/linked-data/vocab/relationType/Documents``
- ``https://schema.datacite.org/linked-data/vocab/relationType/Compiles``
- ``https://schema.datacite.org/linked-data/vocab/relationType/Reviews``
- ``https://schema.datacite.org/linked-data/vocab/relationType/IsSourceOf``
- ``https://schema.datacite.org/linked-data/vocab/relationType/Requires``
- ``https://schema.datacite.org/linked-data/vocab/relationType/Obsoletes``
- ``https://schema.datacite.org/linked-data/vocab/relationType/Collects``

Inverted relationships (eg. ``IsCitedBy`` instead of ``Cites``) are not allowed.

.. _datacite-relations: https://datacite-metadata-schema.readthedocs.io/en/4.7/appendices/appendix-1/relationType/

Example payload
---------------

.. code-block:: json

  {
    "@context": [
      "https://www.w3.org/ns/activitystreams",
      "https://coar-notify.net"
    ],
    "id": "urn:uuid:6908e2d0-ab41-4fbf-8b27-e6d6cf1f7b95",
    "type": [
      "Announce",
      "coar-notify:RelationshipAction"
    ],
    "target": {
      "id": "https://www.softwareheritage.org",
      "inbox": "https://inbox.staging.swh.network",
      "type": "Service"
    },
    "actor": {
      "id": "https://your-organization.tld",
      "name": "Your Organization",
      "type": "Organization"
    },
    "context": {
      "id": "https://your-organization.tld/item/12345/",
      "sorg:name": "My paper title",
      "sorg:author": {
          "@type": "Person",
          "givenName": "Author Name",
          "email": "author@example.com",
      },
      "ietf:cite-as": "https://doi.org/XXX/YYY",
      "ietf:item": {
        "id": "https://your-organization.tld/item/12345/document.pdf",
        "mediaType": "application/pdf",
        "type": [
          "Object",
          "sorg:ScholarlyArticle"
        ]
      },
      "type": [
        "Page",
        "sorg:AboutPage"
      ]
    },
    "object": {
      "as:subject": "https://your-organization.tld/item/12345/",
      "as:relationship": "https://schema.datacite.org/linked-data/vocab/relationType/Cites",
      "as:object": " https://github.com/rdicosmo/parmap",
      "id": "urn:uuid:74FFB356-0632-44D9-B176-888DA85758DC",
      "type": "Relationship"
    },
    "origin": {
      "id": "https://your-organization.tld/repository",
      "inbox": "https://inbox.your-organization.tld",
      "type": "Service"
    }
  }


