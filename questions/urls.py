from django.conf.urls import patterns, url,include
from questions import views

urlpatterns = patterns('',
                       url(r'^$', views.show_game, name='show_game'),
                       url(r'^start/$', views.start_new_game,name='start_new_game'),
                       url(r'^answer/$', views.check_answer, name='check_answer'),
                       url(r'^scores/$', views.show_scores, name='show_scores'),

                       )
