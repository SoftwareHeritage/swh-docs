.. _puppet_howto_renew_agent_certificate:

How to renew an agent certificate
=================================

.. admonition:: Intended audience
   :class: important

   sysadm members


Check the certificate expiration dates
--------------------------------------

On the puppet master (pergamon):

::

  root@pergamon:~# cd /var/lib/puppet/ssl/ca/signed
  root@pergamon:/var/lib/puppet/ssl/ca/signed# openssl x509 -text -in beaubourg.softwareheritage.org.pem | grep -i 'not after'
          Not After : Oct 29 18:37:49 2022 GMT

Check the certificate statuses
------------------------------

On the puppet master (pergamon):

::

  root@pergamon:~# puppet cert list --all 2>/dev/null | grep expired
  - "beaubourg.softwareheritage.org"                                (SHA256) 24:50:2E:7F:8B:B0:C7:...:D9:AB:5A:45:46:4D:17:51 (certificate has expired)
  ...

worker3 certificate is ok, beaubourg certificate is expired

Renew an agent certificate
--------------------------

On the puppet master (pergamon):

- Revoke and delete the old certificate

::

  root@pergamon:~# puppet cert clean beaubourg.softwareheritage.org 2>/dev/null
  Notice: Revoked certificate with serial 49
  Notice: Removing file Puppet::SSL::Certificate beaubourg.softwareheritage.org at '/var/lib/puppet/ssl/ca/signed/beaubourg.softwareheritage.org.pem'
  Notice: Removing file Puppet::SSL::Certificate beaubourg.softwareheritage.org at '/var/lib/puppet/ssl/certs/beaubourg.softwareheritage.org.pem'

On the agent (beaubourg for this example), delete the old certificate and generate a new one:

::

  root@beaubourg:~# rm -r /var/lib/puppet/ssl
  root@beaubourg:/var/lib/puppet# puppet agent --test
  Info: Creating a new SSL key for beaubourg.softwareheritage.org
  Info: Caching certificate for ca
  Info: csr_attributes file loading from /etc/puppet/csr_attributes.yaml
  Info: Creating a new SSL certificate request for beaubourg.softwareheritage.org
  Info: Certificate Request fingerprint (SHA256): F5:C9:99:0B:...:62:E9:4F:1B
  Info: Caching certificate for beaubourg.softwareheritage.org
  Info: Caching certificate_revocation_list for ca
  Info: Caching certificate for ca
  Info: Using configured environment 'production'
  Info: Retrieving pluginfacts
  Info: Retrieving plugin
  Info: Retrieving locales
  Info: Loading facts
  Info: Caching catalog for beaubourg.softwareheritage.org
  Info: Applying configuration version '1638980028'
  ...
