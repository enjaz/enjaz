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
                ('gender', models.CharField(max_length=1, verbose_name='\u0627\u0644\u062c\u0646\u062f\u0631', choices=[(b'F', '\u0623\u0646\u062b\u0649'), (b'M', '\u0630\u0643\u0631')])),
                ('age', models.PositiveSmallIntegerField(default=0, verbose_name='\u0639\u0645\u0631\u0643')),
                ('mobile', models.CharField(max_length=20, verbose_name='\u0631\u0642\u0645 \u0627\u0644\u062c\u0648\u0627\u0644')),
                ('emial', models.EmailField(max_length=100, verbose_name='\u0627\u0644\u0628\u0631\u064a\u062f \u0627\u0644\u0625\u0644\u0643\u062a\u0631\u0648\u0646\u064a')),
                ('city', models.CharField(default='\u0627\u0644\u0631\u064a\u0627\u0636', max_length=10, verbose_name='\u0627\u0644\u0645\u062f\u064a\u0646\u0629')),
                ('fromNGH', models.BooleanField(verbose_name=b'\xd9\x85\xd9\x86 \xd9\x85\xd9\x86\xd8\xb3\xd9\x88\xd8\xa8\xd9\x8a \xd9\x88\xd9\x85\xd9\x86\xd8\xb3\xd9\x88\xd8\xa8\xd8\xa7\xd8\xaa \xd8\xa7\xd9\x84\xd8\xad\xd8\xb1\xd8\xb3\xd8\x9f')),
                ('job_title', models.CharField(max_length=100, verbose_name='\u0627\u0644\u0645\u0633\u0645\u0649 \u0627\u0644\u0648\u0638\u064a\u0641\u064a')),
                ('yourself', models.TextField(verbose_name='\u0639\u0646 \u0646\u0641\u0633\u0643')),
                ('about_tedx', models.TextField(verbose_name='\u0639\u0646 \u062a\u062f\u0643\u0633')),
                ('attend_tedx', models.BooleanField()),
                ('past_experience', models.TextField(verbose_name='\u062a\u062c\u0631\u0628\u062a\u0643 \u0627\u0644\u0633\u0627\u0628\u0642\u0629 \u0645\u0639 \u062a\u062f\u0643\u0633')),
                ('referral', models.CharField(max_length=20, verbose_name='\u0627\u0644\u0633\u0645\u0627\u0639 \u0639\u0646 TEDxKSAUHS?')),
                ('expectations', models.TextField(verbose_name='\u0627\u0644\u062a\u0648\u0642\u0639\u0627\u062a \u0645\u0646 TEDxKSAUHS?')),
                ('meaning', models.TextField(verbose_name='\u0645\u0627 \u0627\u0644\u0630\u064a \u062a\u0639\u0646\u064a\u0647 \u0644\u0643 \u0644\u0648 \u0623\u0646\u061f')),
                ('interview', models.BooleanField()),
                ('take_pic', models.BooleanField()),
                ('your_interest', models.CharField(max_length=50, verbose_name='\u0627\u064a \u0627\u0644\u0645\u062c\u0627\u0644\u0627\u062a \u0627\u0644\u062a\u0627\u0644\u064a\u0629 \u0623\u0642\u0631\u0628 \u0644\u0627\u0647\u062a\u0645\u0627\u0645\u0643\u061f', choices=[(b'A', '\u0627\u0644\u0641\u0646'), (b'E', '\u0627\u0644\u062a\u0639\u0644\u064a\u0645'), (b'H', '\u0627\u0644\u0635\u062d\u0629'), (b'T', '\u0627\u0644\u062a\u0643\u0646\u0648\u0644\u0648\u062c\u064a\u0627'), (b'S', '\u0627\u0644\u0631\u064a\u0627\u0636\u0629'), (b'B', '\u0631\u064a\u0627\u062f\u0629 \u0627\u0644\u0623\u0639\u0645\u0627\u0644'), (b'V', '\u0627\u0644\u062a\u0637\u0648\u0639'), (b'M', '\u0627\u0644\u062a\u0633\u0648\u064a\u0642'), (b'L', '\u0627\u0644\u0623\u062f\u0628')])),
                ('submission', models.DateTimeField(auto_now=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('modification', models.DateTimeField(auto_now=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
            ],
        ),
    ]
