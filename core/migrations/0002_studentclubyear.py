# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentClubYear',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0636\u0627\u0641\u0629')),
                ('start_date', models.DateTimeField(verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0628\u062f\u0627\u064a\u0629')),
                ('end_date', models.DateTimeField(verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0646\u0647\u0627\u064a\u0629')),
            ],
            options={
                'verbose_name': '\u0633\u0646\u0629 \u0646\u0627\u062f\u064a',
                'verbose_name_plural': '\u0633\u0646\u0648\u0627\u062a \u0627\u0644\u0646\u0627\u062f\u064a',
            },
        ),
    ]
