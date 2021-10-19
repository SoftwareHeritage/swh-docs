.. _how_to_manage_creds_store:

How to manage the credentials store
===================================

.. admonition:: Intended audience
   :class: important

   Staff members

We use `pass <https://www.passwordstore.org/>`_, lightweight directory-based password
manager, as our password manager.

Repository
^^^^^^^^^^

The repository location is `in the forge
<https://forge.softwareheritage.org/source/credentials/>`_.

Configuration
^^^^^^^^^^^^^

A ``git diff`` driver is available: it will allow you to run diff/show commands on
encrypted files transparently. Its configuration is stored in the ``.gitconfig`` and
``.gitattributes`` file in the repo. To enable it you should configure your local copy
to read ``.gitconfig`` from the repository, as it is not done by default for security
reasons.

The following will both clone your repo and set it up to use the diff
driver:

::

   git clone ssh://git@forge.softwareheritage.org/diffusion/PWD/credentials.git
   git config --local include.path ../.gitconfig

(yes, it's really ``../``, because the path is relative to the ``.git/``
directory)

Information
^^^^^^^^^^^

More information can be found at `the repository
<https://forge.softwareheritage.org/source/credentials/browse/master/README>`_.
