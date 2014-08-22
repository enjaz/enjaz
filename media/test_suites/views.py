# -*- coding: utf-8  -*-
"""
Tests of the articles part of the media app.
"""
from django.test import TestCase
from django.core.urlresolvers import reverse
from activities.test_utils import create_activity
from clubs.models import Club
from clubs.test_utils import set_club_coordinator, add_club_member

from media.models import Article

from accounts.test_utils import create_user
from media.test_utils import media_center_head, media_center_member, create_articles


def classic_setup(instance):
    instance.coordinator = media_center_head(create_user())
    instance.member = media_center_member(create_user())
    instance.user1 = create_user()
    instance.user2 = create_user()

class ListActivitiesViewTests(TestCase):
    fixtures = ['initial_data.json']
    def setUp(self):
        self.user = create_user(username="msarabi")
        self.client.login(username=self.user.username, password='12345678')

    def tearDown(self):
        self.client.logout()

    def test_list_activities_with_superuser(self):
        self.user.is_superuser = True
        self.user.save()
        self.assertTrue(self.user.is_superuser)  # sanity check

        response = self.client.get(reverse('media:list_activities'))
        self.assertEqual(response.status_code, 200)

    def test_list_activities_with_media_coordinator(self):
        media_center_head(self.user)
        response = self.client.get(reverse('media:list_activities'))
        self.assertEqual(response.status_code, 200)

    def test_list_activities_with_media_member(self):
        media_center_member(self.user)
        response = self.client.get(reverse('media:list_activities'))
        self.assertEqual(response.status_code, 200)

    def test_list_activities_with_club_coordinator(self):
        set_club_coordinator(Club.objects.get(pk=1))
        response = self.client.get(reverse('media:list_activities'))
        self.assertEqual(response.status_code, 403)

    def test_list_activities_with_club_member(self):
        add_club_member(Club.objects.get(pk=1))
        response = self.client.get(reverse('media:list_activities'))
        self.assertEqual(response.status_code, 403)

    def test_list_activities_with_normal_user(self):
        response = self.client.get(reverse('media:list_activities'))
        self.assertEqual(response.status_code, 403)

class ListReportsViewTests(TestCase):
    fixtures = ['initial_data.json']
    def setUp(self):
        self.user = create_user(username="msarabi")
        self.client.login(username=self.user.username, password='12345678')

    def tearDown(self):
        self.client.logout()

    def test_list_reports_with_superuser(self):
        self.user.is_superuser = True
        self.user.save()
        self.assertTrue(self.user.is_superuser)  # sanity check

        response = self.client.get(reverse('media:list_reports'))
        self.assertEqual(response.status_code, 200)

    def test_list_reports_with_media_coordinator(self):
        media_center_head(self.user)
        response = self.client.get(reverse('media:list_reports'))
        self.assertEqual(response.status_code, 200)

    def test_list_reports_with_media_member(self):
        media_center_member(self.user)
        response = self.client.get(reverse('media:list_reports'))
        self.assertEqual(response.status_code, 200)

    def test_list_reports_with_club_coordinator(self):
        set_club_coordinator(Club.objects.get(pk=1))
        response = self.client.get(reverse('media:list_reports'))
        self.assertEqual(response.status_code, 403)

    def test_list_reports_with_club_member(self):
        add_club_member(Club.objects.get(pk=1))
        response = self.client.get(reverse('media:list_reports'))
        self.assertEqual(response.status_code, 403)

    def test_list_reports_with_normal_user(self):
        response = self.client.get(reverse('media:list_reports'))
        self.assertEqual(response.status_code, 403)

