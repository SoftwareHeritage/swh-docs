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

1. First, we close the 'swh-next-version' merge request if it's opened. That's
what triggers the creation of the next-version application. The various
depending services will be stopped. If not, the services will crash without
their stopped backends (and lots of alerts will be raised).

Now, on with the actual reset.

2. Edit cluster-components/values/archive-staging-rke2.yaml and set `enabled:
false` to rabbitmq, kafka, cassandra, elasticsearch, cloudnativePg, redis
configuration entries. Commit and push.

3. In the `argocd application 'archive-staging-rke2-cluster-components'
<https://argocd.internal.admin.swh.network/applications/archive-staging-rke2-cluster-components>`_
, hit the 'Refresh' button and then the 'Sync' button. Check the "prune"
checkbox so it can effectively remove the various deactivated backends. When
removing those, this will also remove their pv/pvc configured (they have a
retention policy 'Delete').

4. Wait for the backends deactivation to be effective (you can check for the
pods to be stopped and their associated pvc to be cleaned up).

5. Revert the commit from step 2. and push. The goal being to start back the
stopped backends (now that they are empty).

6. Go back in argocd and sync (or wait for the sync to happen). That will
start back the backends.

7. The backends will be started from scratch. Note that some postgresql backends can
depend on dump (e.g. scheduler).

8. Wait for the backends to be running.

9. Reopen swh-next-version branch and wait for the services to be up
again. When starting, the various services will initialize their empty
backends appropriately (e.g. rpc, ...) so they can actually run properly.

