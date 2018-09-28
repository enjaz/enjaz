# -*- coding: utf-8  -*-
from __future__ import unicode_literals
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import Http404

from models import Course, Instructor, Graduate, IndexBG, Work

course_codes = (
    ('PR', 'programming'),
    ('PS', 'photoshop'),
    ('VE', 'videoediting'),
    ('CW', 'contentwriting'),
    ('PH', 'photography'),
)

def index(request):
    courses = Course.objects.all()
    try:
        bg = IndexBG.objects.all().latest('pk')
    except ObjectDoesNotExist:
        bg = ''
    context = {'courses': courses,
               'course_codes': course_codes,
               'bg': bg}
    return render(request, 'academy/index.html', context)

def show_course(request, course_name):
    for code, name in course_codes:
        if name == course_name:
            course_code = code
            break
        else:
            continue
    parent_course = get_object_or_404(Course, code=course_code)
    context = {'course_name': course_name,
               'parent_course': parent_course}
    try:
        subcourses = parent_course.subcourse_set.all()
        last_subcourse = subcourses.latest('reg_open_date')
        grad_list = []
        instruct_list = []
        total_sessions = 0
        for course in subcourses:
            if course.session_count:
                total_sessions += course.session_count
            graduates = Graduate.objects.filter(course=course)
            grad_list.append(graduates)
            instructors = Instructor.objects.filter(course=course)
            instruct_list.append(instructors)
        context['subcourses'] = subcourses
        context['last_subcourse'] = last_subcourse
        context['grad_list'] = grad_list
        context['instruct_list'] = instruct_list
        context['total_sessions'] = total_sessions
    except ObjectDoesNotExist:
        context['subcourses'] = 'none'
    return render(request, 'academy/show_course.html', context)

def show_subcourse(request, course_name, batch_no):
    for code, name in course_codes:
        if name == course_name:
            course_code = code
            break
        else:
            continue
    parent_course = get_object_or_404(Course, code=course_code)
    context = {'course_name': course_name,
               'parent_course': parent_course}
    try:
        subcourse = parent_course.subcourse_set.get(batch_no=batch_no)
        context['subcourse'] = subcourse
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'academy/show_subcourse.html', context)

def list_graduates(request):
     pass

def show_person(request, position, person_id):
    if position == "graduate":
        model = Graduate
    elif position == "instructor":
        model = Instructor
    person = get_object_or_404(model, pk=person_id)
    context = {'person': person,
               'position': position}
    return render(request, 'academy/show_person.html', context)

def list_works(request, course_name):
    for code, name in course_codes:
        if name == course_name:
            course_code = code
            break
        else:
            continue
    parent_course = get_object_or_404(Course, code=course_code)
    context = {'course_name': course_name,
               'parent_course': parent_course}
    try:
        subcourses = parent_course.subcourse_set.all()
        context['subcourses'] = subcourses
    except ObjectDoesNotExist:
        context['subcourses'] = 'none'
    return render(request, 'academy/list_works.html', context)

def register_for_course(request, course_name):
    for code, name in course_codes:
        if name == course_name:
            course_code = code
            break
        else:
            continue
    parent_course = get_object_or_404(Course, code=course_code)
    try:
        course = parent_course.subcourse_set.latest('reg_open_date')
    except ObjectDoesNotExist:
        raise Http404
    context = {'course': course,
               'course_name': course_name,
               'parent_course': parent_course}
    return render(request, 'academy/register.html', context)


# TODO: Work on the form: form-builder vs fobi-forms , who will prevail?

# @login_required
# def signup_for_course(request, course_id):
#     course = get_object_or_404(Course, pk=course_id)
#     context = {'course': course}
#
#     #TODO: check if user already signed up for course
#
#     if request.method == 'POST':
#         if course.is_reg_open():
#             reg_form = course.get_registration_form()
#             return HttpResponseRedirect(reverse("forms:form_detail",
#                                              args=(course.id, reg_form.id),
#                                              current_app=FORMS_CURRENT_APP))
#         else:
#             raise PermissionDenied



#def show_staticpage(request, page):
#    return render(request,'academy/static/'+page+'.html')


