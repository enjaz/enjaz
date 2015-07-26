from django.conf.urls import patterns, url
from niqati import views
from niqati.models import COUPON, SHORT_LINK

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^submit/$', views.redeem, name='submit'),
    url(r'^submit/(?P<code>\w+)/$', views.redeem, name='submit_prefilled'),
    url(r'^report/$', views.student_report, name='student_report'),
    url(r'^(?P<order_id>\d+)/download/coupons/$', views.download_collection,
        {"download_type": COUPON}, name="download_coupons"),
    url(r'^(?P<order_id>\d+)/download/links/$', views.download_collection,
        {"download_type": SHORT_LINK}, name="download_links"),
    url(r'^orders/(?P<pk>\d+)/$', views.download_collection, name='view_collec'),
    url(r'^approve/$', views.approve_codes, name='approve'),
    url(r'^generalreport/$', views.general_report, name='general_report'),
)
