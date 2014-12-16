# -*- coding: utf-8  -*-
from datetime import timedelta
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist

from post_office import mail

from activities.models import Activity, Review, Episode
from activities.forms import ActivityForm, DirectActivityForm, DisabledActivityForm, ReviewForm
from accounts.models import get_gender
from activities.utils import get_club_notification_to, get_club_notification_cc
from clubs.models import Club
from clubs.utils import get_presidency, is_coordinator_or_member, is_coordinator_or_deputy_of_any_club, \
    is_coordinator_of_any_club, get_media_center, \
    is_member_of_any_club, is_employee_of_any_club, is_coordinator, is_coordinator_or_deputy, get_user_clubs, \
    get_user_coordination_and_deputyships, has_coordination_to_activity
from core.utilities import FVP_EMAIL, MVP_EMAIL, DHA_EMAIL
from media.utils import MAX_OVERDUE_REPORTS

FORMS_CURRENT_APP = "activity_forms"

# A Note on Activity Permissions
#
# The club has three category of users: coordinator, vices and
# members.
#
# Both primary and secondary club members have identical privileges to
# the associated activities.  The email notifcation, however, is to
# the submitter (whether coordinator or deputy) of the primary club
# with CCs to the primary club coordinator (if they are not the
# submitter) and secondary club coordinator.
#
# Regarding activities, the coordinator and vices are identical in
# their permissions for flexiblity, both can:
# * submit new activities on behalf of their club,
# * edit any activity of their club, [when approved, editing will be limited]
# * view pending and rejected activities,
# * view presidency and deanship reviews of any activity of their club,
# * view participants in any activity of their club,
# * receive notifications for activities they have submitted, [if vice, cc coordinator]
# * submit media reports about any activity of their club,
#
# Members in general can:
# * view pending and rejected activities of their club,

def list_activities(request):
    """
    Return a list of the current year's activities displayed as a calendar as well as a table.
    (For the front-end, only the calendar is visible.)
    * For superusers, SC Presidency members (Chairman, Deputies, and Assistants), all activities should be visible.
    * For Deanship of Student Affairs reviewers, only activities approved by SC Presidency should be visible.
    * For club coordinators, only activities approved by SC-P and DSA in addition to pending and rejected activities
      of their own club.
    * For Deanship of Student Affairs employees and other users, only activities approved by SC-P and DSA should be
      visible.
    """
    # Show approved activites for everybody.
    #
    # By default (i.e. for students, employees and anonymous users),
    # no pending or rejected activities should be shown.
    context = {'approved': Activity.objects.approved(),
               'pending': Activity.objects.none(),
               'rejected': Activity.objects.none()}

    if request.user.is_authenticated():
        template = 'activities/list_privileged.html'
        if request.user.is_superuser or is_coordinator_or_member(get_presidency(), request.user)\
                or request.user.has_perm('activities.add_presidency_review'):
            # If the user is a super user or part of the presidency,
            # then show all activities
            context['pending'] = Activity.objects.pending()
            context['rejected'] = Activity.objects.rejected()

        elif request.user.has_perm('activities.add_deanship_review'):
            # If the user is part of the deanship of student affairs,
            # only show activities approved by presidency
            context['pending'] = Activity.objects.pending().filter(review__review_type="P", review__is_approved=True)
            context['rejected'] = Activity.objects.rejected().filter(review__review_type="P", review__is_approved=True)

        elif (is_coordinator_or_deputy_of_any_club(request.user) or is_member_of_any_club(request.user)) and \
             not is_coordinator_or_member(get_presidency(), request.user) and \
             not is_coordinator_or_member(get_media_center(), request.user):
            # For club coordinators, deputies, and members, show approved
            # activities as well as their own club's pending and rejected
            # activities.
            user_coordination = get_user_coordination_and_deputyships(request.user)
            user_clubs = user_coordination | request.user.memberships.all()
            context['pending'] = Activity.objects.pending().filter(primary_club__in=user_clubs) | \
                                 Activity.objects.pending().filter(secondary_clubs__in=user_clubs)
            context['rejected'] = Activity.objects.rejected().filter(primary_club__in=user_clubs) | \
                                  Activity.objects.rejected().filter(secondary_clubs__in=user_clubs)

            # Media-related
            # Only display to coordinators and deputies
            if is_coordinator_or_deputy_of_any_club(request.user):
                context['due_report_count'] = user_coordination.all()[0].get_due_report_count()
                context['overdue_report_count'] = user_coordination.all()[0].get_overdue_report_count()
                # In activity templates, the MAX_OVERDUE_REPORTS
                # variable is used to check whether the current user
                # is a coordinator or a deputy.  This is to aviod
                # passing duplicated variables.  In case the following
                # variable is changed, the templates need to be
                # changed as well.
                context['MAX_OVERDUE_REPORTS'] = MAX_OVERDUE_REPORTS

        elif is_employee_of_any_club(request.user):
            # For employees, display all approved activities, as well
            # as their clubs' approved activities in a separate table.
            #
            # An employee is basically similar to a normal user, the
            # only difference is having another table that includes
            # the employee's relevant activities
            context['club_approved'] = Activity.objects.approved().filter(primary_club__in=request.user.employee.all())

            template = 'activities/list_employee.html'
        else: # For students and other normal users.
            template = 'activities/list_normal.html'
    else: # For anonymous users
        template = 'activities/front/list.html'

    return render(request, template, context)

