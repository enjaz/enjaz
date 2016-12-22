import functools
import logging
import json
from django.shortcuts import render
from accounts.utils import get_user_city
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.core import exceptions as django_exceptions
from django.contrib.auth.models import User
from accounts.utils import get_user_profile_type

def university_only(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not get_user_profile_type(request.user) in ['S', 'E','']:
             raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper

#def is_student (requist.user):

#def only_for_students (view_func):
#    @functools.wraps(view_func)
#    def is_student(request, *args, **kwargs) :
#        student = User.objects.filter(common_profile__profile_type='S')
#        if request.user == student:
#            return True
#        else
#            return False
#    return is_student

#        apps.get_model('clubs', 'Club')
#    StudentClubYear = apps.get_model('core', 'StudentClubYear')
#    m_f_presidency = Club.objects.filter(english_name__startswith="Presidency (Riyadh/", year=year2015_2016).update(gender='')

f