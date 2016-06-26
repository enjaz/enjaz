# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.db import models, migrations


start2017 = datetime(2016, 5, 2) 
end2017 = datetime(2017, 5, 2)

def add_year(apps, schema_editor):
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    StudentClubYear.objects.create(start_date=start2017,
                                   end_date=end2017)

def remove_year(apps, schema_editor):
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    StudentClubYear.objects.get(start_date=start2017,
                                end_date=end2017).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_niqati_closure_per_city'),
    ]

    operations = [
       migrations.RunPython(
            add_year,
            reverse_code=remove_year),
    ]
