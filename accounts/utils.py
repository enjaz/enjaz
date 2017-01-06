# -*- coding: utf-8  -*-
"""
Utility functions for the accounts app.
"""
from django.core.exceptions import ObjectDoesNotExist

def get_user_city(user):
    """Return the user's city.  If unavailable, return an empty string."""

    if not user.is_authenticated() or \
       user.is_superuser:
        return ''

    # If the profile is absent, return an empty string.
    try: 
        city = user.common_profile.city
    except (ObjectDoesNotExist, AttributeError):
        city = ''

    return city

def get_user_gender(user):
    """Return the user's gender.  If unavailable, return an empty string."""

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

def get_user_profile_type(user):

    if not user.is_authenticated() or \
       user.is_superuser:
        return ''

    # If the profile is absent, return None.
    try:
        profile_type = user.common_profile.profile_type
    except (ObjectDoesNotExist, AttributeError):
        profile_type = ''

    return profile_type

def get_city_code(city):
    if city == u'الرياض':
        return 'R'
    elif city == u'جدة':
        return 'J'
    elif city == u'الأحساء':
        return 'A'

def get_city_from_code(city_code):
    if city_code == 'R': 
        return u'الرياض'
    elif city_code == 'J':
        return u'جدة'
    elif city_code == 'A':
        return u'الأحساء'
