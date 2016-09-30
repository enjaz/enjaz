# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activities', '0022_depository'),
        ('media', '0003_buzz_is_push'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_submitted', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0631\u0641\u0639 \u0627\u0644\u062a\u0642\u0631\u064a\u0631')),
                ('speaker', models.TextField(verbose_name='\u0623\u0633\u0645\u0627\u0621 \u0627\u0644\u0645\u062a\u062d\u062f\u062b\u064a\u0646')),
                ('quotation', models.TextField(verbose_name='\u0627\u0642\u062a\u0628\u0627\u0633\u0627\u062a \u0645\u0646 \u0627\u0644\u0645\u062a\u062d\u062f\u062b\u064a\u0646')),
                ('sponsor_speech', models.TextField(verbose_name='\u0643\u0644\u0645\u0629 \u0627\u0644\u0631\u0639\u0627\u0629')),
                ('prize_winner', models.TextField(verbose_name='\u0623\u0633\u0645\u0627\u0621 \u0627\u0644\u0645\u0643\u0631\u0645\u064a\u0646')),
                ('winner_college_or_club', models.TextField(verbose_name='\u0627\u0644\u0643\u0644\u064a\u0629 \u0623\u0648 \u0627\u0644\u0646\u0627\u062f\u064a \u0627\u0644\u0630\u064a \u064a\u062a\u0628\u0639 \u0644\u0647 \u0627\u0644\u0645\u0643\u0631\u0645')),
                ('booth', models.TextField(verbose_name='\u0623\u0633\u0645\u0627\u0621 \u0627\u0644\u0623\u0631\u0643\u0627\u0646 \u0627\u0644\u0645\u0634\u0627\u0631\u0643\u0629')),
                ('sponsor', models.TextField(verbose_name='\u0623\u0633\u0645\u0627\u0621 \u0627\u0644\u062c\u0647\u0627\u062a \u0627\u0644\u0631\u0627\u0639\u064a\u0629 \u0623\u0648 \u0627\u0644\u0645\u0634\u0627\u0631\u0643\u0629')),
                ('participant_count', models.IntegerField(verbose_name='\u0639\u062f\u062f \u0627\u0644\u0645\u0634\u0627\u0631\u0643\u064a\u0646')),
                ('organizer_count', models.IntegerField(verbose_name='\u0639\u062f\u062f \u0627\u0644\u0645\u0646\u0638\u0645\u064a\u0646')),
                ('speaker_count', models.IntegerField(verbose_name='\u0639\u062f\u062f \u0627\u0644\u0645\u062a\u062d\u062f\u062b\u064a\u0646')),
                ('lecture_count', models.IntegerField(verbose_name='\u0639\u062f\u062f \u0627\u0644\u0645\u062d\u0627\u0636\u0631\u0627\u062a')),
                ('session_count', models.IntegerField(verbose_name='\u0639\u062f\u062f \u0648\u0631\u0634 \u0627\u0644\u0639\u0645\u0644')),
                ('booth_count', models.IntegerField(verbose_name='\u0639\u062f\u062f \u0627\u0644\u0623\u0631\u0643\u0627\u0646')),
                ('end', models.TextField(verbose_name='\u0643\u064a\u0641 \u0625\u0646\u062a\u0647\u0649 \u0627\u0644\u0646\u0634\u0627\u0637\u061f')),
                ('notes', models.TextField(verbose_name='\u0645\u0644\u0627\u062d\u0638\u0627\u062a')),
                ('episode', models.OneToOneField(verbose_name='\u0627\u0644\u0645\u0648\u0639\u062f', to='activities.Episode')),
                ('submitter', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
