# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_balance(apps, schema_editor):
    CommonProfile = apps.get_model('accounts', 'CommonProfile')
    Point = apps.get_model('bulb', 'Point')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)
    points = []
    for common_profile in CommonProfile.objects.filter(is_student=True):
        point = Point(year=year_2015_2016,
                      user=common_profile.user,
                      note="رصيد مبدئي.",
                      category="L",
                      value=1)
        points.append(point)
    Point.objects.bulk_create(points)

def remove_balance(apps, schema_editor):
    Point = apps.get_model('bulb', 'Point')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)
    Point.objects.filter(year=year_2015_2016,
                         note="رصيد مبدئي.",
                         category="L",
                         value=1).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('bulb', '0014_allow_lending'),
        ('accounts', '0003_create_common_profiles')
    ]

    operations = [
       migrations.RunPython(
            add_balance,
            reverse_code=remove_balance),
    ]
