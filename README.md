student-portal
==============

The Student Portal is a [Django-based](https://www.djangoproject.com) platform for university student activity.
Through the platform, students can submit activities for approval,
join clubs, enter their 'Activity Points' (Niqati) and contribute and
borrow books.

# Licensing

Copyright (C) 2014 Muhammad Saeed Arabi and Osama Khalid.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Affero General Public License for more details.


Additionally, the `studentvoice` app includes parts from the Askbot
project.

Copyright (C) 2009 Chen Gang and Sailing Cai.
Copyright (C) 2009-2011 Evgeny Fadeev and individual contributors of Askbot project

The `forms_builder` app is a modified version of django-forms-builder by Stephen McDonald.

Copyright (c) Stephen McDonald and individual contributors.

Licensed under the General Public License version 3 of the License, or
(at your option) any later version.

# Installation 

Current dependencies:
* django-taggit
* django-templated-email
* django-userena
* pdfcrowd
* post_office _(with the cronjob)_
* requests
* unicodecsv

A cronjob is required to process niqati code orders as follows:
```
* * * * * cd ~/path/to/portal/ && /path/to/python manage.py generateniqati >> ~/path/to/log/generate_niqati.log 2>&1
```

In the project `urls.py`, add the following:
```
# [...]
from django.views.generic import TemplateView
from accounts.admin import deanship_admin
from arshidni.admin import arshidni_admin
from accounts.forms import StudentSignupForm, NonStudentSignupForm, ModifiedAuthenticationForm
from core.views import visit_announcement
from activities.urls import activity_forms_urls
from clubs.urls import club_forms_urls
# [...]
    url(r'^$', 'core.views.portal_home', name='home'),
    url(r'^visit/(?P<pk>\d+)/$', visit_announcement, name='visit_announcement'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^aboutsc/$', TemplateView.as_view(template_name='about_sc.html'), name='about_sc'),
    activity_forms_urls,
    url(r'^activities/', include('activities.urls', namespace="activities")),
    club_forms_urls,
    url(r'^clubs/', include('clubs.urls', namespace="clubs")),
    url(r'^books/', include('books.urls', namespace="books")),
    url(r'^niqati/', include('niqati.urls', namespace="niqati")),
    url(r'^voice/', include('studentvoice.urls', namespace="studentvoice")),
    url(r'^arshidni/admin/', include(arshidni_admin.urls, namespace="arshidni_admin")),
    url(r'^arshidni/', include('arshidni.urls', namespace="arshidni")),
    url(r'^media/', include('media.urls', namespace="media")),
    url(r'^accounts/resend/$', 'accounts.views.resend_confirmation_key', name='resend_confirmation_key'),
    url(r'^accounts/signup/$', 'userena.views.signup', {'signup_form': StudentSignupForm, 'template_name': 'userena/student_signup_form.html'}),
    url(r'^accounts/signup/nonstudents/$', 'userena.views.signup', {'signup_form': NonStudentSignupForm, 'template_name': 'userena/nonstudent_signup_form.html'}, name="nonstudent_signup"),
    url(r'^accounts/signin/$', 'userena.views.signin', {'auth_form': ModifiedAuthenticationForm}),
    url(r'^accounts/', include('userena.urls')),
    url(r'^da/', include(deanship_admin.urls)),
# [...]
```

Current required settings:
* DEFAULT_FROM_EMAIL: The default _noreply_ email.
* MEDIA_ROOT: Where do you want to save the covers on the server?
* MEDIA_URL: Where do you want users to access the covers?
* `GOOGLE_BOOKS_KEY`: to be generated from https://code.google.com/apis/console/
* `PDFCROWD_USERNAME`: a pdfcrowd username
* `PDFCROWD_KEY`: a pdfcrowd api key
* `BITLY_KEY`: a bit.ly api key
* `FVP_USERNAME = 'username'` for the female vice president.
* `MVP_USERNAME = 'username'` for the male vice president.
* `DHA_USERNAME = 'username'` for the Deanship Head of Activities
* `STUDENTVOICE_THRESHOLD = 30`, adjustable threshold for sending notifications.
* `AUTH_PROFILE_MODULE = 'accounts.EnjazProfile'`
* `USERENA_WITHOUT_USERNAMES = True`
* `USERENA_ACTIVATION_RETRY = True`
* `USERENA_ACTIVATION_DAYS = 30`
* `FORMS_BUILDER_USE_SLUGS = False`, (or `True` if you like)
* `FORMS_BUILDER_USE_SITES = False`
* `FORMS_BUILDER_CHOICES_SEPARATOR = '/'` or any character of your choice
* Add `"django.core.context_processors.request"` to the [default TEMPLATE_CONTEXT_PROCESSORS](https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATE_CONTEXT_PROCESSORS)

# First run

* The platform has many KSAU-HS-dependent conentns and they are load
  automatically as part of `*/fixtures/initial_data.json`.  Make sure
  you too need them.
* Usernea requires certain permissions to function.  Those are
  provided with the `manage.py check_permissions` command.  Make sure
  that you run it because otherwise, the sign-up page may just stop
  raise exceptions.
