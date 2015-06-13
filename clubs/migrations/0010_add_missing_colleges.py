# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_colleges(apps, schema_editor):
    College = apps.get_model('clubs', 'College')
    # Variables are named: <city_code>_<college_code>_<gender_code>.
    College.objects.create(city='R', section='NG', name='A', gender='F')
    College.objects.create(city='R', section='NG', name='P', gender='F')
    # Collge of Public Health was created manually on enjazportal.com.
    # Let's make sure all other installations have this college as
    # well:
    if not College.objects.filter(city='R', section='NG', name='I',
                                  gender='M'):
        College.objects.create(city='R', section='NG', name='I',
                               gender='M')

def remove_colleges(apps, schema_editor):
    College = apps.get_model('clubs', 'College')
    College.objects.get(city='R', section='NG', name='A',
                        gender='F').delete()
    College.objects.get(city='R', section='NG', name='P',
                        gender='F').delete()
    College.objects.get(city='R', section='NG', name='I',
                           gender='M').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0009_more_sections_and_club_gender'),
    ]

    operations = [
       migrations.RunPython(
            add_colleges,
            reverse_code=remove_colleges),
    ]
