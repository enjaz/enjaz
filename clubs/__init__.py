from django.conf.urls import url, include
from django.contrib.contenttypes.models import ContentType
from clubs.models import Club

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
         'list_perm_check': lambda user, object: user.is_superuser, # TODO: add proper test
         #'create_perm_check': lambda user, object: True,
         #'edit_perm_check': lambda user, object: True,
         #'delete_perm_check': lambda user, object: True,
         #'entries_perm_check': lambda user, object: True,
         #'file_perm_check': lambda user, object: True,
         ### Submitter fields ###
         # 'submitter_fields': ('user.first_name', 'user.last_name',
         #                      'user.someattr.somesubattr')
         ### Settings ###
         'login_required_for_list': True,
         'object_context_name': 'club',
         # 'custom_context': {},
        })