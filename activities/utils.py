"""
Utility functions for the activities app.
"""
import warnings
from activities.models import Activity
from clubs.utils import is_coordinator_or_deputy, get_deanship, get_presidency


def get_approved_activities():
    """
    Return a queryset of the current year's approved activities.
    """
    warnings.warn("This utility function will be removed soon. Use Activity.objects.approved() instead.",
                  DeprecationWarning)
    # Approved activities are those that have an approved presidency review
    # and an approved deanship review
    # return Activity.objects.filter(approved_by_d, approved_by_p)
    return Activity.objects.filter(review__reviewer_club=get_presidency(),
                                   review__is_approved=True)\
                           .filter(review__reviewer_club=get_deanship(),
                                   review__is_approved=True)


def get_rejected_activities():
    """
    Return a queryset of the current year's rejected activities.
    """
    warnings.warn("This utility function will be removed soon. Use Activity.objects.rejected() instead.",
                  DeprecationWarning)
    # Rejected activities are those that have a rejected presidency review
    # or a rejected deanship review
    return Activity.objects.filter(review__is_approved=False)


def get_pending_activities():
    """
    Return a queryset of the current year's pending activities.
    """
    warnings.warn("This utility function will be removed soon. Use Activity.objects.pending() instead.",
                  DeprecationWarning)
    # Pending activities are those that are neither approved nor rejected.
    return Activity.objects.filter(review__reviewer_club=get_presidency(), review__is_approved=None)\
               .filter(review__reviewer_club=get_deanship(), review__is_approved=None)\
        |  Activity.objects.filter(review__reviewer_club=get_presidency(), review__is_approved=True)\
               .filter(review__reviewer_club=get_deanship(), review__is_approved=None)\
        |  Activity.objects.filter(review__reviewer_club=get_presidency(), review__is_approved=None)\
               .filter(review__reviewer_club=get_deanship(), review__is_approved=True)\
        |  Activity.objects.filter(review__reviewer_club=get_deanship())\
               .exclude(review__reviewer_club=get_presidency()).exclude(review__is_approved=False)\
        |  Activity.objects.filter(review__reviewer_club=get_presidency())\
               .exclude(review__reviewer_club=get_deanship()).exclude(review__is_approved=False)\
        |  Activity.objects.filter(review__isnull=True)


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
        addresses.append(activity.primary_club.coordinator.email)
    for secondary_club in activity.secondary_clubs.all():
        addresses.append(secondary_club.coordinator.email)
    return addresses
        
def forms_editor_check(user, object):
    """A function to evaluate if user is eligible to create/edit forms for activities."""
    # Confirm that the passed object is an ``Activity`` instance
    if not isinstance(object, Activity):
        raise TypeError("Expected an Activity object, received %s" % type(object))
    return is_coordinator_or_deputy(object.primary_club, user) or user.is_superuser