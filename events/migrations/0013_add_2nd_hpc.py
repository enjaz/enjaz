# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime, date
from django.db import models, migrations

def add_hpc(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    Event = apps.get_model('events', 'Event')
    Session = apps.get_model('events', 'Session')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    start_date = date(2016, 12, 20)
    end_date = date(2016, 12, 22)
    year_2016_2017 = StudentClubYear.objects.get(start_date__year=2016,
                                                 end_date__year=2017)
    presidency = Club.objects.get(english_name="Presidency",
                                  year=year_2016_2017, gender="", city="R")
    hpc_2nd_club = Club.objects.create(english_name="Organizing Committee of the 2nd HPC",
                        name="لجنة تنظيم مؤتمر التخصصات الصحية الثاني",
                        gender="",
                        parent=presidency,
                        email="hpc@ksau-hs.edu.sa",
                        city="R",
                        visible=False,
                        can_view_assessments=False,
                        is_assessed=False,
                        can_submit_activities=False)
    hpc_2nd_event = Event.objects.create(official_name= "مؤتمر التخصصات ال صحية الثاني",
                                         english_name="2nd Health Profession Conference",
                                         is_official_name_english=True,
                                         code_name="hpc-2nd",
                                         start_date=start_date,
                                         end_date=end_date,
                                         receives_abstract_submission=True,
                                         abstract_submission_instruction_url="https://hpc.enjazportal.com/research/",
                                         abstract_submission_opening_date=datetime(2016, 9, 18),
                                         abstract_submission_closing_date=datetime(2016, 11, 1),
                                         organizing_club=hpc_2nd_club)


def remove_hpc(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    Event = apps.get_model('events', 'Event')
    Club.objects.filter(english_name="Organizing Committee of the 2nd HPC").delete()
    Event.objects.filter(english_name="2nd Health Profession Conference").delete()

class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_event_improvements'),
        ('clubs', '0046_add_jeddah_ams_deanship'),
    ]

    operations = [
       migrations.RunPython(
            add_hpc,
            reverse_code=remove_hpc),
    ]
