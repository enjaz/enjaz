from datetime import datetime, timedelta
from django.test import TestCase
from accounts.test_utils import create_user
from activities.test_utils import create_activity


class ActivityTests(TestCase):
    def setUp(self):
        self.user = create_user()
        self.activity = create_activity()

    # def tearDown(self):
    #     pass

    def test_get_first_episode(self):
        self.episode = self.activity.episode_set.create(start_date=(datetime.today() + timedelta(days=-1)),
                                                        end_date=(datetime.today() + timedelta(days=-1)),
                                                        start_time=datetime.now(),
                                                        end_time=datetime.now(),
                                                        location="Test Location")
        self.assertEqual(self.activity.get_first_episode(), self.episode)

    def test_get_next_episode(self):
        self.assertIsNone(self.activity.get_next_episode())

        # Episode in a past day
        self.episode1 = self.activity.episode_set.create(start_date=(datetime.today() + timedelta(days=-1)),
                                                         end_date=(datetime.today() + timedelta(days=-1)),
                                                         start_time=datetime.now(),
                                                         end_time=datetime.now(),
                                                         location="Test Location")
        self.assertIsNone(self.activity.get_next_episode())

        # Episode in the same day but at a previous time
        self.episode2 = self.activity.episode_set.create(start_date=(datetime.today()),
                                                         end_date=(datetime.today()),
                                                         start_time=(datetime.now() + timedelta(minutes=-1)),
                                                         end_time=(datetime.now() + timedelta(minutes=-1)),
                                                         location="Test Location")
        self.assertIsNone(self.activity.get_next_episode())

        # Episode on a later day (the time is later than the current time)
        # i.e. if now is 19 Aug 2014 14:00, it can be 20 Aug 2014 16:00
        self.episode3 = self.activity.episode_set.create(start_date=(datetime.today() + timedelta(days=1)),
                                                         end_date=(datetime.today()) + timedelta(days=1),
                                                         start_time=(datetime.now() + timedelta(minutes=1)),
                                                         end_time=(datetime.now() + timedelta(minutes=1)),
                                                         location="Test Location")
        self.assertEqual(self.activity.get_next_episode(), self.episode3)

        # Episode on a later day (but the time is before the current time)
        # i.e. if now is 19 Aug 2014 14:00, it can be 20 Aug 2014 10:00
        self.episode4 = self.activity.episode_set.create(start_date=(datetime.today() + timedelta(days=1)),
                                                         end_date=(datetime.today()) + timedelta(days=1),
                                                         start_time=(datetime.now() + timedelta(minutes=-1)),
                                                         end_time=(datetime.now() + timedelta(minutes=-1)),
                                                         location="Test Location")
        self.assertEqual(self.activity.get_next_episode(), self.episode4)

        # Episode in the same day but at a later time
        self.episode5 = self.activity.episode_set.create(start_date=(datetime.today()),
                                                         end_date=(datetime.today()),
                                                         start_time=(datetime.now() + timedelta(minutes=1)),
                                                         end_time=(datetime.now() + timedelta(minutes=1)),
                                                         location="Test Location")
        self.assertEqual(self.activity.get_next_episode(), self.episode5)