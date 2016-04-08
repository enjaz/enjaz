# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_episodes_to_codes(apps, schema_editor):
    Collection = apps.get_model('niqati', 'Collection')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    episode_content_type = ContentType.objects.get(model="episode")

    for collection in Collection.objects.filter(codes__isnull=False).iterator():
        episode = collection.order.episode
        collection.codes.update(object_id=episode.pk,
                                content_type=episode_content_type)
        
class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0020_modify_citeria'),
        ('niqati', '0016_contenttype_for_niqati'),
    ]

    operations = [
       migrations.RunPython(
           add_episodes_to_codes)
    ]
