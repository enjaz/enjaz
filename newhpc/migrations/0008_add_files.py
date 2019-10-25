# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newhpc', '0007_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='previousversion',
            name='speaker_file',
            field=models.ImageField(upload_to=b'newhpc/previous/speaker/file', null=True, verbose_name=b'\xd9\x85\xd9\x84\xd9\x81 \xd8\xa7\xd9\x84\xd9\x85\xd8\xaa\xd8\xad\xd8\xaf\xd8\xab\xd9\x8a\xd9\x86', blank=True),
        ),
        migrations.AddField(
            model_name='previousversion',
            name='winner_file',
            field=models.ImageField(upload_to=b'newhpc/previous/winner/file', null=True, verbose_name=b'\xd9\x85\xd9\x84\xd9\x81 \xd8\xa7\xd9\x84\xd9\x81\xd8\xa7\xd8\xa6\xd8\xb2\xd9\x8a\xd9\x86', blank=True),
        ),
    ]
