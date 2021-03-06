# -*- coding: utf-8  -*-
import datetime

from django.db.models import Q
from django import forms
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required, login_required
from django.views.decorators import csrf

from post_office import mail

from core import decorators
from core.models import StudentClubYear
from arshidni.models import GraduateProfile, Question, Answer, StudyGroup, LearningObjective, JoinStudyGroupRequest, ColleagueProfile, SupervisionRequest

from arshidni.forms import  GraduateProfileForm, QuestionForm, AnswerForm, StudyGroupForm, ColleagueProfileForm, SupervisionRequestForm
from arshidni.utilities import get_arshidni_club_for_user, is_arshindi_coordinator_or_deputy

from clubs.models import College
from accounts.utils import get_user_city, get_user_gender

COLLEAGUE_SUPERVISION_LIMIT = 8

# Anything that should solely be done by the Arshidni coordinator
# should be done through the arshidni admin interface.

# TODO:
#  * Add college to college and graduate form pages. [Osama, Aug 2, 2014]
#  * Add view_* permissions [Osama, Aug 2, 2014]
#  * End date pickers should start at present date. (Don't apply this
#    rule to the start date because some groups may be register after
#    they have already started. [Osama, Aug 2, 2014]

# Home

@login_required
def home(request):
    # Questions:
    my_questions = Question.objects.filter(submitter=request.user)
    approved_questions = Question.objects.filter(is_published=True)
    questions = (my_questions | approved_questions).order_by('-submission_date')
    latest_questions = questions[:10]
    question_count = Question.objects.count()
    my_question_count = Question.objects.filter(submitter=request.user).count()

    # Groups:
    my_groups = StudyGroup.objects.filter(coordinator=request.user)
    approved_groups = StudyGroup.objects.filter(status='A')
    groups = (my_groups | approved_groups).order_by('-submission_date')
    latest_groups = groups[:10]
    group_count = StudyGroup.objects.count()
    my_group_count = StudyGroup.objects.filter(members=request.user).count() + StudyGroup.objects.filter(coordinator=request.user).count()

    # Student colleague:
    latest_colleagues = ColleagueProfile.objects.current_year().available().published().for_user_gender(request.user).for_user_city(request.user).order_by('-submission_date')[:10]
    colleague_count = ColleagueProfile.objects.current_year().count()
    context = {'latest_questions': latest_questions, 'question_count':
               question_count, 'my_question_count': my_question_count,
               'latest_groups': latest_groups, 'group_count':
               group_count, 'my_group_count': my_group_count,
               'latest_colleagues': latest_colleagues,
               'colleague_count': colleague_count}
    return render(request, 'arshidni/home.html', context)

# Graduates

@login_required
def register_graduate_profile(request):
    # Any changes to this view will probably also apply to
    # register_colleague_profile.

    if request.method == 'POST':
        graduate_profile_object = GraduateProfile(user=request.user)
        form = GraduateProfileForm(request.POST,
                                   instance=graduate_profile_object)
        if form.is_valid():
            new_graduate_profile = form.save()
            graduate_profile_url = reverse('arshidni:show_graduate_profile',
                                           args=(new_graduate_profile.pk,))
            full_url = request.build_absolute_uri(graduate_profile_url)
            arshidni_coordinator = get_arshidni_club_for_user(request.user).coordinator
            if arshidni_coordinator:
                email_context = {'arshidni_coordinator': arshidni_coordinator,
                                 'graduate_profile': new_graduate_profile,
                                 'full_url': full_url}
                mail.send([arshidni_coordinator.email],
                          template="graduate_profile_submitted",
                          context=email_context)
            return HttpResponseRedirect(graduate_profile_url)
        else:
            context = {'form': form}
    elif request.method == 'GET':
        # Allow only students to sign up as graduates.
        try:
            common_profile = request.user.common_profile
            is_student = request.user.common_profile.is_student
        except ObjectDoesNotExist:
            is_student = False

        if is_student:
            form = GraduateProfileForm()
            context = {'form': form}
        else:
            context = {'error': 'notstudent'}

    return render(request, 'arshidni/graduate_edit_profile.html', context)

