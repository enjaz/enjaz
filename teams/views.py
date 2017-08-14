from __future__ import absolute_import
from lib2to3.pgen2.driver import load_grammar

from django.db.utils import OperationalError
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required, login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.views.decorators import csrf
from django.views import generic
from rules.contrib.views import PermissionRequiredMixin

from core.models import StudentClubYear
from teams.models import Team, CATEGORY_CHOICES
from clubs.models import city_choices
from teams.utils import is_coordinator
from teams.forms import DisabledTeamForm, TeamForm
from core import decorators
from teams import forms


class ListView(generic.ListView):
    template_name = 'teams/list_teams.html'
    context_object_name = 'all_teams'

    def get_queryset(self, **kwargs):
        # FIXME: The year filter returns no teams at all. Maybe the year is not being set on the team instances?
        # current_year = StudentClubYear.objects.get_current()
        return Team.objects.all()  # filter(year=current_year)


def show_info(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    context = {'team': team}
    return render(request, 'teams/infocard.html', context)


class DetailView(generic.DetailView):
    model = Team
    template_name = "teams/show.html"
    pk_url_kwarg = 'team_id'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['form'] = forms.AddTeamMembersForm(instance=self.object)

        return context


class CreateView(PermissionRequiredMixin, generic.CreateView):
    model = Team
    form_class = TeamForm
    template_name = 'teams/new.html'
    permission_required = 'teams.add_team'

    # TODO: set year automatically

class UpdateView(PermissionRequiredMixin, generic.UpdateView):
    model = Team
    form_class = TeamForm
    template_name = 'teams/new.html'
    pk_url_kwarg = 'team_id'
    permission_required = 'teams.change_team_display_details'

@decorators.ajax_only
@csrf.csrf_exempt
@decorators.post_only
@login_required
def add_members(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    ar_name = team.ar_name

    if not request.user == team.leader and \
            not request.user.is_superuser:
        raise PermissionDenied

    context = {}

    if request.method == 'POST':
        form = forms.AddTeamMembersForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return {"message": "success"}
    context['form'] = form

    return render(request, 'teams/show.html', context)
