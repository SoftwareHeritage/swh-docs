.. _deposit-version:

Deposit a new version of an existing origin
===========================================

Checklist
---------

- You have access to your :ref:`account credentials <deposit-account>`
- You have a software artefact at hand and its associated metadata (if not you need to
  :ref:`prepare your artefacts and metadata <deposit-prepare>`.) and you properly
  used the ``codemeta:version`` property to identify this deposit
- You already made a deposit for this origin (if not you want to
  :ref:`make a first code & metadata deposit <deposit-first>`)


Send the artefact and the metadata
----------------------------------

The API calls / CLI commands are the same than the ones described in
:ref:`make a first code & metadata deposit <deposit-first>` or
:ref:`make a multi-step deposit <deposit-partial>`. The only change is the use of
``swh:add_to_origin`` instead of ``swh:create_origin`` in your metadata file.

Once the status of the deposit is ``done`` you'll be able to check the release tab of
your archived origin to see the different deposits versions.