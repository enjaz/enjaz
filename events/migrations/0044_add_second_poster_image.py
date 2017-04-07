# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0043_add_presentation_upload'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='abstractposter',
            name='poster',
        ),
        migrations.AddField(
            model_name='abstractposter',
            name='first_image',
            field=models.FileField(default='', upload_to=b'events/posters/', verbose_name='Attach the first image'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='abstractposter',
            name='second_image',
            field=models.FileField(upload_to=b'events/second_image/', null=True, verbose_name='Attach the second image'),
        ),
    ]
