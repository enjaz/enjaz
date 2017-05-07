# -*- coding: utf-8  -*-
from datetime import time
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.decorators import csrf
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from post_office import mail
import os.path

from core import decorators
from clubs.models import Team, college_choices
from certificates.models import Certificate
from .models import Event, Session, Abstract, AbstractFigure,\
                          Evaluation, TimeSlot,\
                          SessionRegistration, Initiative,\
                          SessionGroup,CaseReport, Attendance,\
                          QuestionSession, Question, Survey
from . import utils, forms
import core.utils
import clubs.utils


def redirect_home(request, event_code_name):
    event = get_object_or_404(Event, code_name=event_code_name)
    if event.url:
        return HttpResponseRedirect(event.url)
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
        form = forms.AbstractForm(request.POST, request.FILES,
                            instance=instance)
        figure_formset = forms.AbstractFigureFormset(request.POST, request.FILES)
        if form.is_valid() and figure_formset.is_valid():
            abstract = form.save()
            figure_formset.instance = abstract
            figure_formset.save()
            return HttpResponseRedirect(reverse('events:show_abstract',
                                                args=(event.code_name, abstract.pk)))
    elif request.method == 'GET':
        form = forms.AbstractForm()
        figure_formset = forms.AbstractFigureFormset()
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
        form = forms.AbstractForm(request.POST, request.FILES,
                            instance=instance)
        figure_formset = forms.AbstractFigureFormset(request.POST, request.FILES)
        if form.is_valid() and figure_formset.is_valid():
            abstract = form.save()
            figure_formset.instance = abstract
            figure_formset.save()
            show_abstract_url = reverse('events:show_abstract', args=(event.code_name, abstract.pk))
            full_url = request.build_absolute_uri(show_abstract_url)

            return {"message": "success", "show_url": full_url}
    elif request.method == 'GET':
        form = forms.AbstractForm(instance=abstract)
        figure_formset = forms.AbstractFigureFormset(instance=abstract)
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
def list_presenter_attendance(request, event_code_name):
    event = get_object_or_404(Event, code_name=event_code_name,
                              receives_abstract_submission=True)

    if not request.user.is_superuser and \
       not utils.is_organizing_team_member(request.user, event) and \
       not utils.is_attendance_team_member(request.user, event):
        raise PermissionDenied

    oral_present = Abstract.objects.filter(event=event, is_deleted=False, status='A', accepted_presentaion_preference='O', did_presenter_attend=True)
    oral_absent = Abstract.objects.filter(event=event, is_deleted=False, status='A', accepted_presentaion_preference='O', did_presenter_attend=False)

    poster_present = Abstract.objects.filter(event=event, is_deleted=False, status='A', accepted_presentaion_preference='P', did_presenter_attend=True)
    poster_absent = Abstract.objects.filter(event=event, is_deleted=False, status='A', accepted_presentaion_preference='P', did_presenter_attend=False)

    context = {'event': event,
               'oral_present': oral_present,
               'oral_absent': oral_absent,
               'poster_present': poster_present,
               'poster_absent': poster_absent}

    if request.method == "POST":
        action = request.POST.get('action')
        pks = [int(field.lstrip('pk_')) for field in request.POST if field.startswith('pk_')]
        print pks
        if action == "attend":
            Abstract.objects.filter(pk__in=pks).update(did_presenter_attend=True)
        elif action == "absent":
            Abstract.objects.filter(pk__in=pks).update(did_presenter_attend=False)
        return HttpResponseRedirect(reverse('events:list_presenter_attendance',
                                                args=(event.code_name,)))

    elif request.method == "GET":
        return render(request, 'events/abstracts/list_presenter_attendance.html', context)

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
    context = {'event': event, 'abstract': abstract}

    if not abstract.user == request.user and \
            not request.user.is_superuser and \
            not utils.can_evaluate_abstracts(request.user, event) and \
            not utils.is_organizing_team_member(request.user, event):
        raise PermissionDenied

    if request.method == 'POST':
         poster_form = forms.AbstractPosterForm(request.POST, request.FILES)
         if poster_form.is_valid() :
             new_poster_form=poster_form.save()
             new_poster_form.abstract = Abstract.objects.get(pk=pk)
             new_poster_form.save()

             return HttpResponseRedirect(reverse('events:show_abstract',
                                             args=(event.code_name,abstract.pk)))
    elif request.method == 'GET':
        poster_form = forms.AbstractPosterForm()
    context['form'] = poster_form

    return render(request, "events/abstracts/show_abstract.html", context)

