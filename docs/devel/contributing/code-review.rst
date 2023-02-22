.. _code-review:

Code review
===========

This page documents code review practices used for Software Heritage development.

`GitLab has many useful features
<https://docs.gitlab.com/ee/user/project/merge_requests/reviews/>`_ to ease
reviewing the changes, communicating around questions or comments, and making
suggestions. Learning how to use them will help you and the team.

Guidelines
----------

Please adhere to the following guidelines in the context of Software Heritage
development.

When submitting changes:

- **Reviews are strongly recommended** for any non-trivial code change,
  but not mandatory (nor enforced at Git level).
- The :ref:`code submission workflow <patch-submission>` is implemented using
  merge requests sent to our GitLab instance.
- The `assignee
  <https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#assignee>`_
  in the context of merge request is the person supposed to drive it to
  completion. **In almost all cases, you should assign yourself to merge requests you
  create.**
- If your changes are meant to address a specific issue, you should `prefix the
  branch name with the issue number
  <https://docs.gitlab.com/ee/user/project/repository/branches/index.html#naming>`_.
- Feel free to explicitly **mention one or more specific
  reviewer** from people most knowledgeable with the target code. You can also
  assign a single person [#multiple-reviewers]_ as reviewer using the relevant
  field. It will prevent the merge request from going unnoticed.
- **One approval is enough** before merging a request.

As a team member:

- **Review any merge requests you want**: no matter the suggested reviewers,
  feel free to review any pending merge requests.
- **Review every day**: reviews should be timely as fellow developers
  will wait for them. To make the process sustainable each developer should
  strive to dedicate a fixed minimum amount of review time every workday.

.. [#multiple-reviewers] Assigning multiple reviewers are only supported in
   paid editions of GitLab. As we currently use the free *Community Edition*,
   mentions are the only way to get the attention of multiple people at once.

Learning about pending reviews
------------------------------

As we aim to review merge requests in a timely manner, here are several ways to
know about merge requests waiting for input.

Notifications
^^^^^^^^^^^^^

To be sure to receive notifications of new merge requests:

1. Open the `notification controls
   <https://gitlab.softwareheritage.org/-/profile/notifications>`_ for your
   GitLab account.
2. Locate the *Platform* group.
3. Select *Custom* in the list of notification levels.
4. Click on the bell icon.
5. Make sure *New merge request* is ticked. You probably also want to select at
   least *New issue*, *Failed pipeline*, and *Fixed pipeline*.
6. Click *Ok*.
7. Repeat the operation for other groups of interest.

List pending merge requests
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sadly, notifications can easily be missed and GitLab by itself does not provide
a view with all merge requests waiting for action across multiple projects. To
have a better view of pending merge requests, you should consider using:

- `GitLab Notify Extension
  <https://github.com/Mikescops/gitlab-notify-extension>`_ available for Chrome
  and Firefox. It can list all merge requests you are assigned to and all merge
  requests you created.

- `gitlab-revq <https://gitlab.softwareheritage.org/vlorentz/gitlab-revq/>`_, a
  command-line tool listing all actionable pending requests.

Recommended readings
--------------------

* `Best practices (Palantir) <https://medium.com/palantir/code-review-best-practices-19e02780015f>`_ ← comprehensive and recommended read, especially if you're short on time
* `Best practices (Thoughtbot) <https://github.com/thoughtbot/guides/tree/master/code-review>`_
* `Best practices (Smart Bear) <https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/>`_
* `Review checklist <https://www.codeproject.com/Articles/524235/Codeplusreviewplusguidelines>`_ (Code Project)
* `Motivation: code quality <https://blog.codinghorror.com/code-reviews-just-do-it/>`_ (Coding Horror)
* `Motivation: team culture <https://blog.fullstory.com/what-we-learned-from-google-code-reviews-arent-just-for-catching-bugs/>`_ (Google & FullStory)
* `Motivation: humanizing peer reviews <http://www.processimpact.com/articles/humanizing_reviews.pdf>`_ (Wiegers)
* `Motivation: sharing knowledge <https://www.atlassian.com/agile/software-development/code-reviews>`_ (Atlassian)

See also
--------

* :ref:`patch-submission`
* :ref:`python-style-guide`
* :ref:`git-style-guide`
