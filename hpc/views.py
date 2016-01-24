from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from post_office import mail

from clubs.models import college_choices
from hpc.forms import AbstractForm, EvaluationForm, NonUserForm, RegistrationForm
from hpc.models import Abstract, Evaluation, Registration, Session
from hpc import utils


def submit_abstract(request):
    if datetime.now() > datetime(2015, 12, 27, 23, 59):
        return render(request, 'hpc/abstract_closed.html')
    if request.method == 'POST':
        form = AbstractForm(request.POST, request.FILES)
        if form.is_valid():
            abstract = form.save()
            return HttpResponseRedirect(reverse('hpc:abstract_submision_completed'))

    elif request.method == 'GET':
        form = AbstractForm()

    return render(request, 'hpc/abstract_submission.html', {'form': form})

@login_required
def list_abstracts(request):
    if not utils.is_research_committee_member(request.user) and \
       not utils.is_organizing_committee_member(request.user) and \
       not request.user.is_superuser:
        raise PermissionDenied

    pending_abstracts = Abstract.objects.filter(is_deleted=False, evaluation__isnull=True)
    evaluated_abstracts = Abstract.objects.filter(is_deleted=False, evaluation__isnull=False)

    # The Research Committee is only concerned about abstracts from
    # the university.  The rest will be evaluated by the Organizing
    # Committee.
    if utils.is_research_committee_member(request.user):
        pending_abstracts = pending_abstracts.filter(university="KSAU-HS")
        evaluated_abstracts = evaluated_abstracts.filter(university="KSAU-HS")
    elif utils.is_organizing_committee_member(request.user):
        pending_abstracts = pending_abstracts.exclude(university="KSAU-HS")
        evaluated_abstracts = evaluated_abstracts.exclude(university="KSAU-HS")

    context = {'pending_abstracts': pending_abstracts,
               'evaluated_abstracts': evaluated_abstracts}

    return render(request, 'hpc/list_abstracts.html', context)

def list_sessions(request):
    return render(request, 'hpc/session_list.html',
                  {'sessions': Session.objects.all()})

def show_session(request, pk):
    session = get_object_or_404(Session, pk=pk)
    return render(request, 'hpc/session_show.html',
                  {'session': session})

@login_required
def show_abstract(request, pk):
    if not utils.is_research_committee_member(request.user) and \
       not utils.is_organizing_committee_member(request.user) and \
       not request.user.is_superuser:
        raise PermissionDenied

    abstract = get_object_or_404(Abstract, pk=pk, is_deleted=False)
    try:
        evaluation = abstract.evaluation
    except Evaluation.DoesNotExist:
        evaluation = Evaluation(evaluator=request.user,
                                abstract=abstract)

    if request.method == 'POST':
        form = EvaluationForm(request.POST, instance=evaluation)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('hpc:list_abstracts'))
    elif request.method == 'GET':
        form = EvaluationForm(instance=evaluation)

    return render(request, "hpc/show_abstract.html",
                  {'abstract': abstract, 'form': form})

def introduce_registration(request):
    if datetime.now() > datetime(2016, 1, 17, 23, 59):
        return HttpResponseRedirect(reverse('hpc:registration_closed'))
    if request.user.is_authenticated() and \
       not utils.is_organizing_committee_member(request.user) and \
       not request.user.is_superuser:
        return HttpResponseRedirect(reverse('hpc:user_registration'))
    else:
        return render(request, "hpc/registration_introduction.html")

def nonuser_registration(request):
    if datetime.now() > datetime(2016, 1, 17, 23, 59):
        return HttpResponseRedirect(reverse('hpc:registration_closed'))
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('hpc:user_registration'))
    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST)
        nonuser_form = NonUserForm(request.POST)
        if registration_form.is_valid() and nonuser_form.is_valid():
            nonuser = nonuser_form.save()
            registration_form.save(nonuser=nonuser)
            mail.send([nonuser.email],
                      template="hpc_registration_submitted",
                      context={'name': nonuser.ar_first_name})
            return HttpResponseRedirect(reverse('hpc:registration_completed'))
    elif request.method == 'GET':
        registration_form = RegistrationForm()
        nonuser_form = NonUserForm()

    male_time_slot_2_choices = Session.objects.filter(time_slot=2, gender__in=['', 'M'])\
                                              .values_list('pk', 'name')
    female_time_slot_2_choices = Session.objects.filter(time_slot=2, gender__in=['', 'F'])\
                                                .values_list('pk', 'name')
    male_time_slot_3_choices = Session.objects.filter(time_slot=3, gender__in=['', 'M'])\
                                              .values_list('pk', 'name')
    female_time_slot_3_choices = Session.objects.filter(time_slot=3, gender__in=['', 'F'])\
                                                .values_list('pk', 'name')

    context = {'registration_form': registration_form,
               'nonuser_form': nonuser_form,
               'college_choices': college_choices,
               'male_time_slot_2_choices': male_time_slot_2_choices,
               'female_time_slot_2_choices': female_time_slot_2_choices,
               'male_time_slot_3_choices': male_time_slot_3_choices,
               'female_time_slot_3_choices': female_time_slot_3_choices}

    return render(request, "hpc/register_nonuser.html", context)

def user_registration(request):
    if datetime.now() > datetime(2016, 1, 17, 23, 59):
        return HttpResponseRedirect(reverse('hpc:registration_closed'))
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('hpc:registration_introduction'))

    try:
        if request.user.hpc2016_registration:
            return HttpResponseRedirect(reverse('hpc:registration_already'))
    except Registration.DoesNotExist:
        pass

    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST, user=request.user)
        if registration_form.is_valid():
            registration_form.save(user=request.user)
            mail.send([request.user.email],
                      template="hpc_registration_submitted",
                      context={'name': request.user.common_profile.ar_first_name})

            return HttpResponseRedirect(reverse('hpc:registration_completed'))
    elif request.method == 'GET':
        registration_form = RegistrationForm(user=request.user)

    context = {'registration_form': registration_form}
    return render(request, "hpc/register_user.html", context)

@login_required
def list_registrations(request):
    if not utils.is_organizing_committee_member(request.user) and \
       not request.user.is_superuser:
        raise PermissionDenied

    sessions = Session.objects.all()
    return render(request, "hpc/registration_list.html",
                  {'sessions': sessions})
