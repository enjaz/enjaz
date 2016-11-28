# -*- coding: utf-8  -*-
from datetime import timedelta
from django.contrib.auth.decorators import permission_required, login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.decorators import csrf
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
import json

from post_office import mail

from activities.models import Activity, Review, Episode,  Assessment, DepositoryItem, Invitation
from activities.forms import ActivityForm, ReviewerActivityForm, DirectActivityForm, DisabledActivityForm, ReviewForm, AttachmentFormSet, AssessmentForm, ItemRequestFormSet, DisabledItemRequestFormSet, UpdateDepositoryItemForm
from accounts.utils import get_user_gender
from clubs.models import Club
from core import decorators
from core.models import Tweet
from media.models import FollowUpReport, FollowUpReportImage, Story
import activities.utils
import clubs.utils
import core.utils
import media.utils

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
    context = {'approved': Activity.objects.approved().current_year(),
               'pending': Activity.objects.none(),
               'rejected': Activity.objects.none()}

    if request.user.is_authenticated():
        template = 'activities/list_privileged.html'

        if request.user.is_superuser:
            # If the user is a super user or part of the presidency,
            # then show all activities
            context['pending'] = Activity.objects.pending().current_year()
            context['rejected'] = Activity.objects.rejected().current_year()
        elif clubs.utils.is_coordinator_or_deputy_of_any_club(request.user) or \
             clubs.utils.is_member_of_any_club(request.user):
            # For club coordinators, deputies, and members, show
            # approved activities as well as their own club's pending
            # and rejected activities.
            activity_poll = Activity.objects.undeleted().current_year().for_user_clubs(request.user).distinct()
            context['pending'] = activity_poll.pending()
            context['rejected'] = activity_poll.rejected()

            # Only display to coordinators and deputies
            if clubs.utils.is_coordinator_or_deputy_of_any_club(request.user):
                # For coordinators, show also the activities waiting their
                # action.
                user_coordination = clubs.utils.get_user_coordination_and_deputyships(request.user)
                context['todo'] = Activity.objects.current_year().filter(assignee__in=user_coordination).undeleted()
                user_club = user_coordination.first()
                if not user_club.can_skip_followup_reports:
                    # Media-related
                    context['due_report_count'] = user_club.get_due_report_count()
                    context['overdue_report_count'] = user_club.get_overdue_report_count()
                    # In activity templates, the MAX_OVERDUE_REPORTS
                    # variable is used to check whether the current user
                    # is a coordinator or a deputy.  This is to aviod
                    # passing duplicated variables.  In case the following
                    # variable is changed, the templates need to be
                    # changed as well.
                    context['MAX_OVERDUE_REPORTS'] = media.utils.MAX_OVERDUE_REPORTS

        elif clubs.utils.is_employee_of_any_club(request.user):
            # For employees, display all approved activities, as well
            # as their clubs' approved activities in a separate table.
            #
            # An employee is basically similar to a normal user, the
            # only difference is having another table that includes
            # the employee's relevant activities
            context['club_approved'] = Activity.objects.current_year().filter(primary_club__in=request.user.employee.current_year()).undeleted()

            template = 'activities/list_employee.html'
        else: # For students and other normal users.
            context['approved'] = context['approved'].for_user_city(request.user).for_user_gender(request.user)
            template = 'activities/list_normal.html'
    else: # For anonymous users
        template = 'activities/front/list.html'

    return render(request, template, context)

