"""
Tests of the follow-up reports part of the media app.
"""
from datetime import datetime, date, time, timedelta

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.models import User
from clubs.models import Club
from activities.models import Activity, Episode
from media.models import FollowUpReport
from media.utils import REPORT_DUE_AFTER


class ReportDueAndOverdueDateTests(TestCase):
    """
    Test the methods related to report due dates, which are
    associated with the club and episode models.
    """
#     fixtures = ['initial_data.json']
    def setUp(self):
        # Create a user, a club (and make the user its coordinator),
        # and 3 activities with 1, 2, 3 episodes respectively
        self.user = User.objects.create_user('msarabi', 'test@enjazportal.com', '12345678')
        self.club = Club.objects.create(name="Test Arabic Club Name",
                                        english_name="Test English Club Name",
                                        description="Test Club Description",
                                        email="test@enjazportal.com",
                                        coordinator=self.user)
        for i in range(1, 4):
            activity = Activity.objects.create(primary_club=self.club,
                                               name='Test Activity Name ' + str(i),
                                               description='Test Activity Description ' + str(i),
                                               participants=1,
                                               organizers=1,
                                               submitter=self.user,
                                               )
            for j in range(i):
                # Set the episode end date to be 6*j days back
                episode = Episode.objects.create(activity=activity,
                                                start_date=date.today() - timedelta(weeks=3),
                                                end_date=date.today() - timedelta(days=j*6),
                                                start_time=datetime.now(),
                                                end_time=datetime.now(),
                                                location='Test Location',
                                                )
                # Create reports for some episodes
                if j == 0:
                    FollowUpReport.objects.create(episode=episode,
                                                  description="Test Report Description",
                                                  start_date=date.today(),
                                                  end_date=date.today(),
                                                  start_time=datetime.now(),
                                                  end_time=datetime.now(),
                                                  location="Test Report Location",
                                                  organizer_count=10,
                                                  participant_count=100,
                                                  submitter=self.user,
                                                  )

#     # This is run after each test
#     def tearDown(self):
#         print User.objects.all()
#         print Club.objects.all()
#         print Activity.objects.all(), "<- hello!"
#         print Episode.objects.all()
#         print FollowUpReport.objects.all()

    def test_report_is_submitted(self):
        "Test whehter the function returns True when there is a FollowUpReport and False otherwise"
        for episode in Episode.objects.all():
            try:
                r = episode.followupreport
                submitted = True
            except ObjectDoesNotExist:
                submitted = False
            self.assertEqual(episode.report_is_submitted(), submitted)


    def test_report_due_date(self):
        "Test the report_due_date method of the episode model"
        # Report due date should be REPORT_DUE_AFTER days
        # after the episode end datetime.
        for episode in Episode.objects.all():
            self.assertEqual(episode.report_due_date(),
                             episode.end_datetime() + timedelta(days=REPORT_DUE_AFTER)
                             )
    
    def test_report_is_due(self):
        "Test the report_is_due method of the episode model"
        for episode in Episode.objects.all():
            try:
                report = episode.followupreport
                # If report exists, report_is_due should be always false
                self.assertFalse(episode.report_is_due())
            except ObjectDoesNotExist:
                # If no report exists, compare current datetime to the
                # episode's end datetime. If the current datetime occurs
                # between the episode's end datetime and the due datetime,
                # then report_is_due should be true, else false
                due = episode.end_datetime() < datetime.now() < episode.report_due_date()
                self.assertEqual(episode.report_is_due(), due)
    
    def test_report_is_overdue(self):
        "Test the report_is_overdue method of the episode model"
        for episode in Episode.objects.all():
            try:
                report = episode.followupreport
                # If report exists, report_is_overdue should be always false
                self.assertFalse(episode.report_is_overdue())
            except ObjectDoesNotExist:
                # If no report exists, compare current datetime to the
                # episode's end datetime. If the current datetime occurs
                # after the episode's end datetime and the due datetime,
                # then report_is_overdue should be true, else false
                overdue = episode.report_due_date() > datetime.now()
                self.assertEqual(episode.report_is_due(), overdue)
    
    def test_get_due_report_count(self):
        "Test the get_due_report_count method of the club model"
        # Due reports should be 2
        self.assertEqual(self.club.get_due_report_count(), 2)
        
    def test_get_overdue_report_count(self):
        "Test the get_overdue_report_count method of the club model"
        # Overue reports should be 1
        self.assertEqual(self.club.get_overdue_report_count(), 1)
        
