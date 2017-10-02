# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.db import migrations, models

start_2017_2018 = datetime(2017, 5, 19)
end_2017_2018 = datetime(2018, 5, 1)


def add_year(apps, schema_editor):
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    StudentClubYear.objects.create(start_date=start_2017_2018,
                                   end_date=end_2017_2018)


def remove_year(apps, schema_editor):
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    StudentClubYear.objects.get(start_date=start_2017_2018,
                                end_date=end_2017_2018).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0012_studentclubyear_bookexchange_open_date'),
    ]

    operations = [
        migrations.RunPython(
            add_year,
            remove_year,
        )
    ]
