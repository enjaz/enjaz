# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0053_add_2017_2018_clubs'),
        ('media', '0010_auto_20170925_0229'),
    ]

    operations = [
        migrations.AddField(
            model_name='followupreport',
            name='collaborators_inside',
            field=models.TextField(null=True, verbose_name='\u0627\u0633\u0645\u0627\u0621 \u0627\u0644\u0645\u062a\u0639\u0627\u0648\u0646\u064a\u0646 \u0645\u0646 \u062f\u0627\u062e\u0644 \u0627\u0644\u062c\u0627\u0645\u0639\u0629'),
        ),
        migrations.AddField(
            model_name='followupreport',
            name='collaborators_outside',
            field=models.TextField(null=True, verbose_name='\u0627\u0633\u0645\u0627\u0621 \u0627\u0644\u0645\u062a\u0639\u0627\u0648\u0646\u064a\u0646 \u0645\u0646 \u062e\u0627\u0631\u062c \u0627\u0644\u062c\u0627\u0645\u0639\u0629'),
        ),
        migrations.AddField(
            model_name='followupreport',
            name='organizers_names',
            field=models.ManyToManyField(to='clubs.Club', verbose_name='\u0627\u0633\u0645\u0627\u0621 \u0627\u0644\u0645\u0646\u0638\u0645\u064a\u0646'),
        ),
    ]
