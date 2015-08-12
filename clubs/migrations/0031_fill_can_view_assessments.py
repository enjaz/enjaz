# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_can_view_assessments(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)
    Club.objects.filter(english_name__contains="Presidency", year=year2015_2016).update(can_view_assessments=True)

def remove_can_view_assessments(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)
    Club.objects.filter(english_namee__contains="Presidency", year=year2015_2016).update(can_view_assessments=False)

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0030_can_view_assessments'),
    ]

    operations = [
       migrations.RunPython(
            add_can_view_assessments,
            reverse_code=remove_can_view_assessments),

    ]
