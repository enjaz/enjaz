"""
Utility functions for the activities app.
"""
from activities.models import Activity
from clubs.utils import has_coordination_to_activity, get_deanship, get_presidency


def get_club_notification_to(activity):
    """Return the address that should be sent an email notifcation in the
    'to' field.
    """
    # The submitter, whether they are the coordinator or not shoudl
    # receive be in the 'to' field.
    return [activity.submitter.email]


def get_club_notification_cc(activity):
    """Return the address that should be sent an email notifcation in the
    'cc' field.
    """
    addresses = []
    # If the person who submitted the activity is not the coordinator,
    # add the coordinator to the CC list.
    if activity.submitter != activity.primary_club.coordinator:
        if activity.primary_club.coordinator and \
           activity.primary_club.coordinator.email:
            addresses.append(activity.primary_club.coordinator.email)
    for secondary_club in activity.secondary_clubs.filter(coordinator__isnull=False):
        if secondary_club.coordinator.email:
            addresses.append(secondary_club.coordinator.email)
    return addresses


def forms_editor_check(user, object):
    """A function to evaluate if user is eligible to create/edit forms for activities."""
    # Confirm that the passed object is an ``Activity`` instance
    if not isinstance(object, Activity):
        raise TypeError("Expected an Activity object, received %s" % type(object))
    return has_coordination_to_activity(user, object) or user.is_superuser
