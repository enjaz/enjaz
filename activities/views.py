# -*- coding: utf-8  -*-
from datetime import timedelta
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.db.models import Q

from post_office import mail

from activities.models import Activity, Review, Episode
from activities.forms import ActivityForm, DirectActivityForm, DisabledActivityForm, ReviewForm
from accounts.utils import get_user_gender
from activities.utils import get_club_notification_to, get_club_notification_cc
from clubs.models import Club
from clubs.utils import is_coordinator_or_member, is_coordinator_or_deputy_of_any_club, \
    is_coordinator_of_any_club, get_media_center, \
    is_member_of_any_club, is_employee_of_any_club, is_coordinator, is_coordinator_or_deputy, get_user_clubs, \
    get_user_coordination_and_deputyships, has_coordination_to_activity, get_deanship, is_employee, can_review_activity
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
# * delete activities, as long as they are is_editable=True
#
# Members in general can:
# * view pending and rejected activities of their club,
#
# Vice presidents can:
# * delete activities regardless of their is_editable status.

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

        # For logged-in users, only show city-specific and
        # gender-specific activities.
        context['approved'] = Activity.objects.approved().for_user_city(request.user).for_user_gender(request.user)

        if request.user.is_superuser:
            # If the user is a super user or part of the presidency,
            # then show all activities
            context['pending'] = Activity.objects.pending()
            context['rejected'] = Activity.objects.rejected()
        elif is_coordinator_or_deputy_of_any_club(request.user) or \
             is_member_of_any_club(request.user):
            # For club coordinators, deputies, and members, show
            # approved activities as well as their own club's pending
            # and rejected activities.  For coordinators, show also
            # the activities waiting their action.
            user_coordination = get_user_coordination_and_deputyships(request.user)
            user_clubs = user_coordination | request.user.memberships.all()
            # In addition to the gender-specific approved activities,
            # show all activities of the user club.
            context['pending'] = (Activity.objects.pending().filter(primary_club__in=user_clubs) | \
                                  Activity.objects.pending().filter(secondary_clubs__in=user_clubs) | \
                                  Activity.objects.pending().filter(review__reviewer_club__in=user_clubs)).distinct()
            context['rejected'] = (Activity.objects.rejected().filter(primary_club__in=user_clubs) | \
                                   Activity.objects.rejected().filter(secondary_clubs__in=user_clubs) | \
                                   Activity.objects.rejected().filter(review__reviewer_club__in=user_clubs)).distinct()

            # Media-related
            # Only display to coordinators and deputies
            if is_coordinator_or_deputy_of_any_club(request.user):
                context['todo'] = Activity.objects.pending().filter(assignee__in=user_coordination)
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
    activity = get_object_or_404(Activity, pk=activity_id, is_deleted=False)

    # The activity object is the only thing that should be in the context  [Saeed, 17 Jun 2014]    
    context = {'activity': activity}

    # If the activity is approved, everyone can see it.  If it is not,
    # only the head of the Student Club, the Media Team, the members
    # of the related clubs and the person who submitted it can see it.    
    if request.user.is_authenticated():
        user_clubs = get_user_clubs(request.user)

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
    if request.user.is_superuser or can_review_activity(request.user, activity) \
       or request.user.has_perm('activities.view_activity') or any([club in activity_clubs for club in user_clubs]):
        # Don't raise any errors
        pass
    else:
        if not activity.is_approved:
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
    
    if request.method == 'POST':
        # DirectActivityForm get to choose what club to submit the
        # activity under.  Normal users shouldn't.
        can_directly_add = request.user.has_perm('activities.directly_add_activity')
        if can_directly_add:
            activity = Activity(submitter=request.user)
            form = DirectActivityForm(request.POST, instance=activity)
        else:
            user_club = user_coordination[0]
            activity = Activity(submitter=request.user, primary_club=user_club)
            form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form_object = form.save()
            # If the user can directly add activities, make the
            # activity automatically approved.  Otherwise, email the
            # reviewing parent.
            if can_directly_add:
                form_object.is_approved = True
                form_object.assignee = None
            else:
                reviewing_parent = form_object.primary_club.get_next_reviewing_parent()

                if not reviewing_parent:
                    form_object.is_approved = True
                    form_object.assignee = None
                else:
                    form_object.is_approved = None
                    form_object.assignee = reviewing_parent
                    show_activity_url = reverse('activities:show', args=(form_object.pk,))
                    full_url = request.build_absolute_uri(show_activity_url)
                    email_context = {'activity': form_object,
                                     'full_url': full_url,
                                     'reviewer_club': reviewing_parent}
                    mail.send([reviewing_parent.coordinator.email],
                              template="activity_submitted",
                              context=email_context)
            form_object.save()
            return HttpResponseRedirect(reverse('activities:list'))
        else:
            context = {'form': form}
            return render(request, 'activities/new.html', context)
    elif request.method == 'GET':
        context = {}
        if request.user.has_perm("activities.directly_add_activity"):
            form = DirectActivityForm()
        else:
            form = ActivityForm()
            user_club = user_coordination[0]
            context['user_club'] = user_club
        context['form'] = form
        return render(request, 'activities/new.html', context)

