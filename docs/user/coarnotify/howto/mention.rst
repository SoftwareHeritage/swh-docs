Send a mention of a software in a scientific publication
========================================================

.. admonition:: API/CLI reference
   :class: note

   This page will help you send a COAR Notification without getting into too much
   details, the :doc:`API reference <../references/api>` and the
   :doc:`Payload reference <../references/payload>`
   are available to explain all the technical specifications.

It’s possible to deposit metadata on an already existing software origin or SWHID by
using the `Announce Relationship`_ pattern.

.. _Announce Relationship: https://coar-notify.net/specification/1.0.1/announce-relationship/


Checklist
---------

- You have access to your :doc:`account credentials <account>`
- You have your own COAR Notify Inbox running
- You have a tool to make API calls, we will use curl here, but commands could be
  easily adapted to another application


Prepare the notification payload
--------------------------------

To announce that the scientific paper ``https://your-organization.tld/item/12345/``
mentions the software `parmap <https://github.com/rdicosmo/parmap>`_. The notification
will look like:

.. code-block:: json

  {
    "@context": [
      "https://www.w3.org/ns/activitystreams",
      "https://coar-notify.net"
    ],
    "actor": {
      "id": "https://your-organization.tld",
      "name": "Your Organization",
      "type": "Organization"
    },
    "context": {
      "id": "swh:1:dir:ec88e5b901c034d5a91aa133e824d65cff3788a3;origin=https://github.com/rdicosmo/parmap;visit=swh:1:snp:25490d451af2414b2a08ece0df643dfdf2800084;anchor=swh:1:rev:db44dc9cf7a6af7b56d8ebda8c75be3375c89282",
      "type": [
        "sorg:SoftwareSourceCode"
      ]
    },
    "id": "urn:uuid:6908e2d0-ab41-4fbf-8b27-e6d6cf1f7b95",
    "object": {
      "as:subject": "https://your-organization.tld/item/12345/",
      "as:relationship": "https://w3id.org/codemeta/3.0#citation",
      "as:object": " swh:1:dir:ec88e5b901c034d5a91aa133e824d65cff3788a3;origin=https://github.com/rdicosmo/parmap;visit=swh:1:snp:25490d451af2414b2a08ece0df643dfdf2800084;anchor=swh:1:rev:db44dc9cf7a6af7b56d8ebda8c75be3375c89282",
      "id": "urn:uuid:74FFB356-0632-44D9-B176-888DA85758DC",
      "type": "Relationship"
    },
    "origin": {
      "id": "https://your-organization.tld/repository",
      "inbox": "https://inbox.your-organization.tld",
      "type": "Service"
    },
    "target": {
      "id": "https://www.softwareheritage.org",
      "inbox": "https://inbox.staging.swh.network",
      "type": "Service"
    },
    "type": [
      "Announce",
      "coar-notify:RelationshipAction"
    ]
  }

- ``id`` a UUID
- ``type`` to indicate this is an Announce Relationship COAR Notification
- ``target`` describes the system which is intended to receive the notification, our
  inbox for instance
- ``actor`` describes the party responsible for this activity
- ``object`` describes the relationship itself, ``subject`` is the identifier of your
  resource which cites/mentions our resource ``object`` (a SWHID or an origin url)
- ``context`` identifies the resource on the ``target`` which is the object of the
  relationship

Check the full :doc:`Payload reference <../references/payload>` for more details.

Save the file as ``notification.json``.

Send the notification
---------------------

.. code-block:: console

  curl -H 'Authorization: Token <TOKEN>' \
       -H 'Content-Type: application/ld+json' \
       -i --data @notification.json \
       https://inbox.staging.swh.network


Will return a ``201 created`` HTTP response containing a ``location`` header with the
url to your notification:
``https://inbox.staging.swh.network/6908e2d0-ab41-4fbf-8b27-e6d6cf1f7b95``

Please note that a ``201 created`` response does **not** mean we were able to properly
archive this mention, only that we were able to validate its structure.

Now that we have stored your notification we'll process it and send you a reply
following the COAR Notify protocol.

Handle the reply
----------------

If something went wrong you'll receive either a  ``UnprocessableNotification`` or a
``Reject`` with a ``summary`` key explaining the reason why we were not able to
archive this mention.

Otherwise you will receive an ``Accept`` notification which indicates that your mention
was sent to our metadata storage.

The ``InReplyTo`` key of these notifications will contain the ``id`` of your initial
Notification.
