from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^form/$', views.view_form, name="view_form"),
    url(r'^(?P<section>\w+)/$', views.view_section, name="view_section"),
    url(r'^hackathon/form/$', TemplateView.as_view(template_name='science_olympiad/hackathon_form.html'), name='hackathon_form'),
    url(r'^gallery/form/$', TemplateView.as_view(template_name='science_olympiad/gallery_form.html'), name='gallery_form'),
]