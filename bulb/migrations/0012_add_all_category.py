# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def add_categories(apps, schema_editor):
    Category = apps.get_model('bulb', 'Category')
    Category.objects.create(code_name="all", name="جميع الكتب",
                            is_meta=True)

def remove_categories(apps, schema_editor):
    Category = apps.get_model('bulb', 'Category')
    Category.objects.filter(code_name="all").delete()

class Migration(migrations.Migration):

    dependencies = [
        ('bulb', '0011_category_is_meta'),
    ]

    operations = [
       migrations.RunPython(
            add_categories,
            reverse_code=remove_categories),
    ]
