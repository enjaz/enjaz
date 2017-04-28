# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0037_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='criterion',
            name='event',
        ),
        migrations.AddField(
            model_name='criterion',
            name='events',
            field=models.ManyToManyField(to='events.Event', verbose_name='\u0627\u0644\u062d\u062f\u062b'),
        ),
        migrations.AlterField(
            model_name='criterion',
            name='instructions',
            field=models.TextField(default=b'', verbose_name='\u062a\u0639\u0644\u064a\u0645\u0627\u062a'),
        ),
    ]
