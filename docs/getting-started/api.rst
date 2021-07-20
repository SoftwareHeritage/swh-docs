==============================================
Getting Started with the Software Heritage API
==============================================

Introduction
------------

About Software Heritage
^^^^^^^^^^^^^^^^^^^^^^^

The `Software Heritage project <https://www.softwareheritage.org>`__ was
started in 2015 with a rather impressive goal and purpose:

   Software Heritage is an ambitious initiative that aims at collecting,
   organizing, preserving and sharing all the source code publicly
   available in the world.

Yes, you read it well: all source code available in the world. It implies to
build an equally impressive infrastructure to hold the huge amount of
information represented, make the archive available to the public
through a `nice web interface <https://archive.softwareheritage.org/>`__
and even propose a :ref:`well-documented API <swh-web>` to access it
seamlessly. For the records, there are also :ref:`various datasets
available <swh-dataset>` for download, with detailed instructions
about how to set it up. And, yes it’s huge: the full graph generated
from the archive (with only metadata, content is not included) has more
than 20b nodes and weights 1.2TB. Overall size of the archive is in the
hundreds of TBs.

This article presents, and demonstrates the use of, the `Software
Heritage API <https://archive.softwareheritage.org/api/1/>`__ to query
basic information about archived content and fetch the content of a
software project.

Terms and Concepts
^^^^^^^^^^^^^^^^^^

For our activity we need to define the following terms and concepts:

-  The repositories analysed by the SWH are registered as **origins**.
   Examples of origins are: https://bitbucket.org/anthroweb/apache.git,
   https://github.com/apache/ant, or other types of sources (debian
   source packages, npmjs, pypi, cran..).
-  When repositories are analysed, it creates **snapshots**. Snapshots
   describe the state of the repository at the time of analysis, and
   provide links to the repository content. As an example in the case of a git
   repository, the snapshot links to the list of branches, which
   themselves link to revisions and releases.
-  **Revisions** are consistent sets of directories and contents
   representing the repository at a given time, like in a baseline. They
   can be conceptually mapped to commits in subversion, to git
   references, or to source package versions in debian or nmpjs
   repositories.
-  Revisions are linked to a **directory**, which itself links to other
   directories and **contents** (aka blobs).

A full list of terms is provided in the `Software Heritage
doc <https://wiki.softwareheritage.org/index.php?title=Glossary>`__.

Preliminary steps
-----------------

This article uses Python 3.x on the client side, and the ``requests``
Python module to manipulate the HTTP requests. Note however that any
language that provides HTTP requests (GET, POST) can access the API and
could be used. Firstly let’s make sure we have the correct Python
version and module installed::

   boris@castalia:notebook$ python3 -V
   Python 3.7.3
   boris@castalia:notebooks$ pip3 install requests
   Requirement already satisfied: requests in /usr/lib/python3/dist-packages (2.21.0)
   boris@castalia:notebook$

Initialise the script
---------------------

We need to import a few modules and utilities to play with the Software
Heritage API, namely ``json`` and the aforementioned ``requests``
modules. We also define a utility function to pretty-print json data
easily:

.. code:: python

    import json
    import requests

    # Utility to pretty-print json.
    def jprint(obj):
        # create a formatted string of the Python JSON object
        print(json.dumps(obj, sort_keys=True, indent=4))


The syntax mentioned in the `API
documentation <https://archive.softwareheritage.org/api/1/>`__ is rather
straightforward. Since we want to read it from the main Software
Heritage server, we will use ``https://archive.softwareheritage.org/``
as the basename. All API calls will be forged according to the same
syntax:

::

   https://archive.softwareheritage.org/api/1/<endpoint>

Request basic Information
-------------------------

We want to get some basic information about the main server activity and
content. The ``stat`` endpoint provides a summary of the main indexes and
some statistics about the archive. We can request a GET on the main
counters of the archive using the counters path, as described in the
`endpoint
documentation <https://archive.softwareheritage.org/api/1/stat/counters/>`__:

