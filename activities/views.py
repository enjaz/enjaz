# -*- coding: utf-8  -*-
# TODO: replace presidency with get_presidency utility function
# TODO: revise permissions (attach to club coordination and membership rather than django
# permissions - that's for normal users and club members and coordinators)
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist

from post_office import mail
import unicodecsv

from activities.models import Activity, Review, Participation, Episode
from activities.forms import ActivityForm, DirectActivityForm, DisabledActivityForm, ReviewForm
from accounts.models import get_gender
from clubs.models import Club
from core.utilities import FVP_EMAIL, MVP_EMAIL, DHA_EMAIL

def list(request):
    """
    Return a list of the current year's activities displayed as a calendar as well as a table.
    (For the front-end, only the calendar is visible.)
    * For superusers, SC Presidency members (Chairman, Deputies, and Assistants), all activities should be visible.
    * For Deanship of Student Affairs reviewers, only activities approved by SC Presidency should be visible.
    * For club coordinators, only activities approved by SC-P and DSA in addition to pending activities of their
      own club.
    * For Deanship of Student Affairs employees and other users, only activities approved by SC-P and DSA should be
      visible.
    """
    # TODO: Revisit this view in terms of what appears for different groups (permissions) (See specification above)
    if request.user.is_authenticated():
        template = 'activities/list_normal.html'
    else:
        template = 'activities/front/list.html'

    # If the user is part of the presidency of the Student Club, or
    # part of the Media Center, they should be able to view all
    # activities (i.e. approved, rejected and pending).  Otherwise, a
    # user should only see approved activities and the activities of
    # the clubs they have memberships in (regardless of their status).  

    if request.user.has_perm('activities.view_activity'):
        if request.GET.get('pending') == "1":
            activities = Activity.objects.filter(review__is_approved=None)
        else:
            activities = Activity.objects.all()
    else:
        approved_activities = Activity.objects.filter(review__is_approved=True) # This doesn't work
                                                                                # (It returns activities that have
                                                                                # either reviews (P or D) approved,
                                                                                # whereas both have to be True
        if request.user.is_authenticated():
            user_activities = request.user.activity_set.all()
            user_clubs = request.user.memberships.all() | request.user.coordination.all()
            primary_activities = Activity.objects.filter(
                primary_club__in=user_clubs)
            secondary_activities = Activity.objects.filter(
                secondary_clubs__in=user_clubs)
        else:
            user_activities = Activity.objects.none()
            primary_activities = Activity.objects.none()
            secondary_activities = Activity.objects.none()
        activities = approved_activities | user_activities | \
                     primary_activities | secondary_activities

    context = {'page_activities': activities}
    return render(request, template, context)

@login_required
def show(request, activity_id):
    # If the activity is approved, everyone can see it.  If it is not,
    # only the head of the Student Club, the Media Team, the members
    # of the related clubs and the person who submitted it can see it.
    activity = get_object_or_404(Activity, pk=activity_id)
    
    context = {'activity': activity}
    # The activity object is the only thing that should be in the context  [Saeed, 17 Jun 2014]
    
    if request.user.is_authenticated():
        user_clubs = request.user.memberships.all() | request.user.coordination.all()
        is_coordinator = activity.primary_club in request.user.coordination.all()

#        By definition, the coordinator should have all the below-mentioned
#        permissions; all we need is use {{ perms }} from within the template
#        [Saeed, 17 Jun 2014]

#        {{ perms }} cannot figure out whether or not someone is a
#        coordinator of this specific club.  In addition, Django
#        templates are limited when dealing with combined and/or
#        conditions. [Osama, 27 Jun 2014]

        if request.user.has_perm('activities.change_activity') or \
            is_coordinator:
            context['can_edit'] = True
        if request.user.has_perm('activities.view_participation') or \
            is_coordinator:
            context['can_view_participation'] = True
        if request.user.has_perm('activities.view_deanship_review') or \
            is_coordinator:
            context['can_view_deanship_review'] = True
        if request.user.has_perm('activities.view_presidency_review') or \
            is_coordinator:
            context['can_view_presidency_review'] = True
        if request.user.has_perm('media.add_followupreport') or \
            is_coordinator:
            context['can_add_followupreport'] = True
        if request.user.has_perm('niqati.view_order') or \
            is_coordinator:
            context['can_view_niqati_orders'] = True
            
    else:
        user_clubs = Club.objects.none()

    activity_primary_club = activity.primary_club
    activity_secondary_clubs = activity.secondary_clubs.all()
    activity_clubs = [activity_primary_club] + [club for club in activity_secondary_clubs]

    # The third test condition, that is:
    #   any([club in activity_clubs for club in user_clubs])
    #  checks if any of the clubs the user is a member of is also
    #  orginizing the activity that the user is trying to see.  If
    #  will be True if any club is one of the organizers and it will
    #  be False if none is.
    if not activity.is_approved() and \
       not request.user.has_perm('activities.view_activity') and \
       not any([club in activity_clubs for club in user_clubs]) and \
       not request.user == activity.submitter:
        raise PermissionDenied

    return render(request, 'activities/show.html', context)

