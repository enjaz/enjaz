# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_episodes_to_codes(apps, schema_editor):
    Code = apps.get_model('niqati', 'Code')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    episode_content_type = ContentType.objects.get(model="episode")

    for code in Code.objects.filter(collection__isnull=False).iterator():
        episode = code.collection.order.episode
        code.object_id = episode.pk
        code.content_type = episode_content_type
        code.save()

class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0020_modify_citeria'),
        ('niqati', '0016_contenttype_for_niqati'),
    ]

    operations = [
       migrations.RunPython(
            add_episodes_to_codes)
    ]
