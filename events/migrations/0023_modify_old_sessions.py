# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def add_timeslot(apps, schema_editor):
    Session = apps.get_model('events', 'Session')
    Session.objects.update(time_slot=None, acceptance_method="")

def remove_timeslot(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('events', '0022_add_SessionRegistration_model'),
    ]

    operations = [
       migrations.RunPython(
            add_timeslot,
            reverse_code=remove_timeslot),
    ]