@login_required
def edit(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id, is_deleted=False)
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
            if activity.assignee == activity.primary_club:
                pending_review = activity.review_set.get(is_approved=None)
                activity.assignee = pending_review.reviewer_club
                activity.save()
                review_url = reverse('activities:review',
                       args=(activity_id, pending_review.reviewer_club.pk))
                review_full_url =  request.build_absolute_uri(review_url)
                email_context = {'activity': activity,
                                 'pending_review': pending_review,
                                 'full_url': review_full_url}
                mail.send([pending_review.reviewer.email],
                          template="activity_edited_to_reviewer",
                          context=email_context)
            return HttpResponseRedirect(reverse('activities:show',
                                                args=(activity.pk, )))
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
def delete(request,activity_id):
    activity = get_object_or_404(Activity, pk=activity_id, is_deleted=False)
    coordination_status = has_coordination_to_activity(request.user, activity)
    context = {'activity': activity}
    # If the user is neither the submitter, nor has the permission to
    # change activities (i.e. not part of the head of the Student
    # Club, or the Media Team), nor a coordinator or deputy of any of
    # the organizing clubs, raise a PermissionDenied error.
    if not request.user == activity.submitter and \
       not request.user.has_perm('activities.change_activity') and \
       not coordination_status:
        raise PermissionDenied
    # If we are dealing with the coordinator or their deputies, we
    # shouldn't allow them to delete unless the activity is editable.
    # This also means that vice presidents can delte activities
    # regardless of their is_editable status.
    if (request.user == activity.submitter or coordination_status) \
       and not activity.is_editable:
        raise PermissionDenied
    if request.method == 'POST':
        if 'confirm' in request.POST:
            activity.is_deleted = True
            activity.is_editable = False
            activity.save()
            return HttpResponseRedirect(reverse('activities:list'))
        else:
            context['erorr_message'] = 'not_confirmed'
    return render(request, 'activities/delete.html', context)

