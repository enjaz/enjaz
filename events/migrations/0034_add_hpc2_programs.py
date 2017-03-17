# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime

def add_hpc(apps, schema_editor):
    Event = apps.get_model('events', 'Event')
    TimeSlot = apps.get_model('events', 'TimeSlot')
    Session = apps.get_model('events', 'Session')
    hpc_r_event = Event.objects.get(code_name="hpc2-r")
    hpc_j_event = Event.objects.get(code_name="hpc2-j")
    hpc_a_event = Event.objects.get(code_name="hpc2-a")

    #Riyadh:
    hpc_r_timeslot = TimeSlot.objects.create(event=hpc_r_event,
                                            name="البرامج العامة")

    Session.objects.create(name="البرنامج العام",
                           event=hpc_r_event,
                           time_slot=hpc_r_timeslot,
                           acceptance_method="F")


    #Jeddah:
    hpc_j_timeslot = TimeSlot.objects.create(event=hpc_j_event,
                                            name="البرامج العامة")

    Session.objects.create(name="البرنامج العام",
                           event=hpc_j_event,
                           time_slot=hpc_j_timeslot,
                           acceptance_method="F")


    #Alahsa:
    hpc_a_timeslot = TimeSlot.objects.create(event=hpc_a_event,
                                            name="البرامج العامة")

    Session.objects.create(name="البرنامج العام",
                           event=hpc_a_event,
                           time_slot=hpc_a_timeslot,
                           acceptance_method="F")

def remove_hpc(apps, schema_editor):
    TimeSlot = apps.get_model('events', 'TimeSlot')
    Session = apps.get_model('events', 'Session')
    code_names = ["hpc2-r", "hpc2-j","hpc2-a"]
    Session.objects.filter(event__code_name__in=code_names).delete()
    TimeSlot.objects.filter(event__code_name__in=code_names).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0033_add case report'),
    ]

    operations = [
        migrations.RunPython(
            add_hpc,
            reverse_code=remove_hpc),
]
