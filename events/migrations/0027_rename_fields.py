# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0026_rename_models'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='initiation_submission_closing_date',
            new_name='initiative_submission_closing_date',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='initiation_submission_opening_date',
            new_name='initiative_submission_opening_date',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='receives_initiation_submission',
            new_name='receives_initiative_submission',
        ),
        migrations.AddField(
            model_name='initiativefigure',
            name='initiative',
            field=models.ForeignKey(related_name='figures', to='events.Initiative', null=True),
        ),
        migrations.AlterField(
            model_name='initiativefigure',
            name='figure',
            field=models.FileField(upload_to=b'events/figures/initiatives/', verbose_name='Attach the figure'),
        ),
    ]
