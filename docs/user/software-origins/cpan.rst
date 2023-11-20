.. _user-software-origins-cpan:

CPAN
====

.. include:: dynamic/cpan_status.inc

The `Comprehensive Perl Archive Network <https://www.cpan.org/>` is Perl's main package
manager.

CPAN packages archived by |swh| will be associated to the metacpan.org domain rather than
cpan.org in order to point to an original web page with information about the package.
This pattern of origin URLs is: :file:`https://metacpan.org/dist/{package_name}`,
which references all versions of the same package.

metacpan.org is also used by |swh| to list packages, thanks to its ElasticSearch API.

CPAN does not seem to store any extrinsic metadata, beyond mapping between author
username and package. Author name and email is present in intrinsic metadata and in
release fields, anyway.

Source code from CPAN is currently only archived on |swh|'s staging infrastructure.
