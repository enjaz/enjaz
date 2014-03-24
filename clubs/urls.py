from django.conf.urls import patterns, url

from clubs import views

urlpatterns = patterns('',
    url(r'^$', views.list, name='list'),
    url(r'^create/$', views.create, name='create'),
    url(r'^(?P<club_id>\d+)/$', views.show, name='show'),
    url(r'^(?P<club_id>\d+)/edit/$', views.edit, name='edit'),
    url(r'^(?P<club_id>\d+)/join/$', views.join, name='join'),
    url(r'^(?P<club_id>\d+)/view_applications/$', views.view_applications, name='view_applications'),
)
