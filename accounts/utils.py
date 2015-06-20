"""
Utility functions for the accounts app.
"""
from django.core.exceptions import ObjectDoesNotExist

def get_user_city(user):
    """Return the user's city.  If unavailable, return an empty string."""
    # If the profile is absent (i.e. superuser), return None.
    try: 
        city = user.common_profile.city
    except (ObjectDoesNotExist, AttributeError):
        city = ''

    return city

def get_user_gender(user):
    """Return the user's city.  If unavailable, return an empty string."""
    # If either the profile (i.e. superuser) or the college
    # (i.e. non-student) are absent, return an empty string.
    try: 
        gender = user.common_profile.college.gender
    except (ObjectDoesNotExist, AttributeError):
        gender = ''

    return gender
