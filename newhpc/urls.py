from django.conf.urls import url, include
from django.http import HttpResponse
from . import views

urlpatterns = [
    url(r'^$', views.test, name="index"),
]

