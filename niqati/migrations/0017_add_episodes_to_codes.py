# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.contenttypes.management import update_contenttypes

def add_episodes_to_codes(apps, schema_editor):
    app_config = apps.get_app_config("activities")
    app_config.models_module = app_config.models_module or True
    ContentType = apps.get_model('contenttypes', 'ContentType')
    Collection = apps.get_model('niqati', 'Collection')
    update_contenttypes(app_config)
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
