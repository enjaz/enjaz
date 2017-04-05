# -*- coding: utf-8  -*-
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import HttpResponseRedirect, Http404
from django.views.decorators import csrf
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from post_office import mail
import os.path

from core import decorators
from clubs.models import Team, college_choices
from events.forms import NonUserForm, RegistrationForm, AbstractForm, AbstractFigureFormset, EvaluationForm,AbstractFigureForm, InitiativeForm, InitiativeFigureFormset,CaseReportForm
from events.models import Event, Registration, Session, Abstract, AbstractFigure,Evaluation, TimeSlot, SessionRegistration, Initiative, SessionGroup,CaseReport
from events import utils
import core.utils
import clubs.utils


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
        if form.is_valid() and figure_formset.is_valid():
            abstract = form.save()
            figure_formset.instance = abstract
            figure_formset.save()
            return HttpResponseRedirect(reverse('events:show_abstract',
                                                args=(event.code_name, abstract.pk)))
    elif request.method == 'GET':
        form = AbstractForm()
        figure_formset = AbstractFigureFormset()
    context['form'] = form
    context['figure_formset'] = figure_formset

    return render(request, 'events/abstracts/abstract_submission.html', context)

@decorators.ajax_only
@login_required
def edit_abstract(request, event_code_name, pk):
    abstract = get_object_or_404(Abstract, is_deleted=False,
                                 event__code_name=event_code_name,
                                 pk=pk)

    context = {'abstract': abstract}

    if not abstract.user == request.user and \
            not request.user.is_superuser and \
            not utils.is_organizing_team_member(request.user, abstract.event):
        raise PermissionDenied

    if abstract.event.abstract_submission_closing_date and timezone.now() > abstract.event.abstract_submission_closing_date:
        raise Exception(u"انتهت المدة المتاحة لتعديل الملخص ")

    if request.method == 'POST':
        instance = Abstract(event=abstract.event,user=request.user)
        form = AbstractForm(request.POST, request.FILES,
                            instance=instance)
        figure_formset = AbstractFigureFormset(request.POST, request.FILES)
        if form.is_valid() and figure_formset.is_valid():
            abstract = form.save()
            figure_formset.instance = abstract
            figure_formset.save()
            show_abstract_url = reverse('events:show_abstract', args=(event.code_name, abstract.pk))
            full_url = request.build_absolute_uri(show_abstract_url)

            return {"message": "success", "show_url": full_url}
    elif request.method == 'GET':
        form = AbstractForm(instance=abstract)
        figure_formset = AbstractFigureFormset(instance=abstract)
    context['form'] = form
    context['figure_formset'] = figure_formset

    return render(request, 'events/abstracts/edit_abstract_form.html', context)

@login_required
@decorators.ajax_only
@decorators.post_only
@csrf.csrf_exempt
def delete_abstract(request, event_code_name, pk):
    abstract = get_object_or_404(Abstract, is_deleted=False, pk=pk)
    event = abstract.event

    if not abstract.user == request.user and \
       not request.user.is_superuser and \
       not utils.is_organizing_team_member(request.user, event):
        raise PermissionDenied

    if event.abstract_submission_closing_date and timezone.now() > event.abstract_submission_closing_date and \
        not utils.is_organizing_team_member(request.user, event):
        raise Exception(u"انتهت المدة المتاحة لحذف الملخص ")

    abstract.is_deleted = True
    abstract.save()
    list_my_abstracts_url = reverse('events:list_my_abstracts')
    full_url = request.build_absolute_uri(list_my_abstracts_url)
    return {"message": "success", "list_url": full_url}