``/api/1/stat/counters/``

This API endpoint returns the following information:

* **content** is the total number of blobs (files) in the archive.
* **directory** is the total number of repositories in the archive.
* **origin** is the number of distinct origins (repositories) fetched by
  the archive bots.
* **origin_visits** is the total number of visits across all origins.
* **person** is the number of authors (e.g. committers, authors) in the
  archived files.
* **release** is the number of tags retrieved in the archive.
* **revision** is the number of revisions stored in the archive.
* **skipped_content** is the number of objects which could be
  imported in the archive.
* **snapshot** is the number of snapshots stored in the archive.

Note that we use the default JSON format for the output. We could use
YAML if we wanted to, with a custom ``Request Headers`` set to
``application/yaml``.

.. code-block:: python

    resp = requests.get("https://archive.softwareheritage.org/api/1/stat/counters/")
    counters = resp.json()
    jprint(counters)


.. code-block:: python

    {
        "content": 10049535736,
        "directory": 8390591308,
        "origin": 156388918,
        "person": 42263568,
        "release": 17218891,
        "revision": 2109783249
    }


There are almost 10bn blobs (aka files) in the archive and 8bn+
directories already, for 155m repositories analysed.

Now, what about a specific repository? Let’s say we want to find if
`alambic <https://alambic.io>`__ (an open-source data provider and
analysis system for software development) has already been analysed by
the archive’s bots.

Search the archive
------------------

Search for a keyword
^^^^^^^^^^^^^^^^^^^^

The easiest way to look for a keyword in the repositories analysed by
the archive is to use the ``search`` feature of the ``origin`` endpoint.
Documentation for the endpoint is
`here <https://archive.softwareheritage.org/api/1/origin/search/doc/>`__
and the complete syntax is:

::

   `/api/1/origin/search/<keyword>/`

The server returns an array of hashes, with each item being formatted
as:

-  **origin_visits_url** attribute is an URL that points to the API page
   listing all visits (bot fetches) to this repository.
-  **url** is the url of the origin, or repository, itself.

A (truncated) example of a result from this endpoint is shown below:

::

   [
     {
       "origin_visits_url": "https://archive.softwareheritage.org/api/1/origin/https://github.com/borisbaldassari/alambic/visits/",
       "url": "https://github.com/borisbaldassari/alambic"
     }
     ...
   ]

As an example we will look for instances of *alambic* in the archive’s
analysed repositories::

    resp = requests.get("https://archive.softwareheritage.org/api/1/origin/search/alambic/")
    origins = resp.json()
    print(f"We found {len(origins)} entries.")
    for origin in origins[1:10]:
        print(f"- {origin['url']}")


Which produces::

    We found 52 entries.
    -  https://github.com/royal-alambic-club/sauron
    -  https://github.com/scamberlin/alambic
    -  https://github.com/WebTales/alambic-connector-mongodb
    -  https://github.com/WebTales/alambic
    -  https://github.com/AssoAlambic/alambic-website
    -  https://bitbucket.org/nayoub/alambic.git
    -  https://github.com/Alexandru-Dobre/alambic-connector-rest
    -  https://github.com/WebTales/alambic-connector-diffbot
    -  https://github.com/WebTales/alambic-connector-firebase


There are obviously many projects and repositories that embed the word
alambic, and we will need to be a bit more specific if we are to
identify the origin actually related to the alambic project.

If we want to know more about a specific origin, we can simply use the
``url`` attribute (or any known URL) as an entry for any of the
``origin`` endpoints.

Search for a specific origin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now say that we want to query the database for the specific repository
of Alambic, to know what information has been registered by the archive.
The API endpoint can be found `in the swh-web
documentation <https://archive.softwareheritage.org/api/1/origin/doc/>`__,
and has the following syntax:

``/api/1/origin/<origin_url>/get/``

Which returns the same type of JSON object than the ``search`` command
seen previously:

-  **origin_visits_url** attribute is an URL that points to the API page
   listing all visits (bot fetches) to this repository.
