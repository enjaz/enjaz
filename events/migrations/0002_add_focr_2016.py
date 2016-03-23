# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date
from django.db import models, migrations

def add_focr(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    Event = apps.get_model('events', 'Event')
    Session = apps.get_model('events', 'Session')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    start_date = date(2016, 4, 11)
    end_date = date(2016, 4, 13)
    workshop_date = date(2016, 4, 13)
    year_2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)
    presidency = Club.objects.get(english_name="Presidency", year=year_2015_2016)
    focr2016_club = Club.objects.create(english_name="Foundtions of Clinical Research 2016",
                        name="أسس البحث العلمي 2016",
                        gender="",
                        parent=presidency,
                        email="mishkatclub@ksau-hs.edu.sa",
                        city="R",
                        visible=False,
                        can_view_assessments=False,
                        is_assessed=False,
                        can_submit_activities=False)
    focr2016_event = Event.objects.create(name="Foundations of Clinical Research 2016",
                                          is_english_name=True,
                                          code_name="focr2016",
                                          start_date=start_date,
                                          end_date=end_date,
                                          priorities=2,
                                          organizing_club=focr2016_club)
    Session.objects.create(name="البرنامج العام",
                           event=focr2016_event,
                           time_slot=None,
                           code_name='main',
                           gender='')
    Session.objects.create(name="Data collection, management, and handling: Be a smart data manager",
                           event=focr2016_event,
                           time_slot=1,
                           date=workshop_date,
                           gender='')
    Session.objects.create(name="Data collection, management, and handling: Be a smart data manager",
                           event=focr2016_event,
                           time_slot=1,
                           date=workshop_date,
                           gender='')
    Session.objects.create(name="Literature review and research question",
                           event=focr2016_event,
                           time_slot=1,
                           date=workshop_date,
                           gender='')
    Session.objects.create(name="Master Questionnaire from Developing to Response Rates",
                           event=focr2016_event,
                           time_slot=1,
                           date=workshop_date,
                           gender='')
    Session.objects.create(name="Scientific Writing",
                           event=focr2016_event,
                           time_slot=1,
                           date=workshop_date,
                           gender='')
    Session.objects.create(name="Translational Research",
                           event=focr2016_event,
                           time_slot=1,
                           date=workshop_date,
                           gender='')


def remove_focr(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    Event = apps.get_model('events', 'Event')
    Session = apps.get_model('events', 'Session')
    Club.objects.filter(english_name="Foundtions of Clinical Research 2016").delete()
    Event.objects.filter(name="Foundations of Clinical Research 2016").delete()

class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
        ('clubs', '0042_alahsa_deanship'),
    ]

    operations = [
       migrations.RunPython(
            add_focr,
            reverse_code=remove_focr),
    ]
