.. admin-operations-kafka-cluster:

Administrative operations on the Kafka cluster
===================================================

.. admonition:: Intended audience
   :class: important

   sysadm staff members

Purpose
--------

This page lists common operations performed by sysdamins on the Kafka cluster.

Cycle a user's password
-----------------------

On a kafka node or on ``getty.internal.softwareheritage.org``, execute

.. code::
    /opt/kafka/bin/kafka-configs.sh \
        --bootstrap-server "kafka1.internal.softwareheritage.org:9092" \
        --alter \
        --add-config "SCRAM-SHA-256=[iterations=8192,password=$new_password],SCRAM-SHA-512=[password=$new_password]" \
        --entity-type users \
        --entity-name "$new_password"
