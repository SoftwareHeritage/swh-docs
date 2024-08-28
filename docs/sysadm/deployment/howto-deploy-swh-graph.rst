.. _howto-deploy-swh-graph:

How to deploy swh.graph in production?
======================================

.. admonition:: Intended audience
   :class: important

   sysadm staff members

This page describes how to manually deploy the graph in production on the
granet node.

The compression pipeline (which actually extracts the full dataset) is not yet
documented. So this assumes for now that the new graph version will run with
the same dataset as the previous version.

.. _swh-graph-where-does-it-run:

Where does the graph run?
-------------------------

The graph runs runs on the static node named granet.
To access it:

.. code-block:: console

 ssh granet.internal.softwareheritage.org

What systemd service compose the graph service?
-----------------------------------------------

.. _swh-graph-what-systemd-services-are-used:

The graph is actually composed of 3 systemd services:

.. code-block:: console

 root@granet:~# systemctl list-units | grep swh-graph
 swh-graph-grpc.service      loaded active running   swh-graph gRPC server
 swh-graph-http.service      loaded active running   swh-graph HTTP server
 swh-graph-shm-mount.service loaded active running   swh-graph RAM data cache in /dev/shm

- swh-graph-shm-mount: The actual graph dataset computed by the compression
  pipeline. This is the data served by the graph service. This service
  actually copies the data into ``/dev/shm/swh-graph/default/`` in a structure
  expected by the gRPC service.

- swh-graph-grpc: The low-level gRPC service the (http) api uses to reply to
  client queries. This traverses the graph mounted in ram to reply to queries
  from the (http) api service or directly in grpc from the vpn or internal
  network. The port for this service runs on 50091.

- swh-graph-http: The high-level api exposed and hit by graph consumers. It
  does not directly rely on the (ram) graph data. The port for this service
  runs on 5009.

Overall, the dependency is linear:

::

   swh-graph-http.service -depends-> swh-graph-grpc.service -depends-> swh-graph-shm-mount.service

.. _swh-graph-installation-requirements:

Installation requirements
-------------------------

This is to be done once.

- Minimal python 3.10 & some compilation tools (including jre for some old
  parts). Install as root.

   .. code-block:: console

      apt install build-essential libclang-dev python3 python3-venv \
        default-jre zstd protobuf-compiler

- rust toolchain (can be only installed with the user swhworker)

   .. code-block:: console

      curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

.. _swh-graph-deploy-next-graph-version:

How to deploy the next graph version?
-------------------------------------

Currently, the graph is installed in python virtual environment following the
naming convention `swhgraph_venv_{version}`.

Prior to the graph v5, the gRPC service was running through the java
runtime. Since the graph v5, that service is now running with the Rust
runtime. So an extra compilation step to build the binary
`swh-graph-grpc-serve` is needed.

The different versions so far are installed in the `/opt/` path.

The user running the service is `swhworker`.

The current graph version is targeted through a symbolic link
`/opt/swhgraph_venv`.

So technically, deploying a new version ``version`` is:

1. Creating a new venv ${version}

   .. code-block:: console

    python3 -m venv /opt/swhgraph_venv_${version}

2. Activating that venv

   .. code-block:: console

    source /opt/swhgraph_venv_${version}/bin/activate

3. Building the rust binary `swh-graph-grpc-serve`

   .. code-block:: console

    RUSTFLAGS="-C target-cpu=native" \
      cargo install \
      --features grpc-server \
      swh-graph

4. Updating the symbolic link to the new venv

   .. code-block:: console

    ln -nsf /opt/swhgraph_venv_${version} /opt/swhgraph_venv

5. Restart the swh-graph-grpc.service

   .. code-block:: console

    systemctl restart swh-graph-grpc

Example:

