Deposit a new version of an existing origin
===========================================

Checklist
---------

- You have access to your :doc:`account credentials <account>`
- You have a software artefact at hand and its associated metadata (if not you need to
  :doc:`prepare your artefacts and metadata <prepare>`.) and you properly
  used the ``codemeta:version`` property to identify this deposit
- You already made a deposit for this origin (if not you want to
  :doc:`make a first code & metadata deposit <first-deposit>`)


Send the artefact and the metadata
----------------------------------

The API calls / CLI commands are the same than the ones described in
:doc:`make a first code & metadata deposit <first-deposit>` or
:doc:`make a multi-step deposit <multistep-deposit>`. The only change is the use of
``swh:add_to_origin`` instead of ``swh:create_origin`` in your metadata file.

Once the status of the deposit is ``done`` you'll be able to check the release tab of
your archived origin to see the different deposits versions.