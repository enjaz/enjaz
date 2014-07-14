from django.conf.urls import patterns, url
from media import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^activities/$', views.list_activities, name="list_activities"),
    url(r'^activities/reports/$', views.list_reports, name="list_reports"),
    url(r'^activities/reports/(?P<episode_pk>\d+)/submit/$', views.submit_report, name="submit_report"),
    url(r'^activities/reports/(?P<episode_pk>\d+)/$', views.show_report, name="show_report"),
    url(r'^activities/stories/(?P<episode_pk>\d+)/create/$', views.create_story, name="create_story"),
    url(r'^activities/stories/(?P<episode_pk>\d+)/$', views.show_story, name="show_story"),
    url(r'^activities/stories/(?P<episode_pk>\d+)/edit/$', views.edit_story, name="edit_story"),
    url(r'^activities/stories/(?P<episode_pk>\d+)/assign/$', views.assign_story_task, name="assign_story_task"),
)