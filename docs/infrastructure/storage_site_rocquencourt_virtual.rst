Virtual machines at Rocquencourt
================================

The following virtual machines are hosted on Proxmox hypervisors located at Rocquencourt.
All of them use local storage on their virtual hard drive.

VMs without NFS mount points
----------------------------

- munin0
- tate, used for public and private (intranet) wikis
- getty
- thyssen
- jenkins-debian1.internal.softwareheritage.org
- logstash0
- kibana0
- saatchi
- louvre

Containers and VMs with nfs storage:
------------------------------------

- somerset.internal.softwareheritage.org is a lxc container running on *beaubourg*
  It serves as a host for the *softwareheritage* and *softwareheritage-indexer*
  databases.

- worker01 to worker16.internal.softwareheritage.org
- pergamon
- moma

These VMs access one or more of these NFS volumes located on uffizi::

  uffizi:/srv/softwareheritage/objects
  uffizi:/srv/storage/space
  uffizi:/srv/storage/space/annex
  uffizi:/srv/storage/space/annex/public
  uffizi:/srv/storage/space/antelink
  uffizi:/srv/storage/space/oversize-objects
  uffizi:/srv/storage/space/personal
  uffizi:/srv/storage/space/postgres-backups/somerset
  uffizi:/srv/storage/space/provenance-index
  uffizi:/srv/storage/space/swh-deposit