-  **url** is the url of the origin, or repository, itself.

We know that Alambic is hosted at
‘https://github.com/borisbaldassari/alambic/’, so the API call will look
like this:

``/api/1/origin/https://github.com/borisbaldassari/alambic/get/``

.. code:: python

    resp = requests.get("https://archive.softwareheritage.org/api/1/origin/https://github.com/borisbaldassari/alambic/get/")
    found = resp.json()
    jprint(found)


.. parsed-literal::

    {
        "origin_visits_url": "https://archive.softwareheritage.org/api/1/origin/https://github.com/borisbaldassari/alambic/visits/",
        "url": "https://github.com/borisbaldassari/alambic"
    }


Get visits information
^^^^^^^^^^^^^^^^^^^^^^

We can use the ``origin_visits_url`` attribute to know more about when
the repository was analysed by the archive bots. The API endpoint is
fully documented on the `Software Heritage doc
site <https://archive.softwareheritage.org/api/1/origin/visits/doc/>`__,
and has the following syntax:

``/api/1/origin/<origin_url>/visits/``

We will use the same query as before about the main Alambic repository.

.. code:: python

    resp = requests.get("https://archive.softwareheritage.org/api/1/origin/https://github.com/borisbaldassari/alambic/visits/")
    found = resp.json()
    length = len(found)
    print(f"Number of visits found: {format(length)}.")
    print("With dates:")
    for visit in found:
        print(f"- {visit['visit']} {visit['date']}")
    print("\nExample of a single visit entry:")
    jprint(found[0])


.. parsed-literal::

    Number of visits found: 5.
    With dates:
    - 5 2021-01-01T19:35:41.308336+00:00
    - 4 2020-02-06T10:41:45.700641+00:00
    - 3 2019-09-01T22:38:12.056537+00:00
    - 2 2019-06-16T04:52:18.162914+00:00
    - 1 2019-01-30T07:19:20.799217+00:00

    Example of a single visit entry:
    {
        "date": "2021-01-01T19:35:41.308336+00:00",
        "metadata": {},
        "origin": "https://github.com/borisbaldassari/alambic",
        "origin_visit_url": "https://archive.softwareheritage.org/api/1/origin/https://github.com/borisbaldassari/alambic/visit/5/",
        "snapshot": "6436d2c9b06cf9bd9efb0b4e463c3fe6b868eadc",
        "snapshot_url": "https://archive.softwareheritage.org/api/1/snapshot/6436d2c9b06cf9bd9efb0b4e463c3fe6b868eadc/",
        "status": "full",
        "type": "git",
        "visit": 5
    }


Get the content
---------------

As defined in the beginning, a snapshot is a capture of the repository
at a given time with links to all branches and releases. In this example
we will work on the snapshot ID of the last visit to Alambic, as returned
by the previous command we executed.

.. code:: python

    # Store snapshot id
    snapshot = found[0]['snapshot']
    print(f"Snapshot is {format(snapshot)}.")


.. parsed-literal::

    Snapshot is 6436d2c9b06cf9bd9efb0b4e463c3fe6b868eadc.


Note that the latest visit to the repository can also be directly
retrieved using the `dedicated
endpoint <https://archive.softwareheritage.org/api/1/origin/visit/latest/doc/>`__
``/api/1/origin/visit/latest/``.

Get the snapshot
^^^^^^^^^^^^^^^^

We want now to retrieve the content of the project at this snapshot. For
that purpose there is the ``snapshot`` endpoint, and its documentation
is `provided
here <https://archive.softwareheritage.org/api/1/snapshot/doc/>`__. The
complete syntax is:

``/api/1/snapshot/<snapshot_id>/``

The snapshot endpoint returns in the ``branches`` attribute a list of
**revisions** (aka commits in a git context), which
themselves point to the set of directories and files in the branch at
the time of analysis. Let’s follow this chain of links, starting with
the snapshot’s list of revisions (branches):

