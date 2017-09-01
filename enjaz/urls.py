from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from accounts.admin import user_list_admin
from accounts.forms import StudentSignupForm, NonStudentSignupForm, NonUserSignupForm, ModifiedAuthenticationForm
from activities.admin import invitation_admin
from activities.urls import activity_forms_urls
from bulb.admin import bulb_admin
from certificates.admin import certificate_admin
from clubs.urls import club_forms_urls
from core.views import visit_announcement
from researchhub.forms import ResearchHubSignupForm
from tedx.admin import tedx_admin
from teams.urls import team_forms_urls

urlpatterns = [
    url(r'^', include('core.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^tedx/admin/', include(tedx_admin.urls)),
    url(r'^tedx/', include('tedx.urls', namespace="tedx")),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include('loginas.urls')),
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
    url(r'^books/', RedirectView.as_view(pattern_name='bulb:index', permanent=True)),
    url(r'^niqati/', include('niqati.urls', namespace="niqati")),
    url(r'^voice/', include('studentvoice.urls', namespace="studentvoice")),
    url(r'^user_list/', include(user_list_admin.urls)),
    url(r'^arshidni/', RedirectView.as_view(pattern_name='studentguide:index', permanent=True)),
    url(r'^mediacenter/', include('media.urls', namespace="media")),
    url(r'^accounts/profile_type/$', TemplateView.as_view(template_name='profile_type.html'), name='profile_type'),
    url(r'^accounts/signup/$', 'userena.views.signup', {'signup_form': StudentSignupForm, 'template_name': 'userena/student_signup_form.html'}),
    url(r'^accounts/resend/$', 'accounts.views.resend_confirmation_key', name='resend_confirmation_key'),
    url(r'^accounts/signup/nonstudents/$', 'userena.views.signup', {'signup_form': NonStudentSignupForm, 'template_name': 'userena/nonstudent_signup_form.html'}, name="nonstudent_signup"),
    url(r'^accounts/signup/nonusers/$', 'userena.views.signup', {'signup_form': NonUserSignupForm, 'template_name': 'userena/nonuser_signup_form.html'}, name="nonuser_signup"),
    url(r'^accounts/signin/$', 'userena.views.signin', {'auth_form': ModifiedAuthenticationForm}),
    url(r'^accounts/edit/$', 'accounts.views.edit_common_profile', name='edit_common_profile'),
    url(r'^accounts/', include('userena.urls')),
    url(r'^questions/', include('questions.urls', namespace="cultural_program_code")),
    url(r'^certificates/admin/', include(certificate_admin.urls)),
    url(r'^certificates/', include('certificates.urls', namespace="certificates")),
    url(r'^tagging_autocomplete/', include('tagging_autocomplete.urls')),
    team_forms_urls,
    url(r'^teams/', include('teams.urls', namespace="teams")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