@login_required
def show_graduate_profile(request, graduate_profile_id):
    graduate_profile = get_object_or_404(GraduateProfile,
                                         pk=graduate_profile_id,
                                         is_published__in=[True, None])
    context = {'graduate_profile': graduate_profile}
    return render(request, 'arshidni/graduate_show_profile.html', context)

@login_required
def edit_graduate_profile(request, graduate_profile_id):
    # Don't allow editing deleted profiles
    graduate_profile = get_object_or_404(GraduateProfile,
                                         pk=graduate_profile_id,
                                         is_published__in=[True, None])

    # Only allow the user of the profile to edit it or those with the
    # change_graduateprofile permission.
    if not request.user == graduate_profile.user and \
       not request.user.has_perm('arshidni:change_graduateprofile') and \
       not is_arshindi_coordinator_or_deputy(request.user):
        raise PermissionDenied

    context = {'edit': True, 'graduate_profile': graduate_profile}
    if request.method == 'POST':
        form = GraduateProfileForm(request.POST, instance=graduate_profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('arshidni:graduate_show_profile',
                                                args=(graduate_profile.pk,)))
        else:
            context['form'] = form
    elif request.method == 'GET':
        form = GraduateProfileForm(instance=graduate_profile)
        context['form'] = form

    return render(request, 'arshidni/graduate_edit_profile.html', context)

# Questions

def list_colleges(request):
    m_count = Question.objects.filter(college='M').count()
    d_count = Question.objects.filter(college='D').count()
    b_count = Question.objects.filter(college='B').count()
    n_count = Question.objects.filter(college='N').count()
    a_count = Question.objects.filter(college='A').count()
    p_count = Question.objects.filter(college='P').count()

    context = {'m_count': m_count, 'd_count': d_count, 'b_count':
               b_count, 'n_count': n_count, 'a_count': a_count,
               'p_count': p_count}

    return render(request, 'arshidni/list_colleges.html', context)

@login_required
def list_questions(request, college_name):
    # That's how they're stored in the database: upper-case.
    upper_college_name = college_name.upper()
    # Make sure that there are actually colleges with that name (this
    # query makes things as dynamic as possible.)
    college = get_list_or_404(College, name=upper_college_name)[0]
    college_full_name = college.get_name_display()

    form = QuestionForm()

    # If the user has the view_questions permission, show questions
    # that are pending-revision.
    if request.user.has_perm('arshidni.view_question') or \
       is_arshindi_coordinator_or_deputy(request.user):
        questions = Question.objects.filter(college=upper_college_name,
                                            is_published__in=[True, None])
    else:
        questions = Question.objects.filter(college=upper_college_name,
                                            is_published=True)

    question_filter = request.GET.get('filter')
    if question_filter == 'mine':
        filtered_questions = questions.filter(submitter=request.user)
    elif question_filter == 'day':
        one_day_ago = datetime.datetime.now() - datetime.timedelta(days=1)
        filtered_questions = questions.filter(submission_date__gte=one_day_ago)
    elif question_filter == 'week':
        one_week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
        filtered_questions = questions.filter(submission_date__gte=one_week_ago)
    elif question_filter == 'motnh':
        one_month_ago = datetime.datetime.now() - datetime.timedelta(days=30)
        filtered_questions = questions.filter(submission_date__gte=one_month_ago)
    else:
        filtered_questions = questions

    question_order = request.GET.get('order')
    # TODO: order
    if True:
        ordered_questions = filtered_questions.order_by('-submission_date')

    # Each page of results should have a maximum of 25 activities.
    paginator = Paginator(ordered_questions, 25)
    page = request.GET.get('page')

    try:
        page_questions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_questions = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_questions = paginator.page(paginator.num_pages)

    context = {'page_questions': page_questions, 'college_name':
               college_name, 'form': form, 'college_full_name':
               college_full_name}
    return render(request, 'arshidni/question_list.html', context)

@login_required
@csrf.csrf_exempt
@decorators.ajax_only
@decorators.post_only
def mark_answered(request):
    #answer_id = request.POST.get('answer_id')
    #answer = get_object_or_404(Answer, pk=answer_id)
    question_id = request.POST.get('question_id')
    question = get_object_or_404(Question, pk=question_id)

    if not question.submitter == request.user and \
       not request.user.has_perm('arshidni.change_question') and \
       not is_arshindi_coordinator_or_deputy(request.user):
        raise PermissionDenied

    if question.is_answered:
        raise Exception(u'سبق اعتبار هذا السؤال مجابا عليه')

    question.is_answered = True
    question.save()

