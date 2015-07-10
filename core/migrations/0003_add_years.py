# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.db import models, migrations

start2015 = datetime(2014, 5, 13)
end2015 = datetime(2015, 4, 27)
start2016 = datetime(2015, 4, 28)
end2016 = datetime(2016, 4, 27) 

def add_years(apps, schema_editor):
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    StudentClubYear.objects.create(start_date=start2015,
                                   end_date=end2015)
    StudentClubYear.objects.create(start_date=start2016,
                                   end_date=end2016)

def remove_years(apps, schema_editor):
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    StudentClubYear.objects.get(start_date=start2015,
                                end_date=end2015).delete()
    StudentClubYear.objects.get(start_date=start2016,
                                end_date=end2016).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_studentclubyear'),
    ]

    operations = [
       migrations.RunPython(
            add_years,
            reverse_code=remove_years),
    ]
