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
        current_year = StudentClubYear.objects.get_current()
        for city_code, city_name in city_choices:
            for cat_code, cat_name in CATEGORY_CHOICES:
                try:
                    teams = Team.objects.filter(year=current_year,
                                                city=city_code,
                                                category=cat_code)
                    return teams
                except ObjectDoesNotExist:
                    raise Http404

    #TODO: Find out how to avoid this repetition > ~ <
    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        current_year = StudentClubYear.objects.get_current()
        per_city = []
        for city_code, city_name in city_choices:
            per_category = []
            for cat_code, cat_name in CATEGORY_CHOICES:
                try:
                    teams = Team.objects.filter(year=current_year,
                                                city=city_code,
                                                category=cat_code)
                    if teams.exists():
                        per_category.append((cat_name, teams))
                except ObjectDoesNotExist:
                    raise Http404
            per_city.append((city_name, per_category))
        context['per_city'] = per_city
        return context

def show_info(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    context = {'team': team}
    return render(request, 'teams/infocard.html', context)


@decorators.get_only
def show(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    form = forms.AddTeamMembersForm(instance=team)

    can_edit = is_coordinator(team, request.user) or \
                request.user.is_superuser

    context = {'team': team,
               'can_edit': can_edit,
               'form':form}
    return render(request, 'teams/show.html', context)

class CreateView(generic.CreateView):
    form_class = TeamForm
    template_name = 'teams/new.html'
    success_url = 'teams:list_teams'

    #TODO: set year automatically

    # can't decorate the class in django 1.8 like this:
    # @method_decorator(<decorator>, name='dispatch')
    # class CreateView(...): etc

    @method_decorator(permission_required('teams.add_club', raise_exception=True))
    # I did login_required as URLconf decorator; see teams/urls
    def dispatch(self, *args, **kwargs):
        return super(CreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        """
        If the form is valid,...
        """
        print form.cleaned_data
        self.object = form.save()
        return HttpResponseRedirect(reverse('teams:list_teams'))


@login_required
def edit(request, team_id):
    exisiting_team = get_object_or_404(Team, pk=team_id)

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
        exisiting_team = get_object_or_404(Team, pk=team_id)
        if request.user == exisiting_team.coordinator:
            form = DisabledTeamForm(instance=exisiting_team)
        else:
            form = TeamForm(instance=exisiting_team)
        context = {'form': form, 'team_id': team_id}
        return render(request, 'teams/new.html', context)


@decorators.ajax_only
@csrf.csrf_exempt
@decorators.post_only
@login_required
def add_members(request,team_id):

    team = get_object_or_404(Team, pk=team_id)
    ar_name=team.ar_name

    if not request.user == team.leader and \
       not request.user.is_superuser:
       raise PermissionDenied

    context={}

    if request.method == 'POST':
        form = forms.AddTeamMembersForm(request.POST,instance=team)
        if form.is_valid():
            form.save()
            return {"message": "success"}
    context['form'] = form

    return render(request, 'teams/show.html', context)



