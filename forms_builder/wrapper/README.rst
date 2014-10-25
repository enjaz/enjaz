.. _django-forms-builder: https://github.com/stephenmcd/django-forms-builder

django-pluggable-forms
======================

A Django app that builds on django-forms-builder_
by Stephen McDonald. Django-pluggable-forms adds several important features to the ones already present
in django-forms-builder while preserving all features of the original app. Namely:

1. "Pluggability" - Ability to link forms to any ``ContentType`` so that each ``ContentType``'s forms are linked
   at the database level and also have a distinct URL.

2. Non-admin interface for editing of forms - the same admin functionality can be done through a non-admin
   interface while still controlling who can access and edit forms. The editor interfaces are specific for
   each ``ContentType``.

3. Automatically obtaining submitter data from ``AUTH_USER_MODEL`` when a form requires login, with the ability to
   customize what information to obtain about submitters

Other features:

1. Option to use slugs vs. IDs in form urls .

Instructions
============
Installation
^^^^^^^^^^^^
1. Install the package contents by cloning this repository.
2. Add django-pluggable-forms to your project by adding ::

    ...
    'forms_builder.forms',
    'forms_builder.wrapper',
    ...

   to ``INSTALLED_APPS`` in your ``settings.py``.

Configuration and Usage
^^^^^^^^^^^^^^^^^^^^^^^
Linking forms to an existing model is an easy process that takes the following steps:

1. URLconf
   a. Specify ``namespace`` and ``app_name``
   b. ContentType
   c. Templates
   d. Perm checks
      i. For form_list (what it does)
      ii. For other views
   e. Submitter fields

2. GenericRelation
3. FORMS_BUILDER_USE_SLUGS setting
4. FORMS_BUILDER_CHOICES_SEPARATOR setting
   NOTE - Don't change once specified

On making django-pluggable-forms
================================

Django-pluggable-forms adds the extra functionality to django-forms-builder in a minimally invasive approach.
Except for a few edits noted below, all added and modified views, urls, forms, templates, tests, etc are housed
in a ``wrapper`` app that co-exists with the main ``forms`` app of django-forms-builder.

A few exceptions are listed here, where it isn't possible except to modify the original code of ```forms``:

* In ``forms/model.py``:

  * Adding ``GenericForeignKey`` fields to the ``Form`` model

  * Modifying ``get_absolute_url`` in ``AbstractForm`` model

  * Adding ``get_url_attr`` to ``AbstractForm`` model

  * Adding ``submitter`` field that links to ``AUTH_USER_MODEL`` and a modified ``save``
    method that ensures it's not empty if the linked ``Form`` requires login

* In ``forms/forms.py``:

  * Many edits in ``EntriesForm`` in order to enable showing user data in forms that require login. Namely:

    1. ``__init__``: Add lines ``266-268`` and ``319-329``

    2. ``__iter__``: Edit line ``335``

    3. ``columns``: Add lines ``359-363``

    4. ``rows``: Add lines ``388-392`` and ``425-457``

  * Also in ``EntriesForm``: edit line ``491`` to make URL pluggable

* In ``forms/templates/forms/includes/built_form.html``:

  * Removing ``action="{{ form.get_absolute_url }}"`` from the ``<form>`` tag

Known issues
============
1. Django-pluggable-forms is designed to allow multiple instances of the app to exist at the same time. So the URLconf
   takes this fact into account and requires specification of a ``namespace`` for each different instance. To make use of
   the namespaces and return the correct URL that belongs to the current instance, ``reverse`` and ``{% url %}`` require
   the ``current_app`` to be specified (as an argument in case of ``reverse`` or as a context attribute in case of ``{% url %}``),
   the value of which is obtained from ``request.resolver_match.namespace``. The issue is that some ``reverse`` statements in the
   original ``forms`` code are located a bit deep below the ``view`` level, where ``request`` cannot be easily obtained.
   (Namely in ``models.py``) Due to this:

   a. The ``AbstractForm.get_absolute_url`` method, which uses ``models.permalink`` decorator is ignored in all views and templates
      of django-pluggable-forms and replaced by a normal ``{% url %}`` tag

   b. The ``View on site`` link in the admin, which is based on ``get_absolute_url``,
      doesn't work with model-linked forms

2. Django-pluggable-forms allows forms to optionally be linked to any model instance, while still keeping the option
   of non-model-linked forms. The way the ``URLconf`` is designed specifies an optional argument (``object_id``) to identify
   the linked model instance (For example, ``example.com/app1/[object_id]/forms/``). The views are compatible with the fact
   that this parameter is optional (they default ``object_id`` to ``None`` if it's not passed). However, URL reversing via
   ``reverse`` and ``{% url %}`` doesn't take "optional" arguments, raising ``NoReverseMatch`` if these arguments
   aren't passed. Model-linked forms aren't affected by this; but installing instances of the app that use non-model-linked
   forms isn't recommended so far due to this issue.