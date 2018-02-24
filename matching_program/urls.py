from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from . import views

urlpatterns = patterns('',
        url(r'^$',views.index,name='index'),
                       
        url(r'^project/(?P<pk>\d+)/$',views.project,name='project'),
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
