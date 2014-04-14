from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from books import views

urlpatterns = patterns('',
    url(r'^$', views.list_books, name='list'),
    url(r'^contribute/$', views.contribute, name='contribute'),
    url(r'^(?P<book_id>\d+)/$', views.show, name='show'),
    url(r'^(?P<book_id>\d+)/edit/$', views.edit, name='edit'),
    url(r'^(?P<book_id>\d+)/borrow/$', views.borrow, name='borrow'),
    url(r'^(?P<book_id>\d+)/withdraw/$', views.withdraw, name='withdraw'),
    url(r'^review_requests/$', views.review_requests, name='review_requests'),
    url(r'^my_requests/$', views.my_requests, name='my_requests'),
)
