.. _sysadm_mirror_operations:

Mirror Operations
-----------------

A mirror is a full copy of the |swh| archive, operated independently from the
Software Heritage initiative.

A mirror should be able to:
- store a full copy of the archive,
- serve the data using the web UI,
- search the archive using the web UI,
- serve the data using the public API,
- allow users to retrieve the content from the archive using the Vault service
  (swh-vault).


See the :ref:`swh-devel:mirror` for a complete description of the mirror
architecture.

.. toctree::
   :titlesonly:

   deploy
   onboard
   monitor
