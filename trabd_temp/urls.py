from django.conf.urls import url, include
from django.http import HttpResponse
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^add_nominee/$', views.add_nominee, name="add_nominee"),
    url(r'^add_nominee/thanks/$',
        TemplateView.as_view(template_name='voting/nomination_thanks.html'), name='nomination_thanks'),

]