@login_required
def show_question(request, question_id):
    # Only show the questions that are published or pending revision
    # (i.e. don't show deleted questions.)
    question = get_object_or_404(Question, pk=question_id,
                                 is_published__in=[True, None])

    # Only show pending questions to the submitter and to those with
    # view_question.
    if not question.is_published and \
       not request.user == question.submitter and \
       not request.user.has_perm('arshidni:view_question') and \
       not is_arshindi_coordinator_or_deputy(request.user):
        raise PermissionDenied

    published_answers = Answer.objects.filter(question=question,
                                              is_published=True)

    form = AnswerForm()
    context = {'question': question, 'published_answers': published_answers, 'form': form}
    return render(request, 'arshidni/question_show.html', context)

@login_required
@permission_required('arshidni.add_question', raise_exception=True)
def submit_question(request, college_name):
    context = {'college_name': college_name}
    if request.method == 'POST':
        question_object = Question(submitter=request.user, college=college_name.upper())
        form = QuestionForm(request.POST, instance=question_object)
        if form.is_valid():
            new_question = form.save()
            return HttpResponseRedirect(reverse('arshidni:show_question',
                                                args=(new_question.pk,)))
        else:
            context['form'] = form
    elif request.method == 'GET':
        form = QuestionForm()
        context['form'] = form

    return render(request, 'arshidni/question_edit.html', context)

@login_required
def edit_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id,
                                 is_published__in=[True, None])

    if not request.user == question.submitter and \
       not request.user.has_perm('arshidni:change_question') and \
       not is_arshindi_coordinator_or_deputy(request.user):
        raise PermissionDenied

    context = {'edit': True, 'question': question}
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('arshidni:show_question',
                                                args=(question.pk,)))
        else:
            context['form'] = form
    elif request.method == 'GET':
        form = QuestionForm(instance=question)
        context['form'] = form

    return render(request, 'arshidni/question_edit.html', context)

@login_required
@decorators.post_only
@permission_required('arshidni.add_answer', raise_exception=True)
def submit_answer(request, question_id):
    question = get_object_or_404(Question, pk=question_id,
                                 is_published=True)
    answer_object = Answer(submitter=request.user, question=question)

    after_url = reverse('arshidni:show_question',
                        args=(question.pk,))

    if not question.is_editable:
        after_url += "?message=uneditable"
    else:
        form = AnswerForm(request.POST, instance=answer_object)
        if form.is_valid():
            new_answer = form.save()
            after_url += '#answer-' + str(new_answer.pk)
        else:
            after_url += "?message=answererror"

    return HttpResponseRedirect(after_url)

@login_required
def edit_answer(request, question_id, answer_id):
    # Only make it possible to edit answers for published questions
    question = get_object_or_404(Question, pk=question_id,
                               is_published=True)
    # If the answer is deleted (i.e. is_published=False), don't allow
    # editing it.
    answer = get_object_or_404(Answer, pk=answer_id,
                               is_published__in=[True, None])

    if not request.user == answer.submitter and \
       not request.user.has_perm('arshidni:change_answer') and\
       not is_arshindi_coordinator_or_deputy(request.user):
        raise PermissionDenied

    # FIXME: remove edit
    context = {'answer': answwer, 'question': question}

    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            form.save()
            after_url = reverse('arshidni:show_question',
                                args=(question_id,)) + '#answer-' + str(answer_id)
            return HttpResponseRedirect(after_url)
        else:
            context['form'] = form
    elif request.method == 'GET':
        form = AnswerForm(instance=answer)
        context['form'] = form

    return render(request, 'arshidni/answer_edit.html', context)

# Groups

def list_groups(request):
    # If the user has the view_groups permission, show groups
    # that are pending-revision.
    if request.user.has_perm('arshidni.view_group') or \
       is_arshindi_coordinator_or_deputy(request.user):
        groups = StudyGroup.objects.filter(status__in=['A', 'P'])
    else:
        user_groups = StudyGroup.objects.filter(coordinator=request.user)
        approved_groups = StudyGroup.objects.filter(status='A')
        groups = user_groups | approved_groups

    context = {'page_groups': groups}
    return render(request, 'arshidni/group_list.html', context)

