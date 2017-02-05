from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from hpc import views

urlpatterns = patterns('',
    url(r'^registration/list/$', views.list_registrations, name="list_registrations"),
    url(r'^abstracts/list/$', views.list_abstracts, name="list_abstracts"),
    url(r'^abstracts/show/(?P<pk>\d+)/$', views.show_abstract, name="show_abstract"),
    url(r'^sessions/$', views.list_sessions, name="list_sessions"),
    url(r'^sessions/(?P<pk>\d+)/$', views.show_session, name="show_session"),
    url(r'', RedirectView.as_view(url="https://hpc.enjazportal.com", permanent=True)),
)
