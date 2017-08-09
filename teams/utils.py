# -*- coding: utf-8  -*-
"""Utility functions related to the clubs app."""
from .models import Teams
from core.models import StudentClubYear
import accounts.utils


def is_coordinator(teams, user):
    """Return whether the user is the coordinator of a given club or team."""
    return teams.leader == user
