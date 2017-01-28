# -*- coding: utf-8  -*-
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.views.decorators import csrf
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from post_office import mail
import os.path

from core import decorators
from clubs.models import college_choices
from events.forms import NonUserForm, RegistrationForm, AbstractForm, AbstractFigureFormset, EvaluationForm,AbstractFigureForm, InitiationForm, InitiationFigureFormset
from events.models import Event, Registration, Session, Abstract, AbstractFigure,Evaluation, TimeSlot, SessionRegistration, Initiation
from events import utils

def redirect_home(request, event_code_name):
    event = get_object_or_404(Event, code_name=event_code_name)
    if event.url:
        return HttpResponseRedirect(event.url)
    elif event.is_registration_open():
        return HttpResponseRedirect(reverse('events:registration_introduction',
                                            args=(event.code_name,)))
    elif event.is_abstract_submission_open():
        return HttpResponseRedirect(reverse('events:submit_abstract',
                                            args=(event.code_name,)))
    else:
        raise Http404

@login_required
def submit_abstract(request, event_code_name):
    event = get_object_or_404(Event, code_name=event_code_name,
                              receives_abstract_submission=True)
    context = {'event': event}

    if event.abstract_submission_opening_date and timezone.now() < event.abstract_submission_opening_date:
        return render(request, 'events/abstracts/abstract_not_started.html', context)
    elif event.abstract_submission_closing_date and timezone.now() > event.abstract_submission_closing_date:
        return render(request, 'events/abstracts/abstract_closed.html', context)

    if request.method == 'POST':
        instance = Abstract(event=event,user=request.user)
        form = AbstractForm(request.POST, request.FILES,
                            instance=instance)
        figure_formset = AbstractFigureFormset(request.POST, request.FILES)
        if form.is_valid():
            abstract = form.save()
            return HttpResponseRedirect(reverse('events:show_abstract',
                                                args=(event.code_name, abstract.pk)))
    elif request.method == 'GET':
        form = AbstractForm()
        figure_formset = AbstractFigureFormset()
    context['form'] = form
    context['figure_formset'] = figure_formset

    return render(request, 'events/abstracts/abstract_submission.html', context)

@login_required
def list_abstracts(request, event_code_name):
    event = get_object_or_404(Event, code_name=event_code_name,
                              receives_abstract_submission=True)
    if not utils.can_evaluate_abstracts(request.user, event):
        raise PermissionDenied

    pending_abstracts = Abstract.objects.filter(event=event, is_deleted=False, evaluation__isnull=True)
    evaluated_abstracts = Abstract.objects.filter(event=event, is_deleted=False, evaluation__isnull=False)

    context = {'event': event,
               'pending_abstracts': pending_abstracts,
               'evaluated_abstracts': evaluated_abstracts}

    return render(request, 'events/abstracts/list_abstracts.html', context)

@login_required
def list_my_abstracts(request):
    abstracts =  Abstract.objects.filter(is_deleted=False, user=request.user)

    context = {'abstracts': abstracts}
    return render(request, 'events/abstracts/list_my_abstracts.html', context)

@login_required
def show_abstract(request, event_code_name, pk):
    abstract = get_object_or_404(Abstract, is_deleted=False, pk=pk)
    event = abstract.event

    if not abstract.user == request.user and \
       not request.user.is_superuser:
        raise PermissionDenied

    context= {'event':event, 'abstract':abstract}
    return render(request, "events/abstracts/show_abstract.html", context)

@decorators.ajax_only
@decorators.post_only
@csrf.csrf_exempt
@login_required
def upload_abstract_image(request):
    form = AbstractFigureForm(request.POST, request.FILES)
    if form.is_valid():
        abstract_figure = form.save()
        return {"uploaded": 1,
                "fileName": os.path.basename(abstract_figure.upload.url),
                "url": abstract_figure.upload.url}
    else:
        return {"uploaded": 0,
                "error": {
                    "message": u"لم أستطع رفع الملف"}
                }

def list_sessions(request, event_code_name):
    event = get_object_or_404(Event, code_name=event_code_name)
    time_slots = TimeSlot.objects.filter(event=event)
    context = {'time_slots': time_slots,
               'event': event}
    return render(request, 'events/session_list.html', context)

def show_session(request, event_code_name, pk):
    event = get_object_or_404(Event, code_name=event_code_name)
    session = get_object_or_404(Session, pk=pk, event=event)
    return render(request, 'events/session_show.html',
                  {'session': session})

@decorators.post_only
@decorators.ajax_only
@csrf.csrf_exempt
def handle_ajax(request):
    action = request.POST.get('action')
    session_pk = request.POST.get('pk')
    session = get_object_or_404(Session, pk=session_pk)
    SessionRegistration.objects.filter(session=session, user=request.user)

    if action == 'signup':
        if not SessionRegistration.objects.filter(session=session, user=request.user, is_deleted=False).count() <= session.limit :
            raise Exception(u'Session is full')
        else:
            if not SessionRegistration.objects.filter(session=session, user=request.user).exists():
                SessionRegistration.objects.create(session=session, user=request.user)

            elif SessionRegistration.objects.filter(session=session, user=request.user, is_deleted=True).exists():
                SessionRegistration.objects.filter(session=session, user=request.user).update(is_deleted=False)

            else:
                raise Exception(u'You are already registered!')

    elif action == 'cancel':
        if not SessionRegistration.objects.filter(session=session, user=request.user).exists():
            raise Exception(u'You did not registered yet!')

        else:
            SessionRegistration.objects.filter(session=session, user=request.user).update(is_deleted=True)

    return {}


