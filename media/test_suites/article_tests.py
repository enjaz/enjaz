# -*- coding: utf-8  -*-
"""
Tests of the articles part of the media app.
"""
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.models import User
from clubs.models import Club
from media.models import Article

# --- Helper functions

def classic_setup(instance):
    instance.coordinator = media_center_head(create_user())
    instance.member = media_center_member(create_user())
    instance.user1 = create_user()
    instance.user2 = create_user()

def create_user(username=None, email="test@enjazportal.com", password="12345678"):
    if username == None:
        username = "username" + str(User.objects.count() + 1)
    return User.objects.create_user(username, email, password)

def get_media_center():
    return Club.objects.get(english_name="Media Center")

def media_center_head(user):
    media_center = get_media_center()
    media_center.coordinator = user
    media_center.save()
    return user
    
def media_center_member(user):
    media_center = get_media_center()
    media_center.members.add(user)
    return user

def create_article(author=create_user(),
                   title=("Test Article Title " + str(Article.objects.count() + 1)),
                   text="Test Article Text"):
    return Article.objects.create(author=author,
                                  title=title,
                                  text=text)
    
def create_articles(count):
    for i in range(count):
        create_article()

class ListArticlesViewTests(TestCase):
    fixtures = ['initial_data.json']
    def setUp(self):
        self.coordinator = media_center_head(create_user())
        self.member = media_center_member(create_user())
        self.user1 = create_user()
        self.user2 = create_user()
        create_articles(5)
        
    def tearDown(self):
        self.client.logout()

    def test_list_articles_with_mc_head(self):
        self.client.login(username=self.coordinator.username, password='12345678')
        response = self.client.get(reverse("media:list_articles"))
        
        self.assertTemplateUsed(response, 'media/list_articles.html')
        self.assertEqual(list(response.context['articles']), list(Article.objects.all()))
        self.assertContains(response, u"المقالات")
        self.assertNotContains(response, u"مقالاتي")
    
    def test_list_articles_with_mc_member(self):
        self.client.login(username=self.member.username, password='12345678')
        response = self.client.get(reverse("media:list_articles"))
        
        self.assertTemplateUsed(response, 'media/list_articles.html')
        self.assertEqual(list(response.context['articles']), list(Article.objects.all()))
        self.assertContains(response, u"المقالات")
        self.assertNotContains(response, u"مقالاتي")
        
    def test_list_articles_with_normal_user(self):
        self.client.login(username=self.user1.username, password='12345678')
        response = self.client.get(reverse("media:list_articles"))
        
        self.assertTemplateUsed(response, 'media/list_user_articles.html')
        self.assertEqual(list(response.context['articles']), list(Article.objects.filter(author=self.user1)))
#         self.assertNotContains(response, u"المقالات")
        self.assertContains(response, u"مقالاتي")