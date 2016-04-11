# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('niqati', '0015_add_codes_to_collections'),
    ]

    operations = [
        migrations.AddField(
            model_name='code',
            name='content_type',
            field=models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='code',
            name='object_id',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
    ]
