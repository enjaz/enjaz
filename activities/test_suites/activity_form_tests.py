# -*- coding: utf-8  -*-
"""
Tests for the activity submission and editing form.
"""
from datetime import datetime, date, time

from django.test import TestCase

from django.contrib.auth import login
from django.contrib.auth.models import User, Permission
from django.core.urlresolvers import reverse

from clubs.models import Club
from activities.models import Activity, Review, Episode

class EpisodeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user',
                                             email='user@enjazportal.com',
                                             password='top_secret')
        self.client.login(username=self.user.username, password='top_secret')
        
        view_activity = Permission.objects.get(codename='view_activity')
        change_activity = Permission.objects.get(codename='change_activity')
        self.user.user_permissions.add(view_activity, change_activity)
        
        self.club = Club.objects.create(name="Test Club Arabic Name",
                               english_name="Test English Club Name",
                               description="-",
                               email="test@enjazportal.com",
                               )
        self.activity = Activity.objects.create(primary_club=self.club,
                                       name='Test Activity',
                                       description='Test Description',
                                       participants=1,
                                       organizers=1,
                                       submitter=self.user,
                                       )

    # def test_delete_episode(self):
    #     for i in range(2): # Create two episodes
    #         self.activity.episode_set.create(start_date=datetime.now(),
    #                                          end_date=datetime.now(),
    #                                          start_time=datetime.now(),
    #                                          end_time=datetime.now(),
    #                                          location="Test location"
    #                                          )
    #     self.assertEqual(self.activity.episode_set.count(), 2)
    #
    #     ep_lst = self.activity.episode_set.all()
    #     self.assertEqual(ep_lst[0].pk, 1)
    #     self.assertEqual(ep_lst[1].pk, 2)
    #
    #     response = self.client.get(reverse('activities:edit',
    #                                args=(self.activity.pk, )))
    #     self.assertContains(response, 'name="episode_pk0"')
    #     self.assertContains(response, 'name="episode_pk1"')
    #
    #     response = self.client.post(reverse('activities:edit',
    #                                         args=(self.activity.pk, )),
    #                               {'primary_club': '1',
    #                                'name': 'Modified Name',
    #                                'description': 'Modified Description',
    #                                'episode_count': '1',
    #                                'episode_pk0': '1',
    #                                'start_date0': '2014-06-24',
    #                                'end_date0'  : '2014-06-25',
    #                                'start_time0': '23:30',
    #                                'end_time0'  : '23:30',
    #                                'location0'  : 'Test Location',
    #                                'organizers' : '1',
    #                                'participants' : '1',
    #                                'inside_collaborators' : '',
    #                                'outside_collaborators' : '',
    #                                'requirements' : '',
    #                                })
    #
    #     self.assertEqual(response.status_code, 302)
    #     # The second episode should now be deleted
    #     self.assertEqual(self.activity.episode_set.count(), 1)