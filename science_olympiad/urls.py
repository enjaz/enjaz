from django.conf.urls import patterns, url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^form/$', views.view_form, name="view_form"),
    url(r'^section/$', views.view_section, name="view_section"),
]