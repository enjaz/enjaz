from django.conf.urls import patterns, url
from niqati import views
from niqati.models import COUPON, SHORT_LINK

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^submit/$', views.redeem, name='submit'),
    url(r'^submit/claim/$', views.claim_code, name='claim_code'),
    url(r'^submit/(?P<code>[\w\d]+)/$', views.redeem, name='submit_prefilled'),
    url(r'^report/$', views.student_report, name='student_report'),
    url(r'^report/(?P<username>[\.\w\d\-]+)/$', views.student_report, name='student_report_with_username'),
    url(r'^collections/(?P<pk>\d+)/download/coupons/$', views.download_collection,
        {"download_type": COUPON}, name="download_coupons"),
    url(r'^collections/(?P<pk>\d+)/download/links/$', views.download_collection,
        {"download_type": SHORT_LINK}, name="download_links"),
    url(r'^orders/(?P<pk>\d+)/$', views.download_collection, name='view_collec'),
    url(r'^review/$', views.review_order, name='review_order'),
    url(r'^short_url/$', views.get_short_url, name='get_short_url'),
    url(r'^approve/$', views.list_pending_orders, name='list_pending_orders'),
    url(r'^generalreport/$', views.general_report, name='general_report'),
    url(r'^generalreport/(?P<city_code>\w+)/$', views.general_report, name='general_report_for_city'),
    url(r'^medicinereport/(?P<year>\d+)/$', views.medicine_general_report, name='medicine_general_report'),
    url(r'^niqati-user-autocomplete/$', views.NiqatiUserAutocomplete.as_view(), name='niqati-user-autocomplete',),
    url(r'^report/(?P<username>[\.\w\d\-]+)/(?P<year>\d+)/$', views.student_report,name='student_report_with_year'),
)
