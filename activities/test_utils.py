"""
Utility functions for automated testing.
"""

from datetime import datetime, date
from django.contrib.auth.models import User
from activities.models import Activity, Episode
from clubs.models import Club

def create_activity(club=Club.objects.get(pk=1),
                    submitter=User.objects.get(pk=1),
                    collect_participants=False,
                    episode_count=1):
    """ Create an activity with the given parameters. """
    activity = Activity.objects.create(primary_club=club,
                                       name='Test Activity',
                                       description='Test Description',
                                       participants=1,
                                       organizers=1,
                                       submitter=submitter,
                                       collect_participants=collect_participants)
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

