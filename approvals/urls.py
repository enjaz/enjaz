from django.conf.urls import url
from approvals import views

app_name = 'approvals'

urlpatterns = [
    url(r'^activities/new/$', views.SubmitActivityCreateRequest.as_view(), name='submit-activity-create-request'),
    url(r'^activities/$', views.ActivityRequestList.as_view(), name='request-list'),
    url(r'^activities/(?P<pk>\d+)/$', views.RequestThreadDetail.as_view(), name='requestthread-detail'),
]
