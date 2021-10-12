.. _mirror_operations:

Mirror Operations
=================

A mirror is a full copy of the |swh| archive, operated independently from the
Software Heritage initiative.

A mirror should be able to:

- store a full copy of the archive,

- serve the data using the web UI,

- search the archive using the web UI,

- serve the data using the public API,

- allow users to retrieve content from the archive using the :ref:`Vault
  <swh-devel:swh-vault>` service.

See the :ref:`swh-devel:mirror` for a complete description of the mirror
architecture.

You may want to read:

- :ref:`mirror_deploy` if you want to deploy a mirror of the |swh| archive on
  your infrastructure.
- :ref:`mirror_monitor` to learn how to monitor your mirror and how to report
  its health back the |swh|.
- :ref:`mirror_onboard` for the |swh| side view of adding a new mirror.


.. toctree::
   :hidden:

   deploy
   onboard
   monitor
