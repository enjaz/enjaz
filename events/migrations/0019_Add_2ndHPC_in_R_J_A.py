# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime, date
from django.db import migrations, models

def add_hpc(apps, schema_editor):
    Team = apps.get_model('clubs', 'Team')
    Event = apps.get_model('events', 'Event')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    start_date = date(2017, 4, 23)
    end_date = date(2017, 4, 25)
    abstract_submission_opening_date=datetime(2017, 1, 1)
    abstract_submission_closing_date=datetime(2017, 3, 1)
    year_2016_2017 = StudentClubYear.objects.get(start_date__year=2016,
                                                 end_date__year=2017)

    #Riyadh- 'UBDATE'
    hpc2017_team = Team.objects.get(code_name="hpc2017").update(name="لجنة تنظيم مؤتمر التخصصات الصحية الثاني - الرياض",
                                         code_name="hpc2-r")

    Event.objects.filter(code_name="hpc-2nd").update(official_name= "مؤتمر التخصصات الصحية الثاني - الرياض",
                                         english_name="2nd Health Profession Conference - ِRiyadh",
                                         code_name="hpc-2-r",
                                         start_date=start_date,
                                         end_date=end_date,
                                         abstract_submission_opening_date=abstract_submission_opening_date,
                                         abstract_submission_closing_date=abstract_submission_closing_date)

    #Jeddah
    hpc_2_j_team = Team.objects.create(name="لجنة تنظيم مؤتمر التخصصات الصحية الثاني - جدة",
                                       code_name="hpc2-j", year=year_2016_2017,
                                       city="J", gender="")

    hpc_2_j_event = Event.objects.create(official_name= "مؤتمر التخصصات الصحية الثاني - جدة",
                                         english_name="2nd Health Profession Conference - Jeddah",
                                         is_official_name_english=True,
                                         code_name="hpc-2-j",
                                         start_date=start_date,
                                         end_date=end_date,
                                         receives_abstract_submission=True,
                                         abstract_submission_instruction_url="https://hpc.enjazportal.com/research/",
                                         abstract_submission_opening_date=abstract_submission_opening_date,
                                         abstract_submission_closing_date=abstract_submission_closing_date,
                                         organizing_team=hpc_2_j_team)

    #Al-Ahsa
    hpc_2_a_team = Team.objects.create(name="لجنة تنظيم مؤتمر التخصصات الصحية الثاني - الأحساء",
                                       code_name="hpc2-a", year=year_2016_2017,
                                       city="A", gender="")

    hpc_2_a_event = Event.objects.create(official_name= "مؤتمر التخصصات الصحية الثاني - الأحساء",
                                         english_name="2nd Health Profession Conference - ِِAl-Ahsa",
                                         is_official_name_english=True,
                                         code_name="hpc-2-a",
                                         start_date=start_date,
                                         end_date=end_date,
                                         receives_abstract_submission=True,
                                         abstract_submission_instruction_url="https://hpc.enjazportal.com/research/",
                                         abstract_submission_opening_date=abstract_submission_opening_date,
                                         abstract_submission_closing_date=abstract_submission_closing_date,
                                         organizing_team=hpc_2_a_team)

def remove_hpc(apps, schema_editor):
    Team = apps.get_model('clubs', 'Team')
    Event = apps.get_model('events', 'Event')
    Team.objects.filter(code_name__in=["hpc2-r", "hpc2-j","hpc2-a"]).delete()
    Event.objects.filter(english_name__in=["2nd Health Profession Conference - ِRiyadh"
                         "2nd Health Profession Conference - Jeddah",
                         "2nd Health Profession Conference - Al-Ahsa"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0018_merge'),
        ('clubs', '0047_team'),
    ]

    operations = [
       migrations.RunPython(
            add_hpc,
            reverse_code=remove_hpc),
    ]
