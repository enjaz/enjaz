# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def add_categories(apps, schema_editor):
    Category = apps.get_model('niqati', 'Category')
    # We are going to add categories only if none already exists.
    Category.objects.filter(label="Idea").update(label="Planning", ar_label="التخطيط", points=4)
    Category.objects.filter(label="Organizer").update(points=3)
    Category.objects.filter(label="Participation").update(points=2)
    Category.objects.create(label="Attendance",
                            ar_label="حضور",
                            direct_entry=True,
                            points=1)

def remove_categories(apps, schema_editor):
    Category = apps.get_model('niqati', 'Category')
    Category.objects.filter(label="Planning").update(label="Idea", ar_label="الفكرة", points=3)
    Category.objects.filter(label="Organizer").update(points=2)
    Category.objects.filter(label="Participation").update(points=1)
    Category.objects.get(label="Attendance").delete()

class Migration(migrations.Migration):

    dependencies = [
        ('niqati', '0017_add_episodes_to_codes'),
    ]

    operations = [
       migrations.RunPython(
            add_categories,
            reverse_code=remove_categories),
    ]
