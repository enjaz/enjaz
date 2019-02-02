from academy.models import *
from academy.views import course_codes

def parent_courses(request):
    return {'parent_courses': Course.objects.all()}

def academy_codes(request):
    return {'course_codes': course_codes}

def workshops(request):
    return {'workshops': Workshop.objects.all()}
