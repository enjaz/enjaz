# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bulb', '0021_teams'),
    ]

    operations = [
        migrations.CreateModel(
            name='DewanyaSuggestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u0627\u0644\u0627\u0633\u0645')),
                ('subject', models.CharField(max_length=100, verbose_name='\u0627\u0644\u0645\u0648\u0636\u0648\u0639')),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
            ],
        ),
    ]
