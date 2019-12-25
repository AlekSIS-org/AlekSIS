Development principles and contribution guidelines
==================================================

In order to create a high-quality software product, the BiscuIT developers
have agreed upon fundamental principles governing the code layout, coding
style and repository management for BiscuIT and all official apps.


Coding layout and style
-----------------------

The coding style is defined in `PEP 8`_, with the following differences and
decisions:

- The defaults of the `black`_ code formatter are used
  - This implies all string literals usin double-quotes, if it does not lead
    to more escaping. As proposed by `black`: "My recommendation here is to
    keep using whatever is faster to type and let Black handle the transformation."
- The maximum line length is 100 characters
- Imports are structured in five blocks, each of them sorted as defined in
  PEP 8 and the Django style guide:

  1. Standard library imports
  2. Django imports
  3. Third-party imports
  4. Imports from BiscuIT core and other apps (absolute imports)
  5. Imports from the same BiscuIT app (realtive imports)

  Use `isort` to take care of this

For the layout of source trees and style recommendations specific to Django,
the `Django coding style`_ is a good source of information, together with
the `Django Best Practices`_ collection.

To ensure code is styled correctly, before commiting, run::

  tox -e reformat


Working with the Git repository
-------------------------------

The Git repository shall be used as a historic documentation of development
and as change management. It is important that the Git commit history
describes waht was changed, by whom and why.

Feature branches
~~~~~~~~~~~~~~~~

All features and bug fixes should be developed in their own branch and later
merged into the master branch as a whole. Of course, sometimes, it is
sensible to not do that, e.g. for fixing mere typos and the like

WIthin the feature branch, every logical step should be commited separately.
It is neither required nor desired to do micro-commits about every
development step. The commit history should describe the trains of thought
the design and implementation is based on.

Commit messages
~~~~~~~~~~~~~~~

Commit messages should be written as described in `How to Write a Git Commit
Message`_.

Commit messages should mention or even close any related issues. For merely
mentioning progress on an issue, use the keyword `advances`; for closing an
issue, use `closes`; for referring to a related issue for informational
purposes, use `cf.`. This should be done in the body of the commit message.

The subject of a commit message can (and should) be prepended with a tag in
square brackets if it relates to a certain part of the repository, e.g. [CI]
when changing CI/CD configuration or support code, [Dev] when changing
something in the development utilities, etc.

Manifestos governing development
--------------------------------

The FOSS community has created some manifestos describing several aspects of
software development, to agree upon a baseline for these aspects. The
BiscuIT developers have agreed to adhere to the following manifestos:

- The `Sane software manifesto`_
- The `Accessibility Manifesto`_
- The `User Data Manifesto`_

Not all theses from these manifestos are applicable. For example, most data
about persons in a school information system are dictated by the school and
probably governed by laws defining what and when to store. In that case,
giving the user control over these decisions is not possible. Developers
need to decide what should resonably be followed.


The case on supporting non-free services
----------------------------------------

Defined by the `Free Software Definition`_, it is an essential freedom to
be allowed to use free software for any purpose, without limitation. Thus,
interoperability with non-free services shall not be ruled out, and the
BiscuIT project explicitly welcomes implementing support for
interoperability with non-free services.

However, to purposefullt foster free software and services, if
interoperability for a certain kind of non-free service is implemented, this
must be done in a generalised manner (i.e.  using open protocols and
interfaces).  For example, if implementing interoperability with some
cloud-hosted calendar provider can be implemented either through a
proprietary API, or through a standard iCalendar/Webcal interfaces, the
latter is to be preferred.  Lacking such support, if a proprietary service
is connected through a proprietary, single-purpose interface, measures shall
be taken to also support alternative free services.


Text documents
--------------

If there is no objective reason against it, all text documents accompanying
the source use `reStructuredText`_.


Contributing to upstream
------------------------

If possible and reasonable, code that can be of use to others in the general
Django ecosystem shall be contributed to any upstream dependency, or a new
generalised upstream dependency be created, under the most permissive
licence possible.


.. _PEP 8: https://pep8.org/
.. _Django coding style: https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/
.. _black: https://black.readthedocs.io/en/stable/
.. _Django Best Practices: https://django-best-practices.readthedocs.io/en/latest/index.html
.. _How to Write a Git Commit Message: https://chris.beams.io/posts/git-commit/
.. _Sane software manifesto: https://sane-software.globalcode.info/
.. _Accessibility Manifesto: http://accessibilitymanifesto.com/
.. _User Data Manifesto: https://userdatamanifesto.org/
.. _Free Software Definition: https://www.gnu.org/philosophy/free-sw.en.html
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