@login_required
def review(request, activity_id, reviewer_id):
    activity = get_object_or_404(Activity, pk=activity_id,
                                 is_deleted=False)
    reviewer_club = get_object_or_404(Club, pk=reviewer_id)

    # --- Permission checks ---
    # The reviewer club should actually be one of the activity owner's reviewing parents.
    # The user should either be a(n):
    # (1) Coordinator or deputy of the club that owns the activity
    #     (primary or secondary); in this case the user can only READ.
    # (2) Coordinator or deputy of a reviewer club; there are 2 cases here as well:
    #     a- either the reviewer is accessing "their" review; here they can WRITE.
    #     b- or the reviewer is accessing a review of another reviewer; here they can only READ.
    # (3) Employee responsible for the club that owns the activity. (READ)
    # (4) Superuser. (WRITE)

    reviewing_parents = activity.primary_club.get_reviewing_parents()

    # Is the passed reviewer club a member of the activity owner's
    # reviewer parents? If not, raise a 404 error.
    if not reviewer_club in reviewing_parents:
        raise Http404

    # Is the current user a coordinator/deputy of any of the reviewing
    # parents?
    user_is_any_reviewer = can_review_activity(request.user, activity)

    # Is the current user a coordinator/deputy of the reviewer club?
    user_is_current_reviewer = is_coordinator_or_deputy(reviewer_club, request.user)

    # The user can WRITE if they are the coordinator or deputy of the
    # reviewer club; or a superuser
    can_write = user_is_current_reviewer or request.user.is_superuser

    # The user can READ if they are the coordinator or deputy of the
    # activity owning club (primary or secondary); the coordinator or
    # deputy of a parent reviewer other than the ``reviewer_club``; or
    # an employee responsible for the activity owning club.
    can_read = has_coordination_to_activity(request.user, activity) or user_is_any_reviewer or \
               is_employee(activity.primary_club, request.user)

    # If the user has no read or write permissions, then they can't
    # access the view.
    if not can_read and not can_write:
        raise PermissionDenied

    # --- End of Permission Checks ---

    if request.method == "POST":
        try:  # If the review is already there, edit it.
            review_object = Review.objects.get(activity=activity,
                                               reviewer_club=reviewer_club)
        except ObjectDoesNotExist:
            review_object = Review(activity=activity,
                                   reviewer=request.user,
                                   reviewer_club=reviewer_club)
        review = ReviewForm(request.POST, instance=review_object)

        if review.is_valid():
            review.save()
            # Once the activity is approved (or partially approved),
            # lock it from being edited.  This is very critical as to
            # prevent manipulations (ie, editing the request after the
            # approval of the presidency and before it's reviewed by
            # DSA) Only when an edit is requested by the reviewer
            # should editing be allowed.
            activity.is_editable = False
            activity.update_is_approved()
            last_review_url = reverse('activities:review',
                                   args=(activity_id, reviewer_id))
            last_review_full_url =  request.build_absolute_uri(last_review_url)
            activity_url = reverse('activities:show', args=(activity_id,))
            activity_full_url = request.build_absolute_uri(activity_url)
            email_context = {'activity': activity}
            if review.cleaned_data['is_approved']:
                reviewing_parent = reviewer_club.get_next_reviewing_parent()
                # Reached the top of the review hierarchy => activity
                # approved.
                if not reviewing_parent: 
                    if activity.is_approved:  # sanity check
                        activity.assignee = None
                        # Email notifications
                        email_context['full_url'] = activity_full_url
                        mail.send(get_club_notification_to(activity),
                            cc=get_club_notification_cc(activity),
                            template="activity_approved_to_coordinator",
                            context=email_context)
                        if activity.primary_club.employee:
                            email_context['full_url'] = last_review_full_url
                            mail.send([activity.primary_club.employee],
                                  template="activity_approved_to_employee",
                                  context=email_context)
                else:
                    activity.assignee = reviewing_parent
                    email_context['last_reviewer'] = reviewer_club
                    upcoming_review_url = reverse('activities:review',
                                           args=(activity_id, reviewing_parent.pk))
                    upcoming_review_full_url = request.build_absolute_uri(upcoming_review_url)
                    email_context['full_url'] = upcoming_review_full_url
                    email_context['upcoming_reviewer'] = reviewing_parent
                    mail.send(reviewing_parent.coordinator.email,
                        template="activity_approved_to_next_reviewer",
                        context=email_context)                    
            elif review.cleaned_data['is_approved'] == False:
                activity.assignee = None
                email_context['last_reviewer'] = reviewer_club
                email_context['full_url'] = last_review_full_url
                mail.send(get_club_notification_to(activity),
                          cc=get_club_notification_cc(activity),
                          template="activity_rejected_to_coordinator",
                          context=email_context)

            else:  # If changes are requested (review.is_approved == None)
                # TODO: If the review is being edited, only do the
                # following if an actual change has been made.
                # Enable coordinators to edit the activity request in
                # correspondence to the review
                activity.is_editable = True
                activity.assignee = activity.primary_club
                email_context['full_url'] = last_review_full_url
                mail.send(get_club_notification_to(activity),
                          cc=get_club_notification_cc(activity),
                          template="activity_held_to_coordinator",
                          context=email_context)
            activity.save()
            return HttpResponseRedirect(reverse('activities:show',
                                                args=(activity.pk, )))
        # TODO: if not valid, show the error messages.

    else:
        # If the user has the permission to write then return the
        # review form page to add or edit the review.
        # Else, if they can read, then return the review read page.
        if can_write:
            template = 'activities/review_write.html'
            try: # If the review is already there, edit it.
                review_object = Review.objects.get(activity=activity,
                                                   reviewer_club=reviewer_club)
                review = ReviewForm(instance=review_object)
            except ObjectDoesNotExist:
                review = ReviewForm()
                # Note 1: Here, review is a ReviewForm object, because
                # we want to write

        elif can_read:  # If the user has read permissions, show the review read page.
            template = 'activities/review_read.html'
            try:
                review = Review.objects.get(activity=activity,
                                            reviewer_club=reviewer_club)
                # Note 2: Here, review is a Review object, because we
                # just want to read
            except ObjectDoesNotExist:
                review = None

    context = {'activity': activity, 'review': review, 'active_tab':
               reviewer_club.pk}

    return render(request, template, context)

@login_required
def participate(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id, is_deleted=False)
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
