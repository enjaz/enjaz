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

Current required settings:
* DEFAULT_FROM_EMAIL
* GOOGLE_BOOKS_KEY _(to be generated from https://code.google.com/apis/console/)_
* MEDIA_ROOT 
* MEDIA_URL
* TEMPLATE_CONTEXT_PROCESSORS =
```("django.contrib.auth.context_processors.auth",
                               "django.core.context_processors.debug",
                               "django.core.context_processors.i18n",
                               "django.core.context_processors.media",
                               "django.core.context_processors.static",
                               "django.core.context_processors.tz",
                               "django.contrib.messages.context_processors.messages",
                               "django.core.context_processors.request",)
```
