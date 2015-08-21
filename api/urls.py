from django.conf.urls import url, patterns
from rest_framework.routers import DefaultRouter
from api import views

urlpatterns = patterns('',
    url(r'^v1/api-token-auth/', views.ObtainAuthToken.as_view()),
    url(r'^(?P<version>v1)/activities/$', views.ActivityList.as_view(), name='activity-list'),
    url(r'^(?P<version>v1)/activities/(?P<pk>\d+)/$', views.ActivityDetail.as_view(), name='activity-detail'),
    url(r'^(?P<version>v1)/clubs/$', views.ClubList.as_view(), name='club-list'),
    url(r'^(?P<version>v1)/clubs/(?P<pk>\d+)/$', views.ClubDetail.as_view(), name='club-detail'),
    url(r'^(?P<version>v1)/buzzes/$', views.BuzzList.as_view(), name='buzz-list'),
    url(r'^(?P<version>v1)/buzzes/(?P<buzz_pk>\d+)/views/$', views.BuzzViewCreate.as_view(), name='buzzview-create'),
    url(r'^(?P<version>v1)/buzzes/(?P<buzz_pk>\d+)/views/(?P<pk>\d+)/$', views.BuzzViewUpdate.as_view(), name='buzzview-update'),
    url(r'^(?P<version>v1)/niqati/$', views.CodeList.as_view(), name='code-list'),
    url(r'^v1/niqati/sum/$', views.CodeSum.as_view(), name='code-sum'),
)
