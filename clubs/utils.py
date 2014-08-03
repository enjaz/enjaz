"""Utility functions related to the clubs app."""
from .models import Club


def is_coordinator_of_any_club(user):
    """Return whether the user is a coordinator of any club."""
    return any([user == club.coordinator for club in Club.objects.all()])


def is_member_of_any_club(user):
    """Return whether the user is a member of any club."""
    return any([user in club.members.all() for club in Club.objects.all()])


def is_coordinator(club, user):
    """Return whether the user is the coordinator of a given club."""
    return club.coordinator == user


def is_member(club, user):
    """Return whether the user is a member of a given club."""
    return user in club.members.all()


def is_coordinator_or_member(club, user):
    """Return whether the user is the coordinator or a member of a given club."""
    return is_coordinator(club, user) or is_member(club, user)


def get_presidency():
    return Club.objects.get(english_name="Presidency")


def get_media_center():
    return Club.objects.get(english_name="Media Center")