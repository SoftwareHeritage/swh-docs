.. _deposit-integrations:

Integrate a deposit to your website
===================================

There are multiple ways to integrate information about the artefact you deposited to
the archive using the SWHID you obtained in return.


Generate a badge
----------------

To generate a Software Heritage badge for a given object SWHID, for example
`swh:1:dir:bc7ddd62cf3d72ffdc365e1bf2dea6eeaa44e185`:

.. tab-set::

  .. tab-item:: HTML

      .. code-block:: html

         <a href="https://archive.softwareheritage.org/swh:1:dir:bc7ddd62cf3d72ffdc365e1bf2dea6eeaa44e185">
            <img src="https://archive.softwareheritage.org/badge/swh:1:dir:bc7ddd62cf3d72ffdc365e1bf2dea6eeaa44e185/" alt="Archived | swh:1:dir:bc7ddd62cf3d72ffdc365e1bf2dea6eeaa44e185"/>
         </a>

  .. tab-item:: Markdown

      .. code-block:: markdown

         [![SWH](https://archive.softwareheritage.org/badge/swh:1:dir:bc7ddd62cf3d72ffdc365e1bf2dea6eeaa44e185/)](https://archive.softwareheritage.org/swh:1:dir:bc7ddd62cf3d72ffdc365e1bf2dea6eeaa44e185)

   .. tab-item:: reStructuredText

      .. code-block:: rst

         .. image:: https://archive.softwareheritage.org/badge/swh:1:dir:bc7ddd62cf3d72ffdc365e1bf2dea6eeaa44e185/
            :target: https://archive.softwareheritage.org/swh:1:dir:bc7ddd62cf3d72ffdc365e1bf2dea6eeaa44e185

you will obtain the following rendering:

.. image:: https://archive.softwareheritage.org/badge/swh:1:dir:bc7ddd62cf3d72ffdc365e1bf2dea6eeaa44e185/
   :target: https://archive.softwareheritage.org/swh:1:dir:bc7ddd62cf3d72ffdc365e1bf2dea6eeaa44e185


Integrate an iframe
-------------------

A subset of Software Heritage objects (contents and directories) can be embedded in
external websites through the use of iframes_. A dedicated endpoint serving a
minimalist Web UI is available for that use case.

By adding HTML code similar to the one below in a web page,

.. code-block:: html

   <iframe style="width: 100%; height: 500px; border: 1px solid rgba(0, 0, 0, 0.125);"
      src="https://archive.softwareheritage.org/embed/swh:1:cnt:edc043a59197bcebc1d44fb70bf1b84cde3db791;origin=https://github.com/rdicosmo/parmap;visit=swh:1:snp:2d869aa00591d2ac8ec8e7abacdda563d413189d;anchor=swh:1:rev:f140dbc8b05aa3d341c70436a1920a06df9a0ed4;path=/src/parmap.ml">
   </iframe>

you will obtain the following rendering:

.. raw:: html

   <iframe style="width: 100%; height: 500px; border: 1px solid rgba(0, 0, 0, 0.125);"
      src="https://archive.softwareheritage.org/embed/swh:1:cnt:edc043a59197bcebc1d44fb70bf1b84cde3db791;origin=https://github.com/rdicosmo/parmap;visit=swh:1:snp:2d869aa00591d2ac8ec8e7abacdda563d413189d;anchor=swh:1:rev:f140dbc8b05aa3d341c70436a1920a06df9a0ed4;path=/src/parmap.ml">
   </iframe>


Citations
---------

TODO

.. _iframes: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe