from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from arshidni import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    # Graduates
    url(r'^graduates/create/$', views.register_graduate_profile, name='register_graduate_profile'),
    url(r'^graduates/(?P<graduate_profile_id>\d+)/$', views.show_graduate_profile, name='show_graduate_profile'),
    url(r'^graduates/(?P<graduate_profile_id>\d+)/edit/$', views.edit_graduate_profile, name='edit_graduate_profile'),
    # Questions
    url(r'^questions/$', views.list_colleges, name='list_colleges'),
    url(r'^questions/(?P<college_name>[a-z])/$', views.list_questions, name='list_questions'),
    url(r'^questions/answered$', views.mark_answered, name='mark_answered'),
    url(r'^questions/(?P<college_name>[a-z])/create/$', views.submit_question, name='submit_question'),
    url(r'^questions/(?P<question_id>\d+)/$', views.show_question, name='show_question'),
    url(r'^questions/(?P<question_id>\d+)/edit/$', views.edit_question, name='edit_question'),
    url(r'^questions/(?P<question_id>\d+)/answer/$', views.submit_answer, name='submit_answer'),
    url(r'^questions/(?P<question_id>\d+)/answer/(?P<answer_id>\d+)/$', views.edit_answer, name='edit_answer'),
    # Group
    url(r'^groups/$', views.list_groups, name='list_groups'),
    url(r'^groups/join$', views.join_group, name='join_group'),
    url(r'^groups/action$', views.group_action, name='group_action'),
    url(r'^groups/create/$', views.submit_group, name='submit_group'),
    url(r'^groups/(?P<group_id>\d+)/$', views.show_group, name='show_group'),
    url(r'^groups/(?P<group_id>\d+)/edit/$', views.edit_group, name='edit_group'),
    url(r'^groups/(?P<group_id>\d+)/requests/$', views.join_group_requests, name='join_group_requests'),
    url(r'^groups/search/$', views.search_groups, name='search_groups'),
    # Student colleagues
    url(r'^colleagues/$', views.list_colleagues, name='list_colleagues'),
    url(r'^colleagues/student_action$', views.student_action, name='student_action'),
    url(r'^colleagues/colleague_action$', views.colleague_action, name='colleague_action'),
    url(r'^colleagues/create/$', views.register_colleague_profile, name='register_colleague_profile'),
    url(r'^colleagues/mine/$', views.my_supervision_requests, name='my_supervision_requests'),
    url(r'^colleagues/to_me/$', views.supervision_requests_to_me, name='supervision_requests_to_me'),
    url(r'^colleagues/(?P<colleague_profile_id>\d+)/$', views.show_colleague_profile, name='show_colleague_profile'),
    url(r'^colleagues/(?P<colleague_profile_id>\d+)/edit/$', views.edit_colleague_profile, name='edit_colleague_profile'),
    url(r'^colleagues/(?P<colleague_profile_id>\d+)/choose/$', views.submit_supervision_request, name='submit_supervision_request'),
)
