# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='\u0627\u0644\u0627\u0633\u0645')),
                ('code', models.CharField(max_length=2, verbose_name='\u0627\u0644\u0631\u0645\u0632', choices=[('PR', '\u062f\u0648\u0631\u0629 \u0627\u0644\u0628\u0631\u0645\u062c\u0629'), ('PS', '\u062f\u0648\u0631\u0629 \u0627\u0644\u0641\u0648\u062a\u0648\u0634\u0648\u0628'), ('VE', '\u062f\u0648\u0631\u0629 \u0627\u0644\u0645\u0648\u0646\u062a\u0627\u062c'), ('CW', '\u062f\u0648\u0631\u0629 \u0643\u062a\u0627\u0628\u0629 \u0627\u0644\u0645\u062d\u062a\u0648\u0649'), ('PH', '\u062f\u0648\u0631\u0629 \u0627\u0644\u062a\u0635\u0648\u064a\u0631')])),
                ('logo', models.FileField(upload_to=b'', null=True, verbose_name='\u0627\u0644\u0634\u0639\u0627\u0631')),
                ('description', models.TextField(null=True, verbose_name='\u0627\u0644\u0648\u0635\u0641', blank=True)),
            ],
            options={
                'verbose_name': '\u062f\u0648\u0631\u0629 \u0623\u0633\u0627\u0633\u064a\u0629',
                'verbose_name_plural': '\u0627\u0644\u062f\u0648\u0631\u0627\u062a \u0627\u0644\u0623\u0633\u0627\u0633\u064a\u0629',
            },
        ),
        migrations.CreateModel(
            name='Graduate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('batch', models.IntegerField(verbose_name='\u0631\u0642\u0645 \u0627\u0644\u062f\u0641\u0639\u0629')),
                ('experience', models.TextField(verbose_name='\u0627\u0644\u062e\u0628\u0631\u0629', blank=True)),
                ('twitter_account', models.CharField(max_length=200, null=True, verbose_name='\u062d\u0633\u0627\u0628 \u0627\u0644\u062a\u0648\u064a\u062a\u0631')),
                ('telegram_account', models.CharField(max_length=200, null=True, verbose_name='\u062d\u0633\u0627\u0628 \u0627\u0644\u062a\u0644\u0642\u0631\u0627\u0645')),
            ],
            options={
                'verbose_name': '\u062e\u0631\u064a\u062c\u0640/\u0640\u0629',
                'verbose_name_plural': '\u0627\u0644\u062e\u0631\u064a\u062c\u0648\u0646/\u0627\u0644\u062e\u0631\u064a\u062c\u0627\u062a',
            },
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('experience', models.TextField(null=True, verbose_name='\u0627\u0644\u062e\u0628\u0631\u0629', blank=True)),
                ('twitter_account', models.CharField(max_length=200, null=True, verbose_name='\u062d\u0633\u0627\u0628 \u0627\u0644\u062a\u0648\u064a\u062a\u0631')),
                ('telegram_account', models.CharField(max_length=200, null=True, verbose_name='\u062d\u0633\u0627\u0628 \u0627\u0644\u062a\u0644\u0642\u0631\u0627\u0645')),
                ('course', models.ManyToManyField(related_name='course_instructors', verbose_name='\u0627\u0644\u062f\u0648\u0631\u0629', to='academy.Course')),
                ('user', models.OneToOneField(verbose_name='\u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645\u0640/\u0640\u0629', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u0645\u0642\u062f\u0645\u0640/\u0640\u0629',
                'verbose_name_plural': '\u0627\u0644\u0645\u0642\u062f\u0645\u0648\u0646/\u0627\u0644\u0645\u0642\u062f\u0645\u0627\u062a',
            },
        ),
        migrations.CreateModel(
            name='NewStudent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('batch', models.IntegerField()),
                ('sc_work', models.TextField(verbose_name='\u0645\u0634\u0627\u0631\u0643\u0629 \u0641\u064a \u0646\u0627\u062f\u064a \u0627\u0644\u0637\u0644\u0627\u0628 ')),
                ('past_exp', models.TextField(verbose_name='\u062e\u0628\u0631\u0629 \u0633\u0627\u0628\u0642\u0629')),
                ('why_join', models.TextField(verbose_name='\u0633\u0628\u0628 \u0627\u0644\u062a\u0633\u062c\u064a\u0644')),
                ('will_work', models.BooleanField(default=False, verbose_name='\u0627\u0644\u0639\u0645\u0644 \u0645\u0639 \u0627\u0644\u0646\u0627\u062f\u064a \u0628\u0639\u062f \u0627\u0644\u062f\u0648\u0631\u0629')),
                ('course', models.ForeignKey(related_name='new_student', verbose_name='\u0627\u0644\u062f\u0648\u0631\u0629', to='academy.Course')),
                ('user', models.OneToOneField(verbose_name='\u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645\u0640/\u0640\u0629', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u0637\u0627\u0644\u0628\u0640/\u0640\u0629 \u062c\u062f\u064a\u062f/\u0629',
                'verbose_name_plural': '\u0627\u0644\u0637\u0644\u0627\u0628 \u0627\u0644\u062c\u062f\u064a\u062f\u0648\u0646 / \u0627\u0644\u0637\u0627\u0644\u0628\u0627\u062a \u0627\u0644\u062c\u062f\u064a\u062f\u0627\u062a',
            },
        ),
        migrations.CreateModel(
            name='SubCourse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('plan', models.FileField(upload_to=b'', null=True, verbose_name='\u0645\u0644\u0641 \u0627\u0644\u062e\u0637\u0629')),
                ('session_count', models.IntegerField(null=True, verbose_name='\u0639\u062f\u062f \u0627\u0644\u062c\u0644\u0633\u0627\u062a')),
                ('homework_count', models.IntegerField(null=True, verbose_name='\u0639\u062f\u062f \u0627\u0644\u0645\u0647\u0627\u0645 \u0648\u0627\u0644\u0648\u0627\u062c\u0628\u0627\u062a')),
                ('batch_no', models.IntegerField(null=True, verbose_name='\u0631\u0642\u0645 \u0627\u0644\u062f\u0641\u0639\u0629')),
                ('batch_note', models.TextField(null=True, verbose_name='\u0645\u0644\u0627\u062d\u0638\u0629 \u0639\u0644\u0649 \u0627\u0644\u0639\u062f\u062f')),
                ('form_url', models.TextField(null=True, verbose_name='\u0631\u0627\u0628\u0637 \u0646\u0645\u0648\u0630\u062c \u0627\u0644\u062a\u0633\u062c\u064a\u0644')),
                ('reg_open_date', models.DateTimeField(null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0641\u062a\u062d \u0627\u0644\u062a\u0633\u062c\u064a\u0644')),
                ('reg_close_date', models.DateTimeField(null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0625\u063a\u0644\u0627\u0642 \u0627\u0644\u062a\u0633\u062c\u064a\u0644')),
                ('parent_course', models.ForeignKey(verbose_name='\u0627\u0644\u062f\u0648\u0631\u0629 \u0627\u0644\u0623\u0628', to='academy.Course')),
            ],
            options={
                'verbose_name': '\u062f\u0648\u0631\u0629 \u0641\u0631\u0639\u064a\u0629',
                'verbose_name_plural': '\u0627\u0644\u062f\u0648\u0631\u0627\u062a \u0627\u0644\u0641\u0631\u0639\u064a\u0629',
            },
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_description', models.CharField(max_length=200, verbose_name='\u0648\u0635\u0641 \u0642\u0635\u064a\u0631')),
                ('long_description', models.TextField(verbose_name='\u0648\u0635\u0641 \u0643\u0627\u0645\u0644', blank=True)),
                ('projects_in_sc', models.TextField(verbose_name='\u0645\u0634\u0627\u0631\u064a\u0639 \u0641\u064a \u0646\u0627\u062f\u064a \u0627\u0644\u0637\u0644\u0627\u0628', blank=True)),
                ('projects_outside_sc', models.TextField(verbose_name='\u0645\u0634\u0627\u0631\u064a\u0639 \u062e\u0627\u0631\u062c \u0646\u0627\u062f\u064a \u0627\u0644\u0637\u0644\u0627\u0628', blank=True)),
                ('done_projects', models.FileField(upload_to='academy/done_projects', verbose_name='\u0645\u0634\u0627\u0631\u064a\u0639 \u0645\u0643\u062a\u0645\u0644\u0629', blank=True)),
                ('graduate', models.ManyToManyField(to='academy.Graduate', verbose_name='\u0627\u0644\u062e\u0631\u064a\u062c\u0640/\u0640\u0629')),
            ],
            options={
                'verbose_name': '\u0639\u0645\u0644',
                'verbose_name_plural': '\u0627\u0644\u0623\u0639\u0645\u0627\u0644',
            },
        ),
        migrations.AddField(
            model_name='graduate',
            name='course',
            field=models.ManyToManyField(related_name='course_graduates', verbose_name='\u0627\u0644\u062f\u0648\u0631\u0629', to='academy.SubCourse'),
        ),
        migrations.AddField(
            model_name='graduate',
            name='user',
            field=models.OneToOneField(verbose_name='\u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645\u0640/\u0640\u0629', to=settings.AUTH_USER_MODEL),
        ),
    ]
