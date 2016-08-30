student-portal
==============

The Student Portal is a [Django-based](https://www.djangoproject.com)
platform for university student activity.  Through the platform,
students can submit activities for approval, join clubs, enter their
'Activity Points' (Niqati) and contribute and borrow books.

# Licensing

Copyright (C) 2014-2016 Muhammad Saeed Arabi and [Osama Khalid](https://osamakhalid.com).

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

Enjaz Portal works with Python 2.7 and Django 1.8.

You can instlal all the dependencies  using:

```pip install -r requirements.txt```


### Step one: URLS
In the project `urls.py`, add the following:
```
# After default imports:

from django.views.generic import TemplateView
from accounts.forms import StudentSignupForm, NonStudentSignupForm, ModifiedAuthenticationForm
from accounts.admin import user_list_admin
from activities.urls import activity_forms_urls
from researchhub.forms import ResearchHubSignupForm
from clubs.urls import club_forms_urls
from core.views import visit_announcement
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^', include('core.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    activity_forms_urls,
    url(r'^activities/', include('activities.urls', namespace="activities")),
    club_forms_urls,
    url(r'^clubs/', include('clubs.urls', namespace="clubs")),
    url(r'^bulb/', include('bulb.urls', namespace="bulb")),
    url(r'^events/', include('events.urls', namespace="events")),
    url(r'^hpc/', include('hpc.urls', namespace="hpc")),
    url(r'^researchhub/supervisors/signup/$', 'userena.views.signup', {'signup_form': ResearchHubSignupForm, 'template_name': 'researchhub/supervisor_signup_form.html'}, name="supervisor_signup"),
    url(r'^researchhub/', include('researchhub.urls', namespace="researchhub")),
    url(r'^mentors/', include('studentguide.urls', namespace="studentguide")),
    url(r'^niqati/', include('niqati.urls', namespace="niqati")),
    url(r'^voice/', include('studentvoice.urls', namespace="studentvoice")),
    url(r'^user_list/', include(user_list_admin.urls)),
    url(r'^mediacenter/', include('media.urls', namespace="media")),
    url(r'^accounts/signup/$', 'userena.views.signup', {'signup_form': StudentSignupForm, 'template_name': 'userena/student_signup_form.html'}),
    url(r'^accounts/resend/$', 'accounts.views.resend_confirmation_key', name='resend_confirmation_key'),
    url(r'^accounts/signup/nonstudents/$', 'userena.views.signup', {'signup_form': NonStudentSignupForm, 'template_name': 'userena/nonstudent_signup_form.html'}, name="nonstudent_signup"),
    url(r'^accounts/signin/$', 'userena.views.signin', {'auth_form': ModifiedAuthenticationForm}),
    url(r'^accounts/edit/$', 'accounts.views.edit_common_profile', name='edit_common_profile'),
    url(r'^accounts/', include('userena.urls')),
    url(r'^books/', RedirectView.as_view(pattern_name='bulb:index')),
    url(r'^arshidni/', RedirectView.as_view(pattern_name='studentguide:index')),
]
```


Furthermore, if you are running Enjaz on development server, make sure
you confiture the static and media URLs as per the [Django documentation](https://docs.djangoproject.com/en/1.8/howto/static-files/#serving-static-files-during-development).

### Step two: Settings

Replace `INSTALLED_APPS` in `settings.py` with the following:
```
INSTALLED_APPS = (
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'core',
    'userena',
    'taggit',
    'guardian',
    'easy_thumbnails',
    'bootstrap3',
    'post_office',
    'constance',
    'constance.backends.database',
    'activities',
    'books',
    'clubs',
    'niqati',
    'media',
    'studentvoice',
    'forms_builder.forms',
    'forms_builder.wrapper',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'api',
    'bulb',
    'arshidni',
    'studentguide',
    'hpc',
    'researchhub',
    'wkhtmltopdf',
    'events',
)
```

Also add the following settings:
```
AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
SITE_ID = 1
ANONYMOUS_USER_ID = -1
AUTH_PROFILE_MODULE = 'accounts.EnjazProfile'
USERENA_WITHOUT_USERNAMES = True
USERENA_ACTIVATION_RETRY = True
USERENA_ACTIVATION_DAYS = 30
FORMS_BUILDER_USE_SLUGS = False # or True if you like
FORMS_BUILDER_USE_SITES = False
FORMS_BUILDER_CHOICES_SEPARATOR = '/' # or any character of your choice
```

Finally, there are two more required settings:
* `DEFAULT_FROM_EMAIL`: The default _noreply_ email.
* `BITLY_KEY`: a bit.ly API key


### Step three: Migrate!

After everything is set, migrate!

```python manage.py migrate```