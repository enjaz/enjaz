student-portal
==============

The Student Portal is a platform for university student activity.
Through the platform, students can sumbit activities for approval,
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

Licensed under the General Public License version 3 of the License, or
(at your option) any later version.

# Installation 

Current dependencies:
* django-taggit
* django-templated-email
* django-userena
* pdfcrowd
* requests
* unicodecsv

In the project `urls.py`, add the following:
```
# [...]
from django.views.generic import TemplateView
from accounts.admin import deanship_admin
from accounts.forms import StudentSignupForm, NonStudentSignupForm, ModifiedAuthenticationForm
# [...]
    url(r'^$', 'core.views.portal_home', name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^activities/', include('activities.urls', namespace="activities")),
    url(r'^clubs/', include('clubs.urls', namespace="clubs")),
    url(r'^books/', include('books.urls', namespace="books")),
    url(r'^niqati/', include('niqati.urls', namespace="niqati")),
    url(r'^voice/', include('studentvoice.urls', namespace="studentvoice")),
    url(r'^media/', include('media.urls', namespace="media")),
    url(r'^accounts/signup/$', 'userena.views.signup', {'signup_form': StudentSignupForm, 'template_name': 'userena/student_signup_form.html'}),
    url(r'^accounts/signup/nonstudents/$', 'userena.views.signup', {'signup_form': NonStudentSignupForm, 'template_name': 'userena/nonstudent_signup_form.html'}, name="nonstudent_signup"),
    url(r'^accounts/signin/$', 'userena.views.signin', {'auth_form': ModifiedAuthenticationForm}),
    url(r'^accounts/', include('userena.urls')),
    url(r'^da/', include(deanship_admin.urls)),
# [...]
```

Current required settings:
* DEFAULT_FROM_EMAIL: The default _noreply_ email.
* GOOGLE_BOOKS_KEY: to be generated from https://code.google.com/apis/console/
* MEDIA_ROOT: Where do you want to save the covers on the server?
* MEDIA_URL: Where do you want users to access the covers?
* `AUTH_PROFILE_MODULE = 'accounts.EnjazProfile'`
* `USERENA_WITHOUT_USERNAMES = True`
* Add `"django.core.context_processors.request"` to the [default TEMPLATE_CONTEXT_PROCESSORS](https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATE_CONTEXT_PROCESSORS)

# First run

* The platform has many KSAU-HS-dependent conentns and they are load
  automatically as part of `*/fixtures/initial_data.json`.  Make sure
  you too need them.
* Usernea requires certain permissions to function.  Those are
  provided with the `manage.py check_permissions` command.  Make sure
  that you run it because otherwise, the sign-up page may just stop
  raise exceptions.
