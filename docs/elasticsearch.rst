==============
Elasticsearch
==============

Software Heritage uses an Elasticsearch cluster for long-term log storage.

Hardware implementation
=======================

- 3x Xeon E3v6 (Skylake) servers with 32GB of RAM and 3x 2TB of hard drives each
- 2x gigabit switches

List of nodes
-------------

* esnode1.internal.softwareheritage.org.
* esnode2.internal.softwareheritage.org.
* esnode3.internal.softwareheritage.org.

Architecture diagram
====================

.. graphviz:: images/elasticsearch.dot

Per-node storage
================

- one root hard drive with a small filesystem
- 3x 2TB hard drives in RAID0
- xfs filesystem on this volume, mounted on */srv/elasticsearch*

Remark
======

The root hard drive of the Elasticsearch nodes is also used to
store an ext4 `Kafka` dedicated filesystem mounted on */srv/kafka* .
