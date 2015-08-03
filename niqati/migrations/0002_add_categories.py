# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_categories(apps, schema_editor):
    Category = apps.get_model('niqati', 'Category')
    # We are going to add categories only if none already exists.
    if not Category.objects.exists():
        Category.objects.create(label="Idea",
                                ar_label="فكرة",
                                points=3)
        Category.objects.create(label="Organizer",
                                ar_label="تنظيم",
                                points=2)
        Category.objects.create(label="Participation",
                                ar_label="مشاركة",
                                points=1)

def remove_categories(apps, schema_editor):
    Category = apps.get_model('niqati', 'Category')
    Category.objects.filter(label__in=["Idea", "Organizer", "Participation"]).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('niqati', '0001_initial'),
    ]

    operations = [
       migrations.RunPython(
            add_categories,
            reverse_code=remove_categories),
    ]