def introduce_registration(request, event_code_name):
    event = get_object_or_404(Event, code_name=event_code_name)
    utils.check_if_closed(event)
    if request.user.is_authenticated() and \
       not utils.is_organizing_team_member(request.user, event) and \
       not request.user.is_superuser:
        return HttpResponseRedirect(reverse('events:user_registration',
                                            args=(event.code_name,)))
    else:
        context = {'event': event}
        return render(request, "events/registration_introduction.html",
                      context)

def nonuser_registration(request, event_code_name):
    event = get_object_or_404(Event, code_name=event_code_name)
    utils.check_if_closed(event)
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('events:user_registration',
                                            args=(event.code_name,)))
    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST, event=event)
        nonuser_form = NonUserForm(request.POST)
        if registration_form.is_valid() and nonuser_form.is_valid():
            nonuser = nonuser_form.save()
            registration = registration_form.save(nonuser=nonuser)
            if event.onsite_after and timezone.now() >= event.onsite_after:
                for session in registration.first_priority_sessions.all():
                    utils.register_in_vma(session, registration)
                utils.send_onsite_confirmation(registration, event)
            else:
                email_context = {'name': nonuser.ar_first_name,
                                 'event': event}
                mail.send([nonuser.email],
                          template="event_registration_submitted",
                          context=email_context)
            return HttpResponseRedirect(reverse('events:registration_completed',
                                                args=(event.code_name,)))
    elif request.method == 'GET':
        registration_form = RegistrationForm(event=event)
        nonuser_form = NonUserForm()

    session_choices = Session.objects.filter(event=event,
                                             time_slot=1)\
                                     .values_list('pk', 'name')

    context = {'event': event,
               'registration_form': registration_form,
               'nonuser_form': nonuser_form,
               'college_choices': college_choices,
               'session_choices': session_choices}

    return render(request, "events/register_nonuser.html", context)

def user_registration(request, event_code_name):
    event = get_object_or_404(Event, code_name=event_code_name)
    utils.check_if_closed(event)
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('events:registration_introduction',
                                            args=(event.code_name,)))

    if Registration.objects.filter(user=request.user,
                                   first_priority_sessions__event=event,
                                   is_deleted=False):

        return HttpResponseRedirect(reverse('events:registration_already',
                                            args=(event.code_name,)))

    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST, user=request.user, event=event)
        if registration_form.is_valid():
            registration = registration_form.save()
            print registration
            if event.onsite_after and timezone.now() >= event.onsite_after:
                for session in registration.first_priority_sessions.all():
                    utils.register_in_vma(session, registration)
                utils.send_onsite_confirmation(registration, event)
            else:
                context_email = {'name': request.user.common_profile.ar_first_name,
                                 'event': event}
                mail.send([request.user.email],
                          template="event_registration_submitted",
                          context=context_email)
            return HttpResponseRedirect(reverse('events:registration_completed',
                                                args=(event.code_name,)))
    elif request.method == 'GET':
        registration_form = RegistrationForm(user=request.user, event=event)

    context = {'registration_form': registration_form, 'event': event}
    return render(request, "events/register_user.html", context)

@login_required
def list_registrations(request, event_code_name):
    event = get_object_or_404(Event, code_name=event_code_name)
    if not utils.is_organizing_team_member(request.user, event) and \
       not request.user.is_superuser:
        raise PermissionDenied

    sessions = Session.objects.filter(event=event)
    return render(request, "events/registration_list.html",
                  {'event': event, 'sessions': sessions})

@login_required
def show_session_privileged(request, event_code_name, pk):
    event = get_object_or_404(Event, code_name=event_code_name)
    session = get_object_or_404(Session, pk=pk, event=event)
    if not utils.is_organizing_team_member(request.user, event) and \
       not request.user.is_superuser:
        raise PermissionDenied

    return render(request, 'events/session_show_privileged.html',
                  {'session': session, 'event': event})

def registration_completed(request, event_code_name):
    event = get_object_or_404(Event, code_name=event_code_name)
    return render(request, 'events/registration_completed.html',
                  {'event': event})

def registration_already(request, event_code_name):
    event = get_object_or_404(Event, code_name=event_code_name)
    return render(request, 'events/registration_already.html',
                  {'event': event})

def registration_closed(request, event_code_name):
    event = get_object_or_404(Event, code_name=event_code_name)
    return render(request, 'events/registration_closed.html',
                  {'event': event})

@login_required
def submit_initiation(request, event_code_name):
    event = get_object_or_404(Event, code_name=event_code_name,
                              receives_initiation_submission=True)
    context = {'event': event}

    if event.initiation_submission_opening_date and timezone.now() < event.initiation_submission_opening_date:
        return render(request, 'events/initiations/initiation_not_started.html', context)
    elif event.initiation_submission_closing_date and timezone.now() > event.initiation_submission_closing_date:
        return render(request, 'events/initiations/initiation_closed.html', context)

    if request.method == 'POST':
        instance = Initiation(event=event,user=request.user)
        form = InitiationForm(request.POST, request.FILES,
                            instance=instance)
        figure_formset = InitiationFigureFormset(request.POST, request.FILES)
        if form.is_valid():
            initiation = form.save()
            return HttpResponseRedirect(reverse('events:initiation_submission_completed',
                                                args=(event.code_name)))
    elif request.method == 'GET':
        form = InitiationForm()
        figure_formset = InitiationFigureFormset()
    context['form'] = form
    context['figure_formset'] = figure_formset

    return render(request, 'events/initiations/initiation_submission.html', context)
