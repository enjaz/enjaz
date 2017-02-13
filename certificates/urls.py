from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from certificates import views

urlpatterns = patterns('',
    url(r'^$', views.index, name="index"),
    url(r'^certificates/(?:(?P<username>[\.\w\d\-]+)/)?$', views.list_certificates, name="list_certificates"),
    url(r'^certificates/(?P<verification_code>[\w\d]+)/$', views.show_certificate, name="show_certificate"),
    url(r'^certificates/verify/$', views.verify_certificate, name="verify_certificate"),

    url(r'^requests/(?:by_club/(?P<club_pk>\d+)/)?$', views.list_certificate_requests, name="list_certificate_requests"),
    url(r'^requests/add/$', views.add_certificate_request, name="add_certificate_request"),
    url(r'^requests/add/introduction/$', TemplateView.as_view(template_name='certificates/add_request_introduction.html'), name="add_request_introduction"),
    url(r'^requests/(?P<pk>\d+)/$', views.show_certificate_request, name="show_certificate_request"),
    url(r'^requests/(?P<pk>\d+)/edit/$', views.edit_certificate_request, name="edit_certificate_request"),
    url(r'^requests/(?P<pk>\d+)/approve/$', views.approve_request, name="approve_certificate_request"),
    url(r'^requests/(?P<pk>\d+)/approve/delete/$', views.delete_template, name='delete_template'),
    url(r'^requests/(?P<pk>\d+)/approve/save$', views.save_image, name='save_image'),
    url(r'^requests/(?P<pk>\d+)/approve/upload$', views.upload_image, name='upload_image'),
    url(r'^requests/(?P<pk>\d+)/approve/update$', views.update_image, name='update_image'),
)