.. code:: python

    snapshotr = requests.get("https://archive.softwareheritage.org/api/1/snapshot/{}/".format(snapshot))
    snapshotj = snapshotr.json()
    jprint(snapshotj)


.. parsed-literal::

    {
        "branches": {
            "HEAD": {
                "target": "refs/heads/master",
                "target_type": "alias",
                "target_url": "https://archive.softwareheritage.org/api/1/revision/6dd0504b43b4459d52e9f13f71a91cc0fc445a19/"
            },
            "refs/heads/devel": {
                "target": "e298b8c5692b18928013a68e41fd185419515075",
                "target_type": "revision",
                "target_url": "https://archive.softwareheritage.org/api/1/revision/e298b8c5692b18928013a68e41fd185419515075/"
            },
            "refs/heads/features/cr152_anonymise_data": {
                "target": "ba3e0dcbfa0cb212a7186e9e62efb6dafe7fe162",
                "target_type": "revision",
                "target_url": "https://archive.softwareheritage.org/api/1/revision/ba3e0dcbfa0cb212a7186e9e62efb6dafe7fe162/"
            },
            "refs/heads/features/cr164_github_project": {
                "target": "0005abb080e4c67a97533ee923e9d28142877752",
                "target_type": "revision",
                "target_url": "https://archive.softwareheritage.org/api/1/revision/0005abb080e4c67a97533ee923e9d28142877752/"
            },
            "refs/heads/features/cr165_github_its": {
                "target": "0005abb080e4c67a97533ee923e9d28142877752",
                "target_type": "revision",
                "target_url": "https://archive.softwareheritage.org/api/1/revision/0005abb080e4c67a97533ee923e9d28142877752/"
            },
            "refs/heads/features/cr89_gitlabwizard": {
                "target": "b941fd5f93a6cfc2349358b891e47d0fffe0ed2d",
                "target_type": "revision",
                "target_url": "https://archive.softwareheritage.org/api/1/revision/b941fd5f93a6cfc2349358b891e47d0fffe0ed2d/"
            },
            "refs/heads/master": {
                "target": "6dd0504b43b4459d52e9f13f71a91cc0fc445a19",
                "target_type": "revision",
                "target_url": "https://archive.softwareheritage.org/api/1/revision/6dd0504b43b4459d52e9f13f71a91cc0fc445a19/"
            }
        },
        "id": "6436d2c9b06cf9bd9efb0b4e463c3fe6b868eadc",
        "next_branch": null
    }


Get the root directory
^^^^^^^^^^^^^^^^^^^^^^

The revision associated to the branch can be retrieved by following the
corresponding link in the ``target_url`` attribute. We will follow the
``refs/heads/master`` branch and get the associated revision object. In
this case (a git repository) the revision is equivalent to a commit, with
an ID and message.

.. code:: python

    print(f"Revision ID is {snapshotj['id']}.")
    master_url = snapshotj['branches']['refs/heads/master']['target_url']
    masterr = requests.get(master_url)
    masterj = masterr.json()
    jprint(masterj)


.. parsed-literal::

    Revision ID is 6436d2c9b06cf9bd9efb0b4e463c3fe6b868eadc
    {
        "author": {
            "email": "boris.baldassari@gmail.com",
            "fullname": "Boris Baldassari <boris.baldassari@gmail.com>",
            "name": "Boris Baldassari"
        },
        "committer": {
            "email": "boris.baldassari@gmail.com",
            "fullname": "Boris Baldassari <boris.baldassari@gmail.com>",
            "name": "Boris Baldassari"
        },
        "committer_date": "2020-11-01T12:55:13+01:00",
        "date": "2020-11-01T12:55:13+01:00",
        "directory": "fd9fe3477db3b9b7dea63509832b3fa99bdd7eb8",
        "directory_url": "https://archive.softwareheritage.org/api/1/directory/fd9fe3477db3b9b7dea63509832b3fa99bdd7eb8/",
        "extra_headers": [],
        "history_url": "https://archive.softwareheritage.org/api/1/revision/6dd0504b43b4459d52e9f13f71a91cc0fc445a19/log/",
        "id": "6dd0504b43b4459d52e9f13f71a91cc0fc445a19",
        "merge": false,
        "message": "#163 Fix dygraphs zero padding in forums plugin.\n",
        "metadata": {},
        "parents": [
            {
                "id": "a4a2d8925c1cc43612602ac28e4ca9a31728b151",
                "url": "https://archive.softwareheritage.org/api/1/revision/a4a2d8925c1cc43612602ac28e4ca9a31728b151/"
            }
        ],
        "synthetic": false,
        "type": "git",
        "url": "https://archive.softwareheritage.org/api/1/revision/6dd0504b43b4459d52e9f13f71a91cc0fc445a19/"
    }