class SubmitReportViewTests(TestCase):
    fixtures = ['initial_data.json']
    def setUp(self):
        self.user = create_user(username="msarabi")
        self.activity = create_activity(club=Club.objects.get(pk=3))
        self.client.login(username=self.user.username, password='12345678')

    def tearDown(self):
        self.client.logout()

    def test_submit_report_with_superuser(self):
        self.user.is_superuser = True
        self.user.save()
        self.assertTrue(self.user.is_superuser)  # sanity check

        response = self.client.get(reverse('media:submit_report', args=(self.activity.episode_set.first().pk, )))
        self.assertEqual(response.status_code, 200)

    def test_submit_report_with_media_coordinator(self):
        media_center_head(self.user)
        response = self.client.get(reverse('media:submit_report', args=(self.activity.episode_set.first().pk, )))
        self.assertEqual(response.status_code, 403)

    def test_submit_report_with_media_member(self):
        media_center_member(self.user)
        response = self.client.get(reverse('media:submit_report', args=(self.activity.episode_set.first().pk, )))
        self.assertEqual(response.status_code, 403)

    def test_submit_report_with_club_coordinator(self):
        set_club_coordinator(Club.objects.get(pk=3))
        response = self.client.get(reverse('media:submit_report', args=(self.activity.episode_set.first().pk, )))
        self.assertEqual(response.status_code, 200)

    def test_submit_report_with_club_member(self):
        add_club_member(Club.objects.get(pk=1))
        response = self.client.get(reverse('media:submit_report', args=(self.activity.episode_set.first().pk, )))
        self.assertEqual(response.status_code, 403)

    def test_submit_report_with_normal_user(self):
        response = self.client.get(reverse('media:submit_report', args=(self.activity.episode_set.first().pk, )))
        self.assertEqual(response.status_code, 403)

class ShowReportViewTests(TestCase):
    fixtures = ['initial_data.json']
    def setUp(self):
        self.user = create_user(username="msarabi")
        self.activity = create_activity(club=Club.objects.get(pk=3))
        self.client.login(username=self.user.username, password='12345678')

    def tearDown(self):
        self.client.logout()

    def test_submit_report_with_superuser(self):
        self.user.is_superuser = True
        self.user.save()
        self.assertTrue(self.user.is_superuser)  # sanity check

        response = self.client.get(reverse('media:submit_report', args=(self.activity.episode_set.first().pk, )))
        self.assertEqual(response.status_code, 200)

    def test_submit_report_with_media_coordinator(self):
        media_center_head(self.user)
        response = self.client.get(reverse('media:submit_report', args=(self.activity.episode_set.first().pk, )))
        self.assertEqual(response.status_code, 200)

    def test_submit_report_with_media_member(self):
        media_center_member(self.user)
        response = self.client.get(reverse('media:submit_report', args=(self.activity.episode_set.first().pk, )))
        self.assertEqual(response.status_code, 200)

    def test_submit_report_with_club_coordinator(self):
        set_club_coordinator(Club.objects.get(pk=3))
        response = self.client.get(reverse('media:submit_report', args=(self.activity.episode_set.first().pk, )))
        self.assertEqual(response.status_code, 200)

    def test_submit_report_with_club_member(self):
        add_club_member(Club.objects.get(pk=1))
        response = self.client.get(reverse('media:submit_report', args=(self.activity.episode_set.first().pk, )))
        self.assertEqual(response.status_code, 200)

    def test_submit_report_with_normal_user(self):
        response = self.client.get(reverse('media:submit_report', args=(self.activity.episode_set.first().pk, )))
        self.assertEqual(response.status_code, 403)

class ListArticlesViewTests(TestCase):
    fixtures = ['initial_data.json']
    def setUp(self):
        self.coordinator = media_center_head(create_user(username='msarabi'))
        self.member = media_center_member(create_user())
        self.user1 = create_user()
        self.user2 = create_user()
        create_articles(5)
        
    def tearDown(self):
        self.client.logout()

    def test_list_articles_with_mc_head(self):
        self.client.login(username=self.coordinator.username, password='12345678')
        response = self.client.get(reverse("media:list_articles"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'media/list_articles.html')
        self.assertEqual(list(response.context['articles']), list(Article.objects.all()))
        self.assertContains(response, u"المقالات")
        self.assertNotContains(response, u"مقالاتي")
    
    def test_list_articles_with_mc_member(self):
        self.client.login(username=self.member.username, password='12345678')
        response = self.client.get(reverse("media:list_articles"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'media/list_articles.html')
        self.assertEqual(list(response.context['articles']), list(Article.objects.all()))
        self.assertContains(response, u"المقالات")
        self.assertNotContains(response, u"مقالاتي")
        
    def test_list_articles_with_normal_user(self):
        self.client.login(username=self.user1.username, password='12345678')
        response = self.client.get(reverse("media:list_articles"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'media/list_user_articles.html')
        self.assertEqual(list(response.context['articles']), list(Article.objects.filter(author=self.user1)))
#         self.assertNotContains(response, u"المقالات")
        self.assertContains(response, u"مقالاتي")