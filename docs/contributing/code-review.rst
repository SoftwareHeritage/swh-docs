.. _code-review:

Code Review
===========

This page documents code review practices used for [[Software Heritage]] development.

Guidelines
----------

Please adhere to the following guidelines to perform and obtain code reviews
(CRs) in the context of Software Heritage development:

1. **CRs are strongly recommended** for any non-trivial code change,
   but not mandatory (nor enforced at the VCS level).
2. The CR `workflow <phabricator-arcanist>`_ is implemented using
   Phabricator/Differential.
3. Explicitly **suggest reviewer(s)** when submitting new CR requests:
   either the most knowledgeable person(s) for the target code or the general
   `reviewers <https://forge.softwareheritage.org/project/view/50/>`_
   (which is the `default <https://forge.softwareheritage.org/H18>`_).
4. **Review anything you want**: no matter the suggested reviewer(s),
   feel free to review any outstanding CR.
5. **One LGTM is enough**: feel free to approve any outstanding CR.
6. **Review every day**: CRs should be timely as fellow developers
   will wait for them.
   To make CRs sustainable each developer should strive to dedicate
   a fixed minimum amount of CR time every (work) day.

For more detailed suggestions (and much more) on the motivational
and practical aspects of code reviews see Good reads below.

Good reads
----------

Good reads on various angles of code review:

* `Best practices <https://medium.com/palantir/code-review-best-practices-19e02780015f>`_ (Palantir) ← comprehensive and recommended read, especially if you're short on time
* `Best practices <https://github.com/thoughtbot/guides/tree/master/code-review>`_ (Thoughtbot)
* `Best practices <https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/>`_ (Smart Bear)
* `Review checklist <https://www.codeproject.com/Articles/524235/Codeplusreviewplusguidelines>`_ (Code Project)
* `Motivation: code quality <https://blog.codinghorror.com/code-reviews-just-do-it/>`_ (Coding Horror)
* `Motivation: team culture <https://blog.fullstory.com/what-we-learned-from-google-code-reviews-arent-just-for-catching-bugs/>`_ (Google & FullStory)
* `Motivation: humanizing peer reviews <http://www.processimpact.com/articles/humanizing_reviews.pdf>`_ (Wiegers)
* `Motivation: sharing knowledge <https://www.atlassian.com/agile/software-development/code-reviews>`_ (Atlassian)

See also
--------

* :ref:`phabricator-arcanist`
* :ref:`coding-guidelines`
