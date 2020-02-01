from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    # url(r'^$', views.index, name="index"),
    # url(r'^form/$', views.view_form, name="view_form"),
    # url(r'^(?P<section>\w+)/$', views.view_section, name="view_section"),
    # url(r'^hackathon/form/$', TemplateView.as_view(template_name='science_olympiad/hackathon_form.html'), name='hackathon_form'),
    # url(r'^gallery/form/$', TemplateView.as_view(template_name='science_olympiad/gallery_form.html'), name='gallery_form'),
    # url(r'^inventors/add/$', views.add_inventor, name='add_inventor'),
    url(r'^inventors/register/$', views.add_inventor2, name='add_inventor'),
    # url(r'^inventors/add/3/$', views.add_inventor3, name='add_inventor2'),
    url(r'^contest/(?P<contest_id>\d+)/(?P<question_id>\d+)/welcome/$', views.show_contest_welcomepage, name='welcome_contest'),
    # url(r'^contest/(?P<contest_id>\d+)/begin/$', views.begin_contest, name='begin_contest'),
    url(r'^contest/end/$', views.show_contest_endpage, name='end_contest'),
    url(r'^contest/(?P<contest_id>\d+)/walkthrough/$', views.walkthrough_contest, name='handle_walkthrough'),
    url(r'^contest/walkthrough/1/$', views.walkthrough_contest1, name='walkthrough_contest1'),
    url(r'^contest/test_wheel/$', views.test_wheel, name='test_wheel'),

    url(r'^contest/(?P<contest_id>\d+)/question/(?P<question_id>\d+)/$', views.show_question, name='show_question'),
]
