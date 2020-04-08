==============
Object storage
==============

There is not one but at least 4 different object stores directly managed
by the Software Heritage group:

- Main archive
- Rocquencourt replica archive
- Azure archive
- AWS archive

The Main archive
================

Uffizi
Located in Rocquencourt

Replica archive
===============

Banco
Located in Rocquencourt, in a different building than the main one

Azure archive
=============

The Azure archive uses an Azure Block Storage backend, implemented in the
*swh.objstorage_backends.azure.AzureCloudObjStorage* Python class.

Internally, that class uses the *block_blob_service* Azure API.

AWS archive
===========

The AWS archive is stored in the *softwareheritage* Amazon S3 bucket, in the US-East
 (N. Virginia) region. That bucket is public.

It is being continuously populated by the :ref:`content_replayer` program.

Softwareheritage Python programs access it using a libcloud backend.

URL
---

``s3://softwareheritage/content``

.. _content_replayer:

content_replayer
----------------

A Python program which reads new objects from Kafka and then copies them from the
 object storages on Banco and Uffizi.


Implementation details
----------------------

* Uses *swh.objstorage.backends.libcloud*

* Uses *libcloud.storage.drivers.s3*


Architecture diagram
====================

.. graph:: swh_archives

	"Main archive" -- "Replica archive";
	"Azure archive";
	"AWS archive";
	"Main archive" [shape=rectangle];
	"Replica archive" [shape=rectangle];
	"Azure archive" [shape=rectangle];
	"AWS archive" [shape=rectangle];
