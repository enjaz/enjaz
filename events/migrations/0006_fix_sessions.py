# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date
from django.db import models, migrations

def fix_focr_session(apps, schema_editor):
    Session = apps.get_model('events', 'Session')
    Session.objects.filter(name="Translation Research: From the Clinic to the Bench").delete()
    Session.objects.filter(name="Translational Research").update(name="Translational Research: From the Clinic to the Bench")

class Migration(migrations.Migration):
    dependencies = [
        ('events', '0005_add_more_sessions'),
    ]

    operations = [
        migrations.RunPython(fix_focr_session),
    ]
