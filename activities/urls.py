from django.conf.urls import patterns, url, include
from django.contrib.contenttypes.models import ContentType
from activities import views
from activities.models import Activity
from activities.utils import forms_editor_check
from niqati import views as niqati_views


urlpatterns = patterns('',
    url(r'^$', views.list_activities, name='list'),
    url(r'^invitation/(?P<pk>\d+)/$', views.show_invitation, name='show_invitation'),
    url(r'^invitation/(?P<pk>\d+)/list/$', views.list_invitation_participants, name='list_invitation_participants'),
    url(r'^invitation/(?P<pk>\d+)/confirm', views.toggle_confirm_invitation, name='toggle_confirm_invitation'),
    url(r'^create/$', views.create, name='create'),
    url(r'^depository/$', views.list_depository_items, name='list_depository_items'),
    url(r'^(?P<activity_id>\d+)/$', views.show, name='show'),
    url(r'^(?P<activity_id>\d+)/edit/$', views.edit, name='edit'),
    url(r'^(?P<activity_id>\d+)/delete/$', views.delete, name='delete'),
    url(r'^(?P<activity_id>\d+)/review/(?P<reviewer_id>\d+)/$', views.review, name='review'),
    url(r'^(?P<activity_id>\d+)/participate/$', views.participate, name='participate'),
    url(r'^(?P<activity_id>\d+)/assess/$', views.assessment_index, name='assessment_index'),
    url(r'^(?P<activity_id>\d+)/assess/(?P<category>[mp])/$', views.assess, name='assess'),
    url(r'^assessments/$', views.assessment_list, name='assessment_list'),
    url(r'^(?P<activity_id>\d+)/niqati/$', niqati_views.coordinator_view, name='niqati_orders'),
    url(r'^autocomplete_items/$', views.autocomplete_items, name='autocomplete_items'),
    # url(r'^(?P<activity_id>\d+)/niqati/create/$', niqati_views.coordinator_view, name='niqati_create'),
)

# Activity Forms URLS
# Due to restrictions of django-pluggable-forms, the url confs for the app's instances have to be placed
# in the project's main URLconf, yet to prevent cluttering due to the many customization options, the url
# function is placed here and then imported into the main URLconf
activity_forms_urls = url(r'^activities/(?P<object_id>\d+)/forms/',
        include('forms_builder.wrapper.urls', namespace="activity_forms", app_name="forms"),

        # Custom arguments
        {"content_type": ContentType.objects.get_for_model(Activity),
         ### Templates ###
         'form_detail_template': 'activities/forms/form_detail.html',
         'form_sent_template': 'activities/forms/form_sent.html',
         'entries_template': 'activities/forms/form_entries.html',
         'edit_form_template': 'activities/forms/form_edit.html',
         'form_list_template': 'activities/forms/form_list.html',
         'form_list_edit_template': 'activities/forms/form_list_edit.html',
         'delete_form_template': 'activities/forms/form_delete.html',
         ### Permission checks ###
         'list_perm_check': forms_editor_check,
         'create_perm_check': forms_editor_check,
         'edit_perm_check': forms_editor_check,
         'delete_perm_check': forms_editor_check,
         'entries_perm_check': forms_editor_check,
         'file_perm_check': forms_editor_check,
         ### Submitter fields ###
         'submitter_fields': ('user.common_profile.get_ar_full_name|default:user.username',
                              'user.common_profile.get_en_full_name|default:user.username',
                              'user.common_profile.student_id',
                              'user.common_profile.badge_number',
                              'user.common_profile.college',
                              'user.email',
                              'user.common_profile.mobile_number',
                              ),
         ### Settings ###
         'login_required_for_list': True,
         'object_context_name': 'activity',
         'custom_context': {'active_tab': 'forms'},
         })
