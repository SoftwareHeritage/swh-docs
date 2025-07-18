.. _developer-setup:

Developer setup
===============

In this guide we describe how to set up a developer environment in which one
can easily navigate the source code, make modifications, write and execute unit
tests.

For this, we will use a `virtual environment`_ in which all the |swh| packages will be
installed in 'develop' mode, this will allow you to navigate the source code,
hack it, and run locally the unit tests.

To test the effect of your modifications, you can :ref:`install your own local
Software Heritage instance <getting-started>` using Docker.

.. _`documentation`: https://gitlab.softwareheritage.org/swh/devel/swh-environment/-/blob/master/docker/README.rst
.. _`virtual environment`: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment


Install required dependencies
-----------------------------

Software Heritage requires some dependencies that are usually packaged by your
package manager.

.. tab-set::

  .. tab-item:: Debian/Ubuntu

    .. code-block:: console

      sudo apt install lsb-release wget apt-transport-https

      sudo wget https://www.postgresql.org/media/keys/ACCC4CF8.asc -O /etc/apt/trusted.gpg.d/postgresql.asc

      echo "deb https://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" | sudo tee -a /etc/apt/sources.list.d/pgdg.list

      sudo wget https://downloads.apache.org/cassandra/KEYS -O /etc/apt/trusted.gpg.d/cassandra.asc

      echo "deb https://debian.cassandra.apache.org 41x main" | sudo tee -a /etc/apt/sources.list.d/cassandra.list

      sudo apt update

      sudo apt install \
          build-essential pkg-config lzip rsync \
          python3 python3-pip python3-venv virtualenvwrapper \
          libpython3-dev libsystemd-dev libsvn-dev libffi-dev librdkafka-dev \
          fuse3 libfuse3-dev libcmph-dev libleveldb-dev \
          git myrepos \
          graphviz plantuml inkscape \
          postgresql libpq-dev cassandra redis-server

  .. tab-item:: Fedora

    .. code-block:: console

      # Install Java-specific repository and JDK
      sudo dnf install adoptium-temurin-java-repository
      sudo dnf config-manager setopt adoptium-temurin-java-repository.enabled=1
      sudo dnf install temurin-17-jdk

      sudo update-alternatives --set java /usr/lib/jvm/temurin-17-jdk/bin/java

      sudo rpm --import https://downloads.apache.org/cassandra/KEYS

      echo "[cassandra]
      name=Apache Cassandra
      baseurl=https://redhat.cassandra.apache.org/50x/
      gpgcheck=1
      repo_gpgcheck=0
      gpgkey=https://downloads.apache.org/cassandra/KEYS" | sudo tee /etc/yum.repos.d/cassandra.repo

      sudo dnf -y update

      sudo dnf -y install cassandra

      sudo dnf -y group install c-development

      sudo dnf -y install \
          pkgconf-pkg-config lzip rsync python3.11 python3-virtualenvwrapper \
          python3.11-devel systemd-devel subversion-devel libffi-devel \
          librdkafka fuse3 fuse3-devel leveldb-devel git myrepos graphviz \
          plantuml inkscape postgresql-server postgresql-contrib libpq \
          libpq-devel redis

      # You will also need to install CMPH manually, as it is not (yet?) included in the Fedora repositories
      wget https://sourceforge.net/projects/cmph/files/v2.0.2/cmph-2.0.2.tar.gz
      tar -xvf cmph-2.0.2.tar.gz
      cd cmph-2.0.2
      ./configure && make && sudo make install
      cd ..

.. Note:: Python 3.10 or newer is required

This installs basic system utilities, Python library dependencies, development tools,
documentation tools and our main database management systems.

Cassandra and PostgreSQL will be started by tests when they need it, so you
don't need them started globally (this will save you some RAM):

.. code-block:: console

  sudo systemctl disable --now cassandra postgresql

You must also have ``nodejs >= 20`` in your development environment.
You can install node 18 using these commands:

.. tab-set::

  .. tab-item:: Debian/Ubuntu

    .. code-block:: console

      curl -fsSL https://deb.nodesource.com/setup_20.x | sudo bash -
      sudo apt install -y nodejs

  .. tab-item:: Fedora

    .. code-block:: console

       sudo dnf -y install nodejs

