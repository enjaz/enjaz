# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime, date
from django.db import models, migrations

def add_fonts(apps, schema_editor):
    FontFamily = apps.get_model('certificates', 'FontFamily')
    FontFamily.objects.create(name="Carlito-Regular.ttf")
    FontFamily.objects.create(name="Unique.ttf")
    FontFamily.objects.create(name="BebasNeue Bold.ttf")
    FontFamily.objects.create(name="Orkney Medium.ttf")
    FontFamily.objects.create(name="Orkney Bold.ttf")

def remove_fonts(apps, schema_editor):
    FontFamily = apps.get_model('certificates', 'FontFamily')
    FontFamily.objects.filter(name__in=["Carlito-Regular.ttf",
                                        "Unique.ttf", "BebasNeue Bold.ttf",
                                        "Orkney Medium.ttf", "Orkney Bold.ttf"])\
                      .delete()

class Migration(migrations.Migration):

    dependencies = [
        ('certificates', '0001_initial'),
    ]

    operations = [
       migrations.RunPython(
           add_fonts,
           reverse_code=remove_fonts),
    ]
