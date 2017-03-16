# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from datetime import datetime, date


def add_evaluators_team(apps, schema_editor):
    Team = apps.get_model('clubs', 'Team')
    Event = apps.get_model('events', 'Event')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2016_2017 = StudentClubYear.objects.get(start_date__year=2016,
                                                 end_date__year=2017)


    hpc_2_r_evaluators_team = Team.objects.create(name="لجنة تقييم مؤتمر التخصصات الصحية الثاني - الرياض",
                                                  code_name="hpc2-r-e", year=year_2016_2017,
                                                  city="R", gender="")
    hpc_2_j_evaluators_team = Team.objects.create(name="لجنة تقييم مؤتمر التخصصات الصحية الثاني - جدة",
                                       code_name="hpc2-j-e", year=year_2016_2017,
                                       city="J", gender="")
    hpc_2_a_evaluators_team = Team.objects.create(name="لجنة تقييم مؤتمر التخصصات الصحية الثاني - الأحساء",
                                       code_name="hpc2-a-e", year=year_2016_2017,
                                       city="A", gender="")
    Event.objects.filter(code_name="hpc2-r").update(abstract_revision_team=hpc_2_r_evaluators_team)
    Event.objects.filter(code_name="hpc2-j").update(abstract_revision_team=hpc_2_j_evaluators_team)
    Event.objects.filter(code_name="hpc2-a").update(abstract_revision_team=hpc_2_a_evaluators_team)




def remove_evaluators_team(apps, schema_editor):
    Team = apps.get_model('clubs', 'Team')
    Team.objects.filter(code_name__in=["hpc2-r-e", "hpc2-j-e","hpc2-a-e"]).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('events', '0034_add_evaluators_to_abstract'),
    ]

    operations = [
        migrations.RunPython(
            add_evaluators_team,
            reverse_code=remove_evaluators_team),
    ]
