from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', 'core.views.portal_home', name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^aboutsc/$', 'core.views.about_sc', name='about_sc'),
    url(r'^copy/$', TemplateView.as_view(template_name='copy.html'), name='copy'),
    url(r'^debate/$', 'core.views.debate', name='debate'),
    url(r'^indicators/$', 'core.views.indicators', name='indicators'),
    url(r'^indicators/(?P<city>\w)/$', 'core.views.indicators', name='indicators_for_city'),
    url(r'^aboutsc/deanship_cp4/$', TemplateView.as_view(template_name='cp4_bader.html'), name='cp4_bader'),
    url(r'^visit/(?P<pk>\d+)/$', "core.views.visit_announcement", name='visit_announcement'),
    url(r'^cancel_twitter_connection$', "core.views.cancel_twitter_connection", name='cancel_twitter_connection'),
    url('', include('social.apps.django_app.urls', namespace='social')),
)