@login_required
def create(request):
    
    # --- Permission checks ---
    
    # (1) Check if the user is a coordinator
    
    # To check permissions, rather than using the
    # @permission_required('activities.add_activity') decorator,
    # it is more dynamic to check whether the user is a
    # coordinator of any club, or has the permission to add
    # activities (i.e. part of the presidency group)
    user_coordination = request.user.coordination.all()
    if not request.user.has_perm("activities.add_activity") and not user_coordination:
        raise PermissionDenied
    
    # (2) Check if the user's club has no more than 3 overdue follow-up reports.
    # If any club coordinated by the user exceeds the 3-report threshold,
    # prevent new activity submission (again in reality the user will only coordinate
    # one club)
    if any(club.get_overdue_report_count() > 3 for club in user_coordination):
        raise PermissionDenied
    
    presidency = Club.objects.get(english_name="Presidency")
    if request.method == 'POST':
        activity = Activity(submitter=request.user)
        if request.user.has_perm('activities.directly_add_activity'):
            form = DirectActivityForm(request.POST, instance=activity)
        else:
            form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form_object = form.save()
            # If the chosen primary_club is the Presidency, make it
            # automatically approved by the deanship.  Otherwise,
            # email the vice president.
            if form_object.primary_club == presidency:
                review_object = Review.objects.create(
                    activity=form_object, reviewer=request.user,
                    is_approved=True, review_type='D')
            else:
                show_activity_url = reverse('activities:show', args=(form_object.pk,))
                full_url = request.build_absolute_uri(show_activity_url)
                submitter_gender = get_gender(request.user)
                email_context = {'activity': form_object, 'full_url':
                           full_url}
                if submitter_gender == 'M':
                    mail.send([MVP_EMAIL],
                              template="activity_submitted",
                              context=email_context)
                else:
                    mail.send([FVP_EMAIL],
                              template="activity_submitted",
                              context=email_context)
            return HttpResponseRedirect(reverse('activities:list'))
        else:
            context = {'form': form}
            return render(request, 'activities/new.html', context)
    else:

        can_directly_add = request.user.has_perm("activities.directly_add_activity")
        try:
            # It is theoretically true that the user can be a
            # coordinator of more than one single club, but we are not
            # taking that into consideration because it is just not
            # common enough.
            user_club = user_coordination[0]
        except IndexError:
            # Make it more user-friendly: if the user is an admin,
            # automatically choose presidency as the default
            # primary_club.
            if can_directly_add:
                user_club = presidency
            else:
                user_club = None

        activity = Activity(primary_club=user_club)
        if request.user.has_perm("activities.directly_add_activity"):
            form = DirectActivityForm(instance=activity)
        else:
            form = ActivityForm(instance=activity)
        context = {'form': form}
        return render(request, 'activities/new.html', context)

