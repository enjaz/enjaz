# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_year(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2014_2015 = StudentClubYear.objects.get(start_date__year=2014,
                                                 end_date__year=2015)

    for club in Club.objects.exclude(english_name__startswith="Presidency"):
        club.year = year_2014_2015
        club.save()

def remove_year(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2014_2015 = StudentClubYear.objects.get(start_date__year=2014,
                                                 end_date__year=2015)

    for club in Club.objects.filter(year=year_2014_2015):
        club.year = None
        club.save()

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0011_club_year'),
        ('core', '0003_add_years'),
    ]

    operations = [
       migrations.RunPython(
            add_year,
            reverse_code=remove_year),
    ]