The revision references the root directory of the project. We can
list all files and directories at the root by requesting more
information from the ``directory_url`` attribute. The endpoint is
documented
`here <https://archive.softwareheritage.org/api/1/directory/doc/>`__ and
has the following syntax:

``/api/1/directory/<directory_id>/``

The structure of the response is an **array of directory entries**.
**Content entries** are represented like this:

::

   {
       "checksums": {
           "sha1": "5973b582bfaeffa71c924e3fe7150620230391d8",
           "sha1_git": "a6c4d5ebfdf88b3b1a65996f6c438c01bf60740b",
           "sha256": "8761f1e1fd96fc4c86ad343a7c19ecd51c0bde4d7055b3315c3975b31ec61bbc"
       },
       "dir_id": "3ee1366c6dd0b7f4ba9536e9bcc300236ac8f200",
       "length": 101,
       "name": ".dockerignore",
       "perms": 33188,
       "status": "visible",
       "target": "a6c4d5ebfdf88b3b1a65996f6c438c01bf60740b",
       "target_url": "https://archive.softwareheritage.org/api/1/content/sha1_git:a6c4d5ebfdf88b3b1a65996f6c438c01bf60740b/",
       "type": "file"
   }

And **directory entries** are represented with:

::

   {
       "dir_id": "3ee1366c6dd0b7f4ba9536e9bcc300236ac8f200",
       "length": null,
       "name": "doc",
       "perms": 16384,
       "target": "316468df4988351911992ecbf1866f1c1f575c23",
       "target_url": "https://archive.softwareheritage.org/api/1/directory/316468df4988351911992ecbf1866f1c1f575c23/",
       "type": "dir"
   }

We will print the list of contents and directories located at the root of
the repository at the time of analysis:

.. code:: python

    root_url = masterj['directory_url']
    rootr = requests.get(root_url)
    rootj = rootr.json()
    for f in rootj:
        print(f"- {f['name']}.")


.. parsed-literal::

    - .dockerignore
    - .env
    - .gitignore
    - CODE_OF_CONDUCT.html
    - CODE_OF_CONDUCT.md
    - LICENCE.html
    - LICENCE.md
    - Readme.md
    - doc
    - docker
    - docker-compose.run.yml
    - docker-compose.test.yml
    - dockercfg.encrypted
    - mojo
    - resources


We could follow the links up (or down) to the leaves in order to rebuild
the project structure and download all files individually to rebuild the
project locally. However the archive can do it for us, and provides a
feature to download the content of a whole project in one step:
**cooking**. The feature is described in the :ref:`swh-vault
documentation <swh-vault>`.

Download content of a project
-----------------------------

When we ask the Archive to cook a directory for us, it invokes an
asynchronous job to recuversively fetch the directories and files of the
project, following the graph up to the leaves (files) and exporting the
result as a tar.gz file. This procedure is handled by the :ref:`swh-vault
component <swh-vault>`, and it’s all automatic.

Order the meal
^^^^^^^^^^^^^^

A cooking job can be invoked for revisions, directories or snapshots
(soon). It is initiated with a POST request on the ``vault/<type>/``
endpoint, and its complete syntax is:

``/api/1/vault/directory/<directory_id>/``

