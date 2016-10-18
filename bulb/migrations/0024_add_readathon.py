# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from datetime import date

def add_readathon(apps, schema_editor):
    Readathon = apps.get_model('bulb', 'Readathon')
    start_date = date(2016, 10, 20)
    end_date = date(2016, 10, 26)
    Readathon.objects.create(start_date=start_date,
                             end_date=end_date,
                             template_name="bulb/readathon/show_readathon_1.html")

def remove_readathon(apps, schema_editor):
    Readathon = apps.get_model('bulb', 'Readathon')
    start_date = date(2016, 10, 20)
    end_date = date(2016, 10, 26)
    Readathon.objects.filter(start_date=start_date,
                             end_date=end_date).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('bulb', '0023_readathon'),
    ]

    operations = [
       migrations.RunPython(
            add_readathon,
            reverse_code=remove_readathon),
    ]
