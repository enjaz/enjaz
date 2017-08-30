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
from post_office import mail

from core.models import StudentClubYear
from teams.models import Team, CATEGORY_CHOICES, Membership
from clubs.models import city_choices
from teams.utils import is_coordinator
from teams.forms import DisabledTeamForm, TeamForm, EmailForm
from core import decorators
from teams import forms


class ListView(generic.ListView):
    template_name = 'teams/list_teams.html'
    context_object_name = 'all_teams'

    def get_queryset(self, **kwargs):
        current_year = StudentClubYear.objects.get_current()
        return Team.objects.filter(year=current_year)

def show_info(request, code_name):
    team = get_object_or_404(Team, pk=code_name)
    context = {'team': team}
    return render(request, 'teams/infocard.html', context)


class DetailView(generic.DetailView):
    model = Team
    template_name = "teams/show.html"
    slug_field = 'code_name'
    slug_url_kwarg = 'code_name'

    def get_object(self):
        current_year = StudentClubYear.objects.get_current()
        team = get_object_or_404(
            self.model,
            code_name=self.kwargs['code_name'],
            year=current_year)
        return team

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['form'] = forms.AddTeamMembersForm(instance=self.object)

        return context

class ArchiveDetailView(generic.DetailView):
    model = Team
    template_name = "teams/show.html"
    slug_field = 'code_name'
    slug_url_kwarg = 'code_name'

    def get_object(self):
        team = get_object_or_404(
            self.model,
            code_name=self.kwargs['code_name'],
            year__start_date__year=self.kwargs['year'])
        return team

    def get_context_data(self, **kwargs):
        context = super(ArchiveDetailView, self).get_context_data(**kwargs)
        context['form'] = forms.AddTeamMembersForm(instance=self.object)
        return context

class CreateView(PermissionRequiredMixin, generic.CreateView):
    model = Team
    form_class = TeamForm
    template_name = 'teams/new.html'
    success_url = 'teams:list_teams'
    permission_required = 'teams.add_teams'
    current_year = StudentClubYear.objects.get_current()
    # TODO: set year automatically
    def get_initial(self):
        return {'year': self.current_year}

class UpdateView(PermissionRequiredMixin, generic.UpdateView):
    model = Team
    form_class = TeamForm
    template_name = 'teams/new.html'
    slug_field = 'code_name'
    slug_url_kwarg = 'code_name'
    permission_required = 'teams.change_team_display_details'

    def get_object(self):
        current_year = StudentClubYear.objects.get_current()
        team = get_object_or_404(
            self.model,
            code_name=self.kwargs['code_name'],
            year=current_year)
        return team

@decorators.ajax_only
@csrf.csrf_exempt
@decorators.post_only
@login_required
def add_members(request, code_name):
    current_year = StudentClubYear.objects.get_current()
    team = get_object_or_404(Team, code_name=code_name, year=current_year)
    ar_name = team.ar_name

    if not request.user == team.leader and \
            not request.user.is_superuser and \
            team.is_open is False:
        raise PermissionDenied

    context = {}

    if request.method == 'POST':
        form = forms.AddTeamMembersForm(request.POST, instance=team)
        if form.is_valid():
            form.save(commit=False)
            membership = Membership(member=request.user, team=team)
            #TODO: check how to specify memeber ^
            membership.save()
            return {"message": "success"}
    context['form'] = form

    return render(request, 'teams/show.html', context)

@decorators.ajax_only
@login_required
def send_email(request, code_name):
    current_year = StudentClubYear.objects.get_current()
    team = get_object_or_404(Team, code_name=code_name, year=current_year)

    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email_context = {'user': request.user,
                             'team': team,
                             'data': form.cleaned_data}
            mail.send([request.user.email],
                       template="teams_send_email_to_student",
                       context=email_context)
            mail.send([team.email],
                       [request.user.email],
                       template="teams_send_email_to_team",
                       context=email_context,
                       headers={'Reply-to': request.user.email})
            return {"message": "success"}
    elif request.method == 'GET':
        form = EmailForm()

    context = {'form': form,
                'team': team}
    return render(request, 'teams/send_email_form.html', context)

@login_required
@decorators.ajax_only
@csrf.csrf_exempt
def control_registration(request, code_name):
    current_year = StudentClubYear.objects.get_current()
    team = get_object_or_404(Team, code_name=code_name)

    if not request.user == team.leader and \
            not request.user.is_superuser:
        raise PermissionDenied

    #if team.year is not current_year:
    #    team.is_open = False
    #else:
    if team.is_open == True:
        team.is_open = False
    elif team.is_open == False:
        team.is_open = True
    team.save()
    return {'team_isopen': team.is_open}



