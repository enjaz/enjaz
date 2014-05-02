student-portal
==============

The Student Portal is a platform for satisfying many student needs.
Through the platform, students can apply for activities, join clubs,
enter their 'Activity Points' (Niqati) and contribute and borrow
books.

It is licensed under the AGPLv3+.

Current dependencies:
* django-taggit
* django-templated-email
* django-userena
* pdfcrowd
* requests
* unicodecsv

In the project `urls.py`, add the following:
```
from accounts.customizedform import SignupFormExtra, ModifiedAuthenticationForm
# [...]
    (r'^accounts/signup/$', 'userena.views.signup', {'signup_form': SignupFormExtra}),
    (r'^accounts/signin/$', 'userena.views.signin', {'auth_form': ModifiedAuthenticationForm}),
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
