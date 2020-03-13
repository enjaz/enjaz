from django.conf.urls import patterns, url, include
from django.contrib.contenttypes.models import ContentType
from django.views.generic import TemplateView

from . import views
from .models import SubCourse
from clubs.utils import forms_editor_check


urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^(?P<position>(instructor|graduate))/(?P<person_id>\d+)/$',
        views.show_person, name="show_person"),
    url(r'^about/$',
        TemplateView.as_view(template_name='academy/about.html'),
        name='about'),
    url(r'^FAQ/$',
        TemplateView.as_view(template_name='academy/FAQ.html'),
        name='FAQ'),
    url(r'^(?P<course_name>\w+)/$',views.show_course, name='show'),

    url(r'^(?P<course_name>\w+)/register/$',views.register_for_course,
        name='register'),
    url(r'^(?P<course_name>\w+)/projects/$',views.list_works,
        name='list_works'),
    url(r'^(?P<course_name>\w+)/batch(?P<batch_no>\d+)/$',
        views.show_subcourse, name='show_subcourse'),
    url(r'^workshop/(?P<workshop_id>\d+)/$',
        views.show_workshop, name='show_workshop'),
    url(r'^(?P<theme>\w+)/invite/(?P<invitee_id>\w+)/$',views.invite_to_ceremony,
        name='invite_to_ceremony'),
    url(r'^(?P<course_name>\w+)/(?P<batch_no>\d+)/recordings/(?P<session_no>\d+)/$',views.show_recording,
        name='show_recorded_session'),
]

# #delete these when fobi works -soon hopefully >_< -
# # TODO: django-fobi vs django-forms-builder
#
# # Academy Forms URLS
# # Due to restrictions of django-pluggable-forms, the url confs for the app's instances have to be placed
# # in the project's main URLconf, yet to prevent cluttering due to the many customization options, the url
# # function is placed here and then imported into the main URLconf
academy_forms_urls = url(r'^academy/(?P<object_id>\d+)/forms/',
        include('forms_builder.wrapper.urls', namespace="academy_forms",
                app_name="forms"),)
#         # Custom arguments
#         {"content_type": ContentType.objects.get_for_model(SubCourse),
#          ### Templates ###
#          'form_detail_template': 'clubs/forms/form_detail.html',
#          'form_sent_template': 'clubs/forms/form_sent.html',
#          'entries_template': 'clubs/forms/form_entries.html',
#          'edit_form_template': 'clubs/forms/form_edit.html',
#          'form_list_template': 'clubs/forms/form_list.html',
#          'form_list_edit_template': 'clubs/forms/form_list_edit.html',
#          'delete_form_template': 'clubs/forms/form_delete.html',
#          ### Permission checks ###
#          'list_perm_check': forms_editor_check,
#          'create_perm_check': forms_editor_check,
#          'edit_perm_check': forms_editor_check,
#          'delete_perm_check': forms_editor_check,
#          'entries_perm_check': forms_editor_check,
#          'file_perm_check': forms_editor_check,
#          ### Submitter fields ###
#          'submitter_fields': ('user.common_profile.get_ar_full_name|default:user.username',
#                               'user.common_profile.get_en_full_name|default:user.username',
#                               'user.common_profile.student_number',
#                               'user.common_profile.badge_number',
#                               'user.common_profile.college',
#                               'user.email',
#                               'user.common_profile.mobile_number',
#                               ),
#          ### Settings ###
#          'login_required_for_list': True,
#          'object_context_name': 'subcourse',
#          # 'custom_context': {},
#          })
