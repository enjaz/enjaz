# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0004_edit_work'),
    ]

    operations = [
        migrations.CreateModel(
            name='Temporary_Stats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('grad_count', models.CharField(max_length=10, verbose_name='\u0639\u062f\u062f \u0627\u0644\u062e\u0631\u064a\u062c\u064a\u0646 \u0648\u0627\u0644\u062e\u0631\u064a\u062c\u0627\u062a')),
                ('course_count', models.CharField(max_length=10, verbose_name='\u0639\u062f\u062f \u0627\u0644\u062f\u0648\u0631\u0627\u062a')),
                ('instr_count', models.CharField(max_length=10, verbose_name='\u0639\u062f\u062f \u0627\u0644\u0645\u0642\u062f\u0645\u064a\u0646 \u0648\u0627\u0644\u0645\u0642\u062f\u0645\u0627\u062a')),
                ('session_count', models.CharField(max_length=10, verbose_name='\u0639\u062f\u062f \u0627\u0644\u062c\u0644\u0633\u0627\u062a')),
            ],
        ),
    ]
