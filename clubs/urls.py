from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from clubs import views

urlpatterns = patterns('',
    url(r'^$', views.list, name='list'),
    url(r'^create/$', views.create, name='create'),
    url(r'^(?P<club_id>\d+)/$', views.show, name='show'),
    url(r'^(?P<club_id>\d+)/edit/$', views.edit, name='edit'),
    url(r'^(?P<club_id>\d+)/join/$', views.join, name='join'),
    url(r'^(?P<club_id>\d+)/join/done/$', TemplateView.as_view(template_name='clubs/join_done.html'), name='join_done'),
    url(r'^(?P<club_id>\d+)/members/$', views.view_members, name='view_members'),
    url(r'^(?P<club_id>\d+)/deputies/$', views.view_deputies, name='view_deputies'),
    url(r'^(?P<club_id>\d+)/deputies/control_deputies$', views.control_deputies, name='control_deputies'),
    url(r'^(?P<club_id>\d+)/applications/$', views.view_application, name='view_application'),
    url(r'^(?P<club_id>\d+)/applications/approve/$', views.approve_application, name='approve_application'),
    url(r'^(?P<club_id>\d+)/applications/ignore/$', views.ignore_application, name='ignore_application'),
    url(r'^(?P<club_id>\d+)/applications/download$', views.download_application, name='download_application'),
)