@login_required
def list_abstracts(request, event_code_name):
    event = get_object_or_404(Event, code_name=event_code_name,
                              receives_abstract_submission=True)
    if not utils.can_evaluate_abstracts(request.user, event) and \
            not utils.is_organizing_team_member(request.user, event):
        raise PermissionDenied

    pending_abstracts = Abstract.objects.annotate(num_b=Count('evaluation')).filter(event=event, is_deleted=False,num_b__lt=2)
    evaluated_abstracts = Abstract.objects.annotate(num_b=Count('evaluation')).filter(event=event, is_deleted=False,num_b__gte=2)
    context = {'event': event,
               'pending_abstracts': pending_abstracts,
               'evaluated_abstracts': evaluated_abstracts}

    if request.method == "POST":
        action = request.POST.get('action')
        pks = [int(field.lstrip('pk_')) for field in request.POST if field.startswith('pk_')]
        print pks
        if action == "delete":
            Abstract.objects.filter(pk__in=pks).update(is_deleted=True)
        return HttpResponseRedirect(reverse('events:list_abstracts',
                                                args=(event.code_name,)))

    elif request.method == "GET":
        return render(request, 'events/abstracts/list_abstracts.html', context)

@login_required
def list_my_abstracts(request):
    abstracts = Abstract.objects.filter(is_deleted=False, user=request.user)
    casereports = CaseReport.objects.filter(is_deleted=False, user=request.user)
    context = {'abstracts': abstracts,'casereports':casereports}
    return render(request, 'events/abstracts/list_my_abstracts.html', context)

@login_required
def show_abstract(request, event_code_name, pk):
    abstract = get_object_or_404(Abstract, is_deleted=False, pk=pk)
    event = abstract.event

    if not abstract.user == request.user and \
            not request.user.is_superuser and \
            not utils.can_evaluate_abstracts(request.user, event) and \
            not utils.is_organizing_team_member(request.user, event):
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

def list_timeslots(request, event_code_name):
    event = get_object_or_404(Event, code_name=event_code_name)
    timeslots = TimeSlot.objects.filter(event=event)
    context = {'timeslots': timeslots,
               'event': event}

    if event.registration_opening_date and timezone.now() < event.registration_opening_date:
        raise Http404
    elif event.registration_closing_date and timezone.now() > event.registration_closing_date:
        return HttpResponseRedirect(reverse('events:registration_closed',
                                                args=(event.code_name,)))

    return render(request, 'events/timeslots_list.html', context)

def list_sessions(request, event_code_name, pk):
    event = get_object_or_404(Event, code_name=event_code_name)
    timeslots = TimeSlot.objects.filter(event=event, pk=pk)
    context = {'timeslots': timeslots,
               'event': event}

    if event.registration_opening_date and timezone.now() < event.registration_opening_date:
        raise Http404
    elif event.registration_closing_date and timezone.now() > event.registration_closing_date:
        return HttpResponseRedirect(reverse('events:registration_closed',
                                                args=(event.code_name,)))

    return render(request, 'events/sessions_list.html', context)

def show_session(request, event_code_name, pk):
    event = get_object_or_404(Event, code_name=event_code_name)
    session = get_object_or_404(Session, pk=pk, event=event)
    return render(request, 'events/session_show.html',
                  {'session': session})

