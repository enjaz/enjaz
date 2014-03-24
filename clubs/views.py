from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import ModelForm
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required, login_required
from django.core.exceptions import PermissionDenied

from clubs.models import Club, MembershipApplication

class ClubForm(ModelForm):
    class Meta:
        model = Club
        fields = ['name','english_name','description', 'email',
                  'parent', 'coordinator', 'open_membership']

class MembershipForm(ModelForm):
    class Meta:
        model = MembershipApplication
        fields = ['note']

def list(request):
    clubs = Club.objects.all()
    context = {'clubs':clubs}
    return render(request, 'clubs/list.html', context)

def show(request, club_id):
    club = get_object_or_404(Club, pk=club_id)

    # If the user has the view_activity permission, is a member or is
    # the coordinator of the given club, they will be able to see all
    # related activities regardless fo their status.  Otherwise, only
    # see the approved ones.
    if request.user.is_authenticated() and \
       (request.user.has_perm('activities.view_activity') or \
       club in request.user.memberships.all() or \
       club in request.user.memberships.coordination):
        activities = club.primary_activity.all() | club.secondary_activity.all()
    else:
        activities = club.primary_activity.filter(is_approved=True) |\
                     club.seconday_activity.filter(is_approved=True)

    can_edit = request.user == club.coordinator or \
               request.user.has_perm('clubs.change_club')
    can_view_applications = request.user == club.coordinator or \
                            request.user.has_perm('clubs.view_application')
    context = {'club': club, 'can_edit': can_edit,
               'can_view_applications': can_view_applications,
               'activities': activities}
    return render(request, 'clubs/show.html', context)

@permission_required('clubs.add_club', raise_exception=True)
def create(request):
    if request.method == 'POST':
        # Set the submission_date automatically.
        club = Club(creation_date=datetime.now())
        form = ClubForm(request.POST, instance=club)
        if form.is_valid():
            print form.cleaned_data
            form.save()
            return HttpResponseRedirect(reverse('clubs:list'))
        else:
            context = {'form': form}
            return render(request, 'clubs/new.html', context)
    else:
        form = ClubForm()
        print form.has_changed()
        context = {'form': form}
        return render(request, 'clubs/new.html', context)

def edit(request, club_id):
    exisiting_club = get_object_or_404(Club, pk=club_id)

    # If the user is neither the coordinator, nor has the permission
    # to change activities (i.e. not part of the head of the Student
    # Club), raise a PermissionDenied error.
    if not request.user == exisiting_club.coordinator and \
       not request.user.has_perm('clubs.change_club'):
        raise PermissionDenied

    if request.method == 'POST':
        modified_club = ClubForm(request.POST, instance=exisiting_club)
        modified_club.save()
        return HttpResponseRedirect(reverse('clubs:list'))
    else:
        exisiting_club = get_object_or_404(Club, pk=club_id)
        form = ClubForm(instance=exisiting_club)
        context = {'form': form, 'club_id': club_id}
        return render(request, 'clubs/new.html', context)

@login_required
def join(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    context = {'club': club}
    if not club.open_membership:
        context = {'error_message': 'closed_membership'}
        return render(request, 'clubs/join.html', context)

    # Make sure that the user hasn't already applied!
    existing_application = MembershipApplication.objects.filter(club=club,
                                                       user=request.user)
    if existing_application:
        context['error_message'] = 'already_applied'
        return render(request, 'clubs/join.html', context)

    # Make sure the user isn't already a member!
    if club in request.user.memberships.all() or\
       club in request.user.coordination.all():
        context['error_message'] = 'already_in'
        return render(request, 'clubs/join.html', context)        

    if request.method == 'POST':
        application = MembershipApplication(club=club, user=request.user)
        form = MembershipForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('clubs:show', args=(club_id,)))
        else:
            context['form'] = form
            return render(request, 'clubs/join.html', context)
    else:
        form = MembershipForm()
        context['form'] = form
        return render(request, 'clubs/join.html', context)


def view_applications(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    if not club in request.user.coordination.all() and \
       not request.user.has_perm('clubs.view_application'):
        raise PermissionDenied

    applications = MembershipApplication.objects.filter(club=club)
    context = {'applications': applications, 'club': club}
    return render(request, 'clubs/view_applications.html', context)
