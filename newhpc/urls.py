from django.conf.urls import url, include
from django.http import HttpResponse
from . import views

urlpatterns = [
    #url(r'^riyadh/ar/$', views.riy_ar_index, name="riy_ar_index"),
    #url(r'^riyadh/en/$', views.riy_en_index, name="riy_en_index"),
    url(r'^riyadh/en/research$', views.riy_en_research, name="riy_en_research"),
    url(r'^riyadh/(?P<lang>(ar|en))/general/about$', views.show_about, name="riy_about"),
    url(r'^general/FAQ/category/add$', views.add_FaqCategory, name="add_faq_category"),
    url(r'^general/FAQ/question/add$', views.add_FaqQuestion, name="add_faq_question"),

]

