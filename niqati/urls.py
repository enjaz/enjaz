from django.conf.urls import patterns, url
from niqati import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^submit/$', views.redeem, name='submit'),
    url(r'^submit/(?P<code>\w+)/$', views.redeem, name='submit_prefilled'),
    url(r'^report/$', views.student_report, name='student_report'),
    # url(r'^create/$', views.create_codes, name='create'),
    # url(r'^orders/$', views.view_orders, name='orders'),
    url(r'^orders/(?P<pk>\d+)/$', views.view_collection, name='view_collec'),
    url(r'^approve/$', views.approve_codes, name='approve'),
    url(r'^generalreport/$', views.general_report, name='general_report'),
)
