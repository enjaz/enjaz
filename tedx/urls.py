from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^$', views.handle_registration, name='handle_registration'),
    url(r'^thanks/$', TemplateView.as_view(template_name='tedx/thanks.html'), name="thanks"),
    url(r'^list/$', views.list_registration, name='list_registration'),

]
