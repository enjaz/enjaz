# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_can_assess(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')

    year_2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)
    assessing_clubs = Club.objects.filter(english_name__contains="Presidency", year=year_2015_2016) | \
                      Club.objects.filter(english_name__contains="Media Center", year=year_2015_2016)
    assessing_clubs.update(can_assess=True)

def remove_can_assess(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')

    year_2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)
    assessing_clubs = Club.objects.filter(english_name__contains="Presidency", year=year_2015_2016) | \
                      Club.objects.filter(english_name__contains="Media Center", year=year_2015_2016)
    assessing_clubs.update(can_assess=False)
    
class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0026_media_center_jeddah_alahsa'),
    ]

    operations = [
       migrations.RunPython(
            add_can_assess,
            reverse_code=remove_can_assess)
    ]
