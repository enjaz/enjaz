from django.conf.urls import url
from approvals import views

app_name = 'approvals'

urlpatterns = [
    url(r'^activities/new/$', views.SubmitActivityCreateRequest.as_view(), name='submit-activity-create-request'),
    url(r'^activities/$', views.RequestThreadList.as_view(), name='requestthread-list'),
    url(r'^activities/(?P<pk>\d+)/$', views.RequestThreadDetail.as_view(), name='requestthread-detail'),
    url(r'^activities/(?P<pk>\d+)/comment/$', views.HandleActivityRequestCommentForm.as_view(), name='requestthread-comment'),
    url(r'^activities/(?P<pk>\d+)/review/$', views.HandleActivityRequestReviewForm.as_view(), name='requestthread-review'),
]
