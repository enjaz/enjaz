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
    url(r'^(?P<club_id>\d+)/view_application/$', views.view_application, name='view_application'),
    url(r'^(?P<club_id>\d+)/view_application/download$', views.download_application, name='download_application'),
)
