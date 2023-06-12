.. _mirror_takedown_requests:

Takedown notices on mirrors
===========================

Software Heritage creates a universal archive of all publicly available source
code. As most of the data collection is done without supervision, some files
turn out to be unwarranted. The organization might then receive take down
requests for copyright infringements or application of data protection laws.
If deemed legitimate, these requests are acted upon by the Software Heritage
team and targeted data is removed from the main archive.

Each mirror is under its own specific set of laws. Therefore data removal
from the main archive is not propagated automatically to the mirrors and
must be reviewed by mirror operators. This also means that mirror
operators might receive specific takedown requests which they must be
able to handle.

Motivations
-----------

Software Heritage might receive a take down requests for an infringement not
applicable to the mirror jurisdiction. As the mission of Software Heritage is
to preserve as much source code as possible, we want to avoid deleting source
code–even if it is only from mirrors–unless it is really needed. Example:
GitHub had deleted the code of ``youtube-dl`` but we would not.

Policy
------

1. Takedown requests sent to mirror operators must be handled in a timely
   fashion.
2. Data removed from the main Software Heritage archive is not to be
   automatically removed from any mirrors.
3. For online mirrors, data removed from the main archive should be made
   inaccessible, but not deleted, as soon as possible.
4. Mirror operators are responsible for reviewing the reasons of removals and
   decide if they should be propagated. If legitimate, data should be removed
   from the mirror as well. Otherwise, it should be made accessible again.

Rationale
---------

Software Heritage needs to provide a feed of objects removed from the archive
so it can eventually be propagated to the mirrors. But such a list of objects
can easily be weaponized.

Imagine “doxxing”–a form of harassment by revealing private information (like
names, addresses or phone numbers)–is made using a Git repository, then
archived by Software Heritage. After receiving a request, Software Heritage
proceeds to remove the copy of this repository from the main archive. With
access to a running mirror and the list of removed objects from the main
archive, an adversary could create preemptive copy of any information removed
from the main archive. In the case of “doxxing” and other abuse of the archive,
such backups could be browsed for further abuse, like blackmail.

While datasets are not exported everyday, the list of removed origins can still
be inferred with some delay by looking at the ones removed between two exports
(publicly available on S3). Therefore, we should assume that such information
is already public.

We can embrace the situation by publishing a list of removed objects which is
good for transparency and for users of exports (for example users of
`swh-graph`) to avoid referring to stale data.

Such a list must be consumed by mirrors, as soon as possible, to prevent rogue
access to the removed objects. Another channel, only available to mirror
operators, provide the reasons behind the removals to allow them to evaluate
the request legitimacy according to their own contexts.

Make data inaccessible as soon as possible has the added benefit of relieving
mirror operators from having to review take down notices with any strong
time-critical constraints. This helps for holidays that are not aligned between
France and countries hosting the mirrors.

Software Heritage will not relay the request itself–it would be a breach of
privacy–but only the reasons for which the organization deemed the request
legitimate (“copyright violation”, “harmful content”, etc.)

Processes
---------

The necessary tooling to implement this policy is `not yet available
<https://gitlab.softwareheritage.org/swh/meta/-/issues/4976>`_.
Until then, the process to propagate takedown requests to mirrors will be the following:

- When the Software Heritage team acts on a takedown request, an email will be
  sent to mirrors with the origins (as URL) and the reasons why we deemed the
  request legitimate.
- Mirror operators can use :command:`swh alter remove` to also remove the origins (see
  :ref:`swh-alter`).
