# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='casereport',
            name='accepted_presentaion_preference',
            field=models.CharField(blank=True, max_length=1, verbose_name=b'Accepted presentation preference', choices=[(b'O', b'Oral'), (b'P', b'Poster')]),
        ),
        migrations.AddField(
            model_name='casereport',
            name='level',
            field=models.CharField(default=b'', max_length=1, verbose_name=b'Level', choices=[(b'U', b'Undergraduate'), (b'G', b'Graduate')]),
        ),
        migrations.AddField(
            model_name='casereport',
            name='presentation_preference',
            field=models.CharField(default=b'', max_length=1, verbose_name=b'Presentation preference', choices=[(b'O', b'Oral'), (b'P', b'Poster')]),
        ),
        migrations.AddField(
            model_name='casereport',
            name='presenting_author',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'Presenting author'),
        ),
        migrations.AddField(
            model_name='casereport',
            name='status',
            field=models.CharField(default=b'P', max_length=1, verbose_name=b'acceptance status', choices=[(b'A', b'Accepted'), (b'P', b'Pending'), (b'R', b'Rejected')]),
        ),
    ]
