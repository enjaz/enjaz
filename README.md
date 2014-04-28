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
* Add `"django.core.context_processors.request"` to the [default TEMPLATE_CONTEXT_PROCESSORS](https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATE_CONTEXT_PROCESSORS)
```
