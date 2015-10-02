from django.conf.urls import patterns, url
from django.views.generic import TemplateView
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

    # Reading Groups
    url(r'^groups/$', views.list_groups, name="list_groups"),
    url(r'^groups/previews/$', views.list_group_previews, name="list_group_previews"),
    url(r'^groups/add/$', views.add_group, name="add_group"),
    url(r'^groups/add/introduction/$', TemplateView.as_view(template_name='bulb/groups/add_group_introduction.html'), name="add_group_introduction"),
    url(r'^groups/add/thanks/$', TemplateView.as_view(template_name='bulb/groups/add_group_thanks.html'), name="add_group_thanks"),
    url(r'^groups/(?P<group_pk>\d+)/$', views.show_group, name='show_group'),
    url(r'^groups/(?P<group_pk>\d+)/welcome/$', views.new_member_introduction, name='new_member_introduction'),
    url(r'^groups/(?P<group_pk>\d+)/memberships/$', views.list_memberships, name='list_memberships'),
    url(r'^groups/(?P<group_pk>\d+)/edit/$', views.edit_group, name='edit_group'),
    url(r'^groups/(?P<group_pk>\d+)/delete/$', views.delete_group, name='delete_group'),
    url(r'^groups/(?P<group_pk>\d+)/session/add/$', views.add_session, name='add_session'),
    url(r'^groups/(?P<group_pk>\d+)/session/add/introduction/$', TemplateView.as_view(template_name='bulb/groups/add_session_introduction.html'),
        name='add_session_introduction'),
    url(r'^groups/(?P<group_pk>\d+)/session/(?P<session_pk>\d+)/edit/$', views.edit_session, name='edit_session'),
    url(r'^groups/(?P<group_pk>\d+)/session/(?P<session_pk>\d+)/add_report/$', views.add_report, name='add_report'),
    url(r'^groups/(?P<group_pk>\d+)/session/(?P<session_pk>\d+)/delete/$', views.delete_session, name='delete_session'),
    url(r'^groups/(?P<group_pk>\d+)/session/(?P<session_pk>\d+)/edit_report/$', views.edit_report, name='edit_report'),
    url(r'^groups/ajax/membership$', views.control_membership, name="control_membership"),

    # Readers
    url(r'^readers/$', views.list_reader_profiles, name="list_reader_profiles"),
    url(r'^readers/add/$', views.add_reader_profile, name="add_reader_profile"),
    url(r'^readers/add/introduction/$', TemplateView.as_view(template_name='bulb/readers/add_reader_profile_introduction.html'),
        name="add_reader_profile_introduction"),
    url(r'^readers/(?P<reader_pk>\d+)/$', views.show_reader_profile, name='show_reader_profile'),
    url(r'^readers/(?P<reader_pk>\d+)/edit/$', views.edit_reader_profile, name='edit_reader_profile'),
)
