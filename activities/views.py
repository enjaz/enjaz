from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import ModelForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist

from activities.models import Activity, Review, Participation


class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        fields = ['primary_club', 'secondary_clubs',
                  'name','description', 'date', 'time',
                  'custom_datetime', 'participants', 'organizers',
                  'requirements', 'inside_collaborators',
                  'outside_collaborators', 'collect_participants']

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['clubs_notes', 'name_notes', 'description_notes',
                  'datetime_notes', 'requirement_notes',
                  'inside_notes', 'outside_notes',
                  'participants_notes', 'organizers_notes', 'is_approved']

def list(request):
    # If the user is part of the head of the Student Club, or part of
    # the Media Team, they should be able to view all activities
    # (i.e. approved, rejected and pending).  Otherwise, a user should
    # only see approved activities and the activities of the clubs
    # they have memberships in (regardless of their status).
    if request.user.has_perm('activities.view_activity'):
        if request.GET.get('pending') == "1":
            activities = Activity.objects.filter(review__is_approved=None)
        else:
            activities = Activity.objects.all()
    else:
        approved_activities = Activity.objects.filter(review__is_approved=True)
        if request.user.is_authenticated():
            user_activities = request.user.activity_set.all()
            user_clubs = request.user.memberships.all() | request.user.coordination.all()
            primary_club_activities = Activity.objects.filter(
                primary_club__in=user_clubs)
            secondary_club_activities = Activity.objects.filter(
                secondary_clubs__in=user_clubs)
        else:
            user_activities = Activity.objects.none()
            primary_activities = Activity.objects.none()
            secondary_club_activities = Activity.objects.none()
        activities = approved_activities | user_activities | \
                     primary_activities | secondary_club_activities

    order = request.GET.get('order')
    if order == 'date':
        sorted_activities = activities.order_by('-date')
    elif order == 'club':
        sorted_activities = activities.order_by('-primary_club')
    else:
        sorted_activities = activities.order_by('-submission_date')

    #Each page of results should have a maximum of 25 activities.
    paginator = Paginator(sorted_activities, 25)
    page = request.GET.get('page')

    try:
        page_activities = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_activities = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_activities = paginator.page(paginator.num_pages)

    context = {'page_activities': page_activities}
    return render(request, 'activities/list.html', context)

def show(request, activity_id):
    # If the activity is approved, everyone can see it.  If it is not,
    # only the head of the Student Club, the Media Team, the members
    # of the related clubs and the person who submitted it can see it.

    activity = get_object_or_404(Activity, pk=activity_id)
    context = {'activity': activity}
    if request.user.is_authenticated():
        user_clubs = request.user.memberships.all() | request.user.coordination.all()
        is_coordinator = activity.primary_club in request.user.coordination.all()

        if request.user.has_perm('activities.change_activity') or \
           is_coordinator:
            context['can_edit'] = True
        if request.user.has_perm('activities.view_participation') or \
           is_coordinator:
            context['can_view_participation'] = True
        if request.user.has_perm('activities.view_review') or \
           is_coordinator:
            context['can_view_review'] = True
            try:
                review = Review.objects.get(activity=activity)
                context['review'] = review
            except ObjectDoesNotExist:
                pass
    else:
        user_clubs = Activity.objects.none()

    activity_primary_club = activity.primary_club
    activity_secondary_clubs = activity.secondary_clubs.all()
    activity_clubs = [activity_primary_club] + [club for club in activity_secondary_clubs]
    try:
        activity_status = activity.review.is_approved
    except ObjectDoesNotExist:
        activity_status = False

    # The third test condition, that is:
    #   any([club in activity_clubs for club in user_clubs])
    #  checks if any of the clubs the user is a member of is also
    #  orginizing the activity that the user is trying to see.  If
    #  will be True if any club is one of the organizers and it will
    #  be False if none is.

    if not activity_status and \
       not request.user.has_perm('activities.view_activity') and \
       not any([club in activity_clubs for club in user_clubs]) and \
       not request.user == activity.submitter:
        raise PermissionDenied

    return render(request, 'activities/show.html', context)

@permission_required('activities.add_activity', raise_exception=True)
def create(request):
    if request.method == 'POST':
        # Set the submission_date automatically.
        activity = Activity(submitter=request.user)
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('activities:list'))
        else:
            context = {'form': form}
            return render(request, 'activities/new.html', context)
    else:
        form = ActivityForm()
        context = {'form': form}
        return render(request, 'activities/new.html', context)

def edit(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    user_coordination = request.user.coordination.all()
    activity_primary_club = activity.primary_club
    activity_secondary_clubs = activity.secondary_clubs.all()
    activity_clubs = [activity_primary_club] + activity_secondary_clubs

    # If the user is neither the submitter, nor has the permission to
    # change activities (i.e. not part of the head of the Student
    # Club, or the Media Team), not a coordinator of any of the
    # organizing clubs, raise a PermissionDenied error.
    if not request.user == activity.submitter and \
       not request.user.has_perm('activities.change_activity') and \
       not any([club in activity_clubs for club in user_coordination]):
        raise PermissionDenied

    if request.method == 'POST':        
        modified_activity = ActivityForm(request.POST, instance=activity)
        modified_activity.save()
        return HttpResponseRedirect(reverse('activities:list'))
    else:
        form = ActivityForm(instance=activity)
        context = {'form': form, 'activity_id': activity_id,
                   'edit': True}
        return render(request, 'activities/new.html', context)

@permission_required('activities.add_review', raise_exception=True)
def review(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    if request.method == 'POST':
        review_object = Review(activity=activity, reviewer=request.user)
        review = ReviewForm(request.POST, instance=review_object)
        if review.is_valid():
            review.save()
            if review.cleaned_data['is_approved']:
                activity.is_editable = False
                activity.save()
            return HttpResponseRedirect(reverse('activities:show',
                                                args=(activity_id,)))
    else:
        try: # If the review is already there, edit it.
            review_object = Review.objects.get(activity=activity)
            review = ReviewForm(instance=review_object)
        except ObjectDoesNotExist:
            review = ReviewForm()
    context = {'activity': activity, 'is_review': True,
               'review': review}
    return render(request, 'activities/show.html', context)

@login_required
def participate(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
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
            return HttpResponseRedirect(reverse('activities:show',
                                                args=(activity_id,)))
        else:
            context['error_message'] = 'unknown'
            return render(request, 'activities/participate.html', context)
    else:
        return render(request, 'activities/participate.html', context)

def view_participation(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    if not activity.primary_club in request.user.coordination.all() and \
       not request.user.has_perm('activities.view_participation'):
        raise PermissionDenied

    participations = Participation.objects.filter(activity=activity)
    context = {'participations': participations, 'activity': activity}
    return render(request, 'activities/view_participations.html', context)
