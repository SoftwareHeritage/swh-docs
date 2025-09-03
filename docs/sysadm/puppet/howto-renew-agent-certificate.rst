.. _puppet_howto_renew_agent_certificate:

How to renew an agent certificate
=================================

.. admonition:: Intended audience
   :class: important

   sysadm members


Check the certificate expiration dates
--------------------------------------

On the puppet master (pergamon), this lists all certificates that expire within the next three months:

::

  root@pergamon:~# puppetserver ca list --all --format json | jq ".signed|sort_by(.not_after)[]|select(.not_after <= \"$(date -d '3 months' +%Y-%m-%dT%H:%M:%S)\")"

Renew an agent certificate
--------------------------

On the puppet master (pergamon):

- Revoke and delete the old certificate

::

  root@pergamon:~# puppetserver ca clean --certname kelvingrove.internal.softwareheritage.org 2>/dev/null
  Certificate for kelvingrove.internal.softwareheritage.org has been revoked
  Cleaned files related to kelvingrove.internal.softwareheritage.org

On the agent (kelvingrove for this example), delete the old certificate and generate a new one:

::

  root@kelvingrove:~# rm -r /var/lib/puppet/ssl
  root@kelvingrove:~# puppet agent --test
  Info: Creating a new SSL key for kelvingrove.internal.softwareheritage.org
  Info: Caching certificate for ca
  Info: csr_attributes file loading from /etc/puppet/csr_attributes.yaml
  Info: Creating a new SSL certificate request for kelvingrove.internal.softwareheritage.org
  Info: Certificate Request fingerprint (SHA256): 81:3A:FD:83:A2:64:CA:69:E9:EF:14:91:66:24:0D:DA:E0:6F:B5:1B:44:C2:BA:62:82:C9:94:C6:1D:F8:83:2D
  Info: Caching certificate for kelvingrove.internal.softwareheritage.org
  Info: Caching certificate_revocation_list for ca
  Info: Caching certificate for ca
  Info: Using configured environment 'production'
  Info: Retrieving pluginfacts
  Info: Retrieving plugin
  Info: Retrieving locales
  Info: Loading facts
  Info: Caching catalog for kelvingrove.internal.softwareheritage.org
  Info: Applying configuration version '1736934322'
  ...
