# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_categories(apps, schema_editor):
    Category = apps.get_model('bulb', 'Category')
    Category.objects.create(code_name="others", name="أخرى")

def remove_categories(apps, schema_editor):
    Category = apps.get_model('bulb', 'Category')
    Category.objects.filter(code_name="others").delete()

class Migration(migrations.Migration):

    dependencies = [
        ('bulb', '0008_improve_status'),
    ]

    operations = [
       migrations.RunPython(
            add_categories,
            reverse_code=remove_categories),
    ]
