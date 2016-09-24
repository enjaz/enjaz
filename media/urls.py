from django.conf.urls import patterns, url
from media import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^activities/$', views.list_activities, name="list_activities"),
    url(r'^activities/campus/$', views.list_campus_activities, name="list_campus_activities"),
                       
    # Reports
    url(r'^activities/reports/$', views.list_reports, name="list_reports"),
    url(r'^activities/reports/(?P<episode_pk>\d+)/submit/$', views.submit_employee_report, name="submit_employee_report"),
    url(r'^activities/reports/(?P<episode_pk>\d+)/submit/$', views.submit_report, name="submit_report"),
    url(r'^activities/reports/(?P<episode_pk>\d+)/$', views.show_report, name="show_report"),
    url(r'^activities/reports/(?P<episode_pk>\d+)/edit/$', views.edit_report, name="edit_report"),
    url(r'^activities/reports/(?P<episode_pk>\d+)/comment/$', views.report_comment, name="report_comment"),
    url(r'^activities/reports/options/$', views.update_report_options, name="update_report_options"),

    # Stories
    url(r'^activities/stories/(?P<episode_pk>\d+)/create/$', views.create_story, name="create_story"),
    url(r'^activities/stories/(?P<episode_pk>\d+)/$', views.show_story, name="show_story"),
    url(r'^activities/stories/(?P<episode_pk>\d+)/edit/$', views.edit_story, name="edit_story"),
    url(r'^activities/stories/assign/$', views.assign_story_task, name="assign_story_task"),

    # Articles
    url(r'^articles/$', views.list_articles, name="list_articles"),
    url(r'^articles/submit/$', views.submit_article, name="submit_article"),
    url(r'^articles/(?P<pk>\d+)/$', views.show_article, name="show_article"),
    url(r'^articles/(?P<pk>\d+)/edit/$', views.edit_article, name="edit_article"),
    url(r'^articles/(?P<pk>\d+)/review/$', views.review_article, name="review_article"),

    # Tasks
    url(r'^tasks/$', views.list_tasks, name="list_tasks"),
    url(r'^tasks/create/$', views.create_task, name="create_task"),
    url(r'^tasks/(?P<pk>\d+)/$', views.show_task, name="show_task"),
    url(r'^tasks/(?P<pk>\d+)/edit/$', views.edit_task, name="edit_task"),
    url(r'^tasks/(?P<pk>\d+)/complete/$', views.mark_task_complete, name="mark_task_complete"),
    url(r'^tasks/(?P<pk>\d+)/comment/$', views.add_comment, name="add_comment"),

    # What's new?
    url(r'^buzzes/$', views.buzzes_home, name="buzzes_home"),
    url(r'^buzzes/add/$', views.add_buzz, name="add_buzz"),
    url(r'^buzzes/(?P<buzz_id>\d+)/delete/$', views.delete_buzz, name="delete_buzz"),
    url(r'^buzzes/(?P<buzz_id>\d+)/$', views.show_buzz, name="show_buzz"),
    url(r'^buzzes/(?P<buzz_id>\d+)/edit/$', views.edit_buzz, name="edit_buzz"),
    url(r'^buzzes/list/published/$', views.buzzes_list, {"list_filter": views.ACTIVE}, name="buzzes_list_published"),
    url(r'^buzzes/list/upcoming/$', views.buzzes_list, {"list_filter": views.UPCOMING}, name="buzzes_list_upcoming"),

    # Polls
    url(r'^(?P<poll_type>\w+)/$', views.polls_home, name="polls_home"),
    url(r'^(?P<poll_type>\w+)/list/active/$', views.polls_list, {"filter": views.ACTIVE}, name="polls_list_active"),
    url(r'^(?P<poll_type>\w+)/list/upcoming/$', views.polls_list, {"filter": views.UPCOMING}, name="polls_list_upcoming"),
    url(r'^(?P<poll_type>\w+)/list/past/$', views.polls_list, {"filter": views.PAST}, name="polls_list_past"),
    url(r'^(?P<poll_type>\w+)/add/$', views.add_poll, name="add_poll"),
    url(r'^(?P<poll_type>\w+)/(?P<poll_id>\d+)/$', views.show_poll, name="show_poll"),
    url(r'^(?P<poll_type>\w+)/(?P<poll_id>\d+)/edit/$', views.edit_poll, name="edit_poll"),
    url(r'^(?P<poll_type>\w+)/(?P<poll_id>\d+)/delete/$', views.delete_poll, name="delete_poll"),
    url(r'^(?P<poll_type>\w+)/(?P<poll_id>\d+)/comment/$', views.poll_comment, name="poll_comment"),
    url(r'^(?P<poll_type>\w+)/(?P<poll_id>\d+)/deletecomment/$', views.delete_poll_comment, name="delete_poll_comment"),
    url(r'^(?P<poll_type>\w+)/(?P<poll_id>\d+)/results/$', views.poll_results, name="poll_results"),
    url(r'^(?P<poll_type>\w+)/suggest/$', views.suggest_poll, name="suggest_poll"),

    # Buzz

)
