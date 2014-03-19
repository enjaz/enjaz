from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import ModelForm
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied

from clubs.models import Club

class ClubForm(ModelForm):
    class Meta:
        model = Club
        fields = ['name','english_name','description', 'email',
                  'parent', 'coordinator']

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
        activities = club.activity_set.all()
    else:
        activities = club.activity_set.filter(is_approved=True)

    can_edit = request.user == club.coordinator or \
               request.user.has_perm('clubs.change_club')
    context = {'club': club, 'can_edit': can_edit,
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
