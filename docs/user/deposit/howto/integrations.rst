.. _deposit-integrations:

Integrate a deposit to your website
===================================

There are multiple ways to integrate information about the artefact you deposited to
the archive using the SWHID you obtained in return.

Generate a badge
----------------

To generate a |swh| badge for a given object SWHID, for example
``swh:1:dir:a5ceced7711d5043da4be6af76749ff638f93909;origin=https://doi.org/10.5281/zenodo.13375878;visit=swh:1:snp:5f88ed08d3cc491a0aab6c41b5591b9119d0d1bf;anchor=swh:1:rel:c5b2d34a22d8bb5cf3ac3d64f84bb0a000278e00``:

.. tab-set::

   .. tab-item:: HTML

      .. code-block:: html

         <a href="https://archive.softwareheritage.org/swh:1:dir:a5ceced7711d5043da4be6af76749ff638f93909;origin=https://doi.org/10.5281/zenodo.13375878;visit=swh:1:snp:5f88ed08d3cc491a0aab6c41b5591b9119d0d1bf;anchor=swh:1:rel:c5b2d34a22d8bb5cf3ac3d64f84bb0a000278e00">
            <img src="https://archive.softwareheritage.org/badge/directory/a5ceced7711d5043da4be6af76749ff638f93909/" alt="Archived | swh:1:dir:a5ceced7711d5043da4be6af76749ff638f93909"/>
         </a>

   .. tab-item:: Markdown

      .. code-block:: markdown

         [![SWH](https://archive.softwareheritage.org/badge/swh:1:dir:a5ceced7711d5043da4be6af76749ff638f93909/)](https://archive.softwareheritage.org/swh:1:dir:a5ceced7711d5043da4be6af76749ff638f93909;origin=https://doi.org/10.5281/zenodo.13375878;visit=swh:1:snp:5f88ed08d3cc491a0aab6c41b5591b9119d0d1bf;anchor=swh:1:rel:c5b2d34a22d8bb5cf3ac3d64f84bb0a000278e00)

   .. tab-item:: reStructuredText

      .. code-block:: rst

         .. image:: https://archive.softwareheritage.org/badge/swh:1:dir:a5ceced7711d5043da4be6af76749ff638f93909/
            :target: https://archive.softwareheritage.org/swh:1:dir:a5ceced7711d5043da4be6af76749ff638f93909;origin=https://doi.org/10.5281/zenodo.13375878;visit=swh:1:snp:5f88ed08d3cc491a0aab6c41b5591b9119d0d1bf;anchor=swh:1:rel:c5b2d34a22d8bb5cf3ac3d64f84bb0a000278e00

You will obtain the following rendering:

.. image:: https://archive.softwareheritage.org/badge/swh:1:dir:a5ceced7711d5043da4be6af76749ff638f93909/
   :target: https://archive.softwareheritage.org/swh:1:dir:a5ceced7711d5043da4be6af76749ff638f93909;origin=https://doi.org/10.5281/zenodo.13375878;visit=swh:1:snp:5f88ed08d3cc491a0aab6c41b5591b9119d0d1bf;anchor=swh:1:rel:c5b2d34a22d8bb5cf3ac3d64f84bb0a000278e00

Integrate an iframe
-------------------

A subset of Software Heritage objects (contents and directories) can be embedded in
external websites through the use of iframes_. A dedicated endpoint serving a
minimalist Web UI is available for that use case. Use this HTML code to do so:

.. code-block:: html

   <iframe style="width: 100%; height: 500px; border: 1px solid rgba(0, 0, 0, 0.125);"
      src="https://archive.softwareheritage.org/browse/embed/swh:1:dir:a5ceced7711d5043da4be6af76749ff638f93909;origin=https://doi.org/10.5281/zenodo.13375878;visit=swh:1:snp:5f88ed08d3cc491a0aab6c41b5591b9119d0d1bf;anchor=swh:1:rel:c5b2d34a22d8bb5cf3ac3d64f84bb0a000278e00/">
   </iframe>

You will obtain the following rendering:

.. raw:: html

   <iframe style="width: 100%; height: 500px; border: 1px solid rgba(0, 0, 0, 0.125);"
      src="https://archive.softwareheritage.org/browse/embed/swh:1:dir:a5ceced7711d5043da4be6af76749ff638f93909;origin=https://doi.org/10.5281/zenodo.13375878;visit=swh:1:snp:5f88ed08d3cc491a0aab6c41b5591b9119d0d1bf;anchor=swh:1:rel:c5b2d34a22d8bb5cf3ac3d64f84bb0a000278e00/">
   </iframe>
