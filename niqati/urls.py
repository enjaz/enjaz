from django.conf.urls import patterns, url
from niqati import views
from niqati.models import COUPON, SHORT_LINK

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^submit/$', views.redeem, name='submit'),
    url(r'^submit/(?P<code>[\w\d]+)/$', views.redeem, name='submit_prefilled'),
    url(r'^report/$', views.student_report, name='student_report'),
    url(r'^orders/(?P<pk>\d+)/download/coupons/$', views.download_collection,
        {"download_type": COUPON}, name="download_coupons"),
    url(r'^orders/(?P<pk>\d+)/download/links/$', views.download_collection,
        {"download_type": SHORT_LINK}, name="download_links"),
    url(r'^orders/(?P<pk>\d+)/$', views.download_collection, name='view_collec'),
    url(r'^review/$', views.review_order, name='review_order'),
    url(r'^approve/$', views.list_pending_orders, name='list_pending_orders'),
    url(r'^generalreport/$', views.general_report, name='general_report'),
)
