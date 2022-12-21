.. _swh_scn_webhooks:

==========================
Software Heritage Webhooks
==========================

Webhooks are user-defined HTTP callbacks triggered by software forges for some events, like pushing new commits to a repository.
Software Heritage offers some dedicated API endpoints to receive webhooks for push events. When triggered, it requests to add or update a repository in the archive whenever new commits are pushed. It ensures that your repository is up to date in the archive without needing to request for update manually.

Software Heritage has webhook receivers for some of the most popular forges. Currently, this includes:
 - GitHub
 - GitLab
 - BitBucket
 - Gitea
 - SourceForge

Each forge has its own way of setting up webhooks, and the steps for each are mentioned below:

GitHub
------
This is a tutorial for setting up a webhook in GitHub.

The API endpoint is https://archive.softwareheritage.org/api/1/origin/save/webhook/github/

The API documentation for this endpoint can be found at https://archive.softwareheritage.org/api/1/origin/save/webhook/github/doc/

Steps to setup the Webhook:

1. Go to the repository you want to archive.
2. Click on the **Settings** tab of the repository.
3. Go to the Webhooks under the "Code and automation" section on the left.
4. Enter the API endpoint in the payload URL field and select the **Content type** as **application/json**.
5. Select **Just the push event** under "Which events would you like to trigger this webhook?".
6. Click on **Add Webhook**.

GitLab
------
This is a tutorial for setting up Webhook in GitLab.

The API endpoint is https://archive.softwareheritage.org/api/1/origin/save/webhook/gitlab/

The API documentation for this endpoint can be found at https://archive.softwareheritage.org/api/1/origin/save/webhook/gitlab/doc/

Steps to setup the Webhook:

1. Go to the project you want to archive.
2. Under the **Settings** menu on the left side, click on **Webhooks**.
3. Enter the API endpoint in the **URL** field.
4. Check the **Push Events** box under **Trigger**.
5. Click on **Add Webhook**.

BitBucket
---------
This is a tutorial for setting up Webhook in BitBucket.

The API endpoint is https://archive.softwareheritage.org/api/1/origin/save/webhook/bitbucket/

The API documentation for this endpoint can be found at https://archive.softwareheritage.org/api/1/origin/save/webhook/bitbucket/doc/

Steps to setup the Webhook:

1. Go to the repository you want to archive.
2. Click on the **Repository settings** on the left sidebar.
3. Under the **Workflow** menu in the sidebar, click on **Webhooks**.
4. Click on the **Add Webhook** button in the Webhook menu.
5. Give a title to the webhook and enter the API endpoint in the URL field.
6. Ensure that the **Status** is active and **Push** option is checked.
7. Click on **Save**.

Gitea
-----
This is a tutorial for setting up Webhook in Gitea.

The API endpoint is https://archive.softwareheritage.org/api/1/origin/save/webhook/gitea/

The API documentation for this endpoint can be found at https://archive.softwareheritage.org/api/1/origin/save/webhook/gitea/doc/

Steps to setup the Webhook:

1. Go to the repository you want to archive.
2. Click on the **Settings** button on the bar.
3. Click on **Webhooks** in the bar below.
4. Click on **Add Webhook** and select **Gitea**.
5. Enter the API endpoint in the **Target URL** field.
6. Ensure that the HTTP method is **POST**, POST Content type is **application/json** and Trigger On is set to **Push Events**.
7. Ensure that the **Active** checkbox is selected.
8. Click on **Add Webhook**.

SourceForge
-----------
This is a tutorial for setting up Webhook in SourceForge.

The API endpoint is https://archive.softwareheritage.org/api/1/origin/save/webhook/sourceforge/

The API documentation for this endpoint can be found at https://archive.softwareheritage.org/api/1/origin/save/webhook/sourceforge/doc/

Steps to setup the Webhook:

1. Go to the repository you want to archive.
2. Under the **Admin** dropdown on the left side, click on **Webhooks**.
3. Click on **create**.
4. In the URL field, enter the above API endpoint and click on **Create**.