class ActivityViewsWithNoReportPenalty(TestCase):
    """
    Test how the activity views (create and list) behave with
    integration with reports set up.
    """
    def setUp(self):
        # Create a user, a club (and make the user its coordinator),
        # and 4 activities with 1, 2, 3, 4 episodes respectively.
        # Also create a report for the first episode in each activity
        # Set the number of due reports to 3
        # Also set overdue reports to 3
        # Therefore no penalties are expected 
        self.user = User.objects.create_user('msarabi', 'test@enjazportal.com', '12345678')
        self.client.login(username=self.user.username, password='12345678')
        self.club = Club.objects.create(name="Test Arabic Club Name",
                                        english_name="Presidency",
                                        description="Test Club Description",
                                        email="test@enjazportal.com",
                                        coordinator=self.user)
        for i in range(1, 5):
            activity = Activity.objects.create(primary_club=self.club,
                                               name='Test Activity Name ' + str(i),
                                               description='Test Activity Description ' + str(i),
                                               participants=1,
                                               organizers=1,
                                               submitter=self.user,
                                               )
            for j in range(i):
                # Set the episode end date to be 6*j days back
                episode = Episode.objects.create(activity=activity,
                                                start_date=date.today() - timedelta(weeks=3),
                                                end_date=date.today() - timedelta(days=j*6),
                                                start_time=datetime.now(),
                                                end_time=datetime.now(),
                                                location='Test Location',
                                                )
                if j == 0:
                    FollowUpReport.objects.create(episode=episode,
                                                  description="Test Report Description",
                                                  start_date=date.today(),
                                                  end_date=date.today(),
                                                  start_time=datetime.now(),
                                                  end_time=datetime.now(),
                                                  location="Test Report Location",
                                                  organizer_count=10,
                                                  participant_count=100,
                                                  submitter=self.user,
                                                  )
#     # This is run after each test
#     def tearDown(self):
#         print User.objects.all()
#         print Club.objects.all()
#         print Activity.objects.all()
#         print Episode.objects.all()
#         print FollowUpReport.objects.all()
        
    def test_create_activity_view(self):
        "Test how create activity view behaves with no report penalties"
        response = self.client.get(reverse('activities:create'))
        self.assertEqual(response.status_code, 200)
        
class ActivityViewsWithReportPenalty(TestCase):
    """
    Test how the activity views (create and list) behave with
    integration with reports set up.
    """
    def setUp(self):
        # Create a user, a club (and make the user its coordinator),
        # and 4 activities with 1, 2, 3, 4, 5 episodes respectively.
        # Also create a report for the first episode in each activity
        # Set the number of due reports to 4
        # Also set overdue reports to 6
        # Therefore penalties are expected 
        self.user = User.objects.create_user('msarabi', 'test@enjazportal.com', '12345678')
        self.client.login(username=self.user.username, password='12345678')
        self.club = Club.objects.create(name="Test Arabic Club Name",
                                        english_name="Presidency", # due to dependent nature of create view,
                                                                   # there must be a club with the name
                                                                   # Presidency :/
                                        description="Test Club Description",
                                        email="test@enjazportal.com",
                                        coordinator=self.user)
        for i in range(1, 6):
            activity = Activity.objects.create(primary_club=self.club,
                                               name='Test Activity Name ' + str(i),
                                               description='Test Activity Description ' + str(i),
                                               participants=1,
                                               organizers=1,
                                               submitter=self.user,
                                               )
            for j in range(i):
                # Set the episode end date to be 6*j days back
                episode = Episode.objects.create(activity=activity,
                                                start_date=date.today() - timedelta(weeks=3),
                                                end_date=date.today() - timedelta(days=j*6),
                                                start_time=datetime.now(),
                                                end_time=datetime.now(),
                                                location='Test Location',
                                                )
                if j == 0:
                    FollowUpReport.objects.create(episode=episode,
                                                  description="Test Report Description",
                                                  start_date=date.today(),
                                                  end_date=date.today(),
                                                  start_time=datetime.now(),
                                                  end_time=datetime.now(),
                                                  location="Test Report Location",
                                                  organizer_count=10,
                                                  participant_count=100,
                                                  submitter=self.user,
                                                  )
#     # This is run after each test
#     def tearDown(self):
#         print User.objects.all()
#         print Club.objects.all()
#         print Activity.objects.all()
#         print Episode.objects.all()
#         print FollowUpReport.objects.all()
        
    def test_create_activity_view(self):
        "Test how create activity view behaves with report penalties"
        response = self.client.get(reverse('activities:create'))
        self.assertEqual(response.status_code, 403)
