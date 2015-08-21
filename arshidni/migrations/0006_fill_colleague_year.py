# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_year(apps, schema_editor):
    ColleagueProfile = apps.get_model('arshidni', 'ColleagueProfile')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year2014_2015 = StudentClubYear.objects.get(start_date__year=2014,
                                                 end_date__year=2015)
    ColleagueProfile.objects.filter(year__isnull=True).update(year=year2014_2015)

def remove_year(apps, schema_editor):
    ColleagueProfile = apps.get_model('arshidni', 'ColleagueProfile')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year2014_2015 = StudentClubYear.objects.get(start_date__year=2014,
                                                 end_date__year=2015)
    ColleagueProfile.objects.filter(year=year2014_2015).update(year=None)

class Migration(migrations.Migration):

    dependencies = [
        ('arshidni', '0005_better_related_names'),
    ]

    operations = [
       migrations.RunPython(
           add_year,
           reverse_code=remove_year),
    ]
