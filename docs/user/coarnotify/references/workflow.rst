Workflow
========

For every notification sent by a client Repository, the COAR Notify server:

1. authenticates the call
2. checks some simple properties: is the payload structurally valid, is it a ``type`` of
   notification we're able to handle ?
3. stores the notification object in a database
4. sends a 201 HTTP response to the client
5. process the notification depending on its ``type``
6. stores raw extrinsic metadata to the storage
    1. a dedicated ``swh-indexer`` converts the notification to the CodeMeta format
    2. this metadata is now stored and associated to a proper SWHID / Origin URL
7. sends a COAR Notification indicating the result of the ingestion.

Graphically:

.. mermaid ::
    sequenceDiagram
        participant Repository
        participant inbox as SWH COAR Notify Server
        participant handler as Notification handler
        participant rawstorage as Raw Metadata Storage
        participant storage as Metadata Storage
        Repository->>inbox: Send Announce RelationshipAction Notification
        inbox->>inbox: Authenticate sender with token
        opt Invalid auth
            inbox->>Repository: HTTP 401 response
        end
        inbox->>inbox: Validate Notification
        opt Invalid payload
            inbox->>Repository: HTTP 400 response
        end
        inbox->>Database: Store notification
        inbox->>handler: process the notification
        opt Unprocessable
            inbox->>Repository: Unprocessable COAR Notification
        end
        opt Reject
            inbox->>Repository: Reject COAR Notification
        end
        inbox->>Repository: HTTP 201 response
        handler->>rawstorage: Store metadata
        indexer-->rawstorage: fetch and process raw metadata
        indexer->>storage: store CodeMeta metadata
        handler->>inbox: send the processing result
        inbox->>Database: Prepare & store Accept Notification
        inbox->>Repository: Accept COAR Notification