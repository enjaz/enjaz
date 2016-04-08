# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_codes_to_collections(apps, schema_editor):
    Code = apps.get_model('niqati', 'Code')
    Collection = apps.get_model('niqati', 'Collection')

    for code in Code.objects.filter(collection__isnull=False).iterator():
        collection = code.collection
        collection.codes.add(code)

class Migration(migrations.Migration):

    dependencies = [
        ('niqati', '0014_collection_codes'),
    ]

    operations = [
       migrations.RunPython(
            add_codes_to_collections
    ]
