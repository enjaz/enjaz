from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from . import views

urlpatterns = patterns('',
        url(r'^$',views.index,{'massage': 'no'},name='index'),
        url(r'^massage/(?P<massage>\w+)$',views.index,name='massage'),

        url(r'^coordinator/$', views.coordinator_page,name='coordinator_page'),
        url(r'^coordinator/search/$', views.search_ajax, name='search_ajax'),
        url(r'^coordinator/members/$', views.members_list, name='members_list'),
        url(r'^coordinator/(?P<pk>\d+)/add/$', views.add_team, name="add_team"),
        url(r'^coordinator/(?P<pk>\d+)/remove/$', views.remove_team, name="add_remove"),



        url(r'^project/(?P<pk>\d+)/$',views.project,{'massage': 'no'},name='project'),
        url(r'^project/(?P<pk>\d+)/(?P<massage>\w+)$',views.project,name='project_massage'),
        url(r'^projects/add/intro/$', TemplateView.as_view(template_name='matching_program/add_project_introduction.html'), name="add_project_introduction"),
        url(r'^projects/add/$', views.add_project, name="add_project"),
        url(r'^project/(?P<pk>\d+)/edit/$',views.edit_project,name='edit_project'),
        url(r'^project/(?P<pk>\d+)/delete/$',views.delete_project, name='delete_project' ),
        url(r'^project/(?P<proj_pk>\d+)/remove_member/(?P<stu_pk>\d+)/$', views.remove_member, name='remove_member'),
                       
        url(r'^studentapplication/(?P<pk>\d+)/$',views.student_app, name='application'),
        url(r'^studentapplication/add/intro/$', TemplateView.as_view(template_name='matching_program/add_student_app_introduction.html'), name='add_student_app_introduction'),
        url(r'^studentapplication/project/(?P<pk>\d+)/add/$', views.add_student_app, name='add_student_app'),
        url(r'^studentapplication/(?P<pk>\d+)/edit/$',views.edit_app, name='edit_app'),
        url(r'^studentapplication/(?P<pk>\d+)/delete/$', views.delete_app, name='delete_app'),
        url(r'^studentapplication/(?P<pk>\d+)/add_member/$', views.add_member, name='add_member'),
    
)
