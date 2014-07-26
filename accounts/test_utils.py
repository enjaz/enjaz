"""
Utility functions for automated testing.
"""

from django.contrib.auth.models import User


def create_user(username=None, email="test@enjazportal.com", password="12345678"):
    if username == None:
        username = "username" + str(User.objects.count() + 1)
    return User.objects.create_user(username, email, password)
