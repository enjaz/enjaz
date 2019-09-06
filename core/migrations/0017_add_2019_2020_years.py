# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from datetime import datetime

start_2019_2020 = datetime(2019, 6, 2)
end_2019_2020 = datetime(2020, 6, 1)


def add_year(apps, schema_editor):
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    StudentClubYear.objects.create(start_date=start_2019_2020,
                                   end_date=end_2019_2020)


def remove_year(apps, schema_editor):
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    StudentClubYear.objects.get(start_date=start_2019_2020,
                                end_date=end_2019_2020).delete()



class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_add_2018_2019_year'),
    ]

    operations = [
        migrations.RunPython(
            add_year,
            remove_year,
        )
    ]