@login_required
@permission_required('arshidni.add_joinstudygrouprequest', raise_exception=True)
@csrf.csrf_exempt
@decorators.ajax_only
@decorators.post_only
def join_group(request):
    group_id = request.POST.get('group_id')
    group = get_object_or_404(StudyGroup, pk=group_id)

    user_gender = get_user_gender(request.user)
    coordinator_gender = get_user_gender(group.coordinator)

    if user_gender != coordinator_gender:
        if coordinator_gender == 'F':
            raise Exception(u'المجموعة متاحة للطالبات فقط')
        elif coordinator_gender == 'M':
            raise Exception(u'المجموعة متاحة للطلاب فقط')

    if not group.max_members > group.members.count():
        raise Exception(u'المجموعة تجاوزت العدد الأقصى')

    if group.is_published == False:
        raise Exception(u'المجموعة محذوفة')
    elif group.is_published == None:
        raise Exception(u'لم تعتمد المجموعة بعد')

    # Check if user already has a join request
    previous_requests = JoinStudyGroupRequest.objects.filter(submitter=request.user, group=group)
    if previous_requests:
        raise Exception(u'سبق أن طلبت الانضمام لهذه المجموعة')
    else:
        JoinStudyGroupRequest.objects.create(submitter=request.user, group=group)

@permission_required('arshidni.add_studygroup', raise_exception=True)
@login_required
def submit_group(request):
    if request.method == 'POST':
        group_object = StudyGroup(coordinator=request.user)
        form = StudyGroupForm(request.POST, instance=group_object)
        if form.is_valid():
            new_group = form.save()
            group_url = reverse('arshidni:show_group',
                                args=(new_group.pk,))
            group_full_url = request.build_absolute_uri(group_url)
            admin_url = reverse('arshidni_admin:index')
            admin_full_url = request.build_absolute_uri(admin_url)
            arshidni_coordinator = get_arshidni_club_for_user(request.user).coordinator
            if arshidni_coordinator:
                email_context = {'arshidni_coordinator': arshidni_coordinator,
                                 'group': new_group,
                                 'full_url': group_full_url,
                                 'admin_full_url': admin_full_url}
                mail.send([arshidni_coordinator.email],
                          template="study_group_submitted",
                          context=email_context)
            return HttpResponseRedirect(group_url)
        else:
            context = {'form': form}
    elif request.method == 'GET':
        form = StudyGroupForm()
        context = {'form': form}

    return render(request, 'arshidni/group_edit.html', context)

@login_required
def edit_group(request, group_id):
    # TODO: If it has been approved, the dates cannot be edited.
    group = get_object_or_404(StudyGroup, pk=group_id,
                              is_published__in=[True, None])

    if not request.user == group.coordinator and \
       not request.user.has_perm('arshidni:change_group') and \
       not is_arshindi_coordinator_or_deputy(request.user):
        raise PermissionDenied

    context = {'edit': True, 'group': group}
    if request.method == 'POST':
        form = StudyGroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('arshidni:show_group',
                                                args=(group.pk,)))
        else:
            context['form'] = form
    elif request.method == 'GET':
        form = StudyGroupForm(instance=group)
        context['form'] = form

    return render(request, 'arshidni/group_edit.html', context)

@login_required
@decorators.get_only
def show_group(request, group_id):
    # If the group is deleted, it can only be seen in the admin
    # interface.
    group = get_object_or_404(StudyGroup, pk=group_id,
                              status__in=['A', 'P'],
                              is_published__in=[True, None])

    # If the group is not approved, only show it to the coordinator
    # and to those with view_group permission.
    if not group.status == 'A' and \
       not request.user == group.coordinator and \
       not request.user.has_perm('arshidni.view_group') and \
       not is_arshindi_coordinator_or_deputy(request.user):
        raise PermissionDenied

    previous_request = JoinStudyGroupRequest.objects.filter(submitter=request.user, group=group)

    context = {'group': group, 'previous_request': previous_request}
    return render(request, 'arshidni/group_show.html', context)