@decorators.post_only
@decorators.ajax_only
@csrf.csrf_exempt
@login_required
def handle_ajax(request):
    action = request.POST.get('action')
    session_pk = request.POST.get('pk')
    session = get_object_or_404(Session, pk=session_pk)

    if session.acceptance_method == 'F':
        is_approved = True
    else:
        is_approved = None

    has_previous_sessions = SessionRegistration.objects.filter(session__event=session.event, user=request.user).exists()

    registration = SessionRegistration.objects.filter(session=session, user=request.user).first()
    if action == 'signup':
        session_group_pk = request.POST.get('session_group_pk')
        if session_group_pk:
            session_group = get_object_or_404(SessionGroup, pk=session_group_pk)
            already_on = session_group.is_user_already_on(request.user)
            if session_group.is_limited_to_one and already_on:
                raise Exception(u'سبق أن سجّلت!')
        else:
            timeslot = session.time_slot
            if timeslot and timeslot.is_user_already_on(request.user):
                raise Exception(u'سبق أن سجّلت!')

        if not session.limit is None and\
           not session.get_remaining_seats() > 0:
            raise Exception(u'لا توجد مقاعد شاغرة')
        else:
            if not registration:
                registration = SessionRegistration.objects.create(session=session,
                                                   user=request.user,
                                                   is_approved=is_approved)
                if not has_previous_sessions and session.event.is_auto_tweet:
                    if session_group_pk:
                        relative_url = reverse("events:show_session_group", args=(session.event.code_name, session_group.code_name))
                    else:
                        relative_url = reverse("events:list_sessions", args=(session.event.code_name,))
                    full_url = request.build_absolute_uri(relative_url)
                    if session.event.twitter:
                        twitter_text = " (@{})".format(session.event.twitter)
                    else:
                        twitter_text = ""
                    text = u"سجّلت في {}{}!  يمكنك التسجيل من: {}"
                    if session.event.hashtag:
                        text += u"\n#" + session.event.hashtag
                    core.utils.create_tweet(request.user, text.format(session.event.twitter_event_name or session.event.official_name, twitter_text, full_url))
            elif registration.is_deleted:
                registration.is_deleted = False
                registration.is_approved = is_approved
            else:
                raise Exception(u'سبق التسجيل!')

    elif action == 'cancel':
        if not registration:
            raise Exception(u'لم يسبق لك التسجيل!')
        else:
            registration.is_deleted = True

    registration.save()

    return {'remaining_seats': session.get_remaining_seats(),
            'status': registration.get_status()}

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
def submit_initiative(request, event_code_name):
    event = get_object_or_404(Event, code_name=event_code_name,
                              receives_initiative_submission=True)
    context = {'event': event}

    if event.initiative_submission_opening_date and timezone.now() < event.initiative_submission_opening_date:
        return render(request, 'events/initiatives/initiatives_not_started.html', context)
    elif event.initiative_submission_closing_date and timezone.now() > event.initiative_submission_closing_date:
        return render(request, 'events/initiatives/initiatives_closed.html', context)

    if request.method == 'POST':
        instance = Initiative(event=event,user=request.user)
        form = InitiativeForm(request.POST, request.FILES,
                            instance=instance)
        figure_formset = InitiativeFigureFormset(request.POST, request.FILES)
        if form.is_valid() and figure_formset.is_valid():
            initiative = form.save()
            figure_formset.instance = initiative
            figure_formset.save()
            return HttpResponseRedirect(reverse('events:initiative_submission_completed',
                                                args=(event.code_name,)))
    elif request.method == 'GET':
        form = InitiativeForm()
        figure_formset = InitiativeFigureFormset()
    context['form'] = form
    context['figure_formset'] = figure_formset

    return render(request, 'events/initiatives/initiatives_submission.html', context)

@login_required
def list_initiatives(request, event_code_name):
    event = get_object_or_404(Event, code_name=event_code_name,
                              receives_initiative_submission=True)
    if not utils.is_organizing_team_member(request.user, event):
        raise PermissionDenied

    initiatives = Initiative.objects.filter(event=event, is_deleted=False)

    context = {'event': event, 'initiatives':initiatives}

    return render(request, 'events/initiatives/list_initiatives.html', context)

@login_required
def show_initiative(request, event_code_name, pk):
    initiative = get_object_or_404(Initiative, is_deleted=False, pk=pk)
    event = initiative.event

    if not initiative.user == request.user and \
            not request.user.is_superuser and \
            not utils.is_organizing_team_member(request.user, event):
        raise PermissionDenied

    context= {'event':event, 'initiative':initiative}
    return render(request, "events/initiatives/show_initiative.html", context)

