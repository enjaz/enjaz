from django.conf.urls import patterns, url, include
from django.contrib.contenttypes.models import ContentType
from django.views.generic import TemplateView

from clubs import views
from clubs.models import Club
from clubs.utils import forms_editor_check

urlpatterns = patterns('',
    url(r'^$', views.list, name='list'),
    url(r'^create/$', views.create, name='create'),
    url(r'^(?P<club_id>\d+)/$', views.show, name='show'),
    url(r'^(?P<club_id>\d+)/edit/$', views.edit, name='edit'),
    url(r'^(?P<club_id>\d+)/join/$', views.join, name='join'),
    url(r'^(?P<club_id>\d+)/join/done/$', TemplateView.as_view(template_name='clubs/join_done.html'), name='join_done'),
    url(r'^(?P<club_id>\d+)/members/$', views.view_members, name='view_members'),
    url(r'^(?P<club_id>\d+)/applications/$', views.view_application, name='view_application'),
    url(r'^(?P<club_id>\d+)/applications/approve/$', views.approve_application, name='approve_application'),
    url(r'^(?P<club_id>\d+)/applications/ignore/$', views.ignore_application, name='ignore_application'),
    url(r'^(?P<club_id>\d+)/applications/download$', views.download_application, name='download_application'),
)

# Club Forms URLS
# Due to restrictions of django-pluggable-forms, the url confs for the app's instances have to be placed
# in the project's main URLconf, yet to prevent cluttering due to the many customization options, the url
# function is placed here and then imported into the main URLconf
club_forms_urls = url(r'^clubs/(?P<object_id>\d+)/forms/',
        include('forms_builder.wrapper.urls', namespace="club_forms", app_name="forms"),

        # Custom arguments
        {"content_type": ContentType.objects.get_for_model(Club),
         ### Templates ###
         'form_detail_template': 'clubs/forms/form_detail.html',
         'form_sent_template': 'clubs/forms/form_sent.html',
         'entries_template': 'clubs/forms/form_entries.html',
         'edit_form_template': 'clubs/forms/form_edit.html',
         'form_list_template': 'clubs/forms/form_list.html',
         'form_list_edit_template': 'clubs/forms/form_list_edit.html',
         'delete_form_template': 'clubs/forms/form_delete.html',
         ### Permission checks ###
         'list_perm_check': forms_editor_check,
         'create_perm_check': forms_editor_check,
         'edit_perm_check': forms_editor_check,
         'delete_perm_check': forms_editor_check,
         'entries_perm_check': forms_editor_check,
         'file_perm_check': forms_editor_check,
         ### Submitter fields ###
         'submitter_fields': ('user.student_profile.get_ar_full_name|default:user.username',
                              'user.student_profile.get_en_full_name|default:user.username',
                              'user.student_profile.student_number',
                              'user.student_profile.badge_number',
                              'user.student_profile.college',
                              'user.email',
                              'user.student_profile.mobile_number',
                              ),
         ### Settings ###
         'login_required_for_list': True,
         'object_context_name': 'club',
         # 'custom_context': {},
        })