from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from bulb import views
from bulb.models import Book, NeededBook
from tagging.views import TaggedObjectList

urlpatterns = patterns('',
    url(r'^$', views.index, name="index"),
    url(r'^indicators/(?:(?P<city>\w)/)?$', views.indicators, name="indicators"),
    url(r'^join_us/$', views.handle_recruitment, name="handle_recruitment"),
    url(r'^join_us/thanks/$', TemplateView.as_view(template_name='bulb/recruitment_thanks.html'), name="recruitment_thanks"),
    url(r'^bulb-user-autocomplete/$', views.BulbUserAutocomplete.as_view(), name='bulb-user-autocomplete',),

    # Books exchange
    url(r'^exchange/$', views.list_book_categories, name="list_book_categories"),
    url(r'^exchange/search/$', views.search_books, name="search_books"),
    url(r'^exchange/tags/$', TemplateView.as_view(template_name='bulb/exchange/list_tags.html'), name='list_book_tags'),
    url(r'^exchange/tags/(?P<tag>.+(?u))/$', TaggedObjectList.as_view(model=Book, template_name="bulb/exchange/show_tag.html", context_object_name="books"), name='show_tag'),
    url(r'^exchange/needed/$', views.list_needed_book_categories, name="list_needed_book_categories"),
    url(r'^exchange/needed/add/$', views.add_needed_book, name="add_needed_book"),
    url(r'^exchange/needed/add/intro/$', TemplateView.as_view(template_name='bulb/exchange/add_needed_book_introduction.html'), name="add_needed_book_introduction"),
    url(r'^exchange/needed/(?P<pk>\d+)/$', views.show_needed_book, name="show_needed_book"),
    url(r'^exchange/needed/(?P<pk>\d+)/edit/$', views.edit_needed_book, name="edit_needed_book"),
    url(r'^exchange/needed/(?P<pk>\d+)/delete/$', views.delete_needed_book, name="delete_needed_book"),
    url(r'^exchange/needed/(?P<pk>\d+)/delete/confirm/$', views.confirm_needed_book_deletion, name="confirm_needed_book_deletion"),
    url(r'^exchange/needed/category/(?P<code_name>[\w_]+)/$', views.show_category, {'needed': True}, name="show_needed_category"),
    url(r'^exchange/needed/tags/$', TemplateView.as_view(template_name='bulb/exchange/list_needed_tags.html'), name='list_needed_book_tags'),
    url(r'^exchange/needed/tags/(?P<tag>.+(?u))/$', TaggedObjectList.as_view(model=NeededBook, template_name="bulb/exchange/show_needed_tag.html", context_object_name="needed_books"), name='show_needed_tag'),
    url(r'^exchange/needed/list/(?P<source>(?:user|category))/(?P<name>[\d\w_]+)/$', views.list_needed_book_previews, name="list_needed_book_previews"),
    url(r'^exchange/category/(?P<code_name>[\w_]+)/$', views.show_category, name="show_category"),
    url(r'^exchange/books/by_date/$', views.books_by_date, name="books_by_date"),
    url(r'^exchange/books/list/(?P<source>(?:user|category))/(?P<name>[\d\w_]+)/$', views.list_book_previews, name="list_book_previews"),
    url(r'^exchange/books/add/intro/$', TemplateView.as_view(template_name='bulb/exchange/add_book_introduction.html'), name="add_book_introduction"),
    url(r'^exchange/books/add/(?P<contribution>(?:lend|give))/$', views.add_book, name="add_book"),
    url(r'^exchange/my_books/$', views.my_books, name="my_books"),
    url(r'^exchange/report/$', views.student_report, name='student_report'),
    url(r'^exchange/report/convert$', views.convert_balance, name='convert_balance'),
    url(r'^exchange/report/(?P<username>[\.\w\d\-]+)/$', views.student_report, name='student_report_with_username'),
    url(r'^exchange/my_requests/$', views.requests_by_me, name="requests_by_me"),
    url(r'^exchange/indirect_requests/$', views.indirect_requests, name="indirect_requests"),
    url(r'^exchange/books/(?P<pk>\d+)/$', views.show_book, name="show_book"),
    url(r'^exchange/books/(?P<pk>\d+)/order/$', views.order_instructions, name="order_instructions"),
    url(r'^exchange/books/(?P<pk>\d+)/order/confirm/$', views.confirm_book_order, name="confirm_book_order"),
    url(r'^exchange/books/(?P<pk>\d+)/edit/$', views.edit_book, name="edit_book"),
    url(r'^exchange/books/(?P<pk>\d+)/delete/$', views.delete_book, name="delete_book"),
    url(r'^exchange/books/(?P<pk>\d+)/delete/confirm/$', views.confirm_book_deletion, name="confirm_book_deletion"),
    url(r'^exchange/ajax/pending_book$', views.pending_book, name="pending_book"),
    url(r'^exchange/ajax/pending_request$', views.pending_request, name="pending_request"),
    url(r'^exchange/ajax/list_indirect_requests$', views.list_indirect_requests, name="list_indirect_requests"),
    url(r'^exchange/ajax/list_my_requests$', views.list_my_requests, name="list_my_requests"),
    url(r'^exchange/ajax/list_my_books$', views.list_my_books, name="list_my_books"),
    url(r'^exchange/ajax/control_request$', views.control_request, name="control_request"),

    # Reading Groups
    url(r'^groups/$', views.list_groups, name="list_groups"),
    url(r'^groups/archived/$', views.list_groups, {'archived': True}, name="list_archived_groups"),
    url(r'^groups/sessions/$', views.list_sessions, name="list_sessions"),
    url(r'^groups/previews/$', views.list_group_previews, name="list_group_previews"),
    url(r'^groups/previews/archived/$', views.list_group_previews, {'archived': True}, name="list_archived_group_previews"),
    url(r'^groups/add/$', views.add_group, name="add_group"),
    url(r'^groups/add/introduction/$', TemplateView.as_view(template_name='bulb/groups/add_group_introduction.html'), name="add_group_introduction"),
    url(r'^groups/add/thanks/$', TemplateView.as_view(template_name='bulb/groups/add_group_thanks.html'), name="add_group_thanks"),
    url(r'^groups/(?P<group_pk>\d+)/$', views.show_group, name='show_group'),
    url(r'^groups/(?P<group_pk>\d+)/welcome/$', views.new_member_introduction, name='new_member_introduction'),
    url(r'^groups/(?P<group_pk>\d+)/memberships/$', views.list_memberships, name='list_memberships'),
    url(r'^groups/(?P<group_pk>\d+)/edit/$', views.edit_group, name='edit_group'),
    url(r'^groups/(?P<group_pk>\d+)/delete/$', views.delete_group, name='delete_group'),
    url(r'^groups/(?P<group_pk>\d+)/sessions/add/$', views.add_group_session, name='add_group_session'),
    url(r'^groups/(?P<group_pk>\d+)/sessions/add/introduction/$', TemplateView.as_view(template_name='bulb/groups/add_group_session_introduction.html'),
        name='add_group_session_introduction'),
    url(r'^groups/(?:(?P<group_pk>\d+)/)?sessions/(?P<session_pk>\d+)/edit/$', views.edit_session, name='edit_session'),
    url(r'^groups/(?:(?P<group_pk>\d+)/)?sessions/(?P<session_pk>\d+)/delete/$', views.delete_session, name='delete_session'),
    url(r'^groups/(?:(?P<group_pk>\d+)/)?sessions/(?P<session_pk>\d+)/report/$', views.show_report, name='show_report'),
    url(r'^groups/(?:(?P<group_pk>\d+)/)?sessions/(?P<session_pk>\d+)/report/add/$', views.add_report, name='add_report'),
    url(r'^groups/(?:(?P<group_pk>\d+)/)?sessions/(?P<session_pk>\d+)/report/edit/$', views.edit_report, name='edit_report'),
    url(r'^groups/sessions/add/$', views.add_free_session, name='add_free_session'),
    url(r'^groups/sessions/add/introduction/$', TemplateView.as_view(template_name='bulb/groups/add_free_session_introduction.html'), name='add_free_session_introduction'),
    url(r'^groups/sessions/(?P<session_pk>\d+)/$', views.show_session, name='show_session'),
    url(r'^groups/ajax/group$', views.control_group, name="control_group"),
    url(r'^groups/ajax/session$', views.toggle_session_confirmation, name="toggle_session_confirmation"),
    
    # Readers
    url(r'^readers/$', views.list_reader_profiles, name="list_reader_profiles"),
    url(r'^readers/search/$', views.search_readers, name="search_readers"),
    url(r'^readers/add/$', views.add_reader_profile, name="add_reader_profile"),
    url(r'^readers/add/introduction/$', TemplateView.as_view(template_name='bulb/readers/add_reader_profile_introduction.html'),
        name="add_reader_profile_introduction"),
    url(r'^readers/(?P<reader_pk>\d+)/$', views.show_reader_profile, name='show_reader_profile'),
    url(r'^readers/(?P<reader_pk>\d+)/edit/$', views.edit_reader_profile, name='edit_reader_profile'),
)
