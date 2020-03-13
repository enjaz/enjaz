# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0010_logo_n_bg_alterations'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecordedSession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, null=True, verbose_name='\u0639\u0646\u0648\u0627\u0646 \u0627\u0644\u062c\u0644\u0633\u0629 ', blank=True)),
                ('number', models.CharField(max_length=9, null=True, verbose_name='\u0631\u0642\u0645 \u0627\u0644\u062c\u0644\u0633\u0629', blank=True)),
                ('recording', models.FileField(upload_to='academy/session_recordings', null=True, verbose_name='\u062a\u0633\u062c\u064a\u0644 \u0627\u0644\u062c\u0644\u0633\u0629', blank=True)),
                ('attachment', models.FileField(upload_to='academy/session_attachments', null=True, verbose_name='\u0645\u0644\u0641 \u0645\u0631\u0641\u0642', blank=True)),
                ('subcourse', models.ForeignKey(related_name='recorded_session', verbose_name='\u0627\u0644\u062f\u0648\u0631\u0629', to='academy.SubCourse')),
            ],
            options={
                'verbose_name': '\u062a\u0633\u062c\u064a\u0644 \u062c\u0644\u0633\u0629',
                'verbose_name_plural': '\u062a\u0633\u062c\u064a\u0644\u0627\u062a \u0627\u0644\u062c\u0644\u0633\u0627\u062a',
            },
        ),
    ]
