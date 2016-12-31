# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0019_rename_figure_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='abstractfigure',
            name='figure',
            field=models.FileField(default='', upload_to=b'hpc/figures/', verbose_name='Attach the figure'),
            preserve_default=False,
        ),
    ]
