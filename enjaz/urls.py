"""enjaz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from accounts.forms import StudentSignupForm, NonStudentSignupForm, ModifiedAuthenticationForm
from accounts.admin import user_list_admin
from activities.urls import activity_forms_urls
from bulb.admin import bulb_admin
from clubs.urls import club_forms_urls
from core.views import visit_announcement
from django.views.generic.base import RedirectView
from researchhub.forms import ResearchHubSignupForm


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('core.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    activity_forms_urls,
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
    url(r'^accounts/signup/nonstudents/$', 'userena.views.signup', {'signup_form': NonStudentSignupForm, 'template_name': 'userena/nonstudent_signup_form.html'}, name="nonstudent_signup"),
    url(r'^accounts/signin/$', 'userena.views.signin', {'auth_form': ModifiedAuthenticationForm}),
    url(r'^accounts/edit/$', 'accounts.views.edit_common_profile', name='edit_common_profile'),
    url(r'^accounts/', include('userena.urls')),
    url(r'^books/', RedirectView.as_view(pattern_name='bulb:index')),
    url(r'^arshidni/', RedirectView.as_view(pattern_name='studentguide:index')),
]
