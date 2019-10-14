from django.conf.urls import patterns, url, include
from django.contrib.contenttypes.models import ContentType
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^about_ar/$', TemplateView.as_view(template_name='hpc_temp/about_ar.html'), name='about_ar'),
    url(r'^about_en/$', TemplateView.as_view(template_name='hpc_temp/about_en.html'), name='about_en'),
    url(r'^view_versions/$', views.view_previous_versions, name='view_versions'),
    url(r'^HPC/(?P<version_id>\d+)/$', views.view_version, name='view_version'),
]
