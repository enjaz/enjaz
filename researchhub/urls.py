from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from researchhub import views

urlpatterns = patterns('',
    url(r'^$', views.index, name="index"),
    url(r'^indicators/$', views.indicators, name="indicators"),
    url(r'^faq/$', TemplateView.as_view(template_name='researchhub/faq.html'), name="faq"),
    url(r'^how_it_works/$', TemplateView.as_view(template_name='researchhub/how_it_works.html'), name="how_it_works"),

    # Projects
    url(r'^projects/$', views.list_projects, name="list_projects"),
    url(r'^projects/control/$', views.control_projects, name="control_projects"),
    url(r'^projects/add/intro/$', TemplateView.as_view(template_name='researchhub/add_project_introduction.html'), name="add_project_introduction"),
    url(r'^projects/add/$', views.add_project, name="add_project"),
    url(r'^projects/(?P<pk>\d+)/$', views.show_project, name="show_project"),
    url(r'^projects/(?P<pk>\d+)/edit/$', views.edit_project, name="edit_project"),
    url(r'^projects/(?P<pk>\d+)/delete/$', views.delete_project, name="delete_project"),

    # Supervisors
    url(r'^supervisors/$', views.list_supervisors, name="list_supervisors"),
    url(r'^supervisors/control/$', views.control_supervisors, name="control_supervisors"),
    url(r'^supervisors/signup/$', views.signup_supervisor, name="signup_supervisor"),
    url(r'^supervisors/signup/thanks/$', TemplateView.as_view(template_name='researchhub/signup_supervisor_thanks.html'), name="signup_supervisor_thanks"),
    url(r'^supervisors/add/$', views.add_supervisor, name="add_supervisor"),
    url(r'^supervisors/(?P<pk>\d+)/$', views.show_supervisor, name="show_supervisor"),
    url(r'^supervisors/(?P<pk>\d+)/rate/$', views.rate_supervisor, name="rate_supervisor"),
    url(r'^supervisors/(?P<pk>\d+)/edit/$', views.edit_supervisor, name="edit_supervisor"),
    url(r'^supervisors/(?P<pk>\d+)/delete/$', views.delete_supervisor, name="delete_supervisor"),

    # Skills
    url(r'^skills/$', views.list_skills, name="list_skills"),
    url(r'^skills/add/$', views.add_skill, name="add_skill"),
    url(r'^skills/add/intro/$', TemplateView.as_view(template_name='researchhub/add_skill_introduction.html'), name="add_skill_introduction"),
    url(r'^skills/(?P<pk>\d+)/$', views.show_skill, name="show_skill"),
    url(r'^skills/(?P<pk>\d+)/edit/$', views.edit_skill, name="edit_skill"),
    url(r'^skills/(?P<pk>\d+)/delete/$', views.delete_skill, name="delete_skill"),
)
