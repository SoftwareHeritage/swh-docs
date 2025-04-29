Protocol reference
==================

The *COAR Notify Protocol* consists of documented community conventions for the use of
W3C Linked Data Notifications (LDN) to integrate repository systems with relevant
services in a distributed, resilient and web-native architecture.

Our COAR Notify Server is an implementation of the
`COAR Notify Protocol v1.0.1 <https://coar-notify.net/specification/1.0.1/>`_, please
refer to their specification to implement your own client.

Authentication
--------------

At this point the Security aspects of the protocol are not
`standardized yet <https://coar-notify.net/guide/security/>`_. To properly authenticate
calls to our Inbox and guarantee that only trusted partners are allowed a write access
to our metadata storage we decided to implement a Token based authentication system.

:doc:`The token <../howto/account>` has to to be sent with the HTTP headers
accompanying every calls you make to the API: ``Authorization: Token <TOKEN>``.
