from django.conf.urls import patterns, url

from activities import views

urlpatterns = patterns('',
    url(r'^$', views.list, name='list'),
    url(r'^create/$', views.create, name='create'),
    url(r'^(?P<activity_id>\d+)/$', views.show, name='show'),
    url(r'^(?P<activity_id>\d+)/edit/$', views.edit, name='edit'),
    url(r'^(?P<activity_id>\d+)/review/$', views.review, name='review'),
    url(r'^(?P<activity_id>\d+)/participate/$', views.participate, name='participate'),
    url(r'^(?P<activity_id>\d+)/view_participation/$', views.view_participation, name='view_participation'),
)
