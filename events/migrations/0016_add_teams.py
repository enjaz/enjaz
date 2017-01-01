# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def add_teams(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    Team = apps.get_model('clubs', 'Team')
    Event = apps.get_model('events', 'Event')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)
    year_2016_2017 = StudentClubYear.objects.get(start_date__year=2016,
                                                 end_date__year=2017)

    # SFHCW
    sfhcw2016_team = Team.objects.create(name="دورة صناعة النجاح في حياة الممارس الصحي",
                                         code_name="sfhcw2016",
                                         year=year_2015_2016,
                                         city="R", gender="")
    sfhcw2016_club = Club.objects.get(english_name="Success for Health-Care Worker Cource 2016")
    for member in sfhcw2016_club.members.all():
        sfhcw2016_team.members.add(member)
    Event.objects.filter(code_name="sfhcw2016").update(organizing_team=sfhcw2016_team)

    # FOCR
    focr2016_club = Club.objects.get(english_name="Foundtions of Clinical Research 2016")
    focr2016_team = Team.objects.create(name="أسس البحث العلمي 2016",
                                        code_name="focr2016", year=year_2015_2016,
                                        city="R", gender="")
    for member in focr2016_club.members.all():
        focr2016_team.members.add(member)
    Event.objects.filter(code_name="focr2016").update(organizing_team=focr2016_team)

    # HPC
    hpc2017_team = Team.objects.create(name="لجنة تنظيم مؤتمر التخصصات الصحية الثاني",
                                       code_name="hpc2017", year=year_2016_2017,
                                       city="R", gender="")
    hpc2017_club = Club.objects.get(english_name="Organizing Committee of the 2nd HPC")
    for member in hpc2017_club.members.all():
        hpc2017_team.members.add(member)
    Event.objects.filter(code_name="hpc-2nd").update(organizing_team=hpc2017_team)

def remove_teams(apps, schema_editor):
    Team = apps.get_model('clubs', 'Team')
    Event = apps.get_model('events', 'Event')
    Event.objects.update(organizing_team=None)
    Team.objects.filter(code_name__in=["sfhcw2016", "focr2016",
                                      "hpc2017"]).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_use_teams'),
        ('clubs', '0047_team'),
    ]

    operations = [
       migrations.RunPython(
            add_teams,
            reverse_code=remove_teams),
    ]
