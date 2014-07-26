# -*- coding: utf-8  -*-
"""
Tests of the articles part of the media app.
"""
from django.test import TestCase
from django.core.urlresolvers import reverse

from media.models import Article

from accounts.test_utils import create_user
from media.test_utils import media_center_head, media_center_member, create_articles


def classic_setup(instance):
    instance.coordinator = media_center_head(create_user())
    instance.member = media_center_member(create_user())
    instance.user1 = create_user()
    instance.user2 = create_user()

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