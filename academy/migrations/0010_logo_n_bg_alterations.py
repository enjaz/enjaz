# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0009_edit_workshop_n_instructor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='background',
        ),
        migrations.RemoveField(
            model_name='course',
            name='hex_colour',
        ),
        migrations.RemoveField(
            model_name='course',
            name='logo',
        ),
        migrations.AddField(
            model_name='subcourse',
            name='hex_colour',
            field=models.CharField(max_length=7, null=True, verbose_name='\u0644\u0648\u0646 \u0627\u0644\u062b\u064a\u0645 \u0628\u0635\u064a\u063a\u0629 hex', blank=True),
        ),
        migrations.AddField(
            model_name='subcourse',
            name='logo',
            field=models.FileField(upload_to=b'', null=True, verbose_name='\u0627\u0644\u0634\u0639\u0627\u0631'),
        ),
        migrations.AlterField(
            model_name='course',
            name='code',
            field=models.CharField(max_length=2, verbose_name='\u0627\u0644\u0631\u0645\u0632', choices=[('PR', '\u062f\u0648\u0631\u0629 \u0627\u0644\u0628\u0631\u0645\u062c\u0629'), ('PS', '\u062f\u0648\u0631\u0629 \u0627\u0644\u0641\u0648\u062a\u0648\u0634\u0648\u0628'), ('VE', '\u062f\u0648\u0631\u0629 \u0627\u0644\u0645\u0648\u0646\u062a\u0627\u062c'), ('CW', '\u062f\u0648\u0631\u0629 \u0643\u062a\u0627\u0628\u0629 \u0627\u0644\u0645\u062d\u062a\u0648\u0649'), ('PH', '\u062f\u0648\u0631\u0629 \u0627\u0644\u062a\u0635\u0648\u064a\u0631'), ('MM', '\u062f\u0648\u0631\u0629 \u0645\u0647\u0627\u0631\u0627\u062a \u0627\u0644\u062a\u0633\u0648\u064a\u0642 \u0648\u0627\u0644\u0625\u0639\u0644\u0627\u0645'), ('VP', '\u062f\u0648\u0631\u0629 \u0627\u0644\u0623\u062f\u0627\u0621 \u0627\u0644\u0635\u0648\u062a\u064a'), ('IL', '\u062f\u0648\u0631\u0629 \u0627\u0644illustrator'), ('CM', '\u062f\u0648\u0631\u0629 \u0625\u062f\u0627\u0631\u0629 \u0627\u0644\u062d\u0645\u0644\u0627\u062a \u0627\u0644\u0635\u062d\u064a\u0629'), ('3D', '\u062f\u0648\u0631\u0629 \u062a\u0635\u0645\u064a\u0645 \u062b\u0644\u0627\u062b\u064a \u0627\u0644\u0623\u0628\u0639\u0627\u062f')]),
        ),
    ]
