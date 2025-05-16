Errors
======


HTTP Errors
-----------

The Inbox API should always acknowledge your notifications with a ``201 Created`` HTTP
status code but if something went wrong it might return 4XX status codes and a JSON
body containing one or multiple error messages to help you fix the error.


400 Bad Request
~~~~~~~~~~~~~~~

Your payload is either malformed (i.e. we're unable to read the payload) or invalid:

- duplicate Notification ``id``: identifiers MUST be unique
- invalid UUID URN: ``id`` MUST be valid UUID URN (urn:uuid:xxx)
- the origin inbox url of your account MUST match the one in the
  ``payload['origin']['inbox']`` key of your notifications
- the notification payload MUST follow all the requirements described in the
  :doc:`protocol`


401 Unauthorized
~~~~~~~~~~~~~~~~

Usage of our Inbox API is limited to partners with a valid user account.
All API calls MUST be authenticated with the proper HTTP header.
If your authentication token is invalid or missing you will get a ``401 Unauthorized``
HTTP status code.

Please note that your authentication token depends on the environment (staging or
production) you're targeting.


Notifications
-------------

These notifications indicates a failure in properly handling your notification, they
are sent to your inbox with a ``InReplyTo`` key referencing your notification
``id``.

UnprocessableNotification
~~~~~~~~~~~~~~~~~~~~~~~~~

This notification has booth a ``Flag`` ``type`` and a
``coar-notify:UnprocessableNotification`` one.

|swh| inbox url (either the staging or the production one) MUST match the
``payload['target']['inbox']`` value in the notification.

Reject
~~~~~~

This notification has a ``Reject`` ``type``.

- ``context['id']`` MUST match ``object['as:subject']``
- ``context['type']`` MUST contain ``sorg:SoftwareSourceCode``