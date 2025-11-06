.. _howto-reset-next-version-environment:

How to reset the next version environment
=========================================

.. admonition:: Intended audience
   :class: important

   sysadm members who wants to reset said environment

As mentioned, the next-version environment is a sandboxed & scratchable
environment dedicated to run the swh stack with the next version of swh
modules.

It's currently configured to be a stateful environment. But we may need to
reset it once in a while to avoid consuming too much resources.

We will need a local-checkout of the `swh-charts repository
<https://gitlab.softwareheritage.org/swh/infra/ci-cd/swh-charts/>`_.

1. First, we close the 'swh-next-version' `merge request
<https://gitlab.softwareheritage.org/swh/infra/ci-cd/swh-charts/-/merge_requests>` if
any. That's what triggers the creation of the next-version applications. The various
depending services will be stopped (to avoid those to crash without their stopped
backends and raise alerts).

Now, on with the actual reset.

2. Edit `cluster-components/values/archive-staging-rke2.yaml
<https://gitlab.softwareheritage.org/swh/infra/ci-cd/swh-charts/-/blob/staging/cluster-components/values/archive-staging-rke2.yaml?ref_type=heads>`
and set `enabled: false` to the various specific next-version backend instance
configuration entries: rabbitmq, kafka, cassandra, elasticsearch, cloudnativePg, redis,
... Commit and push the changes.

.. code-block:: diff

    $ diff --git c/cluster-components/values/archive-staging-rke2.yaml w/cluster-components/values/archive-staging-rke2.yaml
    index bd0b5ea0..5deaa8ca 100644
    --- c/cluster-components/values/archive-staging-rke2.yaml
    +++ w/cluster-components/values/archive-staging-rke2.yaml
    @@ -61,7 +61,7 @@ svix:
             enabled: false
             dsn: db-swh-svix-rw.cnpg
         svix-next-version:
    -      enabled: true
    +      enabled: false
           ingress:
             host: svix-next-version.internal.staging.swh.network
             createTLS: true
    @@ -263,7 +263,7 @@ cloudnativePg:
         ##################

         next-version-db-swh:
    -      enabled: true
    +      enabled: false
           namespace: cnpg-next-version
           testing: true
           instances: 1
    @@ -278,7 +278,7 @@ cloudnativePg:
             enabled: true

         next-version-db-swh-deposit:
    -      enabled: true
    +      enabled: false
           namespace: cnpg-next-version
           testing: true
           instances: 1
    @@ -293,7 +293,7 @@ cloudnativePg:
             enabled: true

         next-version-db-swh-indexer:
    -      enabled: true
    +      enabled: false
           namespace: cnpg-next-version
           testing: true
           instances: 1
    @@ -308,7 +308,7 @@ cloudnativePg:
             enabled: true

         next-version-db-swh-masking:
    -      enabled: true
    +      enabled: false
           namespace: cnpg-next-version
           testing: true
           externalClustersRef: externalPostgresqlClusters
    @@ -327,7 +327,7 @@ cloudnativePg:
         # Specific swh-scheduler database mounted from a backup from swh-scheduler-k8s
         # (minimalistic swh-scheduler db)
         next-version-db-swh-scheduler:
    -      enabled: true
    +      enabled: false
           namespace: cnpg-next-version
           testing: true
           instances: 1
    @@ -345,7 +345,7 @@ cloudnativePg:
             source: next-version-db-swh-scheduler

         next-version-db-swh-svix:
    -      enabled: true
    +      enabled: false
           namespace: cnpg-next-version
           testing: true
           instances: 1
    @@ -360,7 +360,7 @@ cloudnativePg:
             enabled: true

         next-version-db-swh-vault:
    -      enabled: true
    +      enabled: false
           namespace: cnpg-next-version
           testing: true
           instances: 1
    @@ -375,7 +375,7 @@ cloudnativePg:
             enabled: true

         next-version-db-swh-web:
    -      enabled: true
    +      enabled: false
           namespace: cnpg-next-version
           testing: true
           instances: 1
    @@ -718,7 +718,7 @@ cloudnativePg:
             schedule: "0 15 0 * * *"

     rabbitmq:
    -  enabled: true
    +  enabled: false
       namespace: swh-cassandra-next-version
       replicas: 1
       deployments:
    @@ -727,7 +727,7 @@ rabbitmq:
           namespace: swh-cassandra-next-version

     cassandra:
    -  enabled: true
    +  enabled: false
       storageConfig:
         cassandraDataVolumeClaimSpec:
           storageClassName: local-persistent
    @@ -752,7 +752,7 @@ cassandra:
             enabled: false

     kafka:
    -  enabled: true
    +  enabled: false
       namespace: swh-cassandra-next-version
       replicas: 1
       replicationFactor: 1
    @@ -850,7 +850,7 @@ elasticsearch:
           storageClassName: local-persistent
       deployments:
         search-next-version:
    -      enabled: true
    +      enabled: false
           namespace: swh-cassandra-next-version
           metricsEnabled: true
           replicas: 3
    @@ -875,7 +875,7 @@ redis:
       enabled: true
       deployments:
         counters:
    -      enabled: true
    +      enabled: false
           namespace: swh-cassandra-next-version
           storage:
             volumeClaimTemplate:
    @@ -919,7 +919,7 @@ redis:
               appendonly yes
               appendfsync everysec
         svix-next-version:
    -      enabled: true
    +      enabled: false
           namespace: swh-cassandra-next-version
           priorityClassName: swh-storages
           serviceMonitor:

3. In the `argocd application 'archive-staging-rke2-cluster-components'
<https://argocd.internal.admin.swh.network/applications/archive-staging-rke2-cluster-components>`_
, hit the 'Refresh' button and then the 'Sync' button. Check the "prune" checkbox so it
can effectively remove the various deactivated instance backends. When removing those,
this will also remove their persistent volume (pv) configured (with a retention policy
'Delete', the few ones with 'Retain' will stay).

4. Wait for the backends deactivation to be effective (you can check for the pods to be
stopped and their associated pvc to be cleaned up).

5. Revert the commit from step 2. and push. The goal being to start back the stopped
backends (now that they are empty).

6. Go back in argocd and sync (or wait for the sync to happen). That will start back the
backends.

7. The backends will be started from scratch. Note that some postgresql backends can
depend on dump (e.g. scheduler).

8. Wait for the backends to be running.

9. Reopen swh-next-version branch and wait for the services to be up again. When
starting, the various services will initialize their empty backends appropriately (e.g.
rpc, ...) so they can actually run properly.

10. (optional) Since some pvs have a retention 'Retain' policy, they will remain after
the environment reset. If you want to clean them up, you can use 'k9s' in the 'pv' view
(hit ':' then enter 'pv'), filtering on 'Released' pvs (hit '/' then enter 'Released')
to remove the 'swh-cassandra-next-version/' claimed pvs.