@login_required
def show(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)

    # The activity object is the only thing that should be in the context  [Saeed, 17 Jun 2014]    
    context = {'activity': activity}

    # If the activity is approved, everyone can see it.  If it is not,
    # only the head of the Student Club, the Media Team, the members
    # of the related clubs and the person who submitted it can see it.    
    if request.user.is_authenticated():
        user_clubs = get_user_clubs(request.user)
        coordination_status = has_coordination_to_activity(request.user, activity)

        if request.user.has_perm('activities.change_activity') or \
            coordination_status:
            context['can_edit'] = True
        if request.user.has_perm('activities.view_deanship_review') or \
            coordination_status:
            context['can_view_deanship_review'] = True
        if request.user.has_perm('activities.view_presidency_review') or \
            coordination_status:
            context['can_view_presidency_review'] = True
        if request.user.has_perm('media.add_followupreport') or \
            coordination_status:
            context['can_add_followupreport'] = True
        if request.user.has_perm('niqati.view_order') or \
            coordination_status:
            context['can_view_niqati_orders'] = True
        # Anyone can view forms; yet due to URL reversing issues it has to be restricted to this view only
        # Otherwise, we'll end up having to specify the `current_app` attribute for every view that contains a link
        # to the forms
        context['can_view_forms'] = True

    else:
        user_clubs = Club.objects.none()

    activity_primary_club = Club.objects.filter(pk=activity.primary_club.pk)
    activity_secondary_clubs = activity.secondary_clubs.all()
    activity_clubs = activity_primary_club | activity_secondary_clubs

    # --- Permission checks ---

    # If the user is a superuser or part of presidency or user is the activity's club coordinator or
    #  a coordinator of a secondary club in the activity, show the activity regardless of status
    # Elseif user is a DSA reviewer, show the activity if it's approved by presidency
    # Else (employees or others), show activity only if approved
    if request.user.is_superuser or request.user.has_perm('activities.add_presidency_review') \
       or request.user.has_perm('activities.view_activity') or any([club in activity_clubs for club in user_clubs]):
        # Don't raise any errors
        pass
    elif request.user.has_perm('activities.add_deanship_review'):
        if not activity.is_approved_by_presidency():
            raise PermissionDenied
    else:
        if not activity.is_approved():
            raise PermissionDenied

    return render(request, 'activities/show.html', context, current_app=FORMS_CURRENT_APP)

