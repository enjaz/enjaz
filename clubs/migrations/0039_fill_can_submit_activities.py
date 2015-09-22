# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_can_submit_activities(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                end_date__year=2016)
    non_submitting_clubs = Club.objects.filter(english_name__contains="Media Center", year=year2015_2016) | \
                           Club.objects.filter(english_name__contains="Deanship", year=year2015_2016)
    non_submitting_clubs.update(can_submit_activities=False)

def remove_can_submit_activities(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                end_date__year=2016)
    Club.objects.filter(year=year2015_2016).update(can_submit_activities=True)

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0038_club_can_submit_activities'),
    ]

    operations = [
       migrations.RunPython(
            add_can_submit_activities,
            reverse_code=remove_can_submit_activities),
    ]
