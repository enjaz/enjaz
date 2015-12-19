from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from hpc import views

urlpatterns = patterns('',
    url(r'^abstracts/$', views.submit_abstract, name="submit_abstract"),
    url(r'^abstracts/list/$', views.list_abstracts, name="list_abstracts"),
    url(r'^abstracts/show/(?P<pk>\d+)/$', views.show_abstract, name="show_abstract"),
    url(r'^abstracts/thanks/$', TemplateView.as_view(template_name='hpc/abstract_submission_completed.html'), name="abstract_submision_completed"),
)
