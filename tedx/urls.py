from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^$', views.handle_registration, name='handle_registration'),
    url(r'^thanks/$', TemplateView.as_view(template_name='tedx/thanks.html'), name="thanks"),
    url(r'^list/$', views.list_registration, name='list_registration'),
    url("^game/$", views.handle_game_index, name="handle_game_index"),
    url("^game/ajax/$", views.handle_game_ajax, name="handle_game_ajax"),
]