@login_required
def show(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id, is_deleted=False)

    context = {'activity': activity}

    if request.user.is_authenticated():
        # Save a click, redirect reviewers to the appropriate
        # reviewing page.
        reviewing_parents = Club.objects.activity_reviewing_parents(activity)
        user_reviewing_clubs = reviewing_parents.filter(coordinator=request.user) | \
                               reviewing_parents.filter(deputies=request.user)
        if user_reviewing_clubs.exists():
            reviewer_club = user_reviewing_clubs.first()
            return HttpResponseRedirect(reverse('activities:review',
                                                args=(activity.pk, reviewer_club.pk)))

        # Anyone can view forms; yet due to URL reversing issues it
        # has to be restricted to this view only Otherwise, we'll end
        # up having to specify the `current_app` attribute for every
        # view that contains a link to the forms
        context['can_view_forms'] = True

    # --- Permission checks ---

    if not clubs.utils.can_view_activity(request.user, activity) and \
       not activity.is_approved:
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
    if not request.user.has_perm("activities.add_activity") and \
       not clubs.utils.can_submit_activities(request.user):
        raise PermissionDenied

    # (2) Check if the user's club has no more than 3 overdue
    # follow-up reports.  If any club coordinated by the user exceeds
    # the 3-report threshold, prevent new activity submission (again
    # in reality the user will only coordinate one club)
    user_coordination = clubs.utils.get_user_coordination_and_deputyships(request.user)
    if any([not club.can_skip_followup_reports and club.get_overdue_report_count() > media.utils.MAX_OVERDUE_REPORTS
            for club in user_coordination]):
        raise PermissionDenied

    if user_coordination.exists():
        user_club = user_coordination.first()

    if request.method == 'POST':
        # DirectActivityForm get to choose what club to submit the
        # activity under.  Normal users shouldn't.
        can_directly_add = request.user.has_perm('activities.directly_add_activity')
        attachment_formset = AttachmentFormSet(request.POST, request.FILES)
        item_request_formset = ItemRequestFormSet(request.POST)
        if can_directly_add:
            activity = Activity(submitter=request.user)
            form = DirectActivityForm(request.POST, instance=activity)
        else:
            activity = Activity(submitter=request.user, primary_club=user_club)
            if user_club.possible_parents.exists():
                # If there are multiple possible parents, all the user to choose.
                form = ReviewerActivityForm(request.POST, instance=activity)
                form.fields['chosen_reviewer_club'].queryset = user_club.possible_parents.all()
            else:
                form = ActivityForm(request.POST, instance=activity)
        if form.is_valid() and attachment_formset.is_valid() and item_request_formset.is_valid():
            form_object = form.save()
            attachment_formset.instance = form_object
            item_request_formset.instance = form_object
            attachments = attachment_formset.save(commit=False)
            for attachment in attachments:
                attachment.submitter = request.user
                attachment.save()
            item_request_formset.save()

            # If the user can directly add activities, make the
            # activity automatically approved.  Otherwise, email the
            # reviewing parent.
            if can_directly_add:
                form_object.is_approved = True
                form_object.assignee = None
            else:
                if form.cleaned_data.get('chosen_reviewer_club'):
                    reviewing_parent = form.cleaned_data['chosen_reviewer_club']
                else:
                    reviewing_parent = form_object.primary_club.get_next_activity_reviewing_parent()

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
                    if reviewing_parent.coordinator and \
                       reviewing_parent.coordinator.email:
                        mail.send([reviewing_parent.coordinator.email],
                                   template="activity_submitted",
                                   context=email_context)
            form_object.save()
            return HttpResponseRedirect(reverse('activities:list'))
        else:
            context = {'form': form,
                       'attachment_formset': attachment_formset,
                       'item_request_formset': item_request_formset}
            return render(request, 'activities/new.html', context)
    elif request.method == 'GET':
        context = {'attachment_formset': AttachmentFormSet(), 'item_request_formset': ItemRequestFormSet()}
        if request.user.has_perm("activities.directly_add_activity"):
            form = DirectActivityForm()
        else:
            if user_club.possible_parents.exists():
                form = ReviewerActivityForm()
                form.fields['chosen_reviewer_club'].queryset = user_club.possible_parents.all()
            else:
                form = ActivityForm()
            context['user_club'] = user_club
        context['form'] = form
        return render(request, 'activities/new.html', context)