@login_required
def presntation_upload (request, event_code_name, pk):
    abstract = get_object_or_404(Abstract, is_deleted=False, pk=pk)
    event = abstract.event
    context = {'event': event, 'abstract': abstract}

    if not abstract.user == request.user and \
            not request.user.is_superuser and \
            not utils.can_evaluate_abstracts(request.user, event) and \
            not utils.is_organizing_team_member(request.user, event):
        raise PermissionDenied

    if request.method == 'POST':
         presentation_form = forms.AbstractPresentationForm(request.POST, request.FILES)
         if presentation_form.is_valid():
             presentation=presentation_form.save()
             presentation.abstract = Abstract.objects.get(pk=pk)
             presentation.save()

             return HttpResponseRedirect(reverse('events:show_abstract',
                                             args=(event.code_name,abstract.pk)))
    elif request.method == 'GET':
        presentation_form = forms.AbstractPresentationForm()
    context['presentation_form'] = presentation_form

    return render(request, "events/abstracts/show_abstract.html", context)

@decorators.ajax_only
@decorators.post_only
@csrf.csrf_exempt
@login_required
def upload_abstract_image(request):
    form = forms.AbstractFigureForm(request.POST, request.FILES)
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

def list_sessions_privileged(request, event_code_name):
    event = get_object_or_404(Event, code_name=event_code_name)

    if not request.user.is_superuser and \
       not utils.is_organizing_team_member(request.user, event) and \
       not utils.is_attendance_team_member(request.user, event) and\
            not utils.is_regestrations_team_member(request.user,event):
        raise PermissionDenied

    sessions = Session.objects.filter(event=event)

    return render(request,  'events/session_list_privileged.html',
                  {'event': event})

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

    return render(request,  'events/sessions_list.html', context)

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
                if not has_previous_sessions:
                    if session.event.sends_badges_automatically:
                        relative_url = reverse("events:list_my_registration")
                        my_registration_url = request.build_absolute_uri(relative_url)
                        utils.email_badge(request.user, session.event, my_registration_url)
                        registration.badge_sent = True
                    if session.event.is_auto_tweet:
                        if session_group_pk:
                            relative_url = reverse("events:show_session_group", args=(session.event.code_name, session_group.code_name))
                        else:
                            relative_url = reverse("events:list_timeslots", args=(session.event.code_name,))
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
       not request.user.is_superuser and not utils.is_regestrations_team_member(request.user,event):
        raise PermissionDenied

    return render(request, 'events/session_show_privileged.html',
                  {'session': session, 'event': event})

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
        form = forms.InitiativeForm(request.POST, request.FILES,
                            instance=instance)
        figure_formset = forms.InitiativeFigureFormset(request.POST, request.FILES)
        if form.is_valid() and figure_formset.is_valid():
            initiative = form.save()
            figure_formset.instance = initiative
            figure_formset.save()
            return HttpResponseRedirect(reverse('events:initiative_submission_completed',
                                                args=(event.code_name,)))
    elif request.method == 'GET':
        form = forms.InitiativeForm()
        figure_formset = forms.InitiativeFigureFormset()
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
    session_group = get_object_or_404(SessionGroup,
                                      event__code_name=event_code_name,
                                      code_name=code_name)
    context = {'session_group': session_group}
    if session_group.event.registration_opening_date and timezone.now() < session_group.event.registration_opening_date:
        raise Http404
    elif session_group.event.registration_closing_date and timezone.now() > session_group.event.registration_closing_date:
        return HttpResponseRedirect(reverse('events:registration_closed',
                                                args=(session_group.event.code_name,)))
    if request.user.is_authenticated() and session_group.is_limited_to_one:
        context['already_on'] = session_group.is_user_already_on(request.user)

    return render(request, "events/session_group/show_session_group.html", context)

