# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studentguide', '0003_migrate_old_profiles'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='requester_status_date',
            field=models.DateTimeField(default=None, null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u062d\u0627\u0644\u0629 \u0645\u0642\u062f\u0645 \u0627\u0644\u0637\u0644\u0628', blank=True),
        ),
        migrations.AlterField(
            model_name='guideprofile',
            name='tags',
            field=models.ManyToManyField(help_text='\u064a\u0645\u0643\u0646\u0643 \u0627\u062e\u062a\u064a\u0627\u0631 \u0623\u0643\u062b\u0631 \u0645\u0646 \u0648\u0633\u0645.', related_name='guide_profiles', verbose_name='\u0627\u0644\u0648\u0633\u0648\u0645', to='studentguide.Tag'),
        ),
    ]
