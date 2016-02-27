from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from studentguide import views

urlpatterns = patterns('',
    url(r'^$', views.index, name="index"),
    url(r'^indicators/$', views.indicators, name="indicators"),
    url(r'^edit_mentor_of_the_month/$', views.edit_mentor_of_the_month, name="edit_mentor_of_the_month"),
    url(r'^supervisions/$', views.list_supervised_guides, name="list_supervised_guides"),
    url(r'^my_profile/$', views.my_profile, name="my_profile"),
    url(r'^requests_to_me/$', views.requests_to_me, name="requests_to_me"),

    # New Students URLs
    url(r'^new_students/requests/$', TemplateView.as_view(template_name='studentguide/list_my_requests.html'), name="list_my_requests"),
    url(r'^new_students/requests/summaries/$', views.list_request_summaries, name="list_request_summaries"),
    url(r'^new_students/random/(?P<tag_code_name>[\d\w_]+)/$', views.choose_random_guide, name="choose_random_guide"),

    # Guide URLs
    url(r'^guides/$', views.list_guides, name="list_guides"),
    url(r'^guides/(?P<tag_code_name>[\d\w_]+)$', views.list_guides_by_tag, name="list_guides_by_tag"),
    url(r'^guides/add/$', views.add_guide, name="add_guide"),
    url(r'^guides/add/introduction/$', TemplateView.as_view(template_name='studentguide/add_guide_introduction.html'), name="add_guide_introduction"),
    url(r'^guides/add/thanks/$', TemplateView.as_view(template_name='studentguide/add_guide_thanks.html'), name="add_guide_thanks"),
    url(r'^guides/(?P<guide_pk>\d+)/$', views.show_guide, name='show_guide'),
    url(r'^guides/(?P<guide_pk>\d+)/request/$', views.add_request, name='add_request'),
    url(r'^guides/(?P<guide_pk>\d+)/request/(?P<request_pk>\d+)/$', views.edit_request, name='edit_request'),
    url(r'^guides/(?P<guide_pk>\d+)/request/welcome/$', TemplateView.as_view(template_name='studentguide/add_request_introduction.html'), name='add_request_introduction'),
    url(r'^guides/(?P<guide_pk>\d+)/requests/$', views.list_guide_requests, name='list_guide_requests'),
    url(r'^guides/(?P<guide_pk>\d+)/requests/summaries/$', views.list_request_summaries, name="list_request_summaries"),
    url(r'^guides/(?P<guide_pk>\d+)/edit/$', views.edit_guide, name='edit_guide'),
    url(r'^guides/(?P<guide_pk>\d+)/delete/$', views.delete_guide, name='delete_guide'),
    url(r'^guides/(?P<guide_pk>\d+)/feedback/add/$', views.add_feedback, name='add_feedback'),
    url(r'^guides/(?P<guide_pk>\d+)/feedback/add/introduction/$', TemplateView.as_view(template_name='studentguide/add_feedback_introduction.html'),
        name='add_feedback_introduction'),
    url(r'^guides/(?P<guide_pk>\d+)/feedback/(?P<feedback_pk>\d+)/$', views.show_feedback, name='show_feedback'),
    url(r'^guides/(?P<guide_pk>\d+)/reports/$', views.list_reports, name='list_reports'),
    url(r'^guides/(?P<guide_pk>\d+)/reports/add/$', views.add_report, name='add_report'),
    url(r'^guides/(?P<guide_pk>\d+)/reports/add/introduction/$', TemplateView.as_view(template_name='studentguide/add_report_introduction.html'),
        name='add_report_introduction'),
    url(r'^guides/(?P<guide_pk>\d+)/reports/(?P<report_pk>\d+)/edit/$', views.edit_report, name='edit_report'),
    url(r'^guides/(?P<guide_pk>\d+)/reports/(?P<report_pk>\d+)/delete/$', views.delete_report, name='delete_report'),
    url(r'^guides/(?P<guide_pk>\d+)/reports/(?P<report_pk>\d+)/$', views.show_report, name='show_report'),
    url(r'^guides/ajax/control_request$', views.control_request, name="control_request"),

)
