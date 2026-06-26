Static Website Deployment
=========================

.. admonition:: Intended audience
   :class: important

   sysadm staff members

Context
-------

This page describes how the static website ``https://dataportal.softwareheritage.org/`` is deployed on the Software Heritage Kubernetes infrastructure.

Migrating the website to Kubernetes aligns its deployment and operational model with the rest of the platform services.

The merge request associated with this migration is available at:

- https://gitlab.softwareheritage.org/swh/infra/ci-cd/swh-charts/-/merge_requests/756

1. Docker Image Build
---------------------

The Docker image is built by the CI pipeline located in the
``swh-apps/apps/swh-static-websites`` repository using a multi-stage Dockerfile.

The build process consists of two stages:

**Build stage**

- Clone the repository containing the static website sources.
- Install the dependencies required to generate the website.
- Build the static website assets.

**Runtime stage**

- Use an Nginx image to serve the generated static content.
- Copy the generated artifacts from the build stage into the final Docker image.

2. Kubernetes Deployment with Helm
----------------------------------

The Helm templates responsible for deploying the static website are located in:

::

    swh-charts/swh/templates/static-websites

The deployment configuration includes:

- The application definition and Kubernetes resources in ``deployment.yaml``.
- A ``RollingUpdate`` deployment strategy to ensure zero-downtime updates.
- Node affinity rules to schedule the workload on the appropriate Kubernetes nodes.
- The Docker image produced and published by the CI pipeline.

3. Kubernetes Service Configuration
-----------------------------------

The Helm ``Service`` resource is defined in ``service.yaml`` and is responsible for:

- Exposing the Nginx container within the Kubernetes cluster.
- Allowing communication between the Deployment and the Ingress resource.

4. Ingress Configuration
------------------------

The Helm ``Ingress`` resource is defined in ``ingress.yaml`` and is responsible for:

- Exposing the service outside the Kubernetes cluster.
- Routing incoming traffic for the ``dataportal.internal.staging.swh.network`` domain.

5. DNS Configuration
--------------------

The final step consists of configuring the DNS records so that the public domain points to the deployed application.

These DNS records are managed in the ``swh-site/data`` repository.

Example:

.. code-block:: yaml

    dataportal-staging/CNAME:
      type: CNAME
      record: dataportal.internal.staging.swh.network
      data: k8s-archive-staging-rke2.internal.staging.swh.network.

Result
------

The static website is now packaged as a Docker image, automatically built by CI, and can be deployed to the staging Kubernetes cluster.

Once deployed, it is available at :

::

    dataportal.internal.staging.swh.network