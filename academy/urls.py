from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^(?P<position>(instructor|graduate))/(?P<person_id>\d+)/$',
        views.show_person, name="show_person"),
    url(r'^about/$',
        TemplateView.as_view(template_name='academy/about.html'),
        name='about'),
    url(r'^(?P<course_name>\w+)/$',views.show_course, name='show'),
    url(r'^(?P<course_name>\w+)/register/$',views.register_for_course,
        name='register'),
]

#delete these when fobi works -soon hopefully >_< -

# Academy Forms URLS
# Due to restrictions of django-pluggable-forms, the url confs for the app's instances have to be placed
# in the project's main URLconf, yet to prevent cluttering due to the many customization options, the url
# function is placed here and then imported into the main URLconf
academy_forms_urls = url(r'^academy/(?P<object_id>\d+)/forms/',
        include('forms_builder.wrapper.urls', namespace="academy_forms",
                app_name="forms"),)