@login_required
def join_group_requests(request, group_id):
    group = get_object_or_404(StudyGroup, pk=group_id,
                              status__in=['A', 'P'],
                              is_published=True)

    # Only the coordinator and people with the change_group permission
    # can handle join group requests.
    if not request.user == group.coordinator and \
       not request.user.has_perm('arshidni.change_group') and \
       not is_arshindi_coordinator_or_deputy(request.user):
        raise PermissionDenied

    context = {'group': group}
    return render(request, 'arshidni/group_requests.html', context)

@login_required
@csrf.csrf_exempt
@decorators.ajax_only
@decorators.post_only
def group_action(request):
    join_request_id = request.POST.get('request_id')
    action = request.POST.get('action')
    join_request = get_object_or_404(JoinStudyGroupRequest, pk=join_request_id)
    group = join_request.group

    coordinator = join_request.group.coordinator

    if coordinator != request.user:
        raise Exception(u'الطلب ليس موجها لك!')

    if action == 'accept':
        if join_request.is_accepted:
            raise Exception(u'سبق أن استجبت لهذا الطلب.')
        else:
            join_request.is_accepted = True
            group.members.add(join_request.submitter)
            join_request.save()
            group.save()
    elif action == 'reject':
        if join_request.is_accepted == False:
            raise Exception(u'سبق أن استجبت لهذا الطلب.')
        else:
            join_request.is_accepted = False
            group.members.remove(join_request.submitter)
            join_request.save()
            group.save()
    else:
        raise Exception(u'حدث خطأ غير معروف.')

    return  {'current_status': join_request.is_accepted,
             'full_current_status': join_request.get_is_accepted_display()}

def search_groups(request):
    pass

# Student colleague 

@login_required
def list_colleagues(request):
    # If the user has the view_colleague_profiles permission, show
    # colleague_profiles that are pending-revision.
    if is_arshindi_coordinator_or_deputy(request.user) or \
       request.user.has_perm('arshidni.view_colleagueprofile'):
        user_colleagues = ColleagueProfile.objects.current_year().for_user_city(request.user)
        city = get_user_city(request.user)
        # For cities other than Riyadh, we have gender-unspecific
        # Arshidni (yay).
        if city == 'R':
            user_colleagues = user_colleagues.for_user_gender(request.user)
        available = user_colleagues.available().published()
        unavailable = user_colleagues.filter(Q(is_available=False) | Q(is_published__isnull=True))
    else:
        user_colleagues = ColleagueProfile.objects.current_year().for_user_gender(request.user).for_user_city(request.user).published() 
        available = user_colleagues.available()
        unavailable = user_colleagues.unavailable()
    context = {'available': available, 'unavailable': unavailable}
    return render(request, 'arshidni/colleague_list.html', context)

@login_required
@permission_required('arshidni.add_supervisionrequest', raise_exception=True)
def submit_supervision_request(request, colleague_profile_id):
    colleague_profile = get_object_or_404(ColleagueProfile.objects.current_year(),
                                          pk=colleague_profile_id,
                                          is_published=True)
    context = {'colleague_profile': colleague_profile}
    if request.method == 'POST':
        request_object = SupervisionRequest(user=request.user,
                                            colleague=colleague_profile)
        form = SupervisionRequestForm(request.POST, instance=request_object)
        if form.is_valid():
            new_request = form.save()
            to_me_url = reverse('arshidni:supervision_requests_to_me')
            full_url = request.build_absolute_uri(to_me_url)
            email_context = {'full_url': full_url,
                             'supervision_request': new_request,
                             'colleague_profile': colleague_profile}
            mail.send([colleague_profile.user.email],
                      template="supervision_request_submitted",
                      context=email_context)
            after_url = reverse('arshidni:my_supervision_requests') + '#request-' + str(new_request.pk)
            return HttpResponseRedirect(after_url)
        else:
            context['form'] = form
    elif request.method == 'GET':
        # Check if the user has any pending or accepted supervision
        # requests
        accepted_student_requests = SupervisionRequest.objects.filter(user=request.user, status='A')
        pending_student_requests = SupervisionRequest.objects.filter(user=request.user, status='P')
        # Check if the colleague has exceeded the supervision limit.
        colleague_supervisions = colleague_profile.supervision_requests.accepted()
        if colleague_supervisions.filter(user=request.user).exists():
            context['error'] = 'already_supervisor'
        elif accepted_student_requests.exists():
            context['error'] = 'accepted_supervision_requests'
        elif pending_student_requests.exists():
            context['error'] = 'pending_supervision_requests'
        elif colleague_supervisions.count() >= COLLEAGUE_SUPERVISION_LIMIT:
            context['error'] = 'colleague_supervision_limit'
        elif get_user_gender(request.user) != get_user_gender(colleague_profile.user):
            context['error'] = 'gender'
        else:
            form = SupervisionRequestForm()
            context['form'] = form

    return render(request, 'arshidni/colleague_choose.html', context)

