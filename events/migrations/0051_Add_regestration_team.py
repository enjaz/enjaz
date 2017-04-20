# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

from datetime import datetime, date



def add_regestration_team(apps, schema_editor):
    Team = apps.get_model('clubs', 'Team')
    Event = apps.get_model('events', 'Event')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2016_2017 = StudentClubYear.objects.get(start_date__year=2016,
                                                     end_date__year=2017)
    hpc_r_regestration_team = Team.objects.create(name="لجنة التسجيل  لمؤتمر التخصصات الصحية الثاني - الرياض",
                                                      code_name="hpc2-r-r", year=year_2016_2017,
                                                      city="R", gender="")
    hpc_J_regestration_team = Team.objects.create(name="لجنة التسجيل  لمؤتمر التخصصات الصحية الثاني - جدة",
                                                      code_name="hpc2-j-r", year=year_2016_2017,
                                                      city="J", gender="")
    hpc_A_regestration_team = Team.objects.create(name="لجنة التسجيل  لمؤتمر التخصصات الصحية الثاني - الأحساء",
                                                      code_name="hpc2-a-r", year=year_2016_2017,
                                                      city="A", gender="")
    Event.objects.filter(code_name="hpc2-r").update(registration_team =hpc_r_regestration_team)
    Event.objects.filter(code_name="hpc2-j").update(registration_team =hpc_J_regestration_team)
    Event.objects.filter(code_name="hpc2-a").update(registration_team =hpc_A_regestration_team)


def remove_regestration_team(apps, schema_editor):
    Team = apps.get_model('clubs', 'Team')
    Team.objects.filter(code_name__in=["hpc2-r-r","hpc2-a-r","hpc2-j-r"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0050_add_registration_team_field'),
    ]
    operations = [
        migrations.RunPython(
            add_regestration_team,
            reverse_code=remove_regestration_team),
    ]