# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0006_change_instructor_user_relation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='\u0627\u0644\u0627\u0633\u0645')),
                ('description', models.TextField(null=True, verbose_name='\u0627\u0644\u0648\u0635\u0641', blank=True)),
                ('plan', models.FileField(upload_to=b'', null=True, verbose_name='\u0645\u0644\u0641 \u0627\u0644\u062e\u0637\u0629', blank=True)),
                ('attend_count', models.IntegerField(null=True, verbose_name='\u0639\u062f\u062f \u0627\u0644\u062d\u0636\u0648\u0631', blank=True)),
                ('background', models.FileField(upload_to=b'', null=True, verbose_name='\u0627\u0644\u0635\u0648\u0631\u0629 \u0627\u0644\u062e\u0644\u0641\u064a\u0629', blank=True)),
                ('hex_colour', models.CharField(max_length=7, null=True, verbose_name='\u0644\u0648\u0646 \u0627\u0644\u062b\u064a\u0645 \u0628\u0635\u064a\u063a\u0629 hex', blank=True)),
            ],
            options={
                'verbose_name': '\u0648\u0631\u0634\u0629 \u0639\u0645\u0644',
                'verbose_name_plural': '\u0648\u0631\u0634 \u0627\u0644\u0639\u0645\u0644',
            },
        ),
        migrations.AddField(
            model_name='subcourse',
            name='official_name',
            field=models.CharField(max_length=200, null=True, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0631\u0633\u0645\u064a', blank=True),
        ),
        migrations.AddField(
            model_name='instructor',
            name='workshop',
            field=models.ManyToManyField(related_name='workshop_instructors', verbose_name='\u0648\u0631\u0634\u0629 \u0627\u0644\u0639\u0645\u0644', to='academy.Workshop'),
        ),
    ]