@login_required
def edit(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id,
                                 is_deleted=False)

    if not clubs.utils.can_edit_activity(request.user, activity):
        raise PermissionDenied

    user_coordination = clubs.utils.get_user_coordination_and_deputyships(request.user)
    user_club = user_coordination.first()

    if request.method == 'POST':
        attachment_formset = AttachmentFormSet(request.POST,
                                               request.FILES,
                                               instance=activity)
        item_request_formset = ItemRequestFormSet(request.POST,
                                                  instance=activity)

        if request.user.has_perm('activities.directly_add_activity'):
            modified_activity = DirectActivityForm(request.POST,
                                                   instance=activity)
        elif not activity.is_editable and \
             clubs.utils.has_coordination_to_activity(request.user, activity):
            modified_activity = DisabledActivityForm(request.POST,
                                                     instance=activity)
            item_request_formset = None
        elif activity.primary_club.possible_parents.exists():
            modified_activity = ReviewerActivityForm(request.POST, instance=activity)
            modified_activity.fields['chosen_reviewer_club'].queryset = activity.primary_club.possible_parents.all()
        else:
            modified_activity = ActivityForm(request.POST,
                                             instance=activity)

        # Should check that edits are valid before saving
        if modified_activity.is_valid() and \
           attachment_formset.is_valid() and \
           (not item_request_formset or item_request_formset and item_request_formset.is_valid()):
            modified_activity.save()
            if activity.is_editable:
                item_request_formset.save()

            # Handle attachments
            attachments = attachment_formset.save(commit=False)
            for changed_attachment, fields in attachment_formset.changed_objects:
                changed_attachment.save()
            for new_attachment in attachment_formset.new_objects:
                # Just in case an attachment was uploaded by a user
                # other than the original activity submitter, we need
                # to document that.
                new_attachment.submitter = request.user
                new_attachment.save()
            for deleted_attachment in attachment_formset.deleted_objects:
                deleted_attachment.delete()
            
            # If the choesn reviewer club was changed, the new one
            # should be the assignee (i.e. reset the stage), send them
            # a notification, and no notification should be sent to
            # that pending review club. Otherwise, if the edit has
            # been done in response to a review, send a notification
            # email to the pending review club.
            if 'chosen_reviewer_club' in modified_activity.changed_data:
                chosen_reviewer_club = modified_activity.cleaned_data['chosen_reviewer_club']
                activity.assignee = chosen_reviewer_club
                show_activity_url = reverse('activities:show', args=(activity.pk,))
                full_url = request.build_absolute_uri(show_activity_url)
                email_context = {'activity': activity,
                                 'full_url': full_url,
                                 'reviewer_club': chosen_reviewer_club}
                if chosen_reviewer_club.coordinator and \
                   chosen_reviewer_club.coordinator.email:
                    mail.send([chosen_reviewer_club.coordinator.email],
                               template="activity_submitted",
                               context=email_context)
            elif activity.assignee == activity.primary_club:
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
            context = {'form': modified_activity,
                       'user_club': user_club,
                       'activity_id': activity_id,
                       'attachment_formset': attachment_formset,
                       'item_request_formset': item_request_formset,
                       'edit': True}
            return render(request, 'activities/new.html', context)
    else:
        attachment_formset = AttachmentFormSet(instance=activity)
        item_request_formset = ItemRequestFormSet(instance=activity)

        # There are different activity forms depending on what
        # permission the user has.  Presidency group members
        # (i.e. with directly_add_activity) can add activities
        # directly without waiting for the approval of the deanship.
        # They can also (with change_activity) edit activities
        # regardless of their is_editable value.
        if request.user.has_perm('activities.directly_add_activity'):
            form = DirectActivityForm(instance=activity)
        elif not activity.is_editable and \
             clubs.utils.has_coordination_to_activity(request.user, activity):
            form = DisabledActivityForm(instance=activity)
            item_request_formset = DisabledItemRequestFormSet(instance=activity)
        elif activity.primary_club.possible_parents.exists():
            form = ReviewerActivityForm(instance=activity)
            form.fields['chosen_reviewer_club'].queryset = activity.primary_club.possible_parents.all()
        else:
            form = ActivityForm(instance=activity)
        context = {'form': form, 'activity_id': activity_id,
                   'user_club': user_club, 
                   'activity': activity, 'edit': True,
                   'attachment_formset': attachment_formset,
                   'item_request_formset': item_request_formset}
        return render(request, 'activities/new.html', context)

