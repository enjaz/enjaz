from django.conf.urls import url
from . import views as teams_views

urlpatterns = [
    url(r'^list/$', teams_views.list_teams, name='list_teams'),
    url(r'^create/$', teams_views.create, name='create'),
    url(r'^(?P<team_id>\d+)/infocard/$', teams_views.show_info, name='show_info'),
    url(r'^(?P<team_id>\d+)/$', teams_views.show, name='show'),
    url(r'^(?P<team_id>\d+)/edit/$', teams_views.edit, name='edit'),
]
