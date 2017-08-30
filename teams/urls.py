from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required
from teams import views as teams_views

urlpatterns = [
    url(r'^$', teams_views.ListView.as_view(), name='list_teams'),
    url(r'^create/$', login_required(teams_views.CreateView.as_view()), name='create'),
    url(r'^(?P<code_name>[\d\w_\-]+)/$', login_required(teams_views.DetailView.as_view()), name='show'),
    url(r'^(?P<year>\d{4})/(?P<code_name>[\d\w_\-]+)/$', login_required(teams_views.ArchiveDetailView.as_view()), name='archive'),
    url(r'^(?P<code_name>[\d\w_\-]+)/edit/$', login_required(teams_views.UpdateView.as_view()), name='edit'),
    url(r'^(?P<code_name>[\d\w_\-]+)/send_email', teams_views.send_email, name='send_email'),
    url(r'^(?P<code_name>[\d\w_\-]+)/ajax/add', teams_views.add_members, name='add_members'),
    url(r'^(?P<code_name>[\d\w_\-]+)/ajax/open_close', teams_views.control_registration, name='control_registration'),


]
