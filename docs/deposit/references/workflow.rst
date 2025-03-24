Internal Workflows
==================

Depending on the type of deposit (code or metadata-only) your request will go through
up to three sequential processes before appearing in the archive

1. handle the **reception** of the deposit
2. **check** the content of the software artefacts (code deposit only)
3. **load** the artefacts in the archive


Reception
---------

For every HTTP request sent by a client, the deposit API checks some simple properties,
then creates a :class:`swh.deposit.models.DepositRequest`
object containing the data uploaded by the client verbatim (archive and/or metadata),
and inserts in the database
A corresponding :class:`swh.deposit.models.Deposit` object is also created
and inserted, if this is the initial request creating a deposit.

Upon receiving the last request, identified by the lack of the ``In-Progress: true``
header, the deposit server either:

* checks the targeting objects exists in :ref:`swh-storage <swh-storage>`,
  then sends a request to swh-storage with the Atom metadata and updates the
  deposit status to ``done``,
  if it is a :ref:`metadata-only deposit <use-case-metadata-only-deposit>`
* updates the deposit status and schedules a checking task by querying
  :ref:`swh-scheduler <swh-scheduler>`, otherwise

Graphically:

.. figure:: ../images/deposit-workflow-reception.svg
   :alt:

For metadata-only deposits, this is the end of the story.
The next section narrates what happens next for code deposits.

Checking
--------

As we saw above, the deposit API server's synchronous work ends after sending
a checking task.

This task is implemented by :class:`swh.deposit.loader.checker.DepositChecker`;
which is simply an other call to the deposit API,
implemented in :class:`swh.deposit.api.private.deposit_check.APIChecks`.

This API performs longer checks, which require inspecting the deposited archive
(or archives, for clients depositing archives in multiple steps).
This is why it is run by an asynchronous task instead of being checked immediately
when the client sent a query.

When it is done, it sets the deposit's status to "verified" (so clients polling
for the status know this step succeeded) and schedule a loading task.

Graphically:

.. figure:: ../images/deposit-workflow-checking.svg
   :alt:

Note that the check task is actually just a thin wrapper around an API call.
While the checks could be done in the task itself, it would mean sending
all archives from the deposit API to the celery worker, which would be inefficient.
And the gains would not be great, as checking tasks only need to decompress archives,
which is not resource intensive.
Instead, this long-running call to the API proved to be a simpler
and more efficient solution at the current scale of the deposit.

Loading
-------

When the check task finished, it scheduled a load task, implemented by
:class:`swh.loader.package.deposit.loader.DepositLoader`.

It is part of the ``swh.loader.package`` package instead of ``swh-deposit``,
because its design is close to other :ref:`package loaders <swh-loader-core>`:

1. fetch a tarball
2. extract it
3. use :mod:`swh.model.from_disk` to build SWH objects from it
4. load these objects in :ref:`swh-storage <swh-storage>`

The only difference in this process is fetching the tarball from the deposit server,
instead of external repositories.
This tarball is returned by :class:`swh.deposit.api.private.deposit_read`,
which creates it by aggregating all archives sent by the client (usually
only one, but the SWORD protocol allows more).

Finally, when it is done, the loader updates the deposit status via the deposit API.

Graphically:

.. figure:: ../images/deposit-workflow-loading.svg
   :alt: