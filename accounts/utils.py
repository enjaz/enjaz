"""
Utility functions for the accounts app.
"""
from django.core.exceptions import ObjectDoesNotExist

def get_user_city(user):
    """Return the user's city.  If unavailable, return an empty string."""

    if not user.is_authenticated() or \
       user.is_superuser:
        return ''

    # If the profile is absent, return None.
    try: 
        city = user.common_profile.city
    except (ObjectDoesNotExist, AttributeError):
        city = ''

    return city

def get_user_gender(user):
    """Return the user's city.  If unavailable, return an empty string."""

    if not user.is_authenticated() or \
       user.is_superuser:
        return ''
    
    # If either the profile or the college are absent, return an empty
    # string.
    try: 
        gender = user.common_profile.college.gender
    except (ObjectDoesNotExist, AttributeError):
        gender = ''

    return gender


def get_user_college(user):
    """Return the user's college.  If unavailable, return None."""

    if user.is_superuser:
        return
    
    # If either the profile or the college are absent, return an empty
    # string.
    try: 
        college = user.common_profile.college
    except (ObjectDoesNotExist, AttributeError):
        college = None

    return college

def get_user_profile_type (user):

    if not user.is_authenticated() or \
       user.is_superuser:
        return ''

    # If the profile is absent, return None.
    try:
        profile_type = user.common_profile.profile_type
    except (ObjectDoesNotExist, AttributeError):
        profile_type = ''

    return profile_type