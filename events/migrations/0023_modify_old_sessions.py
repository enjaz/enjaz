# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def add_TimeSlot(apps, schema_editor):
    Session = apps.get_model('events', 'Session')


    Session.objects.filter(event="Foundations of Clinical Research 2016",
                           name="البرنامج العام").update(timeslot=None, acceptance_method_choices=None)
    Session.objects.filter(event="Foundations of Clinical Research 2016",
                           name="Data collection, management, and handling: Be a smart data manager").update(timeslot=None, acceptance_method_choices=None)
    Session.objects.filter(event="Foundations of Clinical Research 2016",
                           name="Literature review and research question").update(timeslot=None, acceptance_method_choices=None)
    Session.objects.filter(event="Foundations of Clinical Research 2016",
                           name="Master Questionnaire from Developing to Response Rates").update(timeslot=None, acceptance_method_choices=None)
    Session.objects.filter(event="Foundations of Clinical Research 2016",
                           name="Scientific Writing").update(timeslot=None, acceptance_method_choices=None)
    Session.objects.filter(event="Foundations of Clinical Research 2016",
                           name="Translational Research: From the Clinic to the Bench").update(timeslot=None, acceptance_method_choices=None)
    Session.objects.filter(event="Foundations of Clinical Research 2016",
                           name="Qualitative Research,Interviews and focused group").update(timeslot=None, acceptance_method_choices=None)
    Session.objects.filter(event="دورة صناعة النجاح في حياة الممارس الصحي",
                           name="الدورة الرئيسية").update(timeslot=None, acceptance_method_choices=None)
    Session.objects.filter(event="Foundations of Clinical Research 2016",
                           name="البرنامج العام").update(timeslot=None, acceptance_method_choices=None)


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0022_add_SessionRegistration_model'),
    ]

    operations = [
    ]






