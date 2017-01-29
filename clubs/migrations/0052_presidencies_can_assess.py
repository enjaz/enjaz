# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def can_assess(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2016_2017 = StudentClubYear.objects.get(start_date__year=2016,
                                                 end_date__year=2017)

    Club.objects.filter(year=year_2016_2017,
                        english_name="Presidency")\
                .exclude(city='الرياض', gender='')\
                .update(can_assess=True)

def cannot_assess(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2016_2017 = StudentClubYear.objects.get(start_date__year=2016,
                                                 end_date__year=2017)
    Club.objects.filter(year=year_2016_2017,
                        english_name="Presidency")\
                .exclude(city='الرياض', gender='')\
                .update(can_assess=False)

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0051_update_city_fields'),
    ]

    operations = [
       migrations.RunPython(
            can_assess,
            reverse_code=cannot_assess),
    ]
