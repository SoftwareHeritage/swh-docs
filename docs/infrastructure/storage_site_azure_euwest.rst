Azure Euwest
============

virtual machines
----------------

- dbreplica0: contains a read-only instance of the *softwareheritage* database
- dbreplica1: contains a read-only instance of the *softwareheritage-indexer* database
- kafka01 to 06
- mirror-node-1 to 3
- storage0
- vangogh (vault implementation)
- webapp0
- worker01 to 13

The PostgreSQL databases are populated using wal streaming from *somerset*.

storage accounts
----------------

16 Azure storage account (0euwestswh to feuwestswh) are dedicated to blob
containers for object storage.
The first hexadecimal digit of an account name is also the first digit of
its content hashes.
Blobs are storred in location names of the form *6euwestswh/contents*

Other storage accounts:

- archiveeuwestswh: mirrors of dead software forges like *code.google.com*
- swhvaultstorage: cooked archives for the *vault* server running in azure.
- swhcontent: object storage content (individual blobs)


TODO: describe kafka* virtual machines
TODO: describe mirror-node* virtual machines
TODO: describe storage0 virtual machine
TODO: describe webapp0 virtual machine
TODO: describe worker* virtual machines
