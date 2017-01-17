# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def fill_fields(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    Team = apps.get_model('clubs', 'Team')
    College = apps.get_model('clubs', 'College')
    Invitation = apps.get_model('activities', 'Invitation')
    models = [Club, Team, College, Invitation]
    for model in models:
        model.objects.filter(city='R').update(city="الرياض")
        model.objects.filter(city='J').update(city="جدة")
        model.objects.filter(city='A').update(city="الأحساء")

def empty_fields(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    Team = apps.get_model('clubs', 'Team')
    College = apps.get_model('clubs', 'College')
    Invitation = apps.get_model('activities', 'Invitation')
    models = [Club, Team, College, Invitation]
    for model in models:
        model.objects.filter(city="الرياض").update(city='R')
        model.objects.filter(city="جدة").update(city='J')
        model.objects.filter(city="الأحساء").update(city='A')

class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0037_invitation_city'),
        ('clubs', '0050_change_city_fields'),
    ]

    operations = [
       migrations.RunPython(
            fill_fields,
            reverse_code=empty_fields)
    ]
