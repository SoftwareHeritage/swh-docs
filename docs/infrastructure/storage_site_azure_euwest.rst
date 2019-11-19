Azure Euwest
============

virtual machines
----------------

- dbreplica0: contains a read-only instance of the *softwareheritage* database
- dbreplica1: contains a read-only instance of the *softwareheritage-indexer* database
- kafka01 to 06: journal nodes
- mirror-node-1 to 3
- storage0: storage and object storage services used by the Azure workers
- vangogh: vault service and r/w database for the vault workers
- webapp0: webapp mirror using storage0 services to expose results
- worker01 to 10 and worker13: indexer workers
- worker11 to 12: vault workers (cooking)

The PostgreSQL databases are populated using wal streaming from *somerset*.

storage accounts
----------------

16 Azure storage account (0euwestswh to feuwestswh) are dedicated to blob
containers for object storage.
The first hexadecimal digit of an account name is also the first digit of
its content hashes.
Blobs are stored in location names of the form *6euwestswh/contents*

Other storage accounts:

- archiveeuwestswh: mirrors of dead software forges like *code.google.com*
- swhvaultstorage: cooked archives for the *vault* server running in azure.
- swhcontent: object storage content (individual blobs)
