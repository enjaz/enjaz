"""
Utility functions for the accounts app.
"""
from django.core.exceptions import ObjectDoesNotExist

def get_user_city(user):
    """Return the user's city.  If unavailable, return None."""
    # If either the profile is absent (i.e. superuser), return None.
    try: 
        city = user.common_profile.city
    except ObjectDoesNotExist:
        city = None

    return city

def get_user_gender(user):
    """Return the user's city.  If unavailable, return None."""
    # If either the profile (i.e. superuser) or the college
    # (i.e. non-student) are absent, return None.
    try: 
        gender = user.common_profile.college.gender
    except (ObjectDoesNotExist, AttributeError):
        gender = None

    return gender
