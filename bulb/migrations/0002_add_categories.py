# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_categories(apps, schema_editor):
    Category = apps.get_model('bulb', 'Category')

    if not Category.objects.exists():
        Category.objects.create(code_name="intellectual",
                                name="فكرية")
        Category.objects.create(code_name="historical",
                                name="تاريخية")
        Category.objects.create(code_name="religious",
                                name="دينية")
        Category.objects.create(code_name="literature",
                                name="أدب وروايات")
        Category.objects.create(code_name="biographical",
                                name="سير وشخصيات")
        Category.objects.create(code_name="business",
                                name="تجارة وأعمال")
        Category.objects.create(code_name="self_help",
                                name="تطوير ذات")

def remove_categories(apps, schema_editor):
    Category = apps.get_model('bulb', 'Category')
    Category.objects.filter(code_name__in=["intellectual",
                                           "historical",
                                           "religious",
                                           "literature",
                                           "biographical",
                                           "business",
                                           "self_help"]).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('bulb', '0001_initial'),
    ]

    operations = [
       migrations.RunPython(
            add_categories,
            reverse_code=remove_categories),
    ]
