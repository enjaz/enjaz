# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date
from django.db import models, migrations

def add_sfhcw(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    Event = apps.get_model('events', 'Event')
    Session = apps.get_model('events', 'Session')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    workshop_date = date(2016, 4, 19)
    year_2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)
    presidency = Club.objects.get(english_name="Presidency", year=year_2015_2016)
    sfhcw2016_club = Club.objects.create(english_name="Success for Health-Care Worker Cource 2016",
                        name="دورة صناعة النجاح في حياة الممارس الصحي",
                        gender="",
                        parent=presidency,
                        email="sc-media@ksau-hs.edu.sa",
                        city="R",
                        visible=False,
                        can_view_assessments=False,
                        is_assessed=False,
                        can_submit_activities=False)
    sfhcw2016_event = Event.objects.create(name="دورة صناعة النجاح في حياة الممارس الصحي",
                                           is_english_name=True,
                                           code_name="sfhcw2016",
                                           is_on_telegram=False,
                                           twitter="StudentsofKSAUH", 
                                           start_date=workshop_date,
                                           end_date=workshop_date,
                                           organizing_club=sfhcw2016_club)
    Session.objects.create(name="الدورة الرئيسية",
                           event=sfhcw2016_event,
                           time_slot=None,
                           code_name='main',
                           gender='')

def remove_sfhcw(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    Event = apps.get_model('events', 'Event')
    Club.objects.filter(english_name="Success for Health-Care Worker Cource 2016").delete()
    Event.objects.filter(code_name="sfhcw2016").delete()

class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_fix_sessions'),
        ('clubs', '0042_alahsa_deanship'),
    ]

    operations = [
       migrations.RunPython(
            add_sfhcw,
            reverse_code=remove_sfhcw),
    ]
