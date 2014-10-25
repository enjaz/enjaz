"""Utility functions related to the clubs app."""
from clubs.models import Club
from .models import Club

# TODO: all() is memory expensive, more specific calls should
# always be used.

def is_coordinator_of_any_club(user):
    """Return whether the user is a coordinator of any club."""
    return bool(Club.objects.filter(coordinator=user).all())

def is_member_of_any_club(user):
    """Return whether the user is a member of any club."""
    user_clubs = Club.objects.filter(members=user)
    return bool(user_clubs.all())

def is_employee_of_any_club(user):
    """Return whether the user is an employee of any club."""
    employee_clubs = Club.objects.filter(employee=user)
    return bool(employee_clubs.all())

def is_coordinator(club, user):
    """Return whether the user is the coordinator of a given club."""
    return club.coordinator == user

def is_deputy(club, user):
    """Return whether the user is a member of a given club."""
    return user in club.deputies.filter(pk=user.pk)

def is_member(club, user):
    """Return whether the user is a member of a given club."""
    return user in club.members.filter(pk=user.pk)

def is_coordinator_or_member(club, user):
    """Return whether the user is the coordinator, a deputy or a member of a given club."""
    return is_coordinator(club, user) or is_deputy(club, user) or is_member(club, user)

def is_coordinator_or_deputy(club, user):
    """Return whether the user is the coordinator or a deputy of a given club."""
    return is_coordinator(club, user) or is_deputy(club, user)

def is_employee(club, user):
    """Return whether the user is the employee assigned to a given club."""
    return user == club.employee

def has_coordination_to_activity(user, activity):
    """Return whether the user is the coordinator or deputy assigned to
    any of the primry or secondary clubs of a given activity.
    """
    # First get clubs associated with the activity.  We need both of
    # them to be QuerySets
    activity_primary_club = Club.objects.filter(
                            id=activity.primary_club.id)
    activity_secondary_clubs = activity.secondary_clubs.all()
    activity_clubs = activity_primary_club | activity_secondary_clubs
    # Second, check if any of which have the given user as a
    # coordinator or deputy
    coordination_clubs = activity_clubs.filter(coordinator=user) | \
                         activity_clubs.filter(deputies=user)
    # Return a Boolean 
    return bool(coordination_clubs.all())

def get_presidency():
    return Club.objects.get(english_name="Presidency")

def get_media_center():
    return Club.objects.get(english_name="Media Center")

def get_user_clubs(user):
    return user.memberships.all() | user.coordination.all()

def get_user_coordination_and_deputyships(user):
    """Return the clubs in which the given user is the coordinator or
    deputy.  Returns None if no clubs are found."""

    coordination = user.coordination.all()
    deputyships = user.deputyships.all()
    # Return a QuerySet to allow further filtering
    return (coordination | deputyships)

def is_coordinator_or_deputy_of_any_club(user):
    """Return whether the user is a coordinator of any club."""
    coordination_and_deputyships = get_user_coordination_and_deputyships(user).all()
    return bool(coordination_and_deputyships)

def forms_editor_check(user, object):
    """A function to evaluate if user is eligible to create/edit forms for clubs."""
    # Confirm that the passed object is a ``Club`` instance
    if not isinstance(object, Club):
        raise TypeError("Expected a Club object, received %s" % type(object))
    return is_coordinator(object, user) or user.is_superuser