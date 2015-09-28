from django.conf.urls import patterns, url
from bulb import views

urlpatterns = patterns('',
    url(r'^$', views.index, name="index"),

    # Books exchange
    url(r'^exchange/$', views.list_book_categories, name="list_book_categories"),
    url(r'^exchange/category/(?P<code_name>[\w_]+)/$', views.show_category, name="show_category"),
    url(r'^exchange/books/list/(?P<source>(?:user|category))/(?P<name>[\d\w_]+)/$', views.list_book_previews, name="list_book_previews"),
    url(r'^exchange/books/add/$', views.add_book, name="add_book"),
    url(r'^exchange/my_books/$', views.my_books, name="my_books"),
    url(r'^exchange/report/$', views.student_report, name='student_report'),
    url(r'^exchange/report/(?P<username>[\w\d]+)/$', views.student_report, name='student_report_with_username'),
    url(r'^exchange/my_requests/$', views.requests_by_me, name="requests_by_me"),
    url(r'^exchange/indirect_requests/$', views.indirect_requests, name="indirect_requests"),
    url(r'^exchange/books/order/$', views.order_instructions, name="order_instructions"),
    url(r'^exchange/books/(?P<pk>\d+)/$', views.show_book, name="show_book"),
    url(r'^exchange/books/(?P<pk>\d+)/edit/$', views.edit_book, name="edit_book"),
    url(r'^exchange/ajax/control_book$', views.control_book, name="control_book"),
    url(r'^exchange/ajax/pending_book$', views.pending_book, name="pending_book"),
    url(r'^exchange/ajax/pending_request$', views.pending_request, name="pending_request"),
    url(r'^exchange/ajax/list_indirect_requests$', views.list_indirect_requests, name="list_indirect_requests"),
    url(r'^exchange/ajax/list_my_pending_books$', views.list_my_pending_books, name="list_my_pending_books"),
    url(r'^exchange/ajax/list_my_pending_requests$', views.list_my_pending_requests, name="list_my_pending_requests"),
    url(r'^exchange/ajax/control_request$', views.control_request, name="control_request"),
)
