.. _user-software-origins-maven:

Maven
=====

.. include:: dynamic/maven_status.inc

`Maven <https://maven.apache.org/>`_ is Java's main package manager. There are multiple
Maven repositories, each of which store both binary packages (JAR files containing Java
classes) and source code (as source JARs). |swh| archives the latter.

Additionally, |swh| archives each package's :file:`pom.xml` as :term:`extrinsic metadata`
and mines them for links to external version control systems to archive.

See the `Maven lister's documentation <https://gitlab.softwareheritage.org/swh/devel/swh-lister/-/blob/master/swh/lister/maven/README.md>`_
for details on its implementation.
