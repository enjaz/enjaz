from django.conf.urls import url, include
from django.http import HttpResponse
from . import views

urlpatterns = [
    # Index Pages
    url(r'^riyadh/ar/$', views.riy_ar_index, name="riy_ar_index"),
    url(r'^riyadh/en/$', views.riy_en_index, name="riy_en_index"),
    # Research Guidelines
    url(r'^riyadh/en/research$', views.riy_en_research, name="riy_en_research"),
    url(r'^jeddah/en/research$', views.jed_en_research, name="jed_en_research"),
    url(r'^alahsa/en/research$', views.ahs_en_research, name="ahs_en_research"),
    # About Pages
    url(r'^riyadh/(?P<lang>(ar|en))/about$', views.show_about, name="riy_about"),
    # FAQ-Related Pages
    url(r'^general/FAQ/category/add$', views.add_FaqCategory, name="add_faq_category"),
    url(r'^general/FAQ/question/add$', views.add_FaqQuestion, name="add_faq_question"),
    url(r'^(?P<lang>(ar|en))/general/FAQ/list/$', views.list_FAQs, name="list_faqs"),
    # Previous Versions-Related Pages
    url(r'^riyadh/ar/previous_versions/$', views.list_prev_versions, name="list_prev_versions"),
    url(r'^riyadh/ar/previous_versions/(?P<version_year>\d+)/$', views.show_version, name="show_version"),
    url(r'^riyadh/ar/previous_versions/(?P<version_year>\d+)/speakers/$', views.show_speakers, name="show_speakers"),
    url(r'^riyadh/en/previous_versions/admin/$', views.admin_prev_versions, name="admin_prev_versions"),
    url(r'^riyadh/en/previous_versions/version/add/$', views.add_prev_version, name="add_version"),
    url(r'^riyadh/en/previous_versions/leader/add/$', views.add_leader, name="add_leader"),
    url(r'^riyadh/en/previous_versions/media_sponsor/add/$', views.add_media_sponsor, name="add_sponsor"),
    url(r'^riyadh/en/previous_versions/statistic/add/$', views.add_prev_statistic, name="add_statistic"),
    url(r'^riyadh/en/previous_versions/winner/add/$', views.add_winner, name="add_winner"),
    # Media Center
    url(r'^riyadh/(?P<lang>(ar|en))/media/$', views.main_media, name="riy_media"),
    url(r'^riyadh/(?P<lang>(ar|en))/media/show_post/(?P<post_id>\d+)$', views.show_post, name="riy_show_post"),
    # Newsletter
    url(r'^riyadh/administrative/media/newsletter/members/list/$', views.list_newsletter_members, name="riy_list_members"),
    url(r'^riyadh/media/newsletter/signup/$', views.handle_newsletter_signup, name="handle_newsletter_signup"),
]

