from django.conf.urls import url,include
from django.contrib.auth.decorators import login_required, permission_required
from teams import views as teams_views
from teams.models import Team
from django.contrib.contenttypes.models import ContentType
from teams.utils import forms_editor_check


urlpatterns = [
    url(r'^$', teams_views.ListView.as_view(), name='list_teams'),
    url(r'^create/$', login_required(teams_views.CreateView.as_view()), name='create'),
    url(r'^(?P<code_name>[\d\w_\-]+)/$', login_required(teams_views.DetailView.as_view()), name='show'),
    url(r'^(?P<year>\d{4})/(?P<code_name>[\d\w_\-]+)/$', login_required(teams_views.ArchiveDetailView.as_view()), name='archive'),
    url(r'^(?P<code_name>[\d\w_\-]+)/edit/$', login_required(teams_views.UpdateView.as_view()), name='edit'),
    url(r'^(?P<code_name>[\d\w_\-]+)/send_email', teams_views.send_email, name='send_email'),
    url(r'^(?P<code_name>[\d\w_\-]+)/ajax/add', teams_views.add_members, name='add_members'),
    url(r'^(?P<code_name>[\d\w_\-]+)/ajax/open_close', teams_views.control_registration, name='control_registration'),
    url(r'^(?P<code_name>[\d\w_\-]+)/ajax/add', teams_views.add_position, name='add_position'),
    url(r'^(?P<code_name>[\d\w_\-]+)/manage$', login_required(teams_views.ManageTeamDetailView.as_view()), name='manage_team'),


]
team_forms_urls = url(r'^teams/(?P<object_id>\d+)/forms/',
        include('forms_builder.wrapper.urls', namespace="team_forms", app_name="forms"),

        # Custom arguments
        {"content_type": ContentType.objects.get_for_model(Team),
         ### Templates ###
         'form_detail_template': 'teams/forms/form_detail.html',
         'form_sent_template': 'teams/forms/form_sent.html',
         'entries_template': 'teams/forms/form_entries.html',
         'edit_form_template': 'teams/forms/form_edit.html',
         'form_list_template': 'teams/forms/form_list.html',
         'form_list_edit_template': 'teams/forms/form_list_edit.html',
         'delete_form_template': 'teams/forms/form_delete.html',
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
                              'user.common_profile.student_number',
                              'user.common_profile.badge_number',
                              'user.common_profile.college',
                              'user.email',
                              'user.common_profile.mobile_number',
                              ),
         ### Settings ###
         'login_required_for_list': True,
         'object_context_name': 'team',
         # 'custom_context': {},
        })