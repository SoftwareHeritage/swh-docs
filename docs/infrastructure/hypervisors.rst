===========
Hypervisors
===========

Software Heritage uses a few hypervisors configured in a Proxmox cluster

List of Proxmox nodes
=====================

- beaubourg:  Xeon E7-4809 server, 16 cores/512 GB RAM, bought in 2015
- hypervisor3: EPYC 7301 server, 32 cores/256 GB RAM, bought in 2018

Per-node storage
================

The servers each have physically installed 2.5" SSDs (SAS or SATA), configured
in mdadm RAID10 pools.
A device mapper layer on top of these pools allows Proxmox to easily manage VM
disk images.

Network storage
===============

A :ref:`ceph_cluster` is setup as a shared storage resource.
It can be used to temporarily transfer VM disk images from one hypervisor
node to another, or to directly store virtual machine disk images.
