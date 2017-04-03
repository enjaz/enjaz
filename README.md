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

Create a new project, for example:
```django-admin startproject enjaz```

Then within the `enjaz` directory, turn it on the git repository:

```
git init
git remote add origin https://github.com/osamak/student-portal.git
git pull origin master
```

You can then install all the dependencies using:

```pip install -r requirements.txt```

### Step one: URLS
In the project `urls.py`, add the following:
```
# After default imports:

from django.views.generic import TemplateView
from accounts.forms import StudentSignupForm, NonStudentSignupForm, NonUserSignupForm, ModifiedAuthenticationForm
from accounts.admin import user_list_admin
from activities.admin import invitation_admin
from activities.urls import activity_forms_urls
from bulb.admin import bulb_admin
from clubs.urls import club_forms_urls
from core.views import visit_announcement
from django.views.generic.base import RedirectView
from researchhub.forms import ResearchHubSignupForm
from tedx.admin import tedx_admin

urlpatterns = [
    url(r'^', include('core.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    activity_forms_urls,
    url(r'^activities/admin/', include(invitation_admin.urls)),
    url(r'^activities/', include('activities.urls', namespace="activities")),
    club_forms_urls,
    url(r'^clubs/', include('clubs.urls', namespace="clubs")),
    url(r'^bulb/admin/', include(bulb_admin.urls)),
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
    url(r'^accounts/profile_type/$', TemplateView.as_view(template_name='profile_type.html'), name='profile_type'),
    url(r'^accounts/signup/nonstudents/$', 'userena.views.signup', {'signup_form': NonStudentSignupForm, 'template_name': 'userena/nonstudent_signup_form.html'}, name="nonstudent_signup"),
    url(r'^accounts/signup/nonusers/$', 'userena.views.signup', {'signup_form': NonUserSignupForm, 'template_name': 'userena/nonuser_signup_form.html'}, name="nonuser_signup"),
    url(r'^accounts/signin/$', 'userena.views.signin', {'auth_form': ModifiedAuthenticationForm}),
    url(r'^accounts/edit/$', 'accounts.views.edit_common_profile', name='edit_common_profile'),
    url(r'^accounts/', include('userena.urls')),
    url(r'^books/', RedirectView.as_view(pattern_name='bulb:index')),
    url(r'^arshidni/', RedirectView.as_view(pattern_name='studentguide:index')),
    url(r'^tagging_autocomplete/', include('tagging_autocomplete.urls')),
    url(r'^tedx/admin/', include(tedx_admin.urls)),
    url(r'^tedx/', include('tedx.urls', namespace="tedx")),
]
```


Furthermore, if you are running Enjaz on development server, make sure
you confiture the static and media URLs as per the [Django documentation](https://docs.djangoproject.com/en/1.8/howto/static-files/#serving-static-files-during-development).

### Step two: Settings

Import the following:
```
from django.contrib.messages import constants as messages
```

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
    'guardian',
    'easy_thumbnails',
    'bootstrap3',
    'post_office',
    'constance',
    'constance.backends.database',
    'activities',
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
    'social.apps.django_app.default',
    'tedx',
)
```

Also add the following settings:
```
AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'social.backends.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',
)
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
SITE_ID = 1
ANONYMOUS_USER_ID = -1
AUTH_PROFILE_MODULE = 'accounts.EnjazProfile'
LOGIN_URL = '/accounts/signin/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = '/accounts/signout/'
LOGOUT_REDIRECT_URL = '/'
USERENA_WITHOUT_USERNAMES = True
USERENA_ACTIVATION_RETRY = True
USERENA_ACTIVATION_DAYS = 30
FORMS_BUILDER_USE_SLUGS = False # or True if you like
FORMS_BUILDER_USE_SITES = False
FORMS_BUILDER_CHOICES_SEPARATOR = '/' # or any character of your choice

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
    }

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_CONFIG = {
    'STUDENTVOICE_THRESHOLD': (30, ''),
    'DEBATE_URL': ('',''),
    }

REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
            )
    }
SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
)
```

Finally, there are two more required settings:
* `DEFAULT_FROM_EMAIL`: The default _noreply_ email.
* `BITLY_KEY`: a bit.ly API key
* `SOCIAL_AUTH_TWITTER_KEY`: Twitter consumer key
* `SOCIAL_AUTH_TWITTER_SECRET`: Twitter secret key


### Step three: Get the database sorted out

After everything is set, migrate!

```python manage.py migrate```

Then import sites, categories and email templates:

```python manage.py loaddata core/fixtures/default_emailtemplates.json core/fixtures/default_sites.json activities/fixtures/default_categories.json```

Finally, create userena permissions using:

```python manage.py check_permissions```