The first POST request initiates the cooking, and subsequent GET
requests can fetch the job result and download the archive. See the
`Software Heritage documentation <vault-primer>` on this, with useful
examples. The API endpoint is documented `here <https://archive.softwareheritage.org/api/1/vault/directory/doc/>`__.

In this example we will fetch the content of the root directory that we
previously identified.

.. code:: python

    mealr = requests.post("https://archive.softwareheritage.org/api/1/vault/directory/3ee1366c6dd0b7f4ba9536e9bcc300236ac8f200/")
    mealj = mealr.json()
    jprint(mealj)


.. parsed-literal::

    {
        "fetch_url": "https://archive.softwareheritage.org/api/1/vault/directory/3ee1366c6dd0b7f4ba9536e9bcc300236ac8f200/raw/",
        "id": 379321799,
        "obj_id": "3ee1366c6dd0b7f4ba9536e9bcc300236ac8f200",
        "obj_type": "directory",
        "progress_message": null,
        "status": "done"
    }


Ask if it’s ready
^^^^^^^^^^^^^^^^^

We can use a GET request on the same URL to get information about the
process status:

.. code:: python

    statusr = requests.get("https://archive.softwareheritage.org/api/1/vault/directory/3ee1366c6dd0b7f4ba9536e9bcc300236ac8f200/")
    statusj = statusr.json()
    jprint(statusj)


.. parsed-literal::

    {
        "fetch_url": "https://archive.softwareheritage.org/api/1/vault/directory/3ee1366c6dd0b7f4ba9536e9bcc300236ac8f200/raw/",
        "id": 379321799,
        "obj_id": "3ee1366c6dd0b7f4ba9536e9bcc300236ac8f200",
        "obj_type": "directory",
        "progress_message": null,
        "status": "done"
    }


Get the plate
^^^^^^^^^^^^^

Once the processing is finished (it can take up to a few minutes) the
tar.gz archive can be downloaded through the ``fetch_url`` link, and
extracted as a tar.gz archive:

::

   boris@castalia:downloads$ curl https://archive.softwareheritage.org/api/1/vault/directory/3ee1366c6dd0b7f4ba9536e9bcc300236ac8f200/raw/ -o myarchive.tar.gz
     % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                    Dload  Upload   Total   Spent    Left  Speed
   100 9555k  100 9555k    0     0  1459k      0  0:00:06  0:00:06 --:--:-- 1717k
   boris@castalia:downloads$ ls
   myarchive.tar.gz
   boris@castalia:downloads$ tar xzf myarchive.tar.gz
   3ee1366c6dd0b7f4ba9536e9bcc300236ac8f200/
   3ee1366c6dd0b7f4ba9536e9bcc300236ac8f200/.dockerignore
   3ee1366c6dd0b7f4ba9536e9bcc300236ac8f200/.env
   3ee1366c6dd0b7f4ba9536e9bcc300236ac8f200/.gitignore
   3ee1366c6dd0b7f4ba9536e9bcc300236ac8f200/CODE_OF_CONDUCT.html
   3ee1366c6dd0b7f4ba9536e9bcc300236ac8f200/CODE_OF_CONDUCT.md
   3ee1366c6dd0b7f4ba9536e9bcc300236ac8f200/LICENCE.html
   3ee1366c6dd0b7f4ba9536e9bcc300236ac8f200/LICENCE.md
   3ee1366c6dd0b7f4ba9536e9bcc300236ac8f200/Readme.md
   3ee1366c6dd0b7f4ba9536e9bcc300236ac8f200/doc/
   3ee1366c6dd0b7f4ba9536e9bcc300236ac8f200/doc/Readme.md
   3ee1366c6dd0b7f4ba9536e9bcc300236ac8f200/doc/config
   [SNIP]

Conclusion
----------

In this article, we learned **how to explore and use the Software
Heritage archive using its API**: searching for a repository,
identifying projects and downloading specific snapshots of a repository.
There is a lot more to the Archive and its API than what we have seen,
and all features are generously documented on the `Software Heritage web
site <https://archive.softwareheritage.org/api/>`__.



