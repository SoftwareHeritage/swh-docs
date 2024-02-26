.. _idrac:

iDRAC
=====

.. admonition:: Intended audience
   :class: important

   sysadm staff members

The **integrated Dell Remote Access Controller** is the remote console that's to control
servers (e.g DELL, ...).

A non-exhaustive list of :ref:`iDRACs <network_configuration>`:

* banco
* hypervisor3
* mucem
* orsay
* uffizi
* ...

Note: Use `pass search idrac` to retrieve the list.

These instructions are not really vendor-specific and can also be useful for generic
IPMI access or even other kinds of out-of-band management system implementations.

.. _connection_how_to:

Connection how to
-----------------

You will need to install the following packages on your local machine:

* `sshuttle <https://tracker.debian.org/pkg/sshuttle>`_
* `icedtea-8-plugin <https://tracker.debian.org/pkg/icedtea-web>`_

On debian like machines:

.. code::

   apt install sshuttle icedtea-8-plugin

sshuttle
~~~~~~~~

sshuttle uses firewall rules to redirect traffic to a set of ip addresses via a SSH
tunnel.

By default, you can run sshuttle as your own user. This will forward all TCP packets to
any hosts through the tunnel.

To be able to use UDP (e.g. for the IPMI SoL), you need to run sshuttle as root with the
tproxy method.

This may need some `specific routing setup
<https://sshuttle.readthedocs.io/en/stable/tproxy.html>`_ to work; for instance, in
``/etc/network/interfaces``:

.. code::

   # This file describes the network interfaces available on your system
   # and how to activate them. For more information, see interfaces(5).
   source /etc/network/interfaces.d/*
   # The loopback network interface
   auto lo
   iface lo inet loopback
       up ip route add local default dev lo table 100
       up ip rule add fwmark 1 lookup 100
       up ip -6 route add local default dev lo table 100
       up ip -6 rule add fwmark 1 lookup 100

Once this is setup and the marked packets are properly routed, sshuttle's tproxy method
can do its work:

.. code::

   $ ssh-add ~/.ssh/<user-key>
   $ username=<user-name>
   $ sudo SSH_AUTH_SOCK="$SSH_AUTH_SOCK" sshuttle --python python3 \
       --method tproxy \
       -r ${username}@sesi-ssh.inria.fr 128.93.162.142 128.93.134.0/26

.. _idrac_authentication:

Authentication
--------------

Usernames and passwords for logging in are in the :ref:`credentials storage
<how_to_manage_creds_store>`, under ``infra/HOSTNAME/idrac``

If not found, check the default DELL or Supermicro/IPMI credentials which are under
``infra/idrac/{dell,supermicro-ipmi}``.

.. _management_network:

Management network
------------------

Look up the hostname of the management interface you want to access in the `inventory
<https://inventory.internal.softwareheritage.org/ipam/prefixes/9/ip-addresses/>`_.

The machines hosted in the main Software Heritage bay at Rocquencourt use the
128.93.134.0/26 network.

The first usable IP address is **128.93.134.1** and the last one **128.93.134.62**.

**128.93.134.30** is a gateway.

.. _connect_to_the_serial_console:

Connect to the serial console
-----------------------------

The console can be unavailable on the webui on servers with an expired license. The
serial console can still be used. Example:

.. code::

   ipmitool -I lanplus -H swh-es3-adm.inria.fr -U root -P  sol activate

NOTE: This command is available on the ``ipmitool`` package.
