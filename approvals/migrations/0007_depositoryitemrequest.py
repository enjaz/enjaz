# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('approvals', '0006_auto_20170913_1847'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepositoryItemRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u0627\u0644\u0627\u0633\u0645')),
                ('quantity', models.PositiveIntegerField(verbose_name='\u0627\u0644\u0643\u0645\u064a\u0629')),
                ('unit', models.CharField(max_length=20, verbose_name='\u0627\u0644\u0648\u062d\u062f\u0629')),
                ('category', models.CharField(max_length=40, verbose_name='\u0627\u0644\u062a\u0635\u0646\u064a\u0641')),
                ('activity_request', models.ForeignKey(related_name='depositoryitemrequests', verbose_name='\u0637\u0644\u0628 \u0627\u0644\u0646\u0634\u0627\u0637', to='approvals.ActivityRequest')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
