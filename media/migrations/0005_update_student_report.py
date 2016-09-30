# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0004_add_epmloyee_report'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowUpReportAdImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.FileField(upload_to=b'media/ad_images/', verbose_name='\u0627\u0644\u0625\u0639\u0644\u0627\u0646')),
            ],
        ),
        migrations.RemoveField(
            model_name='employeereport',
            name='participant_count',
        ),
        migrations.AddField(
            model_name='employeereport',
            name='attendant_count',
            field=models.PositiveIntegerField(null=True, verbose_name='\u0639\u062f\u062f \u0627\u0644\u062d\u0627\u0636\u0631\u064a\u0646 \u0648\u0627\u0644\u062d\u0627\u0636\u0631\u0627\u062a'),
        ),
        migrations.AddField(
            model_name='followupreport',
            name='twitter_announcement',
            field=models.TextField(default=b'', verbose_name='\u0631\u0648\u0627\u0628\u0637 \u0627\u0644\u0625\u0639\u0644\u0627\u0646 \u0639\u0628\u0631 \u062a\u0648\u064a\u062a\u0631'),
        ),
        migrations.AlterField(
            model_name='employeereport',
            name='booth',
            field=models.TextField(verbose_name='\u0623\u0633\u0645\u0627\u0621 \u0627\u0644\u0623\u0631\u0643\u0627\u0646 \u0627\u0644\u0645\u0634\u0627\u0631\u0643\u0629', blank=True),
        ),
        migrations.AlterField(
            model_name='employeereport',
            name='booth_count',
            field=models.PositiveIntegerField(help_text='\u0627\u062e\u062a\u064a\u0627\u0631\u064a', null=True, verbose_name='\u0639\u062f\u062f \u0627\u0644\u0623\u0631\u0643\u0627\u0646', blank=True),
        ),
        migrations.AlterField(
            model_name='employeereport',
            name='end',
            field=models.TextField(verbose_name='\u0643\u064a\u0641 \u0627\u0646\u062a\u0647\u0649 \u0627\u0644\u0646\u0634\u0627\u0637\u061f'),
        ),
        migrations.AlterField(
            model_name='employeereport',
            name='lecture_count',
            field=models.PositiveIntegerField(help_text='\u0627\u062e\u062a\u064a\u0627\u0631\u064a', null=True, verbose_name='\u0639\u062f\u062f \u0627\u0644\u0645\u062d\u0627\u0636\u0631\u0627\u062a', blank=True),
        ),
        migrations.AlterField(
            model_name='employeereport',
            name='notes',
            field=models.TextField(help_text='\u0627\u062e\u062a\u064a\u0627\u0631\u064a', verbose_name='\u0645\u0644\u0627\u062d\u0638\u0627\u062a', blank=True),
        ),
        migrations.AlterField(
            model_name='employeereport',
            name='organizer_count',
            field=models.PositiveIntegerField(verbose_name='\u0639\u062f\u062f \u0627\u0644\u0645\u0646\u0638\u0645\u064a\u0646 \u0648\u0627\u0644\u0645\u0646\u0638\u0645\u0627\u062a'),
        ),
        migrations.AlterField(
            model_name='employeereport',
            name='prize_winner',
            field=models.TextField(help_text='\u0627\u062e\u062a\u064a\u0627\u0631\u064a', verbose_name='\u0623\u0633\u0645\u0627\u0621 \u0627\u0644\u0645\u0643\u0631\u0645\u064a\u0646 \u0648\u0627\u0644\u0645\u0643\u0631\u0645\u0627\u062a', blank=True),
        ),
        migrations.AlterField(
            model_name='employeereport',
            name='quotation',
            field=models.TextField(verbose_name='\u0627\u0642\u062a\u0628\u0627\u0633\u0627\u062a \u0645\u0646 \u0627\u0644\u0645\u062a\u062d\u062f\u062b\u064a\u0646 \u0648\u0627\u0644\u0645\u062a\u062d\u062f\u062b\u0627\u062a'),
        ),
        migrations.AlterField(
            model_name='employeereport',
            name='session_count',
            field=models.PositiveIntegerField(help_text='\u0627\u062e\u062a\u064a\u0627\u0631\u064a', null=True, verbose_name='\u0639\u062f\u062f \u0648\u0631\u0634 \u0627\u0644\u0639\u0645\u0644', blank=True),
        ),
        migrations.AlterField(
            model_name='employeereport',
            name='speaker',
            field=models.TextField(verbose_name='\u0623\u0633\u0645\u0627\u0621 \u0627\u0644\u0645\u062a\u062d\u062f\u062b\u064a\u0646 \u0648\u0627\u0644\u0645\u062a\u062d\u062f\u062b\u0627\u062a'),
        ),
        migrations.AlterField(
            model_name='employeereport',
            name='speaker_count',
            field=models.PositiveIntegerField(help_text='\u0627\u062e\u062a\u064a\u0627\u0631\u064a', null=True, verbose_name='\u0639\u062f\u062f \u0627\u0644\u0645\u062a\u062d\u062f\u062b\u064a\u0646 \u0648\u0627\u0644\u0645\u062a\u062d\u062f\u062b\u0627\u062a', blank=True),
        ),
        migrations.AlterField(
            model_name='employeereport',
            name='sponsor',
            field=models.TextField(help_text='\u0627\u062e\u062a\u064a\u0627\u0631\u064a', verbose_name='\u0623\u0633\u0645\u0627\u0621 \u0627\u0644\u062c\u0647\u0627\u062a \u0627\u0644\u0631\u0627\u0639\u064a\u0629 \u0623\u0648 \u0627\u0644\u0645\u0634\u0627\u0631\u0643\u0629', blank=True),
        ),
        migrations.AlterField(
            model_name='employeereport',
            name='sponsor_speech',
            field=models.TextField(help_text='\u0627\u062e\u062a\u064a\u0627\u0631\u064a', verbose_name='\u0643\u0644\u0645\u0629 \u0627\u0644\u0631\u0639\u0627\u0629', blank=True),
        ),
        migrations.AlterField(
            model_name='employeereport',
            name='winner_college_or_club',
            field=models.TextField(help_text='\u0627\u062e\u062a\u064a\u0627\u0631\u064a', verbose_name='\u0627\u0644\u0643\u0644\u064a\u0629 \u0623\u0648 \u0627\u0644\u0646\u0627\u062f\u064a \u0627\u0644\u0630\u064a \u064a\u062a\u0628\u0639 \u0644\u0647 \u0627\u0644\u0645\u0643\u0631\u0645', blank=True),
        ),
        migrations.AlterField(
            model_name='followupreport',
            name='end_date',
            field=models.DateField(null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0646\u0647\u0627\u064a\u0629', blank=True),
        ),
        migrations.AlterField(
            model_name='followupreport',
            name='end_time',
            field=models.TimeField(null=True, verbose_name='\u0648\u0642\u062a \u0627\u0644\u0646\u0647\u0627\u064a\u0629', blank=True),
        ),
        migrations.AlterField(
            model_name='followupreport',
            name='location',
            field=models.CharField(default=b'', max_length=128, verbose_name='\u0627\u0644\u0645\u0643\u0627\u0646', blank=True),
        ),
        migrations.AlterField(
            model_name='followupreport',
            name='notes',
            field=models.TextField(default=b'', verbose_name='\u0645\u0644\u0627\u062d\u0638\u0627\u062a', blank=True),
        ),
        migrations.AlterField(
            model_name='followupreport',
            name='organizer_count',
            field=models.IntegerField(null=True, verbose_name='\u0639\u062f\u062f \u0627\u0644\u0645\u0646\u0638\u0645\u064a\u0646', blank=True),
        ),
        migrations.AlterField(
            model_name='followupreport',
            name='participant_count',
            field=models.IntegerField(null=True, verbose_name='\u0639\u062f\u062f \u0627\u0644\u0645\u0634\u0627\u0631\u0643\u064a\u0646', blank=True),
        ),
        migrations.AlterField(
            model_name='followupreport',
            name='start_date',
            field=models.DateField(null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0628\u062f\u0627\u064a\u0629', blank=True),
        ),
        migrations.AlterField(
            model_name='followupreport',
            name='start_time',
            field=models.TimeField(null=True, verbose_name='\u0648\u0642\u062a \u0627\u0644\u0628\u062f\u0627\u064a\u0629', blank=True),
        ),
        migrations.AddField(
            model_name='followupreportadimage',
            name='report',
            field=models.ForeignKey(related_name='ad_images', to='media.FollowUpReport'),
        ),
    ]
