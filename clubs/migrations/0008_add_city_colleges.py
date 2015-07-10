# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_colleges(apps, schema_editor):
    College = apps.get_model('clubs', 'College')
    # Missing at KFMC
    College.objects.create(
        name='M',
        section='KF',
        city='R',
        gender='F')
    # Missing In Al-Hasa
    College.objects.create(
        name='A',
        section='A',
        city='A',
        gender='M')
    College.objects.create(
        name='A',
        section='A',
        city='A',
        gender='F')
    College.objects.create(
        name='N',
        section='A',
        city='A',
        gender='F')
    # Missing in Jeddah
    College.objects.create(
        name='M',
        section='J',
        city='J',
        gender='M')
    College.objects.create(
        name='M',
        section='J',
        city='J',
        gender='F')
    College.objects.create(
        name='B',
        section='J',
        city='J',
        gender='M')
    College.objects.create(
        name='B',
        section='J',
        city='J',
        gender='F')
    College.objects.create(
        name='N',
        section='J',
        city='J',
        gender='F')

def delete_colleges(apps, schema_editor):
    College = apps.get_model('clubs', 'College')
    # KFMC
    College.objects.get(
        name='M',
        section='KF',
        city='R',
        gender='F').delete()
    # Al-Hasa
    College.objects.get(
        name='A',
        section='A',
        city='A',
        gender='M').delete()
    College.objects.get(
        name='A',
        section='A',
        city='A',
        gender='F').delete()
    College.objects.get(
        name='N',
        section='A',
        city='A',
        gender='F').delete()
    # Jeddah
    College.objects.get(
        name='M',
        section='J',
        city='J',
        gender='M').delete()
    College.objects.get(
        name='M',
        section='J',
        city='J',
        gender='F').delete()
    College.objects.get(
        name='B',
        section='J',
        city='J',
        gender='M').delete()
    College.objects.get(
        name='B',
        section='J',
        city='J',
        gender='F').delete()
    College.objects.create(
        name='N',
        section='J',
        city='J',
        gender='F').delete()

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0007_all_in_riyadh'),
    ]

    operations = [
       migrations.RunPython(
            add_colleges,
            reverse_code=delete_colleges),
    ]