@login_required
def edit(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    user_coordination = request.user.coordination.all()
    # We need a QuerySet to combine it with secondary clubs.
    activity_primary_club = Club.objects.filter(
        id=activity.primary_club.id)
    activity_secondary_clubs = activity.secondary_clubs.all()
    activity_clubs = activity_primary_club | activity_secondary_clubs

    # If the user is neither the submitter, nor has the permission to
    # change activities (i.e. not part of the head of the Student
    # Club, or the Media Team), nor a coordinator of any of the
    # organizing clubs, raise a PermissionDenied error.
    if not request.user == activity.submitter and \
       not request.user.has_perm('activities.change_activity') and \
       not any([club in activity_clubs for club in user_coordination]):
        raise PermissionDenied

    if request.method == 'POST':
        if request.user.has_perm('activities.directly_add_activity'):
            modified_activity = DirectActivityForm(request.POST,
                                                   instance=activity)
        elif not activity.is_editable and \
             not request.user.has_perm('activities.change_activity'):
            modified_activity = DisabledActivityForm(request.POST,
                                                     instance=activity)
        else:
            modified_activity = ActivityForm(request.POST,
                                             instance=activity)
        # Should check that edits are valid before saving
        if modified_activity.is_valid():
            modified_activity.save()
            return HttpResponseRedirect(reverse('activities:show',
                                                args=(activity.pk, ))
                                        )
        else:
            context = {'form': modified_activity, 'activity_id': activity_id,
                       'edit': True}
            return render(request, 'activities/new.html', context)
    else:
        # There are different activity forms depending on what
        # permission the user has.  Presidency group members
        # (i.e. with directly_add_activity) can add activities
        # directly without waiting for the approval of the deanship.
        # They can also (with change_activity) edit activities
        # regardless of their is_editable value.
        if request.user.has_perm('activities.directly_add_activity'):
            form = DirectActivityForm(instance=activity)
        elif not activity.is_editable and \
             not request.user.has_perm('activities.change_activity'):
            form = DisabledActivityForm(instance=activity)
        else:
            form = ActivityForm(instance=activity)
        context = {'form': form, 'activity_id': activity_id,
                   'activity': activity, 'edit': True}
        return render(request, 'activities/new.html', context)

@login_required
def review(request, activity_id, lower_reivew_type=None):
    activity = get_object_or_404(Activity, pk=activity_id)
    is_coordinator = activity.primary_club in request.user.coordination.all()

    if lower_reivew_type == None:
        # If the user has any permission (read or write) related to
        # the deanship review, redirect to review/d/. Otherwise, if
        # the user has any permission (read or write) related to the
        # presidency review, redirect to review/p/.  Otherwise, raise
        # PermissionDenied
        if request.user.has_perm('activities.add_deanship_review') or \
           request.user.has_perm('activities.view_deanship_review'):
            return HttpResponseRedirect(reverse('activities:review_with_type',
                                                args=(activity_id, 'd')))
            
        elif request.user.has_perm('activities.add_presidency_review') or \
             request.user.has_perm('activities.view_presidency_review'):
            return HttpResponseRedirect(reverse('activities:review_with_type',
                                                args=(activity_id, 'p')))
        else:
            raise PermissionDenied
    elif lower_reivew_type in ['d', 'p']:
        review_type = lower_reivew_type.upper()
    else:
        raise Http404
    
    # Review Type Full
    rt_full = {'P': 'presidency', 'D': 'deanship'}[review_type]
    
    # Permission checks moved down (GET requests).
    # As for POST, it's not necessary because the permission check will already have
    # been done before serving the form page; in addition, CSRF token will prevent any
    # spam. [Saeed 18 Jun 2014]
    if request.method == 'POST':
        try: # If the review is already there, edit it.
            review_object = Review.objects.get(activity=activity,
                                               review_type=review_type)
        except ObjectDoesNotExist:
            review_object = Review(activity=activity,
                                   reviewer=request.user,
                                   review_type=review_type)
        review = ReviewForm(request.POST, instance=review_object)
        if review.is_valid():
            review.save()
            deanship_review_url = reverse('activities:review_with_type', args=(activity_id, 'd'))
            deanship_full_url =  request.build_absolute_uri(deanship_review_url)
            presidency_review_url = reverse('activities:review_with_type', args=(activity_id, 'p'))
            presidency_full_url =  request.build_absolute_uri(presidency_review_url)
            activity_url = reverse('activities:show', args=(activity_id,))
            activity_full_url = request.build_absolute_uri(activity_url)
            email_context = {'activity': activity}
            if review.cleaned_data['is_approved']:
                activity.is_editable = False
                activity.save()
                if review_type == 'P':
                    email_context['full_url'] = presidency_full_url
                    mail.send([DHA_EMAIL],
                              template="activity_presidency_approved",
                              context=email_context)
                elif review_type == 'D':
                    email_context['full_url'] = activity_full_url
                    mail.send([activity.primary_club.coordinator.email],
                              template="activity_deanship_approved",
                              context=email_context)
                    # FIXME: When we launch the website, not all clubs
                    # will have employees assigned.  This check is to
                    # be remvoed later.
                    if activity.primary_club.employee:
                        email_context['full_url'] = deanship_full_url
                        mail.send([activity.primary_club.employee.email],
                                  template="activity_approved_employee",
                                  context=email_context)
            elif review.cleaned_data['is_approved'] == False:
                # if the activity is rejected.
                if review_type == 'P':
                    email_context['full_url'] = presidency_full_url
                    mail.send([activity.primary_club.coordinator.email],
                              template="activity_presidency_rejected",
                              context=email_context)
                elif review_type == 'D':
                    email_context['full_url'] = deanship_full_url
                    mail.send([activity.primary_club.coordinator.email],
                              template="activity_deanship_rejected",
                              context=email_context)
            return HttpResponseRedirect(reverse('activities:show',
                                                args=(activity_id,)))
        # TODO: if not valid, show the error messages.
    else: # if not POST
        # If the user has the permission to add a review of the
        # corresponding type then return the review form page to add
        # or edit the review.
        # Else, if if they have the permission to read, then return
        # the review read page Otherwise, raise PermissionDenied
        if request.user.has_perm('activities.add_' + rt_full + '_review'):
            template = 'activities/review_write.html'
            try: # If the review is already there, edit it.
                review_object = Review.objects.get(activity=activity,
                                                   review_type=review_type)
                review = ReviewForm(instance=review_object)
            except ObjectDoesNotExist:
                review = ReviewForm()
                # Note 1: Here, review is a ReviewForm object, because we want to write
        # Deanship employees, presidency students and the specific
        # club coordinator should be able to see the reviews.
        elif request.user.has_perm('activities.view_' + rt_full + '_review') or is_coordinator:
            template = 'activities/review_read.html'
            try:
                review = Review.objects.get(activity=activity,
                                            review_type=review_type)
                # Note 2: Here, review is a Review object, because we just want to read
            except ObjectDoesNotExist:
                review = None
        else:
            raise PermissionDenied
        
    context = {'activity': activity, 'active_tab': rt_full,
               'review': review, 'review_type': review_type}

    if request.user.has_perm('activities.change_activity') or \
        is_coordinator:
        context['can_edit'] = True
    if request.user.has_perm('activities.view_participation') or \
        is_coordinator:
        context['can_view_participation'] = True
    if request.user.has_perm('activities.view_deanship_review') or \
        is_coordinator:
        context['can_view_deanship_review'] = True
    if request.user.has_perm('activities.view_presidency_review') or \
        is_coordinator:
        context['can_view_presidency_review'] = True

    return render(request, template, context)

@login_required
def participate(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    colleges = activity.participant_colleges.all()
    if colleges:
        request.user
    existing_participation = Participation.objects.filter(activity=activity,
                                                       user=request.user)
    context = {'activity': activity}

    if existing_participation:
        context['error_message'] = 'already_applied'
        return render(request, 'activities/participate.html', context)
        
    if request.method == 'POST':
        if request.POST['status'] == '1':
            Participation.objects.create(activity=activity,
                                         user=request.user)
            return HttpResponseRedirect(reverse('activities:participate_done',
                                                args=(activity_id,)))
        else:
            context['error_message'] = 'unknown'
            return render(request, 'activities/participate.html', context)
    else:
        return render(request, 'activities/participate.html', context)

@login_required
def view_participation(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    if not activity.primary_club in request.user.coordination.all() and \
       not request.user.has_perm('activities.view_participation'):
        raise PermissionDenied

    participations = Participation.objects.filter(activity=activity)
    context = {'participations': participations, 'activity': activity}
    return render(request, 'activities/view_participations.html', context)

# TODO: remove this view and the associated url since its function is now done by datatables
@login_required
def download_participation(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    if not activity.primary_club in request.user.coordination.all() and \
       not request.user.has_perm('activities.view_participation'):
        raise PermissionDenied

    participations = Participation.objects.filter(activity=activity)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Participants in Activity %s.csv"' % activity_id

    writer = unicodecsv.writer(response, encoding='utf-8')
    writer.writerow([u"الاسم", u"البريد"])
    for participantion in participations:
        if participantion.user.first_name:
            name = u"%s %s" % (participantion.user.first_name, participantion.user.last_name)
        else:
            name = participantion.user.username
        email = participantion.user.email
        writer.writerow([name, email])
    return response
