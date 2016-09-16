from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from post_office import mail

from clubs.models import college_choices
from events.forms import NonUserForm, RegistrationForm, AbstractForm, AbstractFigureFormset
from events.models import Event, Registration, Session, Abstract, AbstractFigure
from events import utils

def redirect_home(request, event_code_name):
    event = get_object_or_404(Event, code_name=event_code_name)
    if event.url:
        return HttpResponseRedirect(event.url)
    else:
        return HttpResponseRedirect(reverse('events:registration_introduction',
                                            args=(event.code_name,)))

def submit_abstract(request, event_code_name):
    event = get_object_or_404(Event, code_name=event_code_name,
                              receives_abstract_submission=True)
    context = {'event': event}

    if event.abstract_submission_opening_date and timezone.now() < event.abstract_submission_opening_date:
        return render(request, 'events/abstracts/abstract_not_started.html', context)
    elif event.abstract_submission_closing_date and timezone.now() > event.abstract_submission_closing_date:
        return render(request, 'events/abstracts/abstract_closed.html', context)

    if request.method == 'POST':
        instance = Abstract(event=event)
        form = AbstractForm(request.POST, request.FILES,
                            instance=instance)
        figure_formset = AbstractFigureFormset(request.POST, request.FILES)
        if form.is_valid() and figure_formset.is_valid():
            abstract = form.save()
            figure_formset.instance = abstract
            figure_formset.save()
            return HttpResponseRedirect(reverse('events:abstract_submision_completed'))

    elif request.method == 'GET':
        form = AbstractForm()
        figure_formset = AbstractFigureFormset()

    context = {'form': form,
               'figure_formset': figure_formset}
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
def show_abstract(request, event_code_name, pk):
    abstract = get_object_or_404(Abstract, pk=pk, is_deleted=False)
    event = abstract.event

    if not utils.can_evaluate_abstracts(request.user, event):
        raise PermissionDenied

    try:
        evaluation = abstract.evaluation
    except Evaluation.DoesNotExist:
        evaluation = Evaluation(evaluator=request.user,
                                abstract=abstract)

    if request.method == 'POST':
        form = EvaluationForm(request.POST, instance=evaluation)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('events:list_abstracts'))
    elif request.method == 'GET':
        form = EvaluationForm(instance=evaluation)
    context = {'event': event, 'abstract': abstract, 'form': form}

    return render(request, "events/abstracts/show_abstract.html", context)

def list_sessions(request, event_code_name):
    event = get_object_or_404(Event, code_name=event_code_name)
    context = {'sessions': Session.objects.filter(event=event),
               'event': event}
    return render(request, 'events/session_list.html', context)

def show_session(request, event_code_name, pk):
    event = get_object_or_404(Event, code_name=event_code_name)
    session = get_object_or_404(Session, pk=pk, event=event)
    return render(request, 'events/session_show.html',
                  {'session': session})

def introduce_registration(request, event_code_name):
    event = get_object_or_404(Event, code_name=event_code_name)
    utils.check_if_closed(event)
    if request.user.is_authenticated() and \
       not utils.is_organizing_club_member(request.user, event) and \
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
                for session in registrations.first_priority_sessions.all():
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
    if not utils.is_organizing_club_member(request.user, event) and \
       not request.user.is_superuser:
        raise PermissionDenied

    sessions = Session.objects.filter(event=event)
    return render(request, "events/registration_list.html",
                  {'event': event, 'sessions': sessions})

@login_required
def show_session_privileged(request, event_code_name, pk):
    event = get_object_or_404(Event, code_name=event_code_name)
    session = get_object_or_404(Session, pk=pk, event=event)
    if not utils.is_organizing_club_member(request.user, event) and \
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
