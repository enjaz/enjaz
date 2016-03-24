# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def change_focr(apps, schema_editor):
    Event = apps.get_model('events', 'Event')
    focr2016_event = Event.objects.get(code_name="focr2016")
    focr2016_event.is_on_telegram = False
    focr2016_event.twitter = "StudentsofKSAUH"
    focr2016_event.save()

def change_focr_back(apps, schema_editor):
    Event = apps.get_model('events', 'Event')
    focr2016_event = Event.objects.get(code_name="focr2016")
    focr2016_event.is_on_telegram = True
    focr2016_event.twitter = "KSAU_Events"
    focr2016_event.save()
    
class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_add_media_fields'),
    ]

    operations = [
       migrations.RunPython(
            change_focr,
            reverse_code=change_focr_back),
    ]
