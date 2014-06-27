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

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Affero General Public License for more details.

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
from accounts.customizedform import SignupFormExtra, ModifiedAuthenticationForm
# [...]
    (r'^$', 'activities.views.portal_home', name='home'),
    (r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
    (r'^copy/$', TemplateView.as_view(template_name='copy.html'), name='copy'),
    (r'^clubs/', include('clubs.urls', namespace="clubs")),
    (r'^books/', include('books.urls', namespace="books")),
    (r'^niqati/', include('niqati.urls', namespace="niqati")),
    (r'^accounts/signup/$', 'userena.views.signup', {'signup_form': SignupFormExtra}),
    (r'^accounts/signin/$', 'userena.views.signin', {'auth_form': ModifiedAuthenticationForm}),
    (r'^accounts/', include('userena.urls'),
    (r'^deanship_admin/', include(deanship_admin.urls)),
# [...]
```

Current required settings:
* DEFAULT_FROM_EMAIL: The default _noreply_ email.
* GOOGLE_BOOKS_KEY: to be generated from https://code.google.com/apis/console/
* MEDIA_ROOT: Where do you want to save the covers on the server?
* MEDIA_URL: Where do you want users to access the covers?
* `AUTH_PROFILE_MODULE = 'accounts.MyProfile'`
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
