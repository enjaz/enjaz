# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_is_assessed(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)
    unassessed_clubs = Club.objects.filter(english_name__contains="Presidency", year=year2015_2016) | \
                       Club.objects.filter(english_name__contains="Arshidni", year=year2015_2016) | \
                       Club.objects.filter(english_name__contains="Media Center", year=year2015_2016) | \
                       Club.objects.filter(english_name__contains="Deanship", year=year2015_2016)
    unassessed_clubs.update(is_assessed=False)

def remove_is_assessed(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)
    Club.objects.filter(year=year2015_2016).update(is_assessed=True)

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0036_club_is_assessed'),
    ]

    operations = [
       migrations.RunPython(
            add_is_assessed,
            reverse_code=remove_is_assessed),
    ]
