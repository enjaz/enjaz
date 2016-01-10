# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_mentors(apps, schema_editor):
    MentorOfTheMonth = apps.get_model('studentguide', 'MentorOfTheMonth')
    male_gender = MentorOfTheMonth.objects.create(gender='M')
    female_gender = MentorOfTheMonth.objects.create(gender='F')

def remove_mentors(apps, schema_editor):
    MentorOfTheMonth = apps.get_model('studentguide', 'MentorOfTheMonth')
    MentorOfTheMonth.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('studentguide', '0009_mentorofthemonth'),
    ]

    operations = [
       migrations.RunPython(
            add_mentors,
            reverse_code=remove_mentors),
    ]