@login_required
def register_colleague_profile(request):
    # Any changes to this view will probably also apply to
    # register_graduate_profile.
    
    # Check if the user already has a profile. If so, redirect them to
    # the edit page.
    try:
        current_profile = ColleagueProfile.objects.current_year().get(user=request.user)
        return HttpResponseRedirect(reverse('arshidni:edit_colleague_profile',
                                                args=(current_profile.pk,)))
    except ObjectDoesNotExist:
        pass

    if request.method == 'POST':
        current_year = StudentClubYear.objects.get_current()
        colleague_object = ColleagueProfile(user=request.user, year=current_year)
        form = ColleagueProfileForm(request.POST, instance=colleague_object)
        if form.is_valid():
            new_colleague = form.save()
            return HttpResponseRedirect(reverse('arshidni:show_colleague_profile',
                                                args=(new_colleague.pk,)))
        else:
            context = {'form': form}
    elif request.method == 'GET':
        # Allow only students to sign up as colleagues.
        try:
            common_profile = request.user.common_profile
            is_student = request.user.common_profile.is_student
        except ObjectDoesNotExist:
            is_student = False

        if is_student:
            form = ColleagueProfileForm()
            context = {'form': form}
        else:
            context = {'error': 'notstudent'}

    return render(request, 'arshidni/colleague_edit_profile.html', context)

@login_required
def show_colleague_profile(request, colleague_profile_id):
    colleague_profile = get_object_or_404(ColleagueProfile.objects.current_year(),
                                          pk=colleague_profile_id,
                                          is_published__in=[True,
                                                            None])
    # If the profile is not published, only show to its user or to
    # those with change_colleagueprofile.
    if not colleague_profile.is_published and \
       not request.user == colleague_profile.user and \
       not request.user.has_perm('arshidni:view_colleagueprofile') and \
       not is_arshindi_coordinator_or_deputy(request.user):
        raise PermissionDenied

    context = {'colleague_profile': colleague_profile}
    return render(request, 'arshidni/colleague_show_profile.html', context)

@login_required
def edit_colleague_profile(request, colleague_profile_id):
    # Don't allow editing deleted profiles
    colleague_profile = get_object_or_404(ColleagueProfile.objects.current_year(),
                                          pk=colleague_profile_id,
                                          is_published__in=[True, None])

    # Only allow the user of the profile to edit it or those with the
    # change_colleagueprofile permission.
    if not request.user == colleague_profile.user and \
       not request.user.has_perm('arshidni:change_colleagueprofile') and \
       not is_arshindi_coordinator_or_deputy(request.user):
        raise PermissionDenied

    context = {'edit': True, 'colleague_profile': colleague_profile}
    if request.method == 'POST':
        form = ColleagueProfileForm(request.POST, instance=colleague_profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('arshidni:show_colleague_profile',
                                                args=(colleague_profile.pk,)))
        else:
            context['form'] = form
    elif request.method == 'GET':
        form = ColleagueProfileForm(instance=colleague_profile)
        context['form'] = form

    return render(request, 'arshidni/colleague_edit_profile.html', context)

@login_required
def supervision_requests_to_me(request):
    try:
        colleague_profile = ColleagueProfile.objects.current_year().get(user=request.user)
    except ObjectDoesNotExist:
        colleague_profile = None

    if colleague_profile:
        # No need to show the requests that were removed for
        # acceptance.  They could be just a mistake.
        supervision_requests = SupervisionRequest.objects.filter(colleague=colleague_profile,
                                                                 status__in=['P', 'A', 'R', 'WC', 'WN'])

        context = {'colleague_profile': colleague_profile, 'page_requests': supervision_requests}
    else:
        context = {}

    return render(request, 'arshidni/supervision_requests_to_me.html', context)

