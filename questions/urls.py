from django.conf.urls import patterns, url,include
from questions import views

urlpatterns = patterns('',
                       url(r'^NewGame/$', views.game_home, name='game_home'),
                       url(r'^NewGame/start/', views.toggle_new_game,name='toggle_new_game'),
                       url(r'^NewGame/answer/', views.toggle_right_answer, name='toggle_right_answer'),
                       )
