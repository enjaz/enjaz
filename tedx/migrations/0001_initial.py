# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='\u0627\u0633\u0645\u0643')),
                ('gender', models.CharField(max_length=1, verbose_name='\u0627\u0644\u062c\u0646\u062f\u0631', choices=[('F', '\u0623\u0646\u062b\u0649'), ('M', '\u0630\u0643\u0631')])),
                ('age', models.PositiveSmallIntegerField(verbose_name='\u0639\u0645\u0631\u0643')),
                ('mobile', models.CharField(max_length=20, verbose_name='\u0631\u0642\u0645 \u0627\u0644\u062c\u0648\u0627\u0644')),
                ('emial', models.EmailField(max_length=100, verbose_name='\u0627\u0644\u0628\u0631\u064a\u062f \u0627\u0644\u0625\u0644\u0643\u062a\u0631\u0648\u0646\u064a')),
                ('city', models.CharField(max_length=10, verbose_name='\u0627\u0644\u0645\u062f\u064a\u0646\u0629')),
                ('fromNGH', models.BooleanField(verbose_name='\u0647\u0644 \u0623\u0646\u062a \u0645\u0646 \u0645\u0646\u0633\u0648\u0628\u064a \u0648\u0645\u0646\u0633\u0648\u0628\u0627\u062a \u0627\u0644\u062d\u0631\u0633\u061f')),
                ('job_title', models.CharField(max_length=100, verbose_name='\u0627\u0644\u0645\u0633\u0645\u0649 \u0627\u0644\u0648\u0638\u064a\u0641\u064a')),
                ('yourself', models.TextField(verbose_name='\u062a\u062d\u062f\u062b \u0639\u0646 \u0646\u0641\u0633\u0643')),
                ('about_tedx', models.TextField(verbose_name='\u062a\u062d\u062f\u062b \u0639\u0646 \u062a\u062f\u0643\u0633')),
                ('attend_tedx', models.BooleanField(verbose_name='\u0647\u0644 \u0633\u0628\u0642 \u0648\u062d\u0636\u0631\u062a \u062a\u062f\u0643\u0633\u061f')),
                ('past_experience', models.TextField(verbose_name='\u062a\u062d\u062f\u062b \u0639\u0646 \u062a\u062c\u0631\u0628\u062a\u0643 \u0627\u0644\u0633\u0627\u0628\u0642\u0629 \u0645\u0639 \u062a\u062f\u0643\u0633')),
                ('referral', models.CharField(max_length=20, verbose_name='\u0643\u064a\u0641 \u0633\u0645\u0639\u062a \u0639\u0646 TEDxKSAUHS?')),
                ('expectations', models.TextField(verbose_name='\u0645\u0627 \u0627\u0644\u0630\u064a \u062a\u062a\u0648\u0642\u0639\u0647 \u0645\u0646 TEDxKSAUHS?')),
                ('meaning', models.TextField(verbose_name='\u0645\u0627 \u0627\u0644\u0630\u064a \u062a\u0639\u0646\u064a\u0647 \u0644\u0643 \u0639\u0628\u0627\u0631\u0629 \u0644\u0648 \u0623\u0646\u061f')),
                ('interview', models.BooleanField(verbose_name='\u0647\u0644 \u062a\u0642\u0628\u0644 \u0628\u0639\u0645\u0644 \u0645\u0642\u0627\u0628\u0644\u0627\u062a \u0645\u0639\u0643 \u0642\u0628\u0644 \u0648 \u0628\u0639\u062f \u0627\u0644\u062d\u062f\u062b\u061f')),
                ('take_pic', models.BooleanField(verbose_name='\u0647\u0644 \u062a\u0642\u0628\u0644 \u0628\u0627\u0644\u062a\u0635\u0648\u064a\u0631 \u0623\u062b\u0646\u0627\u0621 \u0627\u0644\u062d\u062f\u062b\u061f')),
                ('your_interest', models.CharField(max_length=50, verbose_name='\u0627\u064a \u0627\u0644\u0645\u062c\u0627\u0644\u0627\u062a \u0627\u0644\u062a\u0627\u0644\u064a\u0629 \u0623\u0642\u0631\u0628 \u0644\u0627\u0647\u062a\u0645\u0627\u0645\u0643\u061f', choices=[('A', '\u0627\u0644\u0641\u0646'), ('E', '\u0627\u0644\u062a\u0639\u0644\u064a\u0645'), ('H', '\u0627\u0644\u0635\u062d\u0629'), ('T', '\u0627\u0644\u062a\u0643\u0646\u0648\u0644\u0648\u062c\u064a\u0627'), ('S', '\u0627\u0644\u0631\u064a\u0627\u0636\u0629'), ('B', '\u0631\u064a\u0627\u062f\u0629 \u0627\u0644\u0623\u0639\u0645\u0627\u0644'), ('V', '\u0627\u0644\u062a\u0637\u0648\u0639'), ('M', '\u0627\u0644\u062a\u0633\u0648\u064a\u0642'), ('L', '\u0627\u0644\u0623\u062f\u0628')])),
                ('submission', models.DateTimeField(auto_now=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('modification', models.DateTimeField(auto_now=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
            ],
        ),
    ]