def show_session_group(request, event_code_name, code_name):
    event = SessionGroup.event
    session_group = get_object_or_404(SessionGroup,
                                      event__code_name=event_code_name,
                                      code_name=code_name)
    context = {'session_group': session_group}
    if session_group.event.registration_opening_date and timezone.now() < session_group.event.registration_opening_date:
        raise Http404
    elif session_group.event.registration_closing_date and timezone.now() > session_group.event.registration_closing_date:
        return HttpResponseRedirect(reverse('events:registration_closed',
                                                args=(event.code_name,)))
    if request.user.is_authenticated() and session_group.is_limited_to_one:
        context['already_on'] = session_group.is_user_already_on(request.user)

    return render(request, "events/session_group/show_session_group.html", context)

@login_required
def review_registrations(request, event_code_name, pk):
    session = get_object_or_404(Session,
                                event__code_name=event_code_name,
                                pk=pk)
    event = session.event
    if not utils.is_organizing_team_member(request.user, event):
        raise PermissionDenied

    approved_registrations = SessionRegistration.objects.filter(session=session, is_deleted=False, is_approved=True)
    pending_registrations = SessionRegistration.objects.filter(session=session, is_deleted=False, is_approved=None)
    regected_registrations = SessionRegistration.objects.filter(session=session, is_deleted=False, is_approved=False)

    if request.method == "POST":
        action = request.POST.get('action')
        pks = [int(field.lstrip('pk_')) for field in request.POST if field.startswith('pk_')]
        print pks
        if action == "approve":
            SessionRegistration.objects.filter(pk__in=pks).update(is_approved=True)
        elif action == "reject":
            SessionRegistration.objects.filter(pk__in=pks).update(is_approved=False)
        elif action == "pend":
            SessionRegistration.objects.filter(pk__in=pks).update(is_approved=None)
        return HttpResponseRedirect(reverse('events:review_registrations',
                                                args=(session.event.code_name, session.pk)))
    elif request.method == "GET":
        return render(request, "events/review_registrations.html", {'session': session,
                                                                    'approved_registrations': approved_registrations,
                                                                    'pending_registrations': pending_registrations,
                                                                    'regected_registrations': regected_registrations})

@login_required
def submit_case_report(request, event_code_name):
    event = get_object_or_404(Event, code_name=event_code_name,
                              receives_abstract_submission=True)
    context = {'event': event}

    if event.abstract_submission_opening_date and timezone.now() < event.abstract_submission_opening_date:
        return render(request, 'events/abstracts/abstract_not_started.html', context)
    elif event.abstract_submission_closing_date and timezone.now() > event.abstract_submission_closing_date:
        return render(request, 'events/abstracts/abstract_closed.html', context)

    if request.method == 'POST':
        instance = CaseReport(event=event,user=request.user)
        form = CaseReportForm(request.POST, request.FILES,
                             instance=instance)
        if form.is_valid():
            abstract = form.save()
            return HttpResponseRedirect(reverse('events:show_casereport',
                                                args=(event.code_name, abstract.pk)))
    elif request.method == 'GET':
        form = CaseReportForm()
    context['form'] = form

    return render(request, 'events/abstracts/casereports/casereport_submission.html', context)

@login_required
def show_casereport(request, event_code_name, pk):
    casereport = get_object_or_404(CaseReport, is_deleted=False, pk=pk)
    event = casereport.event

    if not casereport.user == request.user and \
            not request.user.is_superuser and \
            not utils.can_evaluate_abstracts(request.user, event) and \
            not utils.is_organizing_team_member(request.user, event):
        raise PermissionDenied

    context= {'event':event, 'casereport':casereport}
    return render(request, "events/abstracts/casereports/show_casereport.html", context)


@login_required
@decorators.ajax_only
@decorators.post_only
@csrf.csrf_exempt
def delete_casereport(request, event_code_name, pk):
    casereport = get_object_or_404(CaseReport, is_deleted=False, pk=pk)
    event = casereport.event

    if not casereport.user == request.user and \
            not request.user.is_superuser and \
            not utils.is_organizing_team_member(request.user, event):
        raise PermissionDenied

    if event.abstract_submission_closing_date and timezone.now() > event.abstract_submission_closing_date:
        raise Exception(u"انتهت المدة المتاحة لحذف الملخص ")

    casereport.is_deleted = True
    casereport.save()
    list_my_abstracts_url = reverse('events:list_my_abstracts')
    full_url = request.build_absolute_uri(list_my_abstracts_url)
    return {"message": "success", "list_url": full_url}