@login_required
def review_registrations(request, event_code_name, pk):
    session = get_object_or_404(Session,
                                event__code_name=event_code_name,
                                pk=pk)
    event = session.event
    if not utils.is_organizing_team_member(request.user, event) and not utils.is_regestrations_team_member(request.user, event):
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
        form = forms.CaseReportForm(request.POST, request.FILES,
                             instance=instance)
        if form.is_valid():
            abstract = form.save()
            return HttpResponseRedirect(reverse('events:show_casereport',
                                                args=(event.code_name, abstract.pk)))
    elif request.method == 'GET':
        form = forms.CaseReportForm()
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
        form = forms.EvaluationForm(request.POST, instance=evaluation, evaluator=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('events:evaluators_homepage',
                                                args=(event.code_name,)))
    elif request.method == 'GET':
        form = forms.EvaluationForm(instance=evaluation,
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
        form = forms.EvaluationForm(request.POST, instance=evaluation,evaluator=evaluator)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('events:evaluators_homepage',
                                                args=(event.code_name,)))
        else:
            context['form'] = form
    elif request.method == 'GET':
        form = forms.EvaluationForm(instance=evaluation, evaluator=evaluator)
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

@login_required
def list_my_registration(request):
    registrations = SessionRegistration.objects.filter(is_deleted=False, user=request.user)
    context = {'registrations': registrations}
    return render(request, 'events/list_my_registration.html', context)

@login_required
def list_barcodes(request, event_code_name):
    event = get_object_or_404(Event, code_name=event_code_name,
                              has_attendance=True)

    if not utils.is_attendance_team_member(request.user, event) and \
       not utils.is_organizing_team_member(request.user, event) and \
       not request.user.is_superuser:
        raise PermissionDenied

    barcode_users = User.objects.filter(session_registrations__session__event=event,
                                        session_registrations__is_deleted=False).distinct()

    context = {"barcode_users": barcode_users, 'event': event}
    return render(request, 'events/list_barcodes.html', context)

@login_required
def show_barcode(request, event_code_name=None, user_pk=None):
    if user_pk and event_code_name:
        event = get_object_or_404(Event, code_name=event_code_name,
                                  has_attendance=True)
        barcode_user = get_object_or_404(User, pk=user_pk)
    else:
        event = None
        barcode_user = request.user

    if not utils.can_see_all_barcodes(request.user, barcode_user, event):
        raise PermissionDenied

    text = ("{:0%s}" % utils.BARCODE_LENGTH).format(barcode_user.pk)
    qrcode_value = utils.get_barcode(text)

    context = {'qrcode_value' : qrcode_value,
               'event': event,
               'text': text,
               'barcode_user': barcode_user}
    return render(request, 'events/show_barcode.html', context)

@login_required
@decorators.ajax_only
@decorators.post_only
@csrf.csrf_exempt
def process_barcode(request, event_code_name, pk):
    session = get_object_or_404(Session,
                                event__code_name=event_code_name,
                                event__has_attendance=True,
                                pk=pk)
    if not request.user.is_superuser and \
       not utils.is_organizing_team_member(request.user, session.event) and\
       not utils.is_attendance_team_member(request.user, session.event):
        raise PermissionDenied

    response = {}
    action = request.POST.get("action")
    if action == 'attend':
        category = request.POST.get("category", "")
        only_registered = int(request.POST.get("only_registered"))
        user_pk = request.POST.get("user_pk")

        try:
            user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            raise Exception(u"رقم خاطئ!")

        try:
            full_name = user.common_profile.get_ar_short_name()
        except ObjectDoesNotExist:
            # If user has no CommonProfile
            full_name = user.username

        previous_registrations = SessionRegistration.objects.filter(user=user, session=session)

        if previous_registrations.filter(is_deleted=False,
                                         is_approved=True).exists():
            registration = previous_registrations.first()
        else: # If no approved registrations
            if only_registered:
                raise Exception(u"لا تسجيل ل{}".format(full_name))
            elif previous_registrations.filter(is_deleted=True).exists() or \
                 previous_registrations.exclude(is_approved=True).exists():
                registration = previous_registrations.first()
                registration.is_deleted = False
                registration.is_approved = True
                registration.save()
            else: # If no registration, create one
                registration = SessionRegistration.objects.create(user=user,
                                                                  session=session,
                                                                  is_approved=True)

        attendance = Attendance.objects.create(submitter=request.user,
                                               session_registration=registration,
                                               category=category)
        last_pk = attendance.pk
        response['last_pk'] = last_pk

    elif action == 'cancel':
        last_pk = request.POST.get("last_pk")
        try:
            attendance = Attendance.objects.get(pk=last_pk)
        except Attendance.DoesNotExist:
            raise Exception("هذا التحضير غير موجود")

        attendance.delete()

        try:
            full_name = attendance.session_registration.user.common_profile.get_ar_short_name()
        except ObjectDoesNotExist:
            # If user has no CommonProfile
            full_name = attendance.session_registration.user.username

    response['full_name'] = full_name

    return response

