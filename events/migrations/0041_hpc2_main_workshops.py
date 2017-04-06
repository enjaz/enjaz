# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime

def add_hpc(apps, schema_editor):
    Event = apps.get_model('events', 'Event')
    TimeSlot = apps.get_model('events', 'TimeSlot')
    Session = apps.get_model('events', 'Session')
    hpc_r_event = Event.objects.get(code_name="hpc2-r")

    #Riyadh_Workshops_Day_1:
    workshops_day_1 = TimeSlot.objects.create(event=hpc_r_event,
                                            name="ورش عمل اليوم الأول")

    Session.objects.create(name="Getting out of the Box: Volunteering in the Medical Field",
                           event=hpc_r_event,
                           time_slot=workshops_day_1,
                           acceptance_method="M")

    Session.objects.create(name="Work Place Dynamics: Self Awareness & Professional Success",
                           event=hpc_r_event,
                           time_slot=workshops_day_1,
                           acceptance_method="M")

    Session.objects.create(name="The Art of Converting Great Ideas Into Reality",
                           event=hpc_r_event,
                           time_slot=workshops_day_1,
                           acceptance_method="M")

    Session.objects.create(name="How to Pass an Interview & Write your CV",
                           event=hpc_r_event,
                           time_slot=workshops_day_1,
                           acceptance_method="M")

    Session.objects.create(name="Public Speaking & Presentation Skills",
                           event=hpc_r_event,
                           time_slot=workshops_day_1,
                           acceptance_method="M")


    Session.objects.create(name="MBTI Coarse – Part 1 & Part 1 (Two Days)",
                           event=hpc_r_event,
                           time_slot=workshops_day_1,
                           acceptance_method="M")


    #Riyadh_Workshops_Day_2:
    workshops_day_2 = TimeSlot.objects.create(event=hpc_r_event,
                                            name="ورش عمل اليوم الثاني")

    Session.objects.create(name="Proper Literature Review & How to Make up a Research Question",
                           event=hpc_r_event,
                           time_slot=workshops_day_2,
                           acceptance_method="M")

    Session.objects.create(name="Steps to Write an Impactful Case Report",
                           event=hpc_r_event,
                           time_slot=workshops_day_2,
                           acceptance_method="M")

    Session.objects.create(name="How to Develop your Questionnaire",
                           event=hpc_r_event,
                           time_slot=workshops_day_2,
                           acceptance_method="M")

    Session.objects.create(name="Types of Study Designs & How to Choose One for your Study",
                           event=hpc_r_event,
                           time_slot=workshops_day_2,
                           acceptance_method="M")

    Session.objects.create(name="How to Write all your Proposal Components",
                           event=hpc_r_event,
                           time_slot=workshops_day_2,
                           acceptance_method="M")


    Session.objects.create(name="Scientific Writing: How to Write your Manuscript",
                           event=hpc_r_event,
                           time_slot=workshops_day_2,
                           acceptance_method="M")


    #Riyadh_Workshops_Day_3:
    workshops_day_3 = TimeSlot.objects.create(event=hpc_r_event,
                                            name="ورش عمل اليوم الثالث")

    Session.objects.create(name="Basic Medication Safety Course (Accredited with 5 CME hours)",
                           event=hpc_r_event,
                           time_slot=workshops_day_3,
                           acceptance_method="M")

    Session.objects.create(name="Qualitative and Quantitive Data Analysis on SPSS",
                           event=hpc_r_event,
                           time_slot=workshops_day_3,
                           acceptance_method="M")

    Session.objects.create(name="The principles of Bioethics",
                           event=hpc_r_event,
                           time_slot=workshops_day_3,
                           acceptance_method="M")

def remove_hpc(apps, schema_editor):
    TimeSlot = apps.get_model('events', 'TimeSlot')
    Session = apps.get_model('events', 'Session')
    code_names = ["hpc2-r"]
    Session.objects.filter(event__code_name__in=code_names).delete()
    TimeSlot.objects.filter(event__code_name__in=code_names).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0040_event_extra_fields'),
    ]

    operations = [
        migrations.RunPython(
            add_hpc,
            reverse_code=remove_hpc),
]