|swh| uses the ``yarn`` package manager to retrieve frontend dependencies and development tools.
You must install its latest classic version using this command:

.. tab-set::

  .. tab-item:: Debian/Ubuntu

    .. code-block:: console

       sudo corepack enable

  .. tab-item:: Fedora

    .. code-block:: console

       sudo dnf -y install yarnpkg

If you intend to work on |swh| archive search features, Elasticsearch must also be
present in your development environment. Proceed as follows to install it:

.. tab-set::

  .. tab-item:: Debian/Ubuntu

    .. code-block:: console

      sudo wget https://artifacts.elastic.co/GPG-KEY-elasticsearch -O /etc/apt/trusted.gpg.d/elasticsearch.asc

      echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elasticsearch.list

      sudo apt update

      sudo apt install elasticsearch

  .. tab-item:: Fedora

    .. code-block:: console

      echo "[elasticsearch]
      name=Elasticsearch repository for 8.x packages
      baseurl=https://artifacts.elastic.co/packages/8.x/yum
      gpgcheck=1
      gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
      autorefresh=1
      type=rpm-md" | sudo tee /etc/yum.repos.d/elasticsearch.repo

      sudo dnf -y update

      sudo dnf -y install elasticsearch

If you intend to build the full |swh| documentation, the ``postgresql-autodoc`` utility must
also be installed, follow these `instructions <https://github.com/cbbrowne/autodoc#installation>`_
to do so.

.. _checkout-source-code:

Checkout the source code
------------------------

Clone the |swh| environment repository:

.. code-block:: console

    ~$ git clone https://gitlab.softwareheritage.org/swh/devel/swh-environment.git
    [...]
    ~$ cd swh-environment
    ~/swh-environment$

Create a virtualenv:

.. code-block:: console

    ~/swh-environment$ source /usr/share/virtualenvwrapper/virtualenvwrapper.sh
    ~/swh-environment$ mkvirtualenv -p /usr/bin/python3 -a $PWD swh
    [...]
    (swh) ~/swh-environment$

Checkout all the swh packages source repositories:

.. code-block:: console

    (swh) ~/swh-environment$ pip install pre-commit
    (swh) ~/swh-environment$ ./bin/update

In the future you can re-activate the created virtualenv with:

.. code-block:: console

   $ workon swh
   (swh) ~/swh-environment$

.. Note:: the above assumes you are using virtualenvwrapper_ to manage your
   Python virtualenvs, but that is by no means mandatory. You can use plain
   virtualenvs, or any other virtualenv management tool (pipenv_ or poetry_ for
   example). virtualenvwrapper_ is our preference, but YMMV.

.. _virtualenvwrapper: https://virtualenvwrapper.readthedocs.io/
.. _poetry: https://poetry.eustace.io/
.. _pipenv: https://pipenv.readthedocs.io/


Install all the swh packages (in development mode, with testing dependencies):

.. code-block:: console

    (swh) ~/swh-environment$ bin/install


Executing unit tests
--------------------

Unit tests are using the pytest_ framework, and can be executed directly or via
tox_. The main difference between these 2 test execution environments is:

- When executed via tox_, all the dependencies (including swh ones) are
  installed from pypi_: you test your modifications against the latest
  published version of every swh package but the current one.

- When you execute pytest_ directly, swh dependencies are used from your
  current virtualenv, installed from the git repositories: you test your
  modification against the HEAD of every swh package.

For example, running unit tests for the swh-loader-git_ package:

.. code-block:: console

    (swh) ~/swh-environment$ cd swh-loader-git
    (swh) ~/swh-environment/swh-loader-git$ pytest
	=========================== test session starts ============================
    platform linux -- Python 3.5.3, pytest-3.8.2, py-1.6.0, pluggy-0.7.1
    hypothesis profile 'default' -> database=DirectoryBasedExampleDatabase('/home/ddouard/src/swh-environment/swh-loader-git/.hypothesis/examples')
    rootdir: /home/ddouard/src/swh-environment/swh-loader-git, inifile: pytest.ini
    plugins: requests-mock-1.5.2, postgresql-1.3.4, env-0.6.2, django-3.4.7, cov-2.6.0, pylama-7.6.5, hypothesis-3.76.0, celery-4.2.1
    collected 25 items

    swh/loader/git/tests/test_converters.py ........                     [ 32%]
    swh/loader/git/tests/test_from_disk.py .....                         [ 52%]
    swh/loader/git/tests/test_loader.py ......                           [ 76%]
    swh/loader/git/tests/test_tasks.py ...                               [ 88%]
    swh/loader/git/tests/test_utils.py ...                               [100%]
    ============================= warnings summary =============================
	[...]
	================== 25 passed, 12 warnings in 6.66 seconds ==================

