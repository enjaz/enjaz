from django.db.utils import OperationalError
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.views.decorators import csrf

from core.models import StudentClubYear
from .models import Teams, category_choices
from clubs.models import city_choices
from .utils import is_coordinator
from .forms import DisabledTeamForm, TeamForm


def list_teams(request):
    current_year = StudentClubYear.objects.get_current()
    per_city = []
    for city_code, city_name in city_choices:
        for cat_code, cat_name in category_choices:
            try:
                teams = Teams.objects.filter(year=current_year,
                                             city=city_code,
                                             category=cat_code)
                if teams.exists():
                    per_city.append((city_name, cat_name, teams))
            except OperationalError:
                pass
    context = {'per_city': per_city}
    return render(request, 'teams/list_teams.html', context)

def show_info(request, team_id):
    team = get_object_or_404(Teams, pk=team_id)
    context = {'team': team}
    return render(request, 'teams/infocard.html', context)

def show(request, team_id):
    team = get_object_or_404(Teams, pk=team_id)

    can_edit = is_coordinator(team, request.user) or \
                request.user.is_superuser

    context = {'team': team,
                'can_edit': can_edit}
    return render(request, 'teams/show.html', context)

@login_required
@permission_required('teams.add_club', raise_exception=True)
def create(request):
    if request.method == 'POST':
        # Set the submission_date automatically.
        form = TeamForm(request.POST)
        if form.is_valid():
            print form.cleaned_data
            form.save()
            return HttpResponseRedirect(reverse('teams:list'))
        else:
            context = {'form': form}
            return render(request, 'teams/new.html', context)
    else:
        form = TeamForm()
        context = {'form': form}
        return render(request, 'teams/new.html', context)

@login_required
def edit(request, team_id):
    exisiting_team = get_object_or_404(Teams, pk=team_id)

    # If the user is neither the coordinator, nor has the permission
    # to change activities (i.e. not part of the head of the Student
    # Club), raise a PermissionDenied error.
    if not request.user == exisiting_team.coordinator and \
       not request.user.has_perm('teams.change_team'):
       raise PermissionDenied

    if request.method == 'POST':
        if request.user == exisiting_team.coordinator:
            modified_team = DisabledTeamForm(request.POST,
                                             instance=exisiting_team)
        else:
            modified_team = TeamForm(request.POST, instance=exisiting_team)
        modified_team.save()
        return HttpResponseRedirect(reverse('teams:show',
                                            args=(team_id,)))
    else:
        exisiting_team = get_object_or_404(Teams, pk=team_id)
        if request.user == exisiting_team.coordinator:
            form = DisabledTeamForm(instance=exisiting_team)
        else:
            form = TeamForm(instance=exisiting_team)
        context = {'form': form, 'team_id': team_id}
        return render(request, 'teams/new.html', context)