@login_required
def delete(request,activity_id):
    activity = get_object_or_404(Activity, pk=activity_id, is_deleted=False)
    context = {'activity': activity}

    if not clubs.utils.can_delete_activity(request.user, activity):
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

    reviewing_parents = Club.objects.activity_reviewing_parents(activity)

    # Is the passed reviewer club a member of the activity owner's
    # reviewer parents? If not, raise a 404 error.
    if not reviewing_parents.filter(pk=reviewer_club.pk).exists():
        raise Http404

    # Is the current user a coordinator/deputy of the reviewer club?
    user_is_current_reviewer = clubs.utils.is_coordinator_or_deputy(reviewer_club, request.user)

    # The user can WRITE if they are the coordinator or deputy of the
    # reviewer club; or a superuser
    can_write = user_is_current_reviewer or request.user.is_superuser

    # The user can READ if they are the coordinator or deputy of the
    # activity owning club (primary or secondary); the coordinator or
    # deputy of a parent reviewer other than the ``reviewer_club``; or
    # an employee responsible for the activity owning club.
    can_read = activities.utils.can_read_reviews(request.user, activity)

    # If the user has no read or write permissions, then they can't
    # access the view.
    if not can_read and not can_write:
        raise PermissionDenied

    # --- End of Permission Checks ---

    if request.method == "POST":
        try:  # If the review is already there, edit it.
            review_object = Review.objects.get(activity=activity,
                                               reviewer_club=reviewer_club)
        except Review.DoesNotExist:
            review_object = Review(activity=activity,
                                   reviewer=request.user,
                                   reviewer_club=reviewer_club)
        review = ReviewForm(request.POST, instance=review_object)

        if review.is_valid():
            # If the review instance has an idea, it's being edited.
            # Otherwise, it's a new review.
            is_new = not bool(review.instance.id)
            review.save()
            # Once the activity is approved (or partially approved),
            # lock it from being edited.  This is very critical as to
            # prevent manipulations (ie, editing the request after the
            # approval of the presidency and before it's reviewed by
            # DSA). Only when an edit is requested by the reviewer
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
                # This loop is to handle a situation in which the
                # chosen_parent_reviewer has been changed after the
                # activity has been reviewed by other grandparents.
                # In that case, we just need to skip all parents who
                # have alraedy approved that activity.
                reviewing_parent = reviewer_club.get_next_activity_reviewing_parent()
                while True:
                    parent_review = Review.objects.filter(activity=activity,
                                                          reviewer_club=reviewing_parent,
                                                          is_approved=True).exists()
                    if parent_review:
                        # If the activity has already been approved by
                        # a parent, move to the next and test it again
                        # (if it exists)
                        reviewing_parent = reviewing_parent.get_next_activity_reviewing_parent()
                        if reviewing_parent:
                            continue
                    break

                # Reached the top of the review hierarchy => activity
                # approved.
                if not reviewing_parent:
                    activity.assignee = None
                    if 'is_approved' in review.changed_data:
                        # Email notifications
                        email_context['full_url'] = activity_full_url
                        mail.send(activities.utils.get_club_notification_to(activity),
                            cc=activities.utils.get_club_notification_cc(activity, reviewer_club),
                            template="activity_approved_to_coordinator",
                            context=email_context)
                        if activity.primary_club.employee:
                            email_context['full_url'] = last_review_full_url
                            mail.send([activity.primary_club.employee.email],
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
                    if reviewing_parent.coordinator and \
                       reviewing_parent.coordinator.email and \
                       'is_approved' in review.changed_data:
                        mail.send(reviewing_parent.coordinator.email,
                                  template="activity_approved_to_next_reviewer",
                                  context=email_context)                    
            elif review.cleaned_data['is_approved'] == False:
                activity.assignee = None
                if 'is_approved' in review.changed_data:
                    email_context['last_reviewer'] = reviewer_club
                    email_context['full_url'] = last_review_full_url
                    mail.send(activities.utils.get_club_notification_to(activity),
                              cc=activities.utils.get_club_notification_cc(activity, reviewer_club),
                              template="activity_rejected_to_coordinator",
                              context=email_context)

            elif review.cleaned_data['is_approved'] == None: # If changes were requested.
                # Enable coordinators to edit the activity request in
                # correspondence to the review
                activity.is_editable = True
                activity.assignee = activity.primary_club
                # We don't want to send email notification if
                # is_approved hasn't been changed, but we also want to
                # send a notification when the review is created.  The
                # default choice for is_approved is None.  That's why
                # it won't show in changed_data if a new review was
                # created.  For that, we should add a special test,
                # is_new.
                if is_new or 'is_approved' in review.changed_data:
                    email_context['last_reviewer'] = reviewer_club
                    email_context['full_url'] = last_review_full_url
                    mail.send(activities.utils.get_club_notification_to(activity),
                              cc=activities.utils.get_club_notification_cc(activity, reviewer_club),
                              template="activity_held_to_coordinator",
                              context=email_context)
            activity.save()
            return HttpResponseRedirect(reverse('activities:list'))
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
            except Review.DoesNotExist:
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
            except Review.DoesNotExist:
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

@login_required
def assessment_index(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id, is_deleted=False)

    if not activities.utils.can_assess_club(request.user, activity.primary_club):
        raise PermissionDenied

    # Determine the category.  If not Media Center (i.e. super user or
    # vice president, default to the presidency review)
    if media.utils.can_assess_club_as_media(request.user, activity.primary_club):
        return HttpResponseRedirect(reverse('activities:assess',
                                    args=(activity_id, 'm')))
    else: 
        return HttpResponseRedirect(reverse('activities:assess',
                                    args=(activity_id, 'p')))

@login_required
def assessment_list(request):
    if not activities.utils.can_assess_any_club(request.user):
        raise PermissionDenied

    context = {}
    user_assessing_clubs = clubs.utils.get_user_clubs(request.user).filter(can_assess=True)
    user_media_center = media.utils.get_user_media_center(request.user)
    clubs_for_user = media.utils.get_clubs_for_assessment_by_user(request.user).filter(is_assessed=True)

    approved_activvities = Activity.objects.current_year().approved().done().filter(primary_club__in=clubs_for_user).distinct()
    # 'done' has different meanings for the Media Center, the
    # Presidency and the superuser.
    if user_media_center: # Media
        context['category'] = 'M'
        context['todo'] = approved_activvities.exclude(assessment__criterionvalue__criterion__category='M')
        if media.utils.is_media_coordinator_or_deputy(request.user):
            context['done'] = approved_activvities.filter(assessment__criterionvalue__criterion__category='M')\
                                                  .exclude(assessment__is_reviewed=False)
        else:
            context['done'] = approved_activvities.filter(assessment__criterionvalue__criterion__category='M')
    elif user_assessing_clubs.exists(): # Presidency
        context['category'] = 'P'
        context['done'] = approved_activvities.filter(assessment__criterionvalue__criterion__category='P')
        context['todo'] = approved_activvities.exclude(assessment__criterionvalue__criterion__category='P')
    else: # Superuser
        context['category'] = 'P'
        context['done'] = approved_activvities.filter(assessment__criterionvalue__criterion__category='P')\
                                              .filter(assessment__criterionvalue__criterion__category='M')\
                                              .exclude(assessment__is_reviewed=False)
        # FIXME: The following query is buggy (#24525)
        #context['todo'] = (approved_activvities.exclude(assessment__criterionvalue__criterion__category='M') | \
        #                   approved_activvities.exclude(assessment__criterionvalue__criterion__category='P')\
        #                                       .exclude(assessment__is_reviewed=False))
        context['todo'] = approved_activvities.exclude(assessment__criterionvalue__criterion__category='P')
    # Only show 'toreview' to media coordinator and deputy, and to the
    # superuser.
    if media.utils.is_media_coordinator_or_deputy(request.user) or \
       request.user.is_superuser:
        # Jeddah has no Media Center members, so don't show them the
        # toreview table.  It is all going to be done by the Medica
        # Center President.
        if not (user_media_center and user_media_center.city == 'J'):
            context['toreview'] = approved_activvities.filter(assessment__criterionvalue__criterion__category='M',
                                                              assessment__is_reviewed=False)
    return render(request, 'activities/assessment_list.html', context)
    
@login_required
def assess(request, activity_id, category):
    activity = get_object_or_404(Activity, pk=activity_id, is_deleted=False)
    category = category.upper()

    if not activities.utils.can_assess_club(request.user, activity.primary_club):
        raise PermissionDenied

    assessor_club = activities.utils.get_club_assessing_club_by_user(request.user, activity.primary_club)

    # Don't make it possible for Media Center to enter presidency
    # assessment and vice versa.  If no assessing clubs, we are
    # dealing with the superuser, so don't preform such checks and set
    # the assessor_club to None.
    if assessor_club:
        if media.utils.can_assess_club_as_media(request.user, activity.primary_club):
            if category != 'M':
                raise PermissionDenied
        else: # Vice president
            if category != 'P':
                raise PermissionDenied
    elif request.user.has_perms('activities.add_assessment'): # superuser
        assessor_club = None

    # If the assessment is already there, edit it.
    try:  
        assessment = Assessment.objects.distinct().get(activity=activity,
                                                       criterionvalue__criterion__category=category)
    except Assessment.DoesNotExist:
        assessment = Assessment(activity=activity,
                                assessor=request.user,
                                assessor_club=assessor_club)

    if request.method == 'POST':
        form = AssessmentForm(request.POST, instance=assessment,
                              activity=activity,
                              user=request.user, club=assessor_club,
                              category=category)
        if form.is_valid():
            form.save()
            # By default, after an activity has ended, it will be
            # assigned for presidency for assessment, but an email
            # will be sent to both: presidency and the media center.
            # If the presidency assess it, but the Media Center is
            # still lacking, it will be assigned to the Media Center,
            # otherwise, it will be assigned to no one (#yay).
            if category  == 'P':
                media_center = activity.get_media_assessor()
                if media_center.assessment_set.filter(activity=activity).exists():
                    activity.assignee = None
                else:
                    activity.assignee = media_center
                activity.save()

            return HttpResponseRedirect(reverse('activities:assessment_list'))

    elif request.method == 'GET':
        form = AssessmentForm(instance=assessment, activity=activity,
                              user=request.user, club=assessor_club,
                              category=category)

    context = {'activity': activity, 'form': form, 'active_tab': 'assessment'}
    if category == 'P':
        template_name = 'activities/assessment_presidency.html'
        # Presidency-specific helper calculations
        submission_interval = (activity.get_first_date() - activity.submission_date.date()).days
        context['submission_interval'] = submission_interval
    elif category == 'M':
        context['reports'] = FollowUpReport.objects.filter(episode__activity=activity)
        context['images'] = FollowUpReportImage.objects.filter(report__episode__activity=activity)
        context['stories'] = Story.objects.filter(episode__activity=activity)
        template_name = 'activities/assessment_media_center.html'

    return render(request, template_name, context)

def list_depository_items(request):
    context = {}
    if request.method == 'POST':
        form = UpdateDepositoryItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("activities:list_depository_items"))
    elif request.method == 'GET':            
        categories = DepositoryItem.objects.values_list('category', flat=True).distinct()
        categorized_items_list = []
        for category in categories:
            items = DepositoryItem.objects.filter(category=category)
            categorized_items_list.append({'category': category, 'items': items})
        context['categorized_items_list'] = categorized_items_list
    return render(request, 'activities/list_depository_items.html', context)


