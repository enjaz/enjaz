# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0018_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='abstractfigure',
            name='upload',
            field=models.FileField(default='', upload_to=b'event/figures/', verbose_name='Attach the figure'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='abstract',
            name='discussion',
            field=models.TextField(default=b'', null=True, verbose_name='Discussion', blank=True),
        ),
        migrations.AlterField(
            model_name='abstractfigure',
            name='abstract',
            field=models.ForeignKey(related_name='figures', to='events.Abstract', null=True),
        ),
        migrations.AlterField(
            model_name='abstractfigure',
            name='figure',
            field=models.FileField(upload_to=b'events/figures/', verbose_name='Attach the figure'),
        ),
        migrations.AlterField(
            model_name='event',
            name='organizing_club',
            field=models.ForeignKey(to='clubs.Club', null=True),
        ),
    ]
