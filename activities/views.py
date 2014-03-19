from datetime import datetime

from django.contrib.auth.decorators import permission_required, user_passes_test
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import ModelForm
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied

from activities.models import Activity

class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        fields = ['clubs','name','description', 'participants',
                  'organizers', 'requirements', 'inside_collaborators',
                  'outside_collaborators', 'collect_participants']

def list(request):
    # If the user is part of the head of the Student Club, or part of
    # the Media Team, they should be able to view all activities
    # (i.e. approved, rejected and pending).  Otherwise, a user should
    # only see approved activities and the activities of the clubs
    # they have memberships in (regardless of their status).

    if request.user.has_perm('activities.view_activity'):
        latest_activities = Activity.objects.order_by('-submission_date')[:5]
    else:
        approved_activities = Activity.objects.filter(is_approved=True)
        if request.user.is_authenticated():
            user_activities = request.user.activity_set.all()
            user_clubs = request.user.memberships.all() | request.user.coordination.all()
            club_activities = Activity.objects.filter(clubs__in=user_clubs)
        else:
            user_activities = Activity.objects.none()
            club_activities = Activity.objects.none()
        activities = approved_activities | user_activities | club_activities
        latest_activities = activities.order_by('-submission_date')[:5]

    context = {'latest_activities': latest_activities}
    return render(request, 'activities/list.html', context)

def show(request, activity_id):
    # If the activity is approved, everyone can see it.  If it is not,
    # only the head of the Student Club, the Media Team, the members
    # of the related clubs and the person who submitted it can see it

    activity = get_object_or_404(Activity, pk=activity_id)
    user_clubs = request.user.memberships.all() | request.user.coordination.all()
    activity_clubs = activity.clubs.all()

    # The third test condition, that is:
    #   any([club in activity_clubs for club in user_clubs])
    #  checks if any of the clubs the user is a member of is also
    #  orginizing the activity that the user is trying to see.  If
    #  will be True if any club is one of the organizers and it will
    #  be False if none is.

    if not activity.is_approved and \
       not request.user.has_perm('activities.view_activity') and \
       not any([club in activity_clubs for club in user_clubs]) and \
       not request.user == activity.submitter:
        raise PermissionDenied
    context = {'activity': activity}
    return render(request, 'activities/show.html', context)

@permission_required('activities.add_activity', raise_exception=True)
def create(request):
    if request.method == 'POST':
        # Set the submission_date automatically.
        activity = Activity(submission_date=datetime.now(),
                            submitter=request.user)
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            print form.cleaned_data
            form.save()
            return HttpResponseRedirect(reverse('activities:index'))
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
    activity_clubs = activity.clubs.all()

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
        return HttpResponseRedirect(reverse('activities:index'))
    else:
        form = ActivityForm(instance=activity)
        context = {'form': form, 'activity_id': activity_id}
        return render(request, 'activities/new.html', context)

@permission_required('activities.review_activity', raise_exception=True)
def review(request, activity_id):
    if request.method == 'POST':
        activity = get_object_or_404(Activity, pk=activity_id)
        if "review" in request.POST:
            if 'accept' in request.POST['review']:
                activity.is_approved = True
            elif 'reject' in request.POST['review']:
                activity.is_approved = False
            activity.is_editable = False
            activity.save()
            return HttpResponseRedirect(reverse('activities:show', args=(activity_id,)))
        else:
            return HttpResponse("You are reviewing activity #%s." % activity_id)
    else:
        activity = get_object_or_404(Activity, pk=activity_id)
        context = {'activity': activity, 'review': True}
        return render(request, 'activities/show.html', context)
