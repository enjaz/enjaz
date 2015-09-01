"""
Utility functions for the activities app.
"""
from activities.models import Activity
from clubs.models import Club
from clubs.utils import has_coordination_to_activity, get_user_clubs, get_user_coordination_and_deputyships
from media.utils import get_user_media_center, is_media_member

def get_club_notification_to(activity):
    """Return the address that should be sent an email notifcation in the
    'to' field.
    """
    # The submitter, whether they are the coordinator or not should
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


def get_club_assessing_club_by_user(user, club):
    """Check if the user can assess a given club. Returns the assessor
       club, or None."""
    if club.city == 'R':
        if club.gender:
            club_gender = club.gender
        else:
            # Just in case a Riyadh club doesn't have a gender fall
            # back to male Media Center.
            club_gender = 'M'
    else: # For other cities
        club_gender = ''

    media_center = Club.objects.get(english_name__contains='Media Center',
                                    city=club.city,
                                    gender=club_gender)
    user_media_center = get_user_media_center(user)

    if media_center == user_media_center:
        if is_media_member(user):
            if club.media_assessor and club.media_assessor != user:
                return
        return media_center

    presidency = Club.objects.get(english_name__contains='Presidency',
                                  city=club.city,
                                  gender=club_gender)

    if presidency in get_user_coordination_and_deputyships(user):
        return presidency

def can_assess_club(user, club, category=""):
    # Three user types can assess a given activity:
    # * Superuser
    # * Clubs with can_assess (i.e. student club president deputies)
    # * Medica Club in the same city
    if user.has_perms('activities.add_assessment'): # e.g. superuser
        return True
    return bool(get_club_assessing_club_by_user(user, club))

def can_view_assessments(user, club):
    # Two user types can view assessments a given activity:
    # * Superuser
    # * Clubs with can_view_assessment (i.e. student club president deputies)
    if user.has_perms('activities.delete_assessment'): # e.g. superuser
        return True
    assessor_club = get_club_assessing_club_by_user(user, club)
    if assessor_club and assessor_club.can_view_assessments:
        return True
    else:
        return False

def can_assess_any_club(user):
    return get_user_clubs(user).filter(can_assess=True).exists() or user.is_superuser
