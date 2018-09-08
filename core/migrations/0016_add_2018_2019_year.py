# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.db import migrations, models

start_2018_2019 = datetime(2018, 6, 1)
end_2018_2019 = datetime(2019, 6, 1)


def add_year(apps, schema_editor):
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    StudentClubYear.objects.create(start_date=start_2018_2019,
                                   end_date=end_2018_2019)


def remove_year(apps, schema_editor):
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    StudentClubYear.objects.get(start_date=start_2018_2019,
                                end_date=end_2018_2019).delete()



class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_merge'),
    ]

    operations = [
        migrations.RunPython(
            add_year,
            remove_year,
        )
    ]
