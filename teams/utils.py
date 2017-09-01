# -*- coding: utf-8  -*-
"""Utility functions related to the clubs app."""
from .models import Team
from core.models import StudentClubYear
import accounts.utils


def is_coordinator(user,team):
    """Return whether the user is the coordinator of a given club or team."""
    return team.leader == user

def forms_editor_check(user, object):
    """A function to evaluate if user is eligible to create/edit forms for activities."""
    # Confirm that the passed object is an ``Activity`` instance
    if not isinstance(object, Team):
        raise TypeError("Expected an Team object, received %s" % type(object))
    return is_coordinator(user, object) or user.is_superuser