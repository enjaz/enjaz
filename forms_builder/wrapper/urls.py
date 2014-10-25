from __future__ import unicode_literals

from django.conf.urls import patterns, url
from forms_builder.wrapper import views as wrapper, settings as wrapper_settings

urlpatterns = patterns("forms_builder.forms.views",
    ### Editor URLs ###
    url(r"^new/form/$", wrapper.create_form, name="create_form"),
    url(r"^(?P<form_id>\d+)/edit/$", wrapper.edit_form, name="edit_form"),
    url(r"^(?P<form_id>\d+)/delete/$", wrapper.delete_form, name="delete_form"),
    url(r"^(?P<form_id>\d+)/entries/$", wrapper.entries_view, name="form_entries"),
    url(r"^(?P<form_id>\d+)/entries/show/$", wrapper.entries_view,
        {"show": True}, name="form_entries_show"),
    url(r"^(?P<form_id>\d+)/entries/export/$", wrapper.entries_view,
        {"export": True}, name="form_entries_export"),
    url("^file/(?P<field_entry_id>\d+)/$", wrapper.file_view, name="form_file"),

    ## Both ##
    url(r"^$", wrapper.form_list, name="form_list"),
)

if wrapper_settings.USE_SLUGS:
    urlpatterns += patterns("",
        ### End-user URLs ###
        url(r"(?P<slug>.*)/sent/$", wrapper.form_sent, name="form_sent"),
        url(r"(?P<slug>.*)/$", wrapper.form_detail, name="form_detail"),
    )
else:
    urlpatterns += patterns("",
        ### End-user URLs ###
        url(r"(?P<form_id>\d+)/sent/$", wrapper.form_sent, name="form_sent"),
        url(r"(?P<form_id>\d+)/$", wrapper.form_detail, name="form_detail"),
    )