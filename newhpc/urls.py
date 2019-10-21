from django.conf.urls import url, include
from django.http import HttpResponse
from . import views

urlpatterns = [
    # Index Pages
    #url(r'^riyadh/ar/$', views.riy_ar_index, name="riy_ar_index"),
    #url(r'^riyadh/en/$', views.riy_en_index, name="riy_en_index"),
    url(r'^riyadh/en/research$', views.riy_en_research, name="riy_en_research"),
    # About Pages
    url(r'^riyadh/(?P<lang>(ar|en))/general/about$', views.show_about, name="riy_about"),
    # FAQ-Related Pages
    url(r'^general/FAQ/category/add$', views.add_FaqCategory, name="add_faq_category"),
    url(r'^general/FAQ/question/add$', views.add_FaqQuestion, name="add_faq_question"),
    url(r'^(?P<lang>(ar|en))/general/FAQ/list$', views.list_FAQs, name="list_faqs"),
    # Previous Versions-Related Pages
    url(r'^riyadh/ar/previous_versions/$', views.list_prev_versions, name="list_prev_versions"),
    url(r'^riyadh/en/previous_versions/(?P<version_id>\d+)$', views.show_prev_version, name="show_prev_version"),
    url(r'^riyadh/en/previous_versions/admin$', views.admin_prev_versions, name="admin_prev_versions"),
    url(r'^riyadh/en/previous_versions/version/add$', views.add_prev_version, name="add_version"),
    url(r'^riyadh/en/previous_versions/leader/add$', views.add_leader, name="add_leader"),
    url(r'^riyadh/en/previous_versions/media_sponsor/add$', views.add_media_sponsor, name="add_sponsor"),
    url(r'^riyadh/en/previous_versions/statistic/add$', views.add_prev_statistic, name="add_statistic"),
    url(r'^riyadh/en/previous_versions/winner/add$', views.add_winner, name="add_winner"),


]