@login_required
def create(request):
    
    # --- Permission checks ---
    
    # (1) Check if the user is a coordinator
    
    # To check permissions, rather than using the
    # @permission_required('activities.add_activity') decorator, it is
    # more dynamic to check whether the user is a coordinator of any
    # club, or has the permission to add activities (i.e. part of the
    # presidency group)
    user_coordination = get_user_coordination_and_deputyships(request.user)
    if not request.user.has_perm("activities.add_activity") and not user_coordination:
        raise PermissionDenied
    
    # (2) Check if the user's club has no more than 3 overdue follow-up reports.
    # If any club coordinated by the user exceeds the 3-report threshold,
    # prevent new activity submission (again in reality the user will only coordinate
    # one club)
    if any([club.get_overdue_report_count() > MAX_OVERDUE_REPORTS for club in user_coordination]):
        raise PermissionDenied
    
    presidency = get_presidency() # Club.objects.get(english_name="Presidency")
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
        # By default, just choose the first user coordination that we
        # find.  Typically, it is the only one.
        if user_coordination:
            user_club = user_coordination[0]
        else:
            # Make it more user-friendly: if the user is an admin,
            # automatically choose presidency as the default
            # primary_club.
            can_directly_add = request.user.has_perm("activities.directly_add_activity")
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
    coordination_status = has_coordination_to_activity(request.user, activity)

    # If the user is neither the submitter, nor has the permission to
    # change activities (i.e. not part of the head of the Student
    # Club, or the Media Team), nor a coordinator or deputy of any of
    # the organizing clubs, raise a PermissionDenied error.
    if not request.user == activity.submitter and \
       not request.user.has_perm('activities.change_activity') and \
       not coordination_status:
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

            # If the edit has been done in response to a review, send a notification email
            try:
                pending_review = activity.review_set.get(is_approved=None)

                email_context = {'activity': activity}
                if pending_review.review_type == 'P':
                    if get_gender(activity.primary_club.coordinator) == 'M':
                        mail.send([MVP_EMAIL],
                                  template="activity_presidency_edited",
                                  context=email_context)
                    elif get_gender(activity.primary_club.coordinator) == 'F':
                        mail.send([FVP_EMAIL],
                                  template="activity_presidency_edited",
                                  context=email_context)
                elif pending_review.review_type == 'D':
                    mail.send([DHA_EMAIL],
                              template="activity_deanship_edited",
                              context=email_context)
            except ObjectDoesNotExist:
                pass

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
def review(request, activity_id, lower_review_type=None):
    activity = get_object_or_404(Activity, pk=activity_id)
    # Check if the user is a coordinator or deputy of any of the
    # activity's primary or secondary clubs.
    coordination_status = has_coordination_to_activity(request.user, activity)

    if lower_review_type == None:
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
    elif lower_review_type in ['d', 'p']:
        review_type = lower_review_type.upper()
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
            # Once the activity is approved (or partially approved), lock it from being edited.
            # This is very critical as to prevent manipulations (ie, editing the request after
            # the approval of the presidency and before it's reviewed by DSA)
            # Only when an edit is requested by the reviewer should editing be allowed
            activity.is_editable = False
            activity.save()
            deanship_review_url = reverse('activities:review_with_type', args=(activity_id, 'd'))
            deanship_full_url =  request.build_absolute_uri(deanship_review_url)
            presidency_review_url = reverse('activities:review_with_type', args=(activity_id, 'p'))
            presidency_full_url =  request.build_absolute_uri(presidency_review_url)
            activity_url = reverse('activities:show', args=(activity_id,))
            activity_full_url = request.build_absolute_uri(activity_url)
            email_context = {'activity': activity}
            if review.cleaned_data['is_approved']:
                if review_type == 'P':
                    email_context['full_url'] = presidency_full_url
                    mail.send([DHA_EMAIL],
                              template="activity_presidency_approved",
                              context=email_context)
                elif review_type == 'D':
                    if activity.primary_club.coordinator:
                        email_context['full_url'] = activity_full_url
                        mail.send(get_club_notification_to(activity),
                                  cc=get_club_notification_cc(activity),
                                  template="activity_deanship_approved",
                                  context=email_context)

                        for episode in activity.episode_set.all():
                            # Schedule an email at the date of the episode
                            # to remind the coordinator of submitting the media report
                            
                            mail.send(get_club_notification_to(activity),
                                      cc=get_club_notification_cc(activity),
                                      template="first_report_reminder",
                                      scheduled_time=episode.start_date,
                                      context={"episode": episode})

                            # Schedule another email 3 days after the episode as a second reminder
                            # to submit the media report
                            # TODO: there should be a better way that doesn't send the second email
                            # if the report is already submitted
                            mail.send(get_club_notification_to(activity),
                                      cc=get_club_notification_cc(activity),
                                      template="first_report_reminder",
                                      scheduled_time=episode.start_date + timedelta(days=3),
                                      context={"episode": episode})

                    if activity.primary_club.employee:
                        email_context['full_url'] = deanship_full_url
                        mail.send([activity.primary_club.employee.email],
                                  template="activity_approved_employee",
                                  context=email_context)
            elif review.cleaned_data['is_approved'] == False:
                # if the activity is rejected.
                if review_type == 'P':
                    email_context['full_url'] = presidency_full_url
                    mail.send(get_club_notification_to(activity),
                              cc=get_club_notification_cc(activity),
                              template="activity_presidency_rejected",
                              context=email_context)
                elif review_type == 'D':
                    email_context['full_url'] = deanship_full_url
                    mail.send(get_club_notification_to(activity),
                              cc=get_club_notification_cc(activity),
                              template="activity_deanship_rejected",
                              context=email_context)
            else:  # If changes are requested (review.is_approved == None)
                # TODO: If the review is being edited, only do the following if an actual change has been made
                # Enable coordinators to edit the activity request in correspondence to the review
                activity.is_editable = True
                activity.save()
                if review_type == 'P':
                    mail.send(get_club_notification_to(activity),
                              cc=get_club_notification_cc(activity),
                              template="activity_presidency_holded",
                              context=email_context)
                elif review_type == 'D':
                    mail.send(get_club_notification_to(activity),
                              cc=get_club_notification_cc(activity),
                              template="activity_deanship_holded",
                              context=email_context)
            return HttpResponseRedirect(reverse('activities:show', args=(activity.pk, )))
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
        elif request.user.has_perm('activities.view_' + rt_full + '_review') or coordination_status:
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
        coordination_status:
        context['can_edit'] = True
    if request.user.has_perm('activities.view_deanship_review') or \
        coordination_status:
        context['can_view_deanship_review'] = True
    if request.user.has_perm('activities.view_presidency_review') or \
        coordination_status:
        context['can_view_presidency_review'] = True

    return render(request, template, context)

@login_required
def participate(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    context = {"activity": activity}

    # If the activity's registration is open, then redirect to the registration form
    # Otherwise, return a message that registration is closed
    if activity.registration_is_open():
        reg_form = activity.get_registration_form()
        return HttpResponseRedirect(reverse("forms:form_detail",
                                            args=(activity.id, reg_form.id),
                                            current_app=FORMS_CURRENT_APP))
    else:
        context['error_message'] = 'closed'
        return render(request, 'activities/participate.html', context)
