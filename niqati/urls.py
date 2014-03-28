from django.conf.urls import patterns, url

from niqati import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^submit/$', views.submit, name='submit'),
    url(r'^submit/(?P<code>\w+)/$', views.submit, name='submit_prefilled'),
    url(r'^report/$', views.student_report, name='student_report'),
    url(r'^create/$', views.create_codes, name='create'),
    url(r'^orders/$', views.view_orders, name='orders'),
    url(r'^approve/$', views.approve_codes, name='approve'),
    url(r'^generalreport/$', views.general_report, name='generalreport'),
)