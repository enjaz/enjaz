# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0042_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='abstract',
            name='accepted_presentaion_preference',
            field=models.CharField(default='', max_length=1, verbose_name=b'Accepted presentation preference', choices=[(b'O', b'Oral'), (b'P', b'Poster')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='abstractposter',
            name='presentation_file',
            field=models.FileField(default='', upload_to=b'events/presentations/', verbose_name='Attach the presentation'),
            preserve_default=False,
        ),
    ]
