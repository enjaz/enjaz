from django.shortcuts import render
from django.db.utils import OperationalError
from django.shortcuts import get_object_or_404
from core.models import StudentClubYear
from .models import Teams
from clubs.models import city_choices


def list_teams(request):
    current_year = StudentClubYear.objects.get_current()
    per_city = []
    for city_code, city_name in city_choices:
        try:
            teams = Teams.objects.filter(year=current_year, city=city_code)
            if teams.exists():
                per_city.append((city_name, teams))
        except OperationalError:
            pass
    context = {'per_city': per_city}
    return render(request, 'teams/list_teams.html', context)

def show_info(request, team_id):
    team = get_object_or_404(Teams, pk=team_id)
    context = {'team': team}
    return render(request, 'teams/infocard.html', context)