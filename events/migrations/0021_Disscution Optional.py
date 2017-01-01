# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0020_add figure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abstract',
            name='discussion',
            field=models.TextField(default=b'', null=True, verbose_name='Discussion', blank=True),
        ),
        migrations.AlterField(
            model_name='abstractfigure',
            name='figure',
            field=models.FileField(upload_to=b'events/figures/', verbose_name='Attach the figure'),
        ),
        migrations.AlterField(
            model_name='abstractfigure',
            name='upload',
            field=models.FileField(upload_to=b'event/figures/', verbose_name='Attach the figure'),
        ),
    ]
