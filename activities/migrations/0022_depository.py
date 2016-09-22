# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0021_add_goals'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepositoryItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=100, verbose_name='\u0627\u0644\u0627\u0633\u0645')),
                ('quantity', models.PositiveIntegerField(null=True, verbose_name='\u0627\u0644\u0643\u0645\u064a\u0629', blank=True)),
                ('unit', models.CharField(default=b'', max_length=20, verbose_name='\u0627\u0644\u0648\u062d\u062f\u0629')),
                ('category', models.CharField(default=b'', max_length=40, verbose_name='\u0627\u0644\u062a\u0635\u0646\u064a\u0641')),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('edit_date', models.DateTimeField(auto_now=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062a\u0639\u062f\u064a\u0644')),
            ],
        ),
        migrations.CreateModel(
            name='ItemRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=100, verbose_name='\u0627\u0644\u0627\u0633\u0645')),
                ('quantity', models.PositiveIntegerField(verbose_name='\u0627\u0644\u0643\u0645\u064a\u0629')),
                ('unit', models.CharField(default=b'', max_length=20, verbose_name='\u0627\u0644\u0648\u062d\u062f\u0629')),
                ('category', models.CharField(default=b'', max_length=40, verbose_name='\u0627\u0644\u062a\u0635\u0646\u064a\u0641')),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('edit_date', models.DateTimeField(auto_now=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062a\u0639\u062f\u064a\u0644')),
                ('activity', models.ForeignKey(to='activities.Activity')),
            ],
        ),
        migrations.AlterField(
            model_name='activity',
            name='requirements',
            field=models.TextField(verbose_name='\u0645\u062a\u0637\u0644\u0628\u0627\u062a \u0627\u0644\u0646\u0634\u0627\u0637 \u0627\u0644\u0623\u062e\u0631\u0649', blank=True),
        ),
    ]
