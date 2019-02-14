.. _developer-setup:

Developer setup
===============

In this guide, we will set up a dual environment:

- A virtual env in which all the |swh| packages will be installed in 'develop'
  mode, this will allow you to navigate the source code, hack it, and run
  locally the unit tests.

- A docker 'cluster' built with docker-compose, which allows to easily run all
  the components of the |swh| architecture. It is possible to run those docker
  containers with your locally modified code for one or several |swh| packages.

  Please read the `README file`_ in the swh-docker-dev repository for more
  details on how to do this.

.. _`README file`: https://forge.softwareheritage.org/source/swh-docker-dev/browse/master/README.md

Checkout the source code
------------------------

Clone the |swh| environment repository::

    ~$ git clone https://forge.softwareheritage.org/source/swh-environment.git
    [...]
    ~$ cd swh-environment
    ~/swh-environment$

Create a virtual env::

    ~/swh-environment$ mkvirtualenv -p /usr/bin/python3 -a $PWD swh
    [...]
    (swh) ~/swh-environment$


.. Note: using virtualenvwrapper_ is not mandatory here. You can use plain
   virtualenvs, or any other venv management tool (pipenv_ or poetry_
   for example). Using a tool such as virtualenvwrapper_ just makes life
   easier...


.. _virtualenvwrapper: https://virtualenvwrapper.readthedocs.io/
.. _poetry: https://poetry.eustace.io/
.. _pipenv: https://pipenv.readthedocs.io/


Install all the swh packages (in develop mode)::

    (swh) ~/swh-environment$ pip install $(./bin/pip-swh-packages --with-testing) \
	                         tox pifpaf
    [...]


Setup the docker environment
----------------------------

Install docker-compose::

    (swh) ~/swh-environment$ pip install docker-compose
    [...]

Make your life easier::

    (swh) ~/swh-environment$ cat >>$VIRTUAL_ENV/bin/postactivate <<EOF
    # unfortunately, the interface cmd for the click autocompletion
    # depends on the shell
    # https://click.palletsprojects.com/en/7.x/bashcomplete/#activation

    shell=$(basename $SHELL)
    case "$shell" in
        "zsh")
            autocomplete_cmd=source_zsh
            ;;
        *)
            autocomplete_cmd=source
            ;;
    esac

    eval "$(_SWH_SCHEDULER_COMPLETE=$autocomplete_cmd swh-scheduler)"
    export SWH_SCHEDULER_URL=http://127.0.0.1:5008/
    export CELERY_BROKER_URL=amqp://127.0.0.1:5072/
    export COMPOSE_FILE=~/swh-environment/swh-docker-dev/docker-compose.yml:~/swh-environment/swh-docker-dev/docker-compose.override.yml
    alias doco=docker-compose

    function swhclean {
        find ~/swh-environment -type d -name __pycache__ -exec rm -rf {} \;
        find ~/swh-environment -type d -name .tox -exec rm -rf {} \;
        find ~/swh-environment -type d -name .hypothesis -exec rm -rf {} \;
    }
    EOF

This postactivate script does:

- install a shell completion handler for the swh-scheduler command,
- preset a bunch of environment variables

  - `SWH_SCHEDULER_URL` so that you can just run `sch-scheduler` against the
    scheduler API instance running in docker, without having to specify the
    endpoint URL,

  - `CELERY_BROKER` so you can execute the `celery` tool without options
    against the rabbitmq server running in the docker environment,

  - `COMPOSE_FILE` so you can run `docker-compose` from everywhere,

- create an alias `doco` for `docker-compose` because this later is way too
  long to type,

- add a `swhclean` shell function to clean your source directories so that
  there is no conflict with docker containers using local swh repositories (see
  below). This will delete any `.tox`, `__pycache__` and `.hypothesis`
  directory found in your swh-environment directory.


Start the SWH platform::

    (swh) ~/swh-environment$ docker-compose up -d
    [...]

Check celery::

    (swh) ~/swh-environment$ celery status
    listers@50ac2185c6c9: OK
    loader@b164f9055637: OK
    indexer@33bc6067a5b8: OK

List task-types::

    (swh) ~/swh-environment$ swh-scheduler task-type list
    [...]

Get more info on a task type::

    (swh) ~/swh-environment$ swh-scheduler task-type list -v -t origin-update-hg
    Known task types:
    origin-update-hg: swh.loader.mercurial.tasks.LoadMercurial
      Loading mercurial repository swh-loader-mercurial
      interval: 1 day, 0:00:00 [1 day, 0:00:00, 1 day, 0:00:00]
      backoff_factor: 1.0
      max_queue_length: 1000
      num_retries: None
      retry_delay: None

Add a new task::

    (swh) ~/swh-environment$ swh-scheduler task add origin-update-hg origin_url=https://hg.logilab.org/master/cubicweb
    Created 1 tasks

    Task 1
      Next run: just now (2019-02-06 12:36:58+00:00)
      Interval: 1 day, 0:00:00
      Type: origin-update-hg
      Policy: recurring
      Args:
      Keyword args:
        origin_url: https://hg.logilab.org/master/cubicweb

Respawn a task::

    (swh) ~/swh-environment$ swh-scheduler task respawn 1
