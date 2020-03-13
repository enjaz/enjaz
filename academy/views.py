# -*- coding: utf-8  -*-
from __future__ import unicode_literals
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib.auth.models import User

from models import Course, Instructor, Graduate, IndexBG, Work, Temporary_Stats, Workshop

from forms_builder.forms.models import FormEntry

FORMS_CURRENT_APP = "academy_forms"


course_codes = (
    ('PR', 'programming'),
    ('PS', 'photoshop'),
    ('VE', 'videoediting'),
    ('CW', 'contentwriting'),
    ('PH', 'photography'),
    ('MM', 'marketing'),
    ('VP', 'voiceperformance'),
    ('IL', 'illustrator'),
    ('CM', 'campaignmanagement'),
    ('3D', '3D'),
)

def count_stats(request):
    parent_courses = Course.objects.all()
    workshops = Workshop.objects.all()
    all_graduates = []
    all_instructors = []
    all_sessions = 0
    for parent_course in parent_courses:
        subcourses = parent_course.subcourse_set.all()
        for subcourse in subcourses:
            if subcourse.session_count:
                all_sessions += subcourse.session_count
            graduates = Graduate.objects.filter(course=subcourse)
            for grad in graduates:
                all_graduates.append(grad)
            instructors = Instructor.objects.filter(course=subcourse)
            for inst in instructors:
                all_instructors.append(inst)

    return(parent_courses, all_graduates, all_instructors, all_sessions, workshops)

def index(request):
    courses = Course.objects.all()
    try:
        bg = IndexBG.objects.all().latest('pk')
    except ObjectDoesNotExist:
        bg = ''
    parent_courses, all_graduates, all_instructors, all_sessions, workshops = count_stats(request)
    latest_subcourses = {}
    for parent_course in courses:
        if parent_course.subcourse_set.all().exists():
            latest_subcourse = parent_course.subcourse_set.latest('reg_open_date')
            latest_subcourses[parent_course] = latest_subcourse
        else:
            latest_subcourses[parent_course] = ''
        # try:
        #     latest_subcourse = parent_course.subcourse_set.latest('reg_open_date')
        #     latest_subcourses[parent_course] = latest_subcourse
        # except ObjectDoesNotExist:
        #     continue
    context = {'courses': courses,
               'course_codes': course_codes,
               'workshops': workshops,
               'bg': bg,
               'parent_courses': parent_courses,
               'all_graduates': all_graduates,
               'all_instructors': all_instructors,
               'all_sessions': all_sessions,
               'latest_subcourses': latest_subcourses,
               }

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
            for grad in graduates:
                grad_list.append(grad)
            instructors = Instructor.objects.filter(course=course)
            for inst in instructors:
                instruct_list.append(inst)
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
    subcourses = parent_course.subcourse_set.all()
    context = {'course_name': course_name,
               'parent_course': parent_course,
               'subcourses': subcourses}
    try:
        subcourse = parent_course.subcourse_set.get(batch_no=batch_no)
        context['subcourse'] = subcourse
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'academy/show_subcourse.html', context)

def list_graduates(request):
     pass

def show_workshop(request, workshop_id):
    workshop = get_object_or_404(Workshop, pk=workshop_id)
    context = {'workshop': workshop}
    return render(request, 'academy/show_workshop.html', context)

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

def invite_to_ceremony(request, theme, invitee_id):
    invitee = get_object_or_404(User, username=invitee_id)
    context = {'theme': theme,
                'invitee': invitee}
    return render(request, 'academy/invite_ceremony.html', context)

def show_recording(request, course_name, batch_no, session_no):
    for code, name in course_codes:
        if name == course_name:
            course_code = code
            break
        else:
            continue
    parent_course = get_object_or_404(Course, code=course_code)
    context = {'course_name': course_name,
               'parent_course': parent_course,}
    try:
        subcourse = parent_course.subcourse_set.get(batch_no=batch_no)
        context['subcourse'] = subcourse
    except ObjectDoesNotExist:
        raise Http404
    try:
        recorded_session = subcourse.recorded_session.get(number=session_no)
        context['recorded_session'] = recorded_session
    except ObjectDoesNotExist:
        raise Http404

    return render(request, 'academy/show_recorded_session.html', context)

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


