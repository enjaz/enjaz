"""
Utility functions for automated testing.
"""

from datetime import datetime, date
from django.contrib.auth.models import User
from accounts.test_utils import create_user
from activities.models import Activity, Episode
from clubs.models import Club
from clubs.utils import get_presidency, get_deanship


def create_activity(club=Club.objects.get(pk=1),
                    submitter=User.objects.get(pk=1),
                    episode_count=1):
    """ Create an activity with the given parameters. """
    activity = Activity.objects.create(primary_club=club,
                                       name='Test Activity',
                                       description='Test Description',
                                       participants=1,
                                       organizers=1,
                                       submitter=submitter,
                                       )
    for i in range(episode_count):
        Episode.objects.create(activity=activity,
                               start_date=date.today(),
                               end_date=date.today(),
                               start_time=datetime.now(),
                               end_time=datetime.now(),
                               location='Test Location',
        )
    return activity

def create_activities(count):
    """ Create a number of activities. """
    for i in range(count):
        create_activity()

def add_presidency_review(activity, status, reviewer=create_user()):
    activity.review_set.create(reviewer=reviewer,
                               reviewer_club=get_presidency(),
                               is_approved=status)
    return activity

def add_deanship_review(activity, status, reviewer=create_user()):
    activity.review_set.create(reviewer=reviewer,
                               reviewer_club=get_deanship(),
                               is_approved=status)
    return activity