.. _dns_servers:

DNS servers
===========

.. admonition:: Intended audience
   :class: important

   staff members

Those are (accessible only from INRIA data center):

-  193.51.196.130
-  193.51.196.131

.. _unbound_configuration:

unbound configuration
~~~~~~~~~~~~~~~~~~~~~

If you want to use Software Heritage internal DNS to resolve
**\*.internal.softwareheritage.org**, you might want to use `unbound
<https://www.unbound.net/>`__, which is a local caching DNS capable of dispatching
requests for different domain names to different DNS resolvers. This way you can use
Software Heritage's one for hosts reachable via the VPN and your usual DNS server
(possibly obtained via DHCP) for everything else, as usual.

.. code::

   $ sudo apt install unbound dnssec-trigger
   $ cat /etc/unbound/unbound.conf.d/internal-softwareheritage.conf
   forward-zone:
       name: "internal.softwareheritage.org."
       forward-addr: 192.168.100.29

   forward-zone:
       name: "internal.staging.swh.network."
       forward-addr: 192.168.100.29

   forward-zone:
       name: "100.168.192.in-addr.arpa."
       forward-addr: 192.168.100.29

   forward-zone:
       name: "101.168.192.in-addr.arpa."
       forward-addr: 192.168.100.29

if you use network-manager, make sure that the line ``dns=unbound`` appears in the main
section of its configuration file, e.g.

.. code::

   $ cat /etc/NetworkManager/NetworkManager.conf
   [main]
   plugins=ifupdown,keyfile
   dns=unbound

   [ifupdown]
   managed=true

.. _dnsmasq_configuration_with_network_manager:

dnsmasq configuration (with network-manager)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you use network-manager, using dnsmasq to have the split vpn nameserver configuration
might be the easiest. For this:

- make sure you do not have the stock dnsmasq package installed, as it will turn on an
  instance that conflicts with the one spawned by network-manager
- configure network-manager as follows

.. code::

   $ cat /etc/NetworkManager/NetworkManager.conf
   [main]
   plugins=ifupdown,keyfile
   dns=dnsmasq

   [ifupdown]
   managed=true

You need to add:

::

   $ cat /etc/NetworkManager/dnsmasq.d/swh.conf
   server=/internal.softwareheritage.org/192.168.100.29@tun0
   server=/100.168.192.in-addr.arpa/192.168.100.29@tun0
   server=/101.168.192.in-addr.arpa/192.168.100.29@tun0
   server=/200.168.192.in-addr.arpa/192.168.100.29@tun0
   server=/201.168.192.in-addr.arpa/192.168.100.29@tun0
   server=/202.168.192.in-addr.arpa/192.168.100.29@tun0
   server=/203.168.192.in-addr.arpa/192.168.100.29@tun0
   server=/204.168.192.in-addr.arpa/192.168.100.29@tun0
   server=/205.168.192.in-addr.arpa/192.168.100.29@tun0
   server=/206.168.192.in-addr.arpa/192.168.100.29@tun0
   server=/207.168.192.in-addr.arpa/192.168.100.29@tun0

   # staging area
   server=/staging.swh.network/192.168.100.29@tun0
   server=/128.168.192.in-addr.arpa/192.168.100.29@tun0
   server=/128.168.192.in-addr.arpa/192.168.100.29@tun0
   # admin area
   server=/admin.swh.network/192.168.100.29@tun0
   server=/128.168.192.in-addr.arpa/192.168.100.29@tun0
   server=/admin.swh.network/192.168.100.29@tun0
   server=/128.168.192.in-addr.arpa/192.168.100.29@tun0

Note: assuming your vpn connection is using the tun0 device, if not please adapt
accordingly.

.. _dnsmasq_standalone:

dnsmasq standalone
~~~~~~~~~~~~~~~~~~

**Only if** you're not using network-manager to handle OpenVPN configuration nor dnsmasq
configuration above.

::

   $ apt install dnsmasq
   $ cat /etc/dnsmasq.d/swh.conf
   ... # same content as prior paragraph
   $ systemctl restart dnsmasq

.. _dns_manual:

/etc/hosts
~~~~~~~~~~

If you rather not use a DNS, a (ad-hoc maintained) sample /etc/hosts is available:

.. code::

   192.168.100.18   banco         banco.internal.softwareheritage.org  backup.internal.softwareheritage.org
   192.168.100.21   worker01      worker01.internal.softwareheritage.org
   192.168.100.22   worker02      worker02.internal.softwareheritage.org
   192.168.100.23   worker03      worker03.internal.softwareheritage.org
   192.168.100.24   worker04      worker04.internal.softwareheritage.org
   192.168.100.25   worker05      worker05.internal.softwareheritage.org
   192.168.100.26   worker06      worker06.internal.softwareheritage.org
   192.168.100.27   worker07      worker07.internal.softwareheritage.org
   192.168.100.28   worker08      worker08.internal.softwareheritage.org
   192.168.100.35   worker09      worker09.internal.softwareheritage.org
   192.168.100.36   worker10      worker10.internal.softwareheritage.org
   192.168.100.37   worker11      worker11.internal.softwareheritage.org
   192.168.100.38   worker12      worker12.internal.softwareheritage.org
   192.168.100.39   worker13      worker13.internal.softwareheritage.org
   192.168.100.40   worker14      worker14.internal.softwareheritage.org
   192.168.100.41   worker15      worker15.internal.softwareheritage.org
   192.168.100.42   worker16      worker16.internal.softwareheritage.org
   192.168.100.50   kibana        kibana.internal.softwareheritage.org
   192.168.100.29   pergamon      pergamon.internal.softwareheritage.org  debian.internal.softwareheritage.org icinga.internal.softwareheritage.org
   192.168.100.30   tate          tate.internal.softwareheritage.org
   192.168.100.31   moma          moma.internal.softwareheritage.org
   192.168.100.32   beaubourg     beaubourg.internal.softwareheritage.org
   192.168.101.58   petit-palais  petit-palais.internal.softwareheritage.org
   192.168.101.62   grand-palais  grand-palais.internal.softwareheritage.org
   192.168.101.118  giverny       giverny.internal.softwareheritage.org
   192.168.100.101  uffizi        uffizi.internal.softwareheritage.org
   192.168.100.102  getty         getty.internal.softwareheritage.org
   192.168.100.103  somerset      somerset.internal.softwareheritage.org
   192.168.100.104  saatchi       saatchi.internal.softwareheritage.org
   192.168.100.210  belvedere     belvedere.internal.softwareheritage.org
   192.168.100.4    louvre        louvre.internal.softwareheritage.org
   192.168.100.101  uffizi        uffizi.internal.softwareheritage.org

.. _ssh_configuration:

SSH configuration
~~~~~~~~~~~~~~~~~

The only host with public (internet) SSH access, ``gitlab.softwareheritage.org``, does
not need any specific configuration.

All other hosts (``*.internal.softwareheritage.org``,
``*.internal.staging.swh.network``, ``*.internal.admin.swh.network``) are only (but
directly) accessible through the `VPN <https://wiki.softwareheritage.org/wiki/VPN>`_.

*Note:* the default ssh port on ``tate.internal.softwareheritage.org`` is used for the
sandboxed access to phabricator. Access to the system goes through port 2222. In
``.ssh/config``:

.. code::

   Host tate.internal.softwareheritage.org
       Port 2222
       User LOGIN
