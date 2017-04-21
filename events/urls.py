from django.conf.urls import patterns, url,include
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from . import views


urlpatterns = patterns('',
    url(r'^my_abstract_list/$', views.list_my_abstracts, name="list_my_abstracts"),
    url(r'^my_registration_list/$', views.list_my_registration, name="list_my_registration"),
    url(r'^barcode/$', views.show_barcode, name="show_my_barcode"),
    url(r'^barcode/download$', views.download_barcode_pdf, name="download_barcode_pdf"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/barcode/(?P<user_pk>\d+)/download$', views.download_barcode_pdf, name="download_barcode_pdf_privileged"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/barcode/(?P<user_pk>\d+)/$', views.show_barcode, name="show_barcode_privileged"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/barcode_list/$', views.list_barcodes, name="list_barcodes"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/$', views.redirect_home, name="redirect_home"),
    #URL already puplished (to be changed after the end of hpc2)
    url(r'^(?P<event_code_name>[\d\w_\-]+)/sessions/list/$', views.list_sessions_privileged, name="list_sessions_privileged"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/sessions/$', views.list_timeslots, name="list_timeslots"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/timeslots/(?P<pk>\d+)/$', views.list_sessions, name="list_sessions"),
    url(r'^sessions/ajax/group$', views.handle_ajax, name="handle_ajax"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/sessions/(?P<pk>\d+)/$', views.show_session, name="show_session"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/sessions/(?P<pk>\d+)/attendance/$', views.show_attendance_interface, name="show_attendance_interface"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/sessions/(?P<pk>\d+)/attendance/process$', views.process_barcode, name="process_barcode"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/sessions/(?P<pk>\d+)/review/$', views.review_registrations, name="review_registrations"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/registration/$', views.introduce_registration, name="registration_introduction"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/registration/user/$', views.user_registration, name="user_registration"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/registration/list/$', views.list_registrations, name="list_registrations"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/registration/list/(?P<pk>\d+)/$', views.show_session_privileged, name="show_session_privileged"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/registration/nonuser/$', views.nonuser_registration, name="nonuser_registration"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/registration/thanks/$', views.registration_completed, name="registration_completed"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/registration/closed/$', views.registration_closed, name="registration_closed"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/registration/already/$', views.registration_already, name="registration_already"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/abstracts/$', views.submit_abstract, name="submit_abstract"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/abstracts/list/$', views.list_abstracts, name="list_abstracts"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/abstracts/(?P<pk>\d+)/$', views.show_abstract, name="show_abstract"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/abstracts/(?P<pk>\d+)/upload/$', views.presntation_upload,name="presntation_upload"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/abstracts/thanks/$', TemplateView.as_view(template_name='events/abstracts/abstract_submission_completed.html'), name="abstract_submision_completed"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/abstracts/(?P<pk>\d+)/edit/$', views.edit_abstract, name="edit_abstract"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/abstracts/(?P<pk>\d+)/delete/$', views.delete_abstract, name="delete_abstract"),
    url(r'^abstracts/img/$',views.upload_abstract_image, name="upload_abstract_image"),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/initiatives/$', views.submit_initiative, name="submit_initiative"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/initiatives/list/$', views.list_initiatives, name="list_initiatives"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/initiatives/(?P<pk>\d+)/$', views.show_initiative, name="show_initiative"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/initiatives/thanks/$', TemplateView.as_view(template_name='events/initiatives/initiatives_submission_completed.html'), name="initiative_submission_completed"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/casereports/$', views.submit_case_report,name="submit_case_report"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/casereports/(?P<pk>\d+)/$', views.show_casereport,name="show_casereport"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/casereports/(?P<pk>\d+)/delete/$', views.delete_casereport,name="delete_casereport"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/(?P<code_name>[\d\w\-]+)/$', views.show_session_group,name="show_session_group"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/abstracts/(?P<pk>\d+)/evaluate/$', views.evaluate, name="evaluate"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/abstracts/(?P<pk>\d+)/evaluate/(?P<evaluation_id>[\d\w\-]+)/$', views.edit_evaluation,name="edit_evaluation"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/abstracts/evaluators/$', views.evaluators_homepage,name="evaluators_homepage"),
                       )