Running the same test, plus code linting and static analysis, using tox:

.. code-block:: console

    (swh) ~/swh-environment/swh-loader-git$ tox
    GLOB sdist-make: ~/swh-environment/swh-loader-git/setup.py
    flake8 create: ~/swh-environment/swh-loader-git/.tox/flake8
    flake8 installdeps: flake8
    flake8 installed: entrypoints==0.3,flake8==3.7.7,mccabe==0.6.1,pycodestyle==2.5.0,pyflakes==2.1.1,swh.loader.git==0.0.48.post3
    flake8 run-test-pre: PYTHONHASHSEED='2028963506'
    flake8 runtests: commands[0] | ~/swh-environment/swh-loader-git/.tox/flake8/bin/python -m flake8
    py3 create: ~/swh-environment/swh-loader-git/.tox/py3
    py3 installdeps: .[testing], pytest-cov
    py3 inst: ~/swh-environment/swh-loader-git/.tox/.tmp/package/1/swh.loader.git-0.0.48.post3.zip
    py3 installed: aiohttp==3.5.4,amqp==2.4.2,arrow==0.13.1,async-timeout==3.0.1,atomicwrites==1.3.0,attrs==19.1.0,billiard==3.5.0.5,celery==4.2.1,certifi==2018.11.29,chardet==3.0.4,Click==7.0,coverage==4.5.2,decorator==4.3.2,dulwich==0.19.11,elasticsearch==6.3.1,Flask==1.0.2,idna==2.8,idna-ssl==1.1.0,itsdangerous==1.1.0,Jinja2==2.10,kombu==4.4.0,MarkupSafe==1.1.1,more-itertools==6.0.0,msgpack-python==0.5.6,multidict==4.5.2,pathlib2==2.3.3,pluggy==0.9.0,psutil==5.6.0,psycopg2==2.7.7,py==1.8.0,pytest==3.10.1,pytest-cov==2.6.1,python-dateutil==2.8.0,pytz==2018.9,PyYAML==3.13,requests==2.21.0,retrying==1.3.3,six==1.12.0,swh.core==0.0.55,swh.loader.core==0.0.39,swh.loader.git==0.0.48.post3,swh.model==0.0.30,swh.objstorage==0.0.30,swh.scheduler==0.0.49,swh.storage==0.0.129,systemd-python==234,typing-extensions==3.7.2,urllib3==1.24.1,vcversioner==2.16.0.0,vine==1.2.0,Werkzeug==0.14.1,yarl==1.3.0
    py3 run-test-pre: PYTHONHASHSEED='2028963506'
    py3 runtests: commands[0] | pytest --cov=swh --cov-branch
    =========================== test session starts ============================
    platform linux -- Python 3.5.3, pytest-3.10.1, py-1.8.0, pluggy-0.9.0
    rootdir: ~/swh-environment/swh-loader-git, inifile: pytest.ini
    plugins: cov-2.6.1, celery-4.2.1
    collected 25 items

    swh/loader/git/tests/test_converters.py ........                     [ 32%]
    swh/loader/git/tests/test_from_disk.py .....                         [ 52%]
    swh/loader/git/tests/test_loader.py ......                           [ 76%]
    swh/loader/git/tests/test_tasks.py ...                               [ 88%]
    swh/loader/git/tests/test_utils.py ...                               [100%]

    ----------- coverage: platform linux, python 3.5.3-final-0 -----------
    Name                                      Stmts   Miss Branch BrPart  Cover
    ---------------------------------------------------------------------------
    swh/__init__.py                               1      0      0      0   100%
    swh/loader/__init__.py                        1      0      0      0   100%
    swh/loader/git/__init__.py                    0      0      0      0   100%
    swh/loader/git/converters.py                102     10     44      7    86%
    swh/loader/git/from_disk.py                 157     44     50      6    67%
    swh/loader/git/loader.py                    271     59    114     17    75%
    swh/loader/git/tasks.py                      14      0      0      0   100%
    swh/loader/git/tests/__init__.py              1      0      0      0   100%
    swh/loader/git/tests/conftest.py              4      0      0      0   100%
    swh/loader/git/tests/test_converters.py      94      0      6      0   100%
    swh/loader/git/tests/test_from_disk.py      100      4      0      0    96%
    swh/loader/git/tests/test_loader.py          12      0      0      0   100%
    swh/loader/git/tests/test_tasks.py           26      0      0      0   100%
    swh/loader/git/tests/test_utils.py           14      0      2      0   100%
    swh/loader/git/utils.py                      25      8      8      1    61%
    ---------------------------------------------------------------------------
    TOTAL                                       822    125    224     31    80%


    ============================= warnings summary =============================
    .tox/py3/lib/python3/site-packages/psycopg2/__init__.py:144
      ~/swh-environment/swh-loader-git/.tox/py3/lib/python3/site-packages/psycopg2/__init__.py:144: UserWarning: The psycopg2 wheel package will be renamed from release 2.8; in order to keep installing from binary please use "pip install psycopg2-binary" instead. For details see: <http://initd.org/psycopg/docs/install.html#binary-install-from-pypi>.
        """)

    -- Docs: https://docs.pytest.org/en/latest/warnings.html
    ================== 25 passed, 1 warnings in 7.34 seconds ===================
    _________________________________ summary __________________________________
      flake8: commands succeeded
      py3: commands succeeded
      congratulations :)

Beware that some swh packages require a postgresql server properly configured
to execute the tests. In this case, you will want to use pifpaf_, which will
spawn a temporary instance of postgresql, to encapsulate the call to pytest.
For example, running pytest in the swh-core package:

.. code-block:: console

    (swh) ~/swh-environment$ cd swh-core
	(swh) ~/swh-environment/swh-core$ pifpaf run postgresql -- pytest
    =========================== test session starts ============================
    platform linux -- Python 3.5.3, pytest-3.8.2, py-1.6.0, pluggy-0.7.1
    hypothesis profile 'default' -> database=DirectoryBasedExampleDatabase('/home/ddouard/src/swh-environment/swh-core/.hypothesis/examples')
    rootdir: /home/ddouard/src/swh-environment/swh-core, inifile: pytest.ini
    plugins: requests-mock-1.5.2, postgresql-1.3.4, env-0.6.2, django-3.4.7, cov-2.6.0, pylama-7.6.5, hypothesis-3.76.0, celery-4.2.1
    collected 79 items

    swh/core/tests/test_api.py ..                                        [  2%]
    swh/core/tests/test_config.py ..............                         [ 20%]
    swh/core/tests/test_db.py ....                                       [ 25%]
    swh/core/tests/test_logger.py .                                      [ 26%]
    swh/core/tests/test_serializers.py .....                             [ 32%]
    swh/core/tests/test_statsd.py ...................................... [ 81%]
    ........                                                             [ 91%]
    swh/core/tests/test_utils.py .......                                 [100%]

    ======================== 79 passed in 6.59 seconds =========================

Setup the databases (optional)
------------------------------

If you want to run some packages manually, you may need to setup their databases.

The different databases for each subproject that requires one (like ``storage`` or ``scheduler``) should be setup through the ``swh db create`` or ``swh db init`` command. See their help for more information.


Test changes using a local instance
-----------------------------------

How to test your changes with a local instance is explained in the :ref:`documentation about our Docker setup <docker-environment>`.


Sending your changes
--------------------

After you are done making the changes you want, you can send them on our
forge. See the guide on :ref:`how to submit patches <patch-submission>`.

.. _pytest: https://pytest.org
.. _tox: https://tox.readthedocs.io
.. _pypi: https://pypi.org
.. _swh-loader-git: https://gitlab.softwareheritage.org/swh/devel/swh-loader-git
.. _pifpaf: https://github.com/jd/pifpaf
