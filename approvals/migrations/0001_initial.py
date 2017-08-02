# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('activities2', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityCancelRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('submission_datetime', models.DateTimeField(auto_now_add=True, verbose_name='\u0648\u0642\u062a \u062a\u0642\u062f\u064a\u0645 \u0627\u0644\u0637\u0644\u0628')),
                ('activity', models.ForeignKey(to='activities2.Activity', verbose_name='\u0627\u0644\u0646\u0634\u0627\u0637')),
            ],
            options={
                'verbose_name': '\u0637\u0644\u0628 \u0625\u0644\u063a\u0627\u0621 \u0646\u0634\u0627\u0637',
                'verbose_name_plural': '\u0637\u0644\u0628\u0627\u062a \u0625\u0644\u063a\u0627\u0621 \u0623\u0646\u0634\u0637\u0629',
            },
        ),
        migrations.CreateModel(
            name='ActivityRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('submission_datetime', models.DateTimeField(auto_now_add=True, verbose_name='\u0648\u0642\u062a \u062a\u0642\u062f\u064a\u0645 \u0627\u0644\u0637\u0644\u0628')),
                ('name', models.CharField(max_length=200, verbose_name='\u0627\u0633\u0645 \u0627\u0644\u0646\u0634\u0627\u0637')),
                ('description', ckeditor.fields.RichTextField(verbose_name='\u0648\u0635\u0641 \u0627\u0644\u0646\u0634\u0627\u0637')),
                ('is_update_request', models.BooleanField(default=False, verbose_name='\u0646\u0648\u0639 \u0627\u0644\u0637\u0644\u0628', choices=[(False, '\u0637\u0644\u0628 \u0625\u0636\u0627\u0641\u0629'), (True, '\u0637\u0644\u0628 \u062a\u0639\u062f\u064a\u0644')])),
                ('activity', models.ForeignKey(verbose_name='\u0627\u0644\u0646\u0634\u0627\u0637', blank=True, to='activities2.Activity', null=True)),
            ],
            options={
                'verbose_name': '\u0637\u0644\u0628 \u0646\u0634\u0627\u0637',
                'verbose_name_plural': '\u0637\u0644\u0628\u0627\u062a \u0623\u0646\u0634\u0637\u0629',
            },
        ),
        migrations.CreateModel(
            name='DescriptionField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=50, verbose_name='\u0627\u0644\u0648\u0635\u0641')),
                ('value', models.CharField(max_length=200, verbose_name='\u0627\u0644\u0642\u064a\u0645\u0629')),
                ('activity_request', models.ForeignKey(related_name='descriptionfields', to='approvals.ActivityRequest', verbose_name='\u0637\u0644\u0628 \u0627\u0644\u0646\u0634\u0627\u0637')),
            ],
            options={
                'verbose_name': '\u062d\u0642\u0644 \u0648\u0635\u0641\u064a',
                'verbose_name_plural': '\u062d\u0642\u0648\u0644 \u0648\u0635\u0641\u064a\u0629',
            },
        ),
        migrations.CreateModel(
            name='EventRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('location', models.CharField(max_length=50)),
                ('activity_request', models.ForeignKey(related_name='eventrequests', to='approvals.ActivityRequest', verbose_name='\u0637\u0644\u0628 \u0627\u0644\u0646\u0634\u0627\u0637')),
            ],
            options={
                'verbose_name': '\u0637\u0644\u0628 \u0641\u0639\u0627\u0644\u064a\u0629',
                'verbose_name_plural': '\u0637\u0644\u0628\u0627\u062a \u0641\u0639\u0627\u0644\u064a\u0627\u062a',
            },
        ),
    ]