@login_required
def show_attendance_interface(request, event_code_name, pk):
    session = get_object_or_404(Session,
                                event__code_name=event_code_name,
                                event__has_attendance=True,
                                pk=pk)

    if not request.user.is_superuser and \
       not utils.is_organizing_team_member(request.user, session.event) and \
       not utils.is_attendance_team_member(request.user, session.event):
        raise PermissionDenied

    form = forms.AttendanceForm()

    context = {'session': session, 'event': session.event,
               'BARCODE_LENGTH': utils.BARCODE_LENGTH,
               'form': form}

    return render(request, 'events/show_attendance_interface.html', context)

@login_required
def download_barcode_pdf(request, event_code_name=None, user_pk=None):
    if user_pk and event_code_name:
        event = get_object_or_404(Event, code_name=event_code_name,
                                  has_attendance=True)
        barcode_user = get_object_or_404(User, pk=user_pk)
    else:
        event = None
        barcode_user = request.user

    if not utils.can_see_all_barcodes(request.user, barcode_user, event):
        raise PermissionDenied

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Badge.pdf"'
    pdf_content = utils.render_badge_pdf(barcode_user)
    response.write(pdf_content)
    return response

def show_question_session(request, event_code_name, pk):
    question_session = get_object_or_404(QuestionSession, pk=pk,
                                         event__code_name=event_code_name)

    old_questions = question_session.question_set.order_by('-submission_date')
    last_question = old_questions.first()
    if last_question:
        last_pk = old_questions.first().pk
    else:
        last_pk = 1

    context = {"question_session": question_session,
               "last_pk": last_pk,
               "old_questions": old_questions}

    if request.method == "GET":
        form = forms.QuestionForm()
    elif request.method == "POST":
        instance = Question(question_session=question_session)
        form = forms.QuestionForm(request.POST, instance=instance)
        if form.is_valid():
            question = form.save()
            return HttpResponseRedirect(reverse('events:show_question_session',
                                                args=(question_session.event.code_name, pk,)) + \
                                        "#q"+str(question.pk))

    context['form'] = form

    return render(request, "events/questions/index.html", context)

@csrf.csrf_exempt
@decorators.ajax_only
def handle_question_ajax(request, event_code_name, pk):
    question_session = get_object_or_404(QuestionSession, pk=pk,
                                         event__code_name=event_code_name)

    old_last_pk = request.POST['last_pk']
    new_last_pk = question_session.question_set.order_by('-submission_date').first().pk

    if old_last_pk != new_last_pk:
        new_questions = question_session.question_set.filter(pk__gt=old_last_pk)
        new_questions = new_questions.values_list('text', flat=True)
        new_questions = list(new_questions)
        response = {'new_questions':new_questions,
                   'new_last_pk':new_last_pk}
    else:
        response = {}

    return response

