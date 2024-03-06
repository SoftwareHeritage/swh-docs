pandoc -f markdown -t rst   tables.md  -o /tmp/tables.rst --columns=120

|    Range     |      Description       |             VLAN             | Frontend | MONs  | OSDs  | Switches | Bastion |
| ------------ | ---------------------- | ---------------------------- | :------: | :---: | :---: | :------: | :-----: |
| X.X.X.X/28   | Uplink vlan            | Uplink - Frontend / ID CEA   |    X     |       |       |          |         |
| X.X.X.X/28   | Uplink vlan            | Uplink - Management / ID CEA |          |       |       |          |    X    |
| 10.25.6.0/24 | Default / installation | Default / 1                  |    X     |   X   |   X   |          |         |
| 10.25.1.0/24 | VLAN for ceph access   | Ceph clients / 2             |    X     |   X   |   X   |          |         |
| 10.25.2.0/24 | VLAN for ceph internal | Ceph cluster / 3             |          |       |   X   |          |         |
| 10.25.3.0/24 | Management addresses   | None                         |    X     |   X   |   X   |    X     |         |


|   Type   |   Range   |
| -------- | --------- |
| Frontend | .1-.10    |
| MONs     | .11-.20   |
| OSDs     | .21-.100  |
| switches | .240-.253 |
| GW       | .254      |
