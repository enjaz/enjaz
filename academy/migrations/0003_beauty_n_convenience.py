# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0002_add_BG'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='graduate',
            name='batch',
        ),
        migrations.RemoveField(
            model_name='newstudent',
            name='batch',
        ),
        migrations.AddField(
            model_name='course',
            name='background',
            field=models.FileField(upload_to=b'', null=True, verbose_name='\u0627\u0644\u0635\u0648\u0631\u0629 \u0627\u0644\u062e\u0644\u0641\u064a\u0629', blank=True),
        ),
        migrations.AddField(
            model_name='course',
            name='hex_colour',
            field=models.CharField(max_length=7, null=True, verbose_name='\u0644\u0648\u0646 \u0627\u0644\u062b\u064a\u0645 \u0628\u0635\u064a\u063a\u0629 hex', blank=True),
        ),
        migrations.AddField(
            model_name='subcourse',
            name='background',
            field=models.FileField(upload_to=b'', null=True, verbose_name='\u0627\u0644\u0635\u0648\u0631\u0629 \u0627\u0644\u062e\u0644\u0641\u064a\u0629', blank=True),
        ),
        migrations.AlterField(
            model_name='graduate',
            name='telegram_account',
            field=models.CharField(max_length=200, null=True, verbose_name='\u062d\u0633\u0627\u0628 \u0627\u0644\u062a\u0644\u0642\u0631\u0627\u0645', blank=True),
        ),
        migrations.AlterField(
            model_name='graduate',
            name='twitter_account',
            field=models.CharField(max_length=200, null=True, verbose_name='\u062d\u0633\u0627\u0628 \u0627\u0644\u062a\u0648\u064a\u062a\u0631', blank=True),
        ),
        migrations.AlterField(
            model_name='indexbg',
            name='img',
            field=models.FileField(upload_to=b'', null=True, verbose_name='\u0627\u0644\u0635\u0648\u0631\u0629 ', blank=True),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='course',
            field=models.ManyToManyField(related_name='course_instructors', verbose_name='\u0627\u0644\u062f\u0648\u0631\u0629', to='academy.SubCourse'),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='telegram_account',
            field=models.CharField(max_length=200, null=True, verbose_name='\u062d\u0633\u0627\u0628 \u0627\u0644\u062a\u0644\u0642\u0631\u0627\u0645', blank=True),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='twitter_account',
            field=models.CharField(max_length=200, null=True, verbose_name='\u062d\u0633\u0627\u0628 \u0627\u0644\u062a\u0648\u064a\u062a\u0631', blank=True),
        ),
        migrations.AlterField(
            model_name='newstudent',
            name='course',
            field=models.ForeignKey(related_name='new_student', verbose_name='\u0627\u0644\u062f\u0648\u0631\u0629', to='academy.SubCourse'),
        ),
        migrations.AlterField(
            model_name='subcourse',
            name='batch_note',
            field=models.TextField(null=True, verbose_name='\u0645\u0644\u0627\u062d\u0638\u0629 \u0639\u0644\u0649 \u0627\u0644\u0639\u062f\u062f', blank=True),
        ),
        migrations.AlterField(
            model_name='subcourse',
            name='form_url',
            field=models.TextField(null=True, verbose_name='\u0631\u0627\u0628\u0637 \u0646\u0645\u0648\u0630\u062c \u0627\u0644\u062a\u0633\u062c\u064a\u0644', blank=True),
        ),
        migrations.AlterField(
            model_name='subcourse',
            name='homework_count',
            field=models.IntegerField(null=True, verbose_name='\u0639\u062f\u062f \u0627\u0644\u0645\u0647\u0627\u0645 \u0648\u0627\u0644\u0648\u0627\u062c\u0628\u0627\u062a', blank=True),
        ),
        migrations.AlterField(
            model_name='subcourse',
            name='plan',
            field=models.FileField(upload_to=b'', null=True, verbose_name='\u0645\u0644\u0641 \u0627\u0644\u062e\u0637\u0629', blank=True),
        ),
        migrations.AlterField(
            model_name='subcourse',
            name='reg_close_date',
            field=models.DateTimeField(null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0625\u063a\u0644\u0627\u0642 \u0627\u0644\u062a\u0633\u062c\u064a\u0644', blank=True),
        ),
        migrations.AlterField(
            model_name='subcourse',
            name='reg_open_date',
            field=models.DateTimeField(null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0641\u062a\u062d \u0627\u0644\u062a\u0633\u062c\u064a\u0644', blank=True),
        ),
        migrations.AlterField(
            model_name='subcourse',
            name='session_count',
            field=models.IntegerField(null=True, verbose_name='\u0639\u062f\u062f \u0627\u0644\u062c\u0644\u0633\u0627\u062a', blank=True),
        ),
        migrations.AlterField(
            model_name='work',
            name='done_projects',
            field=models.FileField(upload_to='academy/done_projects', null=True, verbose_name='\u0645\u0634\u0627\u0631\u064a\u0639 \u0645\u0643\u062a\u0645\u0644\u0629', blank=True),
        ),
        migrations.AlterField(
            model_name='work',
            name='long_description',
            field=models.TextField(null=True, verbose_name='\u0648\u0635\u0641 \u0643\u0627\u0645\u0644', blank=True),
        ),
        migrations.AlterField(
            model_name='work',
            name='projects_in_sc',
            field=models.TextField(null=True, verbose_name='\u0645\u0634\u0627\u0631\u064a\u0639 \u0641\u064a \u0646\u0627\u062f\u064a \u0627\u0644\u0637\u0644\u0627\u0628', blank=True),
        ),
        migrations.AlterField(
            model_name='work',
            name='projects_outside_sc',
            field=models.TextField(null=True, verbose_name='\u0645\u0634\u0627\u0631\u064a\u0639 \u062e\u0627\u0631\u062c \u0646\u0627\u062f\u064a \u0627\u0644\u0637\u0644\u0627\u0628', blank=True),
        ),
    ]
