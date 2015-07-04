from django.conf.urls import url, patterns
from rest_framework.routers import DefaultRouter
from api import views

# router = DefaultRouter()
# router.register(r'activities', views.ActivityViewSet)
# router.urls

urlpatterns = patterns('',
    url(r'^(?P<version>v1)/activities/$', views.ActivityList.as_view(), name='activity-list'),
    url(r'^(?P<version>v1)/activities/(?P<pk>\d+)/$', views.ActivityDetail.as_view(), name='activity-detail'),
    url(r'^(?P<version>v1)/clubs/$', views.ClubList.as_view(), name='club-list'),
    url(r'^(?P<version>v1)/clubs/(?P<pk>\d+)/$', views.ClubDetail.as_view(), name='club-detail'),
)