@login_required
def evaluate(request, event_code_name, pk):
    abstract = get_object_or_404(Abstract, is_deleted=False, pk=pk)
    event = abstract.event
    if not utils.is_organizing_team_member(request.user, event) and \
       not utils.can_evaluate_abstracts(request.user, event):
        raise PermissionDenied

    evaluation = Evaluation(evaluator=request.user,
                            abstract=abstract)
    if request.method == 'POST':
        form = EvaluationForm(request.POST, instance=evaluation, evaluator=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('events:evaluators_homepage',
                                                args=(event.code_name,)))
    elif request.method == 'GET':
        form = EvaluationForm(instance=evaluation,
                              evaluator=request.user)
    context = {'event': event, 'abstract': abstract, 'form': form}

    return render(request, "events/abstracts/abstracts_evaluation_form.html", context)

@login_required
def edit_evaluation(request,event_code_name,evaluation_id, pk):
    evaluation = get_object_or_404(Evaluation, pk=evaluation_id)
    abstract = get_object_or_404(Abstract,pk=pk)
    event = abstract.event
    evaluator= evaluation.evaluator

    if not evaluation.evaluator == request.user and \
       not utils.is_organizing_team_member(request.user, event) and \
       not request.user.is_superuser:
        raise PermissionDenied

    context = {'event': event, 'abstract': abstract, 'evaluation': evaluation,'edit':True}

    if request.method == 'POST':
        form = EvaluationForm(request.POST, instance=evaluation,evaluator=evaluator)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('events:evaluators_homepage',
                                                args=(event.code_name,)))
        else:
            context['form'] = form
    elif request.method == 'GET':
        form = EvaluationForm(instance=evaluation, evaluator=evaluator)
        context['form'] = form

    return render(request, "events/abstracts/abstracts_evaluation_form.html", context)

@login_required
def evaluators_homepage(request,event_code_name):
    event = get_object_or_404(Event, code_name=event_code_name,
                              receives_abstract_submission=True)
    if not utils.is_organizing_team_member(request.user, event) and \
       not utils.can_evaluate_abstracts(request.user,event):
        raise PermissionDenied

    if request.user.is_superuser:
        user_evaluations = Evaluation.objects.annotate(evaluation_count=Count("abstract__evaluation"))\
                                             .filter(abstract__event=event,
                                                     evaluation_count__gte=event.evaluators_per_abstract,
                                                     abstract__is_deleted=False)
        pending_abstracts = Abstract.objects.annotate(evaluation_count=Count("evaluation"))\
                                            .filter(is_deleted=False,
                                                    event=event,
                                                    evaluation_count__lt=event.evaluators_per_abstract)

    else:
        user_evaluations = Evaluation.objects.filter(evaluator=request.user,
                                                     abstract__event=event,
                                                     abstract__is_deleted=False)
        pending_abstracts = Abstract.objects.filter(is_deleted=False,
                                                    evaluators=request.user,
                                                    event=event)\
                                            .exclude(evaluation__user=user_evaluations)\
                                            .distinct()
    riyadh_evaluators = Team.objects.get(code_name='hpc2-r-e')
    jeddah_evaluators = Team.objects.get(code_name='hpc2-j-e')
    alahsa_evaluators = Team.objects.get(code_name='hpc2-a-e')
    context = {'riyadh_evaluators': riyadh_evaluators,
               'jeddah_evaluators':jeddah_evaluators,
               'alahsa_evaluators':alahsa_evaluators,
               'pending_abstracts':pending_abstracts,
               'event': event}
    return render(request, 'events/abstracts/evaluator_homepage.html', context)
