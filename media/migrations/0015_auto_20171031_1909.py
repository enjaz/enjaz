# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0052_presidencies_can_assess'),
        ('media', '0014_snapchatreservation_activity'),
    ]

    operations = [
        migrations.AddField(
            model_name='followupreport',
            name='inside_collaborators',
            field=models.TextField(verbose_name='\u0627\u0644\u0645\u062a\u0639\u0627\u0648\u0646\u0648\u0646 \u0645\u0646 \u062f\u0627\u062e\u0644 \u0627\u0644\u062c\u0627\u0645\u0639\u0629', blank=True),
        ),
        migrations.AddField(
            model_name='followupreport',
            name='outside_collaborators',
            field=models.TextField(verbose_name='\u0627\u0644\u0645\u062a\u0639\u0627\u0648\u0646\u0648\u0646 \u0645\u0646 \u062e\u0627\u0631\u062c \u0627\u0644\u062c\u0627\u0645\u0639\u0629', blank=True),
        ),
        migrations.AddField(
            model_name='followupreport',
            name='primary_club',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0646\u0627\u062f\u064a \u0627\u0644\u0645\u0646\u0638\u0645', to='clubs.Club', null=True),
        ),
    ]
