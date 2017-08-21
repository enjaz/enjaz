from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required
from teams import views as teams_views

urlpatterns = [
    url(r'^$', teams_views.ListView.as_view(), name='list_teams'),
    url(r'^create/$', login_required(teams_views.CreateView.as_view()), name='create'),
    url(r'^(?P<team_id>\d+)/$', teams_views.DetailView.as_view(), name='show'),
    url(r'^(?P<team_id>\d+)/edit/$', login_required(teams_views.UpdateView.as_view()), name='edit'),
    url(r'^(?P<team_id>\d+)/send_email', teams_views.send_email, name='send_email'),
    url(r'^(?P<team_id>\d+)/ajax/add', teams_views.add_members, name='add_members'),
]
