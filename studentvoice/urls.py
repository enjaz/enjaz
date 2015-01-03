from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from studentvoice import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
   url(r'^about/$', views.about, name='about'),
    url(r'^create/$', views.create, name='create'),
    url(r'^search/', views.search, name='search'),
    url(r'^(?P<voice_id>\d+)/$', views.show, name='show'),
    url(r'^vote/$', views.vote, name='vote'),
    url(r'^(?P<voice_id>\d+)/report/$', views.report, name='report'),
    url(r'^(?P<voice_id>\d+)/create_comment/$', views.create_comment, name='create_comment'),
    url(r'^delete/(?P<voice_id>\d+)/$', views.delete, name='delete'),
    url(r'^(?P<voice_id>\d+)/edit/$', views.edit, name='edit'),
    url(r'^(?P<voice_id>\d+)/respond/$', views.respond, name='respond'),
    url(r'^(?P<voice_id>\d+)/respond/edit/$', views.edit_response, name='edit_response'),
)