@login_required
def my_supervision_requests(request):
    # TODO: [Arshidni-wide] if you the user is colleague himself, they
    # shouldn't be able to submit any requests.
    supervision_requests = SupervisionRequest.objects.current_year().filter(user=request.user)

    context = {'page_requests': supervision_requests}
    return render(request, 'arshidni/my_supervision_requests.html', context)


@login_required
@csrf.csrf_exempt
@decorators.ajax_only
@decorators.post_only
def student_action(request):
    supervision_request_id = request.POST.get('supervision_request_id')
    action = request.POST.get('action')
    supervision_request = get_object_or_404(SupervisionRequest.objects.current_year(),
                                            pk=supervision_request_id)

    if supervision_request.user != request.user:
        raise Exception(u'لست أنت مقدم الطلب!')

    if action == 'delete':
        if supervision_request.status == 'A':
            now = datetime.datetime.now()
            supervision_request.status = 'WN'
            supervision_request.withdrawal_date = now
            to_me_url = reverse('arshidni:supervision_requests_to_me')
            full_url = request.build_absolute_uri(to_me_url)
            arshidni_coordinator = get_arshidni_club_for_user(request.user).coordinator
            if arshidni_coordinator:
                email_context = {'full_url': full_url,
                                 'supervision_request': supervision_request}
                mail.send([supervision_request.colleague.user.email],
                          cc=[arshidni_coordinator.email],
                          template="supervision_request_withdrawn",
                          context=email_context)
        elif supervision_request.status == 'P':
            supervision_request.status = 'D'
        else: # Just in case
            raise Exception(u'حدث خطأ غير معروف.')
        supervision_request.save()
    else:
        raise Exception(u'حدث خطأ غير معروف.')

    return  {'current_status': supervision_request.status,
             'full_current_status': supervision_request.get_status_display()}

@login_required
@csrf.csrf_exempt
@decorators.ajax_only
@decorators.post_only
def colleague_action(request):
    supervision_request_id = request.POST.get('supervision_request_id')
    action = request.POST.get('action')
    supervision_request = get_object_or_404(SupervisionRequest.objects.current_year(),
                                            pk=supervision_request_id)
    colleague_profile = supervision_request.colleague

    if colleague_profile.user != request.user:
        raise Exception(u'الطلب ليس موجها لك!')

    if action == 'accept':
        if supervision_request.status == 'A':
            raise Exception(u'سبق أن استجبت لهذا الطلب.')
        elif supervision_request.status in ['P', 'R']:
            # We accept 'R' as a previous status to allow the user to
            # undo an immediate mistake.
            supervision_request.status = 'A'
            supervision_request.save()
            if colleague_profile.supervision_requests.accepted().count() >= COLLEAGUE_SUPERVISION_LIMIT:
                colleague_profile.is_available = False
                colleague_profile.save()
            mine_url = reverse('arshidni:my_supervision_requests')
            full_url = request.build_absolute_uri(mine_url)
            arshidni_coordinator = get_arshidni_club_for_user(request.user).coordinator
            if arshidni_coordinator:
                email_context = {'full_url': full_url,
                                 'supervision_request': supervision_request}
                mail.send([supervision_request.user.email],
                          cc=[arshidni_coordinator.email],
                          template="supervision_request_accepted",
                          context=email_context)
        else: # Just in case
            raise Exception(u'حدث خطأ غير معروف.')

    elif action == 'reject':
        if supervision_request.status == 'R':
            raise Exception(u'سبق أن استجبت لهذا الطلب.')
        elif supervision_request.status == 'A':
            now = datetime.datetime.now()
            supervision_request.status = 'WC'
            supervision_request.withdrawal_date = now
            colleague_profile.is_available = True
            colleague_profile.save()
        elif supervision_request.status == 'P':
            supervision_request.status = 'R'
        else: # Just in case
            raise Exception(u'حدث خطأ غير معروف.')
        supervision_request.save()
    else:
        raise Exception(u'حدث خطأ غير معروف.')

    return  {'current_status': supervision_request.status,
             'full_current_status': supervision_request.get_status_display(),
             'contacts': supervision_request.contacts}