@login_required
def show_event_stats(request, event_code_name):
    event = get_object_or_404(Event, code_name=event_code_name)

    if not request.user.is_superuser and \
       not utils.is_organizing_team_member(request.user, session.event) and \
       not utils.is_attendance_team_member(request.user, session.event):
        raise PermissionDenied

    sessions = {}

    sessions = event.session_set.annotate(attendance=Count("sessionregistration__attendance")).order_by("-attendance").all()
    context = {'event': event, 'sessions': sessions}
    return render(request, 'events/show_event_stats.html', context)

def get_csv(request, event_code_name, session_pk):
    session = get_object_or_404(Session,
                                event__code_name=event_code_name,
                                pk=session_pk)

    if not request.user.is_superuser and \
       not utils.is_organizing_team_member(request.user, session.event) and \
       not utils.is_attendance_team_member(request.user, session.event):
        raise PermissionDenied

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    session_attendances = Attendance.objects.filter(session_registration__session=session)

    if session.event.has_attendance and session_attendances.count() >= 2:
        start_time = time(00,00)
        first_attendance = session_attendances.order_by("date_submitted").first().date_submitted
        first_attendance = timezone.datetime.combine(first_attendance, start_time)
        first_attendance = timezone.make_aware(first_attendance, timezone.get_current_timezone())
        end_time = time(23,59,59)
        last_attendance = session_attendances.order_by("date_submitted").last().date_submitted
        last_attendance = timezone.datetime.combine(last_attendance, end_time)
        last_attendance = timezone.make_aware(last_attendance, timezone.get_current_timezone())

        current_datetime = first_attendance
        last_datetime = last_attendance
        rows = ['Date,Total,In,Mid,Out,Uncategorized']
        while last_datetime > current_datetime:
            current_datetime += timezone.timedelta(hours=1)
            datetime_str = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
            attendance_count = session_attendances.filter(date_submitted__lte=current_datetime).count()
            attendance_i_count = session_attendances.filter(date_submitted__lte=current_datetime, category="I").count()
            attendance_m_count = session_attendances.filter(date_submitted__lte=current_datetime, category="M").count()
            attendance_o_count = session_attendances.filter(date_submitted__lte=current_datetime, category="O").count()
            attendance_u_count = session_attendances.filter(date_submitted__lte=current_datetime, category="").count()
            rows.append(','.join([datetime_str] + [str(count) for count in
                                                   attendance_count,
                                                   attendance_i_count,
                                                   attendance_m_count,
                                                   attendance_o_count,
                                                   attendance_u_count]))
        output = "\n".join(rows)
        response.write(output)
    else:
        response.write("")

    return response

@decorators.ajax_only
@login_required
def handle_survey(request, session_pk, survey_pk):
    session = get_object_or_404(Session, pk=session_pk)
    survey = get_object_or_404(Survey,pk=survey_pk)
    if request.method == 'POST':
        form = forms.SurveyForm(request.POST, session=session)
        if form.is_valid():
            form.save(user=request.user)
            return {"message": "success"}
    elif request.method == 'GET':
        form = forms.SurveyForm(request.POST, session=session)

    context = {'form': form}
    return render(request, 'bulb/groups/edit_group_form.html', context)

@login_required
def list_session_certificates(request, event_code_name, pk):
    session = get_object_or_404(Session,
                                event__code_name=event_code_name,
                                pk=pk)

    if not request.user.is_superuser and \
       not utils.is_organizing_team_member(request.user, session.event):
        raise PermissionDenied

    context = {'session': session}
    return render(request, 'events/list_session_certificates.html', context)

@login_required
def list_abstract_certificates(request, event_code_name):
    event = get_object_or_404(Event, code_name=event_code_name,
                              receives_abstract_submission=True)

    if not request.user.is_superuser and \
       not utils.is_organizing_team_member(request.user, event):
        raise PermissionDenied

    approved_pks = Abstract.objects.filter(event=event)\
                                   .exclude(accepted_presentaion_preference="")\
                                   .values_list('pk', flat=True)

    certificates = Certificate.objects.filter(abstracts__pk__in=approved_pks)

    context = {'certificates': certificates,
               'event': event}
    return render(request, 'events/list_abstract_certificates.html', context)


