Development principles and contribution guidelines
==================================================

In order to create a high-quality software product, the BiscuIT developers
have agreed upon fundamental principles governing the code layout, coding
style and repository management for BiscuIT and all official apps.


Coding layout and style
-----------------------

The coding style is defined in `PEP 8`_, with the following differences and
decisions:

- The maximum line length is 100 characters
- Imports are structured in five blocks, each of them sorted as defined in
  PEP 8:

  1. Standard library imports
  2. Django imports
  3. Third-party imports
  4. Imports from other BiscuIT apps (absolute imports)
  5. Imports from the same BiscuIT app (realtive imports)

- All string literals use single quotes

For the layout of source trees and style recommendations specific to Django,
the `Django coding style`_ is a good source of information, together with
the `Django Best Practices`_ collection.


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


Text documents
--------------

If there is no objective reason against it, all text documents accompanying
the source use `reStructuredText`_.


.. _PEP 8: https://pep8.org/
.. _Django coding style: https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/
.. _Django Best Practices: https://django-best-practices.readthedocs.io/en/latest/index.html
.. _How to Write a Git Commit Message: https://chris.beams.io/posts/git-commit/
.. _Sane software manifesto: https://sane-software.globalcode.info/
.. _Accessibility Manifesto: http://accessibilitymanifesto.com/
.. _User Data Manifesto: https://userdatamanifesto.org/
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