def autocomplete_items(request):
    term = request.GET.get('term')
    if not term:
        raise Http404

    qs = DepositoryItem.objects.filter(quantity__gte=0) | \
         DepositoryItem.objects.filter(quantity__isnull=True)

    result_query = core.utils.get_search_queryset(qs, ['name', 'category'], term)
    result_list = [u"{} ({})".format(r.name, r.category) for r in result_query]
    return HttpResponse(json.dumps(result_list))

def show_invitation(request, pk):
    invitation = get_object_or_404(Invitation, pk=pk)
    if invitation.publication_date and \
       invitation.publication_date > timezone.now():
        raise Http404

    if request.user.is_authenticated() and \
       invitation.students.filter(pk=request.user.pk).exists():
        already_on = True
    else:
        already_on = False
    if invitation.is_available_for_user_city(request.user):
        restricted_by_city = False
    else:
        restricted_by_city = True

    if invitation.is_available_for_user_gender(request.user):
        restricted_by_gender = False
    else:
        restricted_by_gender = True

    if invitation.is_open_registration:
        open_registration = True
    else:
        open_registration = False


    context = {'invitation': invitation, 'already_on': already_on,
               'restricted_by_gender': restricted_by_gender,
               'restricted_by_city': restricted_by_city,
               'open_registration':open_registration}
    return render(request, 'activities/show_invitation.html', context)

