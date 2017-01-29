from django.conf.urls import patterns, url,include
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from events import views

urlpatterns = patterns('',
    url(r'^my_abstract_list/$', views.list_my_abstracts, name="list_my_abstracts"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/$', views.redirect_home, name="redirect_home"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/sessions/$', views.list_sessions, name="list_sessions"),
    url(r'^sessions/ajax/group$', views.handle_ajax, name="handle_ajax"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/sessions/(?P<pk>\d+)/$', views.show_session, name="show_session"),
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
    url(r'^(?P<event_code_name>[\d\w_\-]+)/abstracts/thanks/$', TemplateView.as_view(template_name='events/abstracts/abstract_submission_completed.html'), name="abstract_submision_completed"),
    url(r'^abstracts/img/$',views.upload_abstract_image, name="upload_abstract_image"),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/initiatives/$', views.submit_initiation, name="submit_initiative"),
    url(r'^(?P<event_code_name>[\d\w_\-]+)/initiatives/thanks/$', TemplateView.as_view(template_name='events/initiatives/initiatives_submission_completed.html'), name="initiative_submission_completed"),

)
