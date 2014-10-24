"""Utility functions related to the clubs app."""
from clubs.models import Club
from .models import Club


def is_coordinator_of_any_club(user):
    """Return whether the user is a coordinator of any club."""
    return any([user == club.coordinator for club in Club.objects.all()])


def is_member_of_any_club(user):
    """Return whether the user is a member of any club."""
    return any([user in club.members.all() for club in Club.objects.all()])

def is_employee_of_any_club(user):
    """Return whether the user is an employee of any club."""
    return any([is_employee(club, user) for club in Club.objects.all()])

def is_coordinator(club, user):
    """Return whether the user is the coordinator of a given club."""
    return club.coordinator == user


def is_member(club, user):
    """Return whether the user is a member of a given club."""
    return user in club.members.all()


def is_coordinator_or_member(club, user):
    """Return whether the user is the coordinator or a member of a given club."""
    return is_coordinator(club, user) or is_member(club, user)

def is_employee(club, user):
    """Return whether the user is the employee assigned to a given club."""
    return user == club.employee

def get_presidency():
    return Club.objects.get(english_name="Presidency")


def get_media_center():
    return Club.objects.get(english_name="Media Center")


def forms_editor_check(user, object):
    """A function to evaluate if user is eligible to create/edit forms for clubs."""
    # Confirm that the passed object is a ``Club`` instance
    if not isinstance(object, Club):
        raise TypeError("Expected a Club object, received %s" % type(object))
    return is_coordinator(object, user) or user.is_superuser