# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def fill_fields(apps, schema_editor):
    CommonProfile = apps.get_model('accounts', 'CommonProfile')
    CommonProfile.objects.filter(city='R').update(city="الرياض")
    CommonProfile.objects.filter(city='J').update(city="جدة")
    CommonProfile.objects.filter(city='A').update(city="الأحساء")
    CommonProfile.objects.filter(is_student=True).update(profile_type='S')
    CommonProfile.objects.filter(is_student=False).update(profile_type='E')

def empty_fields(apps, schema_editor):
    CommonProfile = apps.get_model('accounts', 'CommonProfile')
    CommonProfile.objects.filter(city="الرياض").update(city='R')
    CommonProfile.objects.filter(city="جدة").update(city='J')
    CommonProfile.objects.filter(city="الأحساء").update(city='A')
    CommonProfile.objects.filter(profile_type='S').update(is_student=True, profile_type="")
    CommonProfile.objects.filter(profile_type='E').update(is_student=False, profile_type="")

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_nonuser'),
    ]

    operations = [
       migrations.RunPython(
            fill_fields,
            reverse_code=empty_fields)
    ]