@decorators.ajax_only
@decorators.post_only
@csrf.csrf_exempt
@login_required
def toggle_confirm_invitation(request, pk):
    invitation = get_object_or_404(Invitation, pk=pk)
    action = request.POST.get('action')
    if timezone.now() > invitation.get_end_datetime():
        raise Exception(u"انتهى النشاط")

    if action == "add":
        if not invitation.is_available_for_user_city(request.user):
            raise Exception(u"هذا النشاط ليس متاحًا في مدينتك.")
        if not invitation.is_available_for_user_gender(request.user):
            raise Exception(u"هذا النشاط يستهدف {} فقط".format(invitation.get_gender_display()))
        if invitation.is_fully_booked():
            raise Exception(u"اكتملت المقاعد الممكنة لهذا الحدث، ولم يعد ممكنا التسجيل فيه!")
        invitation.students.add(request.user)
        if request.user.social_auth.exists():
            show_url = reverse('activities:show_invitation', args=(invitation.pk,))
            full_url = request.build_absolute_uri(show_url)
            text = u"سأحضر {}.\nيمكنك التسجيل للحضور من هنا: {}"
            if invitation.hashtag:
                text += u"\n#" + invitation.hashtag
            Tweet.objects.create(text=text.format(invitation.title, full_url),
                                 user=request.user)


    elif action == "remove":
        if invitation.students.filter(pk=request.user.pk).exists():
            invitation.students.remove(request.user)
        else:
            raise Exception(u"لا تسجيل.")

    return {}
def invitation_participants(request, pk):
    invitation = get_object_or_404(Invitation, pk=pk)
    activity = invitation.activity
    if not request.user.is_superuser and not is_media_coordinator_or_member(user):
        raise PermissionDenied
    if invitation.activity:
        if not clubs.utils.has_coordination_to_activity(user, activity) and not \
            clubs.utils.is_member(activity.primary_club, user):
            raise PermissionDenied
    return render(request, 'activities/invitation_participants.html')

