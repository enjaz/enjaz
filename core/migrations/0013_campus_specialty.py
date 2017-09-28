# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_studentclubyear_bookexchange_open_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('city', models.CharField(max_length=30, verbose_name='\u0627\u0644\u0645\u062f\u064a\u0646\u0629')),
            ],
            options={
                'verbose_name': '\u0645\u062f\u064a\u0646\u0629 \u062c\u0627\u0645\u0639\u064a\u0629',
                'verbose_name_plural': '\u0645\u062f\u0646 \u062c\u0627\u0645\u0639\u064a\u0629',
            },
        ),
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='\u0627\u0644\u0627\u0633\u0645')),
            ],
            options={
                'verbose_name': '\u062a\u062e\u0635\u0635',
                'verbose_name_plural': '\u062a\u062e\u0635\u0635\u0627\u062a',
            },
        ),
    ]
