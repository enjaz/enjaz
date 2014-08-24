from django.conf.urls import patterns, url
from media import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^activities/$', views.list_activities, name="list_activities"),

    # Reports
    url(r'^activities/reports/$', views.list_reports, name="list_reports"),
    url(r'^activities/reports/(?P<episode_pk>\d+)/submit/$', views.submit_report, name="submit_report"),
    url(r'^activities/reports/(?P<episode_pk>\d+)/$', views.show_report, name="show_report"),

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
)