# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date
from django.db import models, migrations

def add_exta_focr_sessions(apps, schema_editor):
    Event = apps.get_model('events', 'Event')
    Session = apps.get_model('events', 'Session')
    workshop_date = date(2016, 4, 13)
    focr2016_event = Event.objects.get(code_name="focr2016")
    Session.objects.create(name="Qualitative Research,Interviews and focused group",
                           event=focr2016_event,
                           time_slot=1,
                           date=workshop_date,
                           gender='')
    Session.objects.create(name="Translation Research: From the Clinic to the Bench",
                           event=focr2016_event,
                           time_slot=1,
                           date=workshop_date,
                           gender='')

def remove_exta_focr_sessions(apps, schema_editor):
    Session = apps.get_model('events', 'Session')
    Session.objects.filter(name="Qualitative Research,Interviews and focused group").delete()
    Session.objects.filter(name="Translation Research: From the Clinic to the Bench").delete()

class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_add_media_for_focr2016'),
    ]

    operations = [
       migrations.RunPython(
            add_exta_focr_sessions,
            reverse_code=remove_exta_focr_sessions),
    ]