.. code::

   root@granet:~# su - swhworker
   swhworker@granet:~$ version=5.1.0
   swhworker@granet:~$ python3 -m venv /opt/swhgraph_venv_$version
   swhworker@granet:~$ source /opt/swhgraph_venv_$version/bin/activate
   (swhgraph_venv_5.1.0) swhworker@granet:~$ pip install swh.graph==$version
   Collecting swh.graph==5.1.0
     Using cached swh.graph-5.1.0-py3-none-any.whl (58.5 MB)
   Collecting protobuf<5.26.0,>=4.21.11
     Downloading protobuf-4.25.4-cp37-abi3-manylinux2014_x86_64.whl (294 kB)
        |████████████████████████████████| 294 kB 6.2 MB/s
   ...
   Collecting pycparser
     Downloading pycparser-2.22-py3-none-any.whl (117 kB)
        |████████████████████████████████| 117 kB 51.9 MB/s
   Using legacy 'setup.py install' for psycopg2, since package 'wheel' is not installed.
   Installing collected packages: multidict, idna, frozenlist, zipp, yarl, wrapt, urllib3, sortedcontainers, six, packaging, MarkupSafe, exceptiongroup, charset-normalizer, certifi, attrs, async-timeout, aiosignal, aiohappyeyeballs, Werkzeug, typing-extensions, tenacity, sentry-sdk, requests, pyyaml, python-mimeparse, python-magic, python-dateutil, pycparser, Jinja2, itsdangerous, iso8601, importlib-metadata, hypothesis, gunicorn, deprecated, click, blinker, attrs-strict, aiohttp, swh.model, swh.core, msgpack, jmespath, flask, confluent-kafka, cffi, aiohttp-utils, swh.perfecthash, swh.journal, redis, psycopg2, geomet, botocore, types-urllib3, swh.objstorage, swh.counters, s3transfer, mypy-extensions, cassandra-driver, types-requests, types-protobuf, tqdm, swh.storage, pyorc, protobuf, plyvel, grpcio, boto3, swh.dataset, py4j, psutil, mypy-protobuf, grpcio-tools, swh.graph
       Running setup.py install for psycopg2 ... done
   Successfully installed Jinja2-3.1.4 MarkupSafe-2.1.5 Werkzeug-3.0.3 aiohappyeyeballs-2.3.5 aiohttp-3.10.3 aiohttp-utils-3.2.1 aiosignal-1.3.1 async-timeout-4.0.3 attrs-24.2.0 attrs-strict-1.0.1 blinker-1.8.2 boto3-1.34.160 botocore-1.34.160 cassandra-driver-3.29.1 certifi-2024.7.4 cffi-1.17.0 charset-normalizer-3.3.2 click-8.1.7 confluent-kafka-2.5.0 deprecated-1.2.14 exceptiongroup-1.2.2 flask-3.0.3 frozenlist-1.4.1 geomet-0.2.1.post1 grpcio-1.65.4 grpcio-tools-1.62.3 gunicorn-23.0.0 hypothesis-6.111.0 idna-3.7 importlib-metadata-8.2.0 iso8601-2.1.0 itsdangerous-2.2.0 jmespath-1.0.1 msgpack-1.0.8 multidict-6.0.5 mypy-extensions-1.0.0 mypy-protobuf-3.2.0 packaging-24.1 plyvel-1.5.1 protobuf-4.25.4 psutil-6.0.0 psycopg2-2.9.9 py4j-0.10.9.7 pycparser-2.22 pyorc-0.9.0 python-dateutil-2.9.0.post0 python-magic-0.4.27 python-mimeparse-1.6.0 pyyaml-6.0.2 redis-5.0.8 requests-2.32.3 s3transfer-0.10.2 sentry-sdk-2.13.0 six-1.16.0 sortedcontainers-2.4.0 swh.core-3.4.0 swh.counters-0.11.0 swh.dataset-1.6.0 swh.graph-5.1.0 swh.journal-1.5.2 swh.model-6.14.0 swh.objstorage-3.3.0 swh.perfecthash-1.3.2 swh.storage-2.7.0 tenacity-9.0.0 tqdm-4.66.5 types-protobuf-5.27.0.20240626 types-requests-2.31.0.6 types-urllib3-1.26.25.14 typing-extensions-4.12.2 urllib3-1.26.19 wrapt-1.16.0 yarl-1.9.4 zipp-3.20.0
   (swhgraph_venv_5.1.0) swhworker@granet:~$ pip freeze | grep graph
   swh.graph==5.1.0

   root@granet# apt install build-essential libclang-dev python3 python3-venv default-jre zstd protobuf-compiler
   swhworker@granet:~$ curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   info: downloading installer

   Welcome to Rust!

   This will download and install the official compiler for the Rust
   programming language, and its package manager, Cargo.

   Rustup metadata and toolchains will be installed into the Rustup
   home directory, located at:

     /home/swhworker/.rustup

   This can be modified with the RUSTUP_HOME environment variable.

   The Cargo home directory is located at:

     /home/swhworker/.cargo

   This can be modified with the CARGO_HOME environment variable.

   The cargo, rustc, rustup and other commands will be added to
   Cargo's bin directory, located at:

     /home/swhworker/.cargo/bin

   This path will then be added to your PATH environment variable by
   modifying the profile files located at:

     /home/swhworker/.profile
     /home/swhworker/.zshenv
     /home/swhworker/.config/fish/conf.d/rustup.fish

   You can uninstall at any time with rustup self uninstall and
   these changes will be reverted.

   Current installation options:


      default host triple: x86_64-unknown-linux-gnu
        default toolchain: stable (default)
                  profile: default
     modify PATH variable: yes

   1) Proceed with standard installation (default - just press enter)
   2) Customize installation
   3) Cancel installation
   >2

   I'm going to ask you the value of each of these installation options.
   You may simply press the Enter key to leave unchanged.

   Default host triple? [x86_64-unknown-linux-gnu]


   Default toolchain? (stable/beta/nightly/none) [stable]


   Profile (which tools and data to install)? (minimal/default/complete) [default]
   minimal

   Modify PATH variable? (Y/n)
   Y


   Current installation options:


      default host triple: x86_64-unknown-linux-gnu
        default toolchain: stable
                  profile: minimal
     modify PATH variable: yes

   1) Proceed with selected options (default - just press enter)
   2) Customize installation
   3) Cancel installation
   >

   info: profile set to 'minimal'
   info: setting default host triple to x86_64-unknown-linux-gnu
   info: syncing channel updates for 'stable-x86_64-unknown-linux-gnu'
   info: latest update on 2024-08-08, rust version 1.80.1 (3f5fd8dd4 2024-08-06)
   info: downloading component 'cargo'
   info: downloading component 'rust-std'
   info: downloading component 'rustc'
   info: installing component 'cargo'
   info: installing component 'rust-std'
    26.7 MiB /  26.7 MiB (100 %)  12.5 MiB/s in  2s ETA:  0s
   info: installing component 'rustc'
    65.0 MiB /  65.0 MiB (100 %)  13.4 MiB/s in  4s ETA:  0s
   info: default toolchain set to 'stable-x86_64-unknown-linux-gnu'

     stable-x86_64-unknown-linux-gnu installed - rustc 1.80.1 (3f5fd8dd4 2024-08-06)


   Rust is installed now. Great!

   To get started you may need to restart your current shell.
   This would reload your PATH environment variable to include
   Cargo's bin directory ($HOME/.cargo/bin).

   To configure your current shell, you need to source
   the corresponding env file under $HOME/.cargo.

   This is usually done by running one of the following (note the leading DOT):
   . "$HOME/.cargo/env"            # For sh/bash/zsh/ash/dash/pdksh
   source "$HOME/.cargo/env.fish"  # For fish

   swhworker@granet:~$ cargo version
   cargo 1.80.1 (376290515 2024-07-16)

   swhworker@granet:~$ RUSTFLAGS="-C target-cpu=native" \
     cargo install --git https://gitlab.softwareheritage.org/swh/devel/swh-graph.git \
       --features grpc-server \
       swh-graph
       Updating git repository `https://gitlab.softwareheritage.org/swh/devel/swh-graph.git`
     Installing swh-graph v5.1.0 (https://gitlab.softwareheritage.org/swh/devel/swh-graph.git#8840f5a2)
       Updating crates.io index
        Locking 350 packages to latest compatible versions
         Adding addr2line v0.22.0 (latest: v0.24.1)
         Adding anes v0.1.6 (latest: v0.2.0)
         Adding aquamarine v0.1.12 (latest: v0.5.0)

   ...
      Compiling tonic-middleware v0.1.4
      Compiling tonic-reflection v0.11.0
       Finished `release` profile [optimized + debuginfo] target(s) in 3m 08s
     Installing /home/swhworker/.cargo/bin/swh-graph-grpc-serve
     Installing /home/swhworker/.cargo/bin/swh-graph-hash
     Installing /home/swhworker/.cargo/bin/swh-graph-index
     Installing /home/swhworker/.cargo/bin/swh-graph-node2type
      Installed package `swh-graph v5.1.0 (https://gitlab.softwareheritage.org/swh/devel/swh-graph.git#8840f5a2)` (executables `swh-graph-grpc-serve`, `swh-graph-hash`, `swh-graph-index`, `swh-graph-node2type`)

   swhworker@granet:~$ ls -lah .cargo/bin/swh-graph*
   -rwxr-xr-x 1 swhworker swhworker 62M Aug 14 16:28 .cargo/bin/swh-graph-grpc-serve
   -rwxr-xr-x 1 swhworker swhworker 14M Aug 14 16:27 .cargo/bin/swh-graph-hash
   -rwxr-xr-x 1 swhworker swhworker 29M Aug 14 16:27 .cargo/bin/swh-graph-index
   -rwxr-xr-x 1 swhworker swhworker 28M Aug 14 16:27 .cargo/bin/swh-graph-node2type

   root@granet:~# ln -nsf /opt/swhgraph_venv_5.1.0/ /opt/swhgraph_venv
   root@granet:~# systemctl restart swh-graph-grpc.service
   root@granet:~# systemctl status swh-graph-grpc.service
   ● swh-graph-grpc.service - swh-graph gRPC server
        Loaded: loaded (/etc/systemd/system/swh-graph-grpc.service; enabled; preset: enabled)
        Active: active (running) since Tue 2024-08-27 09:29:13 UTC; 3h 36min ago
      Main PID: 486308 (swh-graph-grpc-)
         Tasks: 49 (limit: 629145)
        Memory: 9.9G
           CPU: 8.294s
        CGroup: /system.slice/swh-graph-grpc.service
                └─486308 /home/swhworker/.cargo/bin/swh-graph-grpc-serve -vv --bind "[::]:50091" /dev/shm/swh-graph/default/graph

   Aug 27 09:29:13 granet systemd[1]: Started swh-graph-grpc.service - swh-graph gRPC server.
   Aug 27 09:29:14 granet swh[486308]: INFO:swh.graph.config:using swh-graph JAR: /opt/swhgraph_venv_5.1.0/lib/python3.11/site-packages/swh/graph/swh-graph.jar
   Aug 27 09:29:14 granet swh[486308]: INFO:swh.graph.cli:Starting gRPC server: /home/swhworker/.cargo/bin/swh-graph-grpc-serve -vv --bind '[::]:50091' /dev/shm/swh-graph/default/graph
   Aug 27 09:29:14 granet swh[486308]: 2024-08-27T09:29:14+00:00 - INFO - Loading graph
   Aug 27 09:29:21 granet swh[486308]: 2024-08-27T09:29:21+00:00 - INFO - Starting server
