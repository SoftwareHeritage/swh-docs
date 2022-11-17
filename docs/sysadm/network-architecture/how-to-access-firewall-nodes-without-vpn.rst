.. _firewall_access_no_vpn:

How to access firewall nodes without the vpn
============================================

.. admonition:: Intended audience
   :class: important

   sysadm staff members

Any physical server in the ``192.168.100.0/24`` network should be able to reach the
firewall.

But accessing one of the hypervisor's :ref:`iDRAC <idrac_authentication>` should allow
using the associated serial console of the hypervisor, and then gain access to the
:ref:`firewall <firewall_settings>` node without the vpn.

How?
----

From the serial console, use the root account and the virtual ip of one of the fw node
(``192.168.100.2`` or ``192.168.100.3``):

.. code::

   root@<hypervisor>:/root# ssh root@192.168.100.2
   The authenticity of host '192.168.100.2 (192.168.100.2)' can't be established.
   Password:
   Last login: Fri Dec 10 14:00:00 2021 from 192.168.100.29
   ----------------------------------------------
   |      Hello, this is OPNsense 21.7          |         @@@@@@@@@@@@@@@
   |                                            |        @@@@         @@@@
   | Website:      https://opnsense.org/        |         @@@\\\   ///@@@
   | Handbook:     https://docs.opnsense.org/   |       ))))))))   ((((((((
   | Forums:       https://forum.opnsense.org/  |         @@@///   \\\@@@
   | Code:         https://github.com/opnsense  |        @@@@         @@@@
   | Twitter:      https://twitter.com/opnsense |         @@@@@@@@@@@@@@@
   ----------------------------------------------

   *** pushkin.internal.softwareheritage.org: OPNsense 21.7.6 (amd64/OpenSSL) ***

    ... (redacted) ...

     0) Logout                              7) Ping host
     1) Assign interfaces                   8) Shell
     2) Set interface IP address            9) pfTop
     3) Reset the root password            10) Firewall log
     4) Reset to factory defaults          11) Reload all services
     5) Power off system                   12) Update from console
     6) Reboot system                      13) Restore a backup

   Enter an option:
   ...

Why?
----

In case there is an issue with the firewalls (for example, a VIP election issue
resulting to no available gateway) or the vpn.
