"""
Utility functions for automated testing.
"""
from accounts.test_utils import create_user


def set_club_coordinator(club, user=create_user()):
    """ Set the club's coordinator to the given user. """
    club.coordinator = user
    club.save()
    return user


def add_club_member(club, user=create_user()):
    """ Add the user to the club's members. """
    club.members.add(user)
    return